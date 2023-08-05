""" Methods used for interacting with RhoModels stored in Sermos Cloud.

    Most frequently, two methods are used programmatically::

        store_rho_model() --> Store a RhoModel for your deployments in Sermos.
        load_rho_model()  --> Retrieve a stored model to use.

    And one method is used for tooling/exploring::

        search_rho_model() --> Search available stored models.
"""
import io
import json
import logging
import os
import pprint
import tempfile
from typing import Dict, Type, Optional, Tuple, Union, List
import requests
import boto3
import filelock
from boto3.s3.transfer import TransferConfig
from rho_ml.rho_model import RhoModel
from rho_ml.serialization import StoredModel, LocalModelStorage
from rho_ml.model_locator import DEFAULT_DELIMITER_PATTERN,\
    generate_model_locator, split_model_locator
from rho_ml.constants import DEFAULT_STORE_MODEL_URL, \
    DEFAULT_GET_MODEL_URL, DEFAULT_SEARCH_MODEL_URL

logger = logging.getLogger(__name__)


class UnauthorizedError(Exception):
    """ Custom exception that is raised when the provided access key is invalid.

    Used in :meth:`~load_rho_model` and :meth:`~search_rho_model`
    """
    pass


class ModelNotFoundError(Exception):
    """ Exception raised when no model is found.

    Used in :meth:`~.load_rho_model`, :meth:`~.search_rho_model`
    """
    pass


class ModelFailedToStoreError(Exception):
    """ Exception raised when a model is unable to be stored.

    Used in :meth:`~.store_rho_model`
    """
    pass


def _get_sermos_api_headers(api_key: str) -> Dict[str, str]:
    """ Get basic headers required for interacting with Sermos Admin API.
    """
    return {'Content-Type': 'application/json', 'apikey': api_key}


def _get_s3_client_from_api_response(response_data: Dict[str, str]):
    """ Get a valid s3 client based on credentials response from Sermos.

        This assumes the response data has been verified to be a 200 response,
        this will throw a keyerror otherwise.
    """
    try:
        access_key = response_data['data']['aws_access_key']
        secret_key = response_data['data']['aws_secret_key']
        session_token = response_data['data']['aws_session_token']
        region = response_data['data']['aws_region']
    except KeyError as e:
        logger.warning("Missing IAM keys in response:\n{0}".format(
            pprint.pformat(response_data)))
        raise e
    else:
        client = boto3.client('s3',
                              aws_access_key_id=access_key,
                              aws_secret_access_key=secret_key,
                              aws_session_token=session_token,
                              region_name=region)
        return client


def _get_transfer_config(
        max_concurrency: Optional[int] = None,
        max_io_queue: Optional[int] = None,
        multipart_chunksize: Optional[int] = None) -> TransferConfig:
    """ Create a boto3 s3 TransferConfig object. Default class doesn't handle
        None values to kwargs.
    """
    kwargs = {}
    if max_concurrency:
        kwargs['max_concurrency'] = max_concurrency
    if max_io_queue:
        kwargs['max_io_queue'] = max_io_queue
    if multipart_chunksize:
        kwargs['multipart_chunksize'] = multipart_chunksize
    config = TransferConfig(**kwargs)
    return config


def store_rho_model(model: Type[RhoModel],
                    access_key: Optional[str] = None,
                    store_model_endpoint: Optional[str] = None,
                    max_concurrency: Optional[int] = None,
                    max_io_queue: Optional[int] = None,
                    multipart_chunksize: Optional[int] = None,
                    sermos_organization_id: Optional[str] = None):
    """ Get S3 credentials from the sermos-admin API, then use the credentials
        to store the model and metadata in the appropriate bucket / subfolder

    Args:
        model (RhoModel): model to put in storage
        access_key (str, optional): Sermos access key.  If not passed here it
            must be set in the environment as `SERMOS_ACCESS_KEY`
        store_model_endpoint (str, optional): Sermos storage API.  The default
            is almost always what you will want.
        max_concurrency (int, optional): Max processes to use for uploading.
        max_io_queue (int, optional): Max I/O queue to use for uploading.
        multipart_chunksize (int, optional): Chunk size for upload
        sermos_organization_id (str, optional): Id of the organization that owns
            the model. Defaults to enviornment variable `SERMOS_ORGANIZATION_ID`

    Returns:
        None: Uploads to cloud storage, raises if upload fails.

    Example::

        store_rho_model(model=my_rho_model)  # access key set in environment
    """
    # TODO: come up w/ way to compare hashes of stored models and loaded
    #       models
    logger.info(f"Attempting to serialize {model.name}")

    # Given a RhoModel, create a StoredModel instance and pickle it to bytes
    stored_model = model.build_stored_model()
    store_bytes = stored_model.to_pickle()
    f = io.BytesIO()
    f.write(store_bytes)
    f.seek(0)

    logger.info("Serialization finished, requesting credentials from API...")

    # Get access key from environment if not explicitly provided. Fail here
    # if it's also not defined in environment.
    if not access_key:
        access_key = os.environ['SERMOS_ACCESS_KEY']

    if not store_model_endpoint:
        store_model_endpoint = DEFAULT_STORE_MODEL_URL

    if not sermos_organization_id:
        sermos_organization_id = os.environ['SERMOS_ORGANIZATION_ID']

    # Get our post headers and post data
    headers = _get_sermos_api_headers(access_key)
    model_locator = generate_model_locator(model.name,
                                           model.version.to_string())
    post_data = {
        'organization_id': sermos_organization_id,
        'model_locator': model_locator
    }

    # Ask Sermos for credentials
    r = requests.post(url=store_model_endpoint,
                      headers=headers,
                      json=post_data)
    if r.status_code != 200:
        logger.error(f"Failed to store RhoModel: {r.content}")
        raise ModelFailedToStoreError("Unable to store RhoModel!")

    response_data = r.json()
    client = _get_s3_client_from_api_response(response_data)
    storage_key = response_data['data']['model_key']

    logger.info(f"Uploading serialized {model_locator}")

    transfer_config = _get_transfer_config(
        max_concurrency=max_concurrency,
        max_io_queue=max_io_queue,
        multipart_chunksize=multipart_chunksize)

    client.upload_fileobj(f,
                          Bucket=response_data['data']['bucket'],
                          Key=storage_key,
                          Config=transfer_config)


def _get_model_api_response(
        model_name: str,
        version_pattern: str,
        access_key: str,
        get_model_endpoint: Optional[str] = None,
        sermos_organization_id: Optional[str] = None) -> Dict[str, str]:
    """ Ask Sermos' get-model/ api endpoint for credentials and location
        of a specific model. Allows version pattern to be an exact version
        (e.g. 1.2.0) or a pattern with wildcard search (e.g. 1.*.*), which
        will return the highest compatible version.

        # TODO make a public method "get model's highest version" or something
        # some clients use this method directly which is no bueno
    """
    headers = _get_sermos_api_headers(access_key)

    if not get_model_endpoint:
        get_model_endpoint = DEFAULT_GET_MODEL_URL

    if not sermos_organization_id:
        sermos_organization_id = os.environ['SERMOS_ORGANIZATION_ID']

    filters = json.dumps({
        'model_name': model_name,
        'version_pattern': version_pattern
    })

    logger.debug("Requesting storage info from Admin API...")

    try:
        url = f'{get_model_endpoint}?organization_id={sermos_organization_id}'\
            f'&filters={filters}'
        r = requests.get(url=url, headers=headers)
        response_data = r.json()
    except Exception as e:
        logger.error("Failed to communicate with models API ...")
        logger.exception(e)
        raise e

    if r.status_code == 401:
        raise UnauthorizedError("Unauthorized. Most likely due to "
                                "invalid access_key")

    if response_data['data'] is None:
        raise ModelNotFoundError(response_data['message'])

    return response_data


def _get_stored_model_bytes_from_api_response(response_data: Dict[str, str]) \
        -> bytes:
    """ Given a model 'get' response from Sermos, retrieve the StoredModel
        from cloud storage.
    """
    client = _get_s3_client_from_api_response(response_data)
    model_key = response_data['data']['model_key']
    bucket = response_data['data']['bucket']

    logger.debug("Retrieving {0} from storage...".format(model_key))

    s3_response = client.get_object(Bucket=bucket, Key=model_key)
    model_bytes = s3_response['Body'].read()

    return model_bytes


def _determine_load_local_or_remote(
    model_name: str,
    version_pattern: str,
    delimiter_pattern: Optional[str] = DEFAULT_DELIMITER_PATTERN,
    access_key: Optional[str] = None,
    local_base_path: Optional[str] = None,
    get_model_endpoint: Optional[str] = None,
    force_search: bool = False
) -> Tuple[Union['local', 'remote'], Union[str, dict]]:
    """ Determine whether to load the RhoModel from local disk or from the cloud

        Return value is either
            ('local', '/full/path/to/Model_0.1.0')
        or
            ('remote', {'api': 'response from sermos'})
    """
    # Get a properly initialized LocalModelStorage() instance
    local_storage = LocalModelStorage(base_path=local_base_path)

    # Check to see if a compatible model already exists locally (don't load it)
    local_model_path = local_storage.get_key_from_pattern(
        model_name=model_name, version_pattern=version_pattern)

    # If a local model exists and there is not a forced-search, proceed to load
    if local_model_path is not None and not force_search:
        logger.info(f"Local model found at: {local_model_path}. "
                    "Loading due to no force_search.")
        load_from = 'local'
        retrieval_info = local_model_path
    else:
        # Get access key from environment if not provided.
        # Fail if can't find there.
        if not access_key:
            access_key = os.environ['SERMOS_ACCESS_KEY']

        # If force_search is True AND/OR we didn't find a local_model_path,
        # retrieve the highest compatible version of this model from cloud.
        api_response = _get_model_api_response(
            model_name=model_name,
            version_pattern=version_pattern,
            access_key=access_key,
            get_model_endpoint=get_model_endpoint)
        remote_model_version = api_response['data']['model_version']

        # If we did find a local model, parse it's local key to find the
        # version. This is way more CPU/memory so we don't need to load/unpickle
        # if the local model is actually outdated
        if local_model_path is not None:
            _model_name, local_model_version = split_model_locator(
                local_model_path, delimiter_pattern=delimiter_pattern)
        else:
            local_model_version = None

        # If remote has a newer version of the model, load it
        if (local_model_version is None)\
                or (local_model_version < remote_model_version):
            logger.info(f"Loading {model_name} from REMOTE due to higher "
                        f"version: {remote_model_version} vs "
                        f"{local_model_version}")
            load_from = 'remote'
            retrieval_info = api_response
        else:
            # Otherwise, load up the model from disk
            logger.info(f"Local model found at: {local_model_path}. "
                        "Loading due to no higher version found on remote.")
            load_from = 'local'
            retrieval_info = local_model_path

    return load_from, retrieval_info


def _generate_lockfile_path(model_name: str, version_pattern: str) -> str:
    """ Generate a lockfile path in temporary directory
    """
    lock_dir = os.path.join(tempfile.gettempdir(), 'rho-model-locks/')
    os.makedirs(name=lock_dir, exist_ok=True)
    key = f"{model_name}_{version_pattern}.lock"
    return os.path.join(lock_dir, key)


def load_rho_model(
        model_name: str,
        version_pattern: str,
        delimiter_pattern: Optional[str] = DEFAULT_DELIMITER_PATTERN,
        access_key: Optional[str] = None,
        local_base_path: Optional[str] = None,
        save_to_local_disk: bool = True,
        get_model_endpoint: Optional[str] = None,
        force_search: bool = False,
        request_lock_seconds: int = 60) -> Type[RhoModel]:
    """ Retrieve models stored using the Sermos Admin API by name and version.

        Optionally cache the result locally for later use (caching is ON by
        default).

        If force_search == True, always check cloud storage for latest version,
        regardless of whether a local model exists.

        Will raise `ModelNotFoundError` in the event no matching model is found.

    Args:
        model_name (str): Name of the model to load (e.g., "my_rho_model")
        version_pattern (str): version string with wildcards to search for in
            storage.  If multiple matching models are found, the one with the
            highest version is taken.
        delimiter_pattern (str, optional): delimiter between the model name and
            version.
        access_key (str, optional): Sermos access key.  If not passed here it must
            be set in the environment as `SERMOS_ACCESS_KEY`
        local_base_path (str, optional): If `save_to_local == True`, cache the
            model locally in this directory
        save_to_local_disk (bool, optional): If `True`, cache the model locally
            for future runs of `load_rho_model`.  Defaults to `True`.
        get_model_endpoint (str): Sermos storage API for retrieving models
            force_search (bool): If `True`
        request_lock_seconds (int, optional): Seconds to lock requests to a
            remote model (i.e. one which needs to be retrieved

    Returns:
        RhoModel: An instance of the RhoModel matching the name and version
        pattern (highest version available if multiple matches are found).

    Example::

        # access key set in the environment
        my_rho_model = load_rho_model(model_name='my_model_name',
                                      version_pattern='1.*.*')
    """
    # Get access key from environment if not provided. Fail if can't find there.
    if not access_key:
        access_key = os.environ['SERMOS_ACCESS_KEY']

    lock = None
    try:
        if request_lock_seconds:
            lockfile_path = _generate_lockfile_path(
                model_name=model_name, version_pattern=version_pattern)
            lock = filelock.FileLock(lock_file=lockfile_path,
                                     timeout=request_lock_seconds)
            lock.acquire(timeout=request_lock_seconds)
        local_or_remote, retrieval_info = _determine_load_local_or_remote(
            model_name=model_name,
            version_pattern=version_pattern,
            delimiter_pattern=delimiter_pattern,
            access_key=access_key,
            local_base_path=local_base_path,
            get_model_endpoint=get_model_endpoint,
            force_search=force_search)

        if local_or_remote == 'local':
            if lock:
                lock.release()
            local_storage = LocalModelStorage(base_path=local_base_path)
            model = local_storage.retrieve(retrieval_info)

        elif local_or_remote == 'remote':
            stored_bytes = _get_stored_model_bytes_from_api_response(
                response_data=retrieval_info)
            stored_model = StoredModel.from_pickle(stored_bytes=stored_bytes)
            model = stored_model.load_model()
            if lock:
                lock.release()

            if save_to_local_disk and model is not None:
                logger.info("Caching retrieved model {0} locally...".format(
                    model.name))
                local_storage = LocalModelStorage(base_path=local_base_path)
                local_storage.store(model=model)
        else:
            raise ValueError(f"Invalid choice of local or remote storage! "
                             f"(received {local_or_remote}")
    finally:
        if lock:
            lock.release()
    return model


def _search_model_api_response(
        access_key: str,
        model_name: Optional[str] = None,
        version_pattern: Optional[str] = None,
        search_model_endpoint: Optional[str] = None) -> Dict[str, str]:
    """ Internal method for retrieving search API response.
    """
    headers = _get_sermos_api_headers(access_key)
    if not search_model_endpoint:
        search_model_endpoint = DEFAULT_SEARCH_MODEL_URL

    filters = {}
    if model_name is not None:
        filters['model_name'] = model_name
    if version_pattern is not None:
        filters['version_pattern'] = version_pattern

    logger.debug("Requesting available models info from Admin API...")

    try:
        url = search_model_endpoint
        if filters:
            url += f'?filters={json.dumps(filters)}'
        r = requests.get(url=url,
                          headers=headers)
        response_data = r.json()
    except Exception as e:
        logger.error("Failed to communicate with /search-models/ API ...")
        logger.exception(e)
        raise e

    if r.status_code == 401:
        raise UnauthorizedError("Unauthorized. Most likely due to "
                                "invalid access_key")

    if response_data['data'] is None:
        raise ModelNotFoundError(response_data['message'])

    return response_data


def search_rho_model(
    model_name: str,
    version_pattern: str,
    access_key: Optional[str] = None,
    search_model_endpoint: Optional[str] = None,
) -> List[Dict[str, str]]:
    """ Ask Sermos' search-models/ api endpoint for available models that
        match the provided model_name and version_pattern.

        Both `model_name` and `version_pattern` allow wildcard searching
        using `*`. E.g. `MyName*`, `1.*.*`, etc. If a `version_pattern`
        is provided, then *only the highest compatible version* will be
        returned.

        If `model_name` is None, search will be bound to provided version
        pattern but across 'all' models.

        If `version_pattern` is None, search will be bound to provided model
        name but will return 'all' versions.

        Returns:
          List of objects. Each object contains keys `locator`, `name`, and
          `version`.

          Raises `ModelNotFoundError` exception if no matching models found.

        Example Responses::

            $ search_rho_model --model-name *Classifier* --version-pattern *.*.*

            {
                "models": [
                    {
                        "locator": "MyDocumentClassifier_0.3.1",
                        "name": "MyDocumentClassifier",
                        "version": "0.2.1"
                    }
                ]
            }

            $ search_rho_model --model-name *Classifier*

            {
                "models": [
                    {
                        "locator": "MyDocumentClassifier_0.1.0",
                        "name": "MyDocumentClassifier",
                        "version": "0.1.0"
                    },
                    {
                        "locator": "MyDocumentClassifier_0.2.0",
                        "name": "MyDocumentClassifier",
                        "version": "0.2.0"
                    },
                    {
                        "locator": "MyDocumentClassifier_0.2.1",
                        "name": "MyDocumentClassifier",
                        "version": "0.2.1"
                    },
                    {
                        "locator": "MySentenceClassifier_0.1.0",
                        "name": "MySentenceClassifier",
                        "version": "0.1.0"
                    },
                    {
                        "locator": "MySentenceClassifier_0.1.1",
                        "name": "MySentenceClassifier",
                        "version": "0.1.1"
                    }
                ]
            }
    """
    # Get access key from environment if not provided. Fail if can't find there.
    if not access_key:
        access_key = os.environ['SERMOS_ACCESS_KEY']

    resp = _search_model_api_response(access_key, model_name, version_pattern,
                                      search_model_endpoint)

    return resp
