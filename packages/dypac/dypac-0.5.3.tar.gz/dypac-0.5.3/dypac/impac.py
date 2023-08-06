"""Image Parcel Aggregation with Clustering (impac)."""

# Authors: Pierre Bellec
# License: BSD 3 clause
import glob
import itertools
import warnings

from scipy.sparse import vstack
import numpy as np

from sklearn.utils import check_random_state

from nilearn import EXPAND_PATH_WILDCARDS
from joblib import Memory
from nilearn import datasets, image
from nilearn._utils.niimg_conversions import _resolve_globbing
from nilearn.input_data import NiftiMasker
from nilearn.input_data.masker_validation import check_embedded_nifti_masker

import dypac.bascpp as bpp
from dypac.embeddings import Embedding


class Impac:
    """
    Perform Image Parcel Aggregation with Clustering.

    Parameters
    ----------
    n_clusters: int, optional
        Number of clusters to extract per time window

    n_states: int, optional
        Number of expected dynamic states

    n_replications: int, optional
        Number of replications of cluster analysis in each fMRI run

    n_batch: int, optional
        Number of batches to run through consensus clustering.
        If n_batch<=1, consensus clustering will be applied
        to all replications in one pass. Processing with batch will
        reduce dramatically the compute time, but will change slightly
        the results.

    n_init: int, optional
        Number of initializations for k-means

    subsample_size: int, optional
        Number of time points in a subsample

    max_iter: int, optional
        Max number of iterations for k-means

    threshold_sim: float (0 <= . <= 1), optional
        Minimal acceptable average dice in a state

    random_state: int or RandomState, optional
        Pseudo number generator state used for random sampling.

    standardize: boolean, optional
        If standardize is True, the images are centered and normed:
        their mean is put to 0 and their variance to 1 in the time dimension.

    verbose: integer, optional
        Indicate the level of verbosity. By default, print progress.

    """

    def __init__(
        self,
        n_clusters=10,
        n_states=3,
        n_replications=40,
        n_batch=1,
        n_init=30,
        n_init_aggregation=100,
        subsample_size=30,
        max_iter=30,
        threshold_sim=0.3,
        random_state=None,
        standardize=True,
        verbose=1,
    ):
        """Set up default attributes for the class."""
        # All those settings are taken from nilearn BaseDecomposition
        self.random_state = random_state
        self.standardize = standardize
        self.verbose = verbose

        # Those settings are specific to parcel aggregation
        self.n_clusters = n_clusters
        self.n_states = n_states
        self.n_batch = n_batch
        self.n_replications = n_replications
        self.n_init = n_init
        self.n_init_aggregation = n_init_aggregation
        self.subsample_size = subsample_size
        self.max_iter = max_iter
        self.threshold_sim = threshold_sim

    def _sanitize_imgs(imgs):
        """Check that provided images are in the correct format."""
        if (not isinstance(imgs, np.ndarray)) or (imgs.ndim is not 3):
            raise ValueError(
                "imgs is not a numpy array "
                "Impac expects an ndarray of size [n_samps, nx, ny]"
            )
        
    def _check_components_(self):
        """Check for presence of estimated components."""
        if not hasattr(self, "components_"):
            raise ValueError(
                "Object has no components_ attribute. "
                "This is probably because fit has not "
                "been called."
            )

    def fit(self, imgs, confounds=None):
        """
        Compute the stable parcels across images.

        Parameters
        ----------
        imgs: ndarray
            expected size is [n_samps, nx, ny], where n_samps is the number of
            samples (images) and (nx, ny) are the number of pixels along the x
            and y axis, respectively.

         Returns
         -------
         self: object
            Returns the instance itself. Contains attributes listed
            at the object level.
        """
        imgs = _sanitize_imgs(imgs)

        # Check that number of batches is reasonable
        if self.n_batch > len(imgs):
            warnings.warn(
                "{0} batches were requested, but only {1} datasets available. Using {2} batches instead.".format(
                    self.n_batch, len(imgs), self.n_batch
                )
            )
            self.n_batch = len(imgs)

        # mask_and_reduce step
        if self.n_batch > 1:
            stab_maps, dwell_time = self._mask_and_reduce_batch(imgs, confounds)
        else:
            stab_maps, dwell_time = self._mask_and_reduce(imgs, confounds)

        # Return components
        self.components_ = stab_maps
        self.dwell_time_ = dwell_time

        # Create embedding
        self.embedding = Embedding(stab_maps.todense())
        return self

    def _mask_and_reduce_batch(self, imgs, confounds=None):
        """Iterate dypac on batches of files."""
        stab_maps_list = []
        dwell_time_list = []
        for bb in range(self.n_batch):
            slice_batch = slice(bb, len(imgs), self.n_batch)
            if self.verbose:
                print("[{0}] Processing batch {1}".format(self.__class__.__name__, bb))
            stab_maps, dwell_time = self._mask_and_reduce(
                imgs[slice_batch], confounds[slice_batch]
            )
            stab_maps_list.append(stab_maps)
            dwell_time_list.append(dwell_time)

        stab_maps_cons, dwell_time_cons = bpp.consensus_batch(
            stab_maps_list,
            dwell_time_list,
            self.n_replications,
            self.n_states,
            self.max_iter,
            self.n_init_aggregation,
            self.random_state,
            self.verbose,
        )

        return stab_maps_cons, dwell_time_cons

    def _mask_and_reduce(self, imgs, confounds=None):
        """
        Cluster aggregation on a list of 4D fMRI datasets.

        Returns
        -------
        stab_maps: ndarray
            stability maps of each state.

        dwell_time: ndarray
            dwell time of each state.
        """
        onehot_list = []
        for ind, img, confound in zip(range(len(imgs)), imgs, confounds):
            this_data = self.masker_.transform(img, confound)
            # Now get rid of the img as fast as possible, to free a
            # reference count on it, and possibly free the corresponding
            # data
            del img
            onehot = bpp.replicate_clusters(
                this_data.transpose(),
                subsample_size=self.subsample_size,
                n_clusters=self.n_clusters,
                n_replications=self.n_replications,
                max_iter=self.max_iter,
                n_init=self.n_init,
                random_state=self.random_state,
                desc="Replicating clusters in data #{0}".format(ind),
                verbose=self.verbose,
            )
            onehot_list.append(onehot)
        onehot_all = vstack(onehot_list)
        del onehot_list
        del onehot

        # find the states
        states = bpp.find_states(
            onehot_all,
            n_states=self.n_states,
            max_iter=self.max_iter,
            threshold_sim=self.threshold_sim,
            random_state=self.random_state,
            n_init=self.n_init_aggregation,
            verbose=self.verbose,
        )

        # Generate the stability maps
        stab_maps, dwell_time = bpp.stab_maps(
            onehot_all, states, self.n_replications, self.n_states
        )

        return stab_maps, dwell_time

    def transform(self, img, confound=None):
        """
        Transform a 4D dataset in a component space.

        Parameters
        ----------
        img : Niimg-like object.
            See http://nilearn.github.io/manipulating_images/input_output.html
            An fMRI dataset
        confound : CSV file or 2D matrix, optional.
            Confound parameters, to be passed to nilearn.signal.clean.

        Returns
        -------
        weights : numpy array of shape [n_samples, n_states + 1]
            The fMRI tseries after projection in the parcellation
            space. Note that the first coefficient corresponds to the intercept,
            and not one of the parcels.
        """
        self._check_components_()
        tseries = self.masker_.transform(img, confound)
        del img
        return self.embedding.transform(tseries)

    def inverse_transform(self, weights):
        """
        Transform component weights as a 4D dataset.

        Parameters
        ----------
        weights : numpy array of shape [n_samples, n_states + 1]
            The fMRI tseries after projection in the parcellation
            space. Note that the first coefficient corresponds to the intercept,
            and not one of the parcels.

        Returns
        -------
        img : Niimg-like object.
            The 4D fMRI dataset corresponding to the weights.
        """
        self._check_components_()
        return self.masker_.inverse_transform(self.embedding.inverse_transform(weights))

    def compress(self, img, confound=None):
        """
        Provide the approximation of a 4D dataset after projection in parcellation space.

        Parameters
        ----------
        img : Niimg-like object.
            See http://nilearn.github.io/manipulating_images/input_output.html
            An fMRI dataset
        confound : CSV file or 2D matrix, optional.
            Confound parameters, to be passed to nilearn.signal.clean.

        Returns
        -------
        img_c : Niimg-like object.
            The 4D fMRI dataset corresponding to the input, compressed in the parcel space.
        """
        self._check_components_()
        tseries = self.masker_.transform(img, confound)
        del img
        return self.masker_.inverse_transform(self.embedding.compress(tseries))

    def score(self, img, confound=None):
        """
        R2 map of the quality of the compression.

        Parameters
        ----------
        img : Niimg-like object.
            See http://nilearn.github.io/manipulating_images/input_output.html
            An fMRI dataset
        confound : CSV file or 2D matrix, optional.
            Confound parameters, to be passed to nilearn.signal.clean.

        Returns
        -------
        score : Niimg-like object.
            A 3D map of R2 score of the quality of the compression.

        Note
        ----
        The R2 score map is the fraction of the variance of fMRI time series captured
        by the parcels at each voxel. A score of 1 means perfect approximation.
        The score can be negative, in which case the parcellation approximation
        performs worst than the average of the signal.
        """
        self._check_components_()
        tseries = self.masker_.transform(img, confound)
        del img
        return self.masker_.inverse_transform(self.embedding.score(tseries))
