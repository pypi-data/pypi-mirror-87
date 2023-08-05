"""Classes responsible for serializing models in order to be stored.

This module defines a :class:`.StoredModel` which provides a standardized way to
interact with :class:`.RhoModel` instances.  An abstract base class
:class:`.PipelineStorageConfig` defines the behavior for storing models to
various data stores.
"""
import glob
import logging
import os
import tempfile
import pickle
from typing import Union

import attr

from rho_ml.model_locator import generate_model_locator, \
    find_highest_compatible_version

logger = logging.getLogger(__name__)


@attr.s(auto_attribs=True, frozen=True)
class StoredModel(object):
    """  Stores the bytes of a serialized model and is intended for storage.

    This is used as a generic format to store `RhoModel` instances.  The default
    behavior is to use pickle to serialize a given `RhoModel`, and then unpickle
    in `StoredModel`.  In cases where pickle is not appropriate for model
    serialization, a `StoredModel` child class should be created with the
    load_model method overridden.

    Attributes:
        model_bytes (bytes): The serialized byte string of some `RhoModel`
    """
    model_bytes: bytes = attr.ib(repr=False)

    def load_model(self) -> 'RhoModel':
        """ Use the instantiated StoredModel to load & return RhoModel instance.

            Note: this method should be overridden if the underlying RhoModel
            requires specialized deserialization logic.

            Returns:
                `RhoModel`: the deserialized model instance in storage

            Examples::
                my_stored_model = StoredModel.from_pickle(some_stored_bytes)
                my_rho_model = my_stored_model.load_model()
        """
        return pickle.loads(self.model_bytes)

    def to_pickle(self) -> bytes:
        """ Serialize the `StoredModel` instance (note: this is *not* for
        serializing the underlying RhoModel instance, which is serialized
        before instantiating the `StoredModel`.

        Returns:
            bytes: the pickled bytes of the `StoredModel` instance.

        Examples::
            serialized_stored_model = my_stored_model.to_pickle()
        """
        return pickle.dumps(self, protocol=4)

    @classmethod
    def from_pickle(cls, stored_bytes: bytes) -> 'StoredModel':
        """ Load a StoredModel from it's pickled bytes.

        This is the inverse of :meth:`~StoredModel.to_pickle`.

        Args:
            stored_bytes (bytes): The serialized `StoredModel`

        Returns:
            StoredModel: re-instantiated `StoredModel`
        """
        return pickle.loads(stored_bytes)


class PipelineStorageConfig(object):
    """ Base class for utility classes used to store RhoModel objects.

    TODO: Add example of when this is necessary and how it's used.
    """
    def store(self, model: 'RhoModel'):
        """ Store a RhoModel.

        Creates a StoredModel, and stores the pickle bytes of that StoredModel
        to the appropriate store.

        Args:
            model (`RhoModel`): The `RhoModel` instance to store

        Returns:
            NoneType
         """
        raise NotImplementedError

    def retrieve(self, *args, **kwargs) -> 'RhoModel':
        """ Pull the pickled bytes of the StoredModel from the data store and
        use that to instantiate the underlying RhoModel.
        """
        raise NotImplementedError

    def get_key_from_pattern(self, model_name: str,
                             version_pattern: str) -> str:
        """ Given some pattern of the form 'name-1.2.3', 'name-1.2.*', or
            'name-1.*', etc., return the matching key with the highest version.
            Returns None if nothing is found.

            Args:
                model_name (str): The name of the `RhoModel` search for
                version_pattern (str): Version (incl. wildcards) to search for

            Returns:
                 str: key of the highest matching artifact in the data store

            Examples::
                model_key = my_stored_model.get_key_from_pattern(
                'my_model_name', '0.*.*`)
                assert model_key == 'my_model_name_0.1.2'
        """
        raise NotImplementedError


@attr.s(auto_attribs=True)
class LocalModelStorage(PipelineStorageConfig):
    """ Class for caching `RhoModel` objects locally.

    Args:
        base_path (str): the directory to store, search, and/or retrieve models
            from.

    """
    base_path: str = attr.ib(default=None)

    def __attrs_post_init__(self):
        """ Provide default temp directory if no base_path set.
        """
        if not self.base_path:
            self.base_path = tempfile.gettempdir()

    def store(self, model: 'RhoModel'):
        """ Save pickled bytes of a RhoModel to local storage, in the
        `self.base_path` directory. """
        storage_key = generate_model_locator(
            model_name=model.name, model_version=model.version_string)
        storage_path = os.path.join(self.base_path, storage_key)
        stored_model = model.build_stored_model()
        store_bytes = stored_model.to_pickle()
        with open(storage_path, 'wb') as f:
            f.write(store_bytes)

    def retrieve(self, key: str) -> Union['RhoModel', None]:
        """ Attempt to retrieve model at a path that is stored locally. Return
            the loaded model if found, otherwise None.
        """
        storage_path = os.path.join(self.base_path, key)
        try:
            with open(storage_path, 'rb') as f:
                stored_model = StoredModel.from_pickle(stored_bytes=f.read())
                model = stored_model.load_model()
        except FileNotFoundError:
            return None
        return model

    def get_key_from_pattern(self, model_name: str,
                             version_pattern: str) -> Union[str, None]:
        """ Search `self.base_path` for an artifact matching the model name and
            pattern.
        """
        search_pattern = generate_model_locator(model_name=model_name,
                                                model_version=version_pattern)
        search_path = os.path.join(self.base_path, search_pattern)
        local_candidates = glob.glob(search_path)
        result_key = find_highest_compatible_version(
            search_version=version_pattern, search_list=local_candidates)
        return result_key
