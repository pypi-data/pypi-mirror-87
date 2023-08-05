""" Constants used in application
"""
import os
from urllib.parse import urljoin

DEFAULT_BASE_URL = os.environ.get('DEFAULT_BASE_URL',
                                  "https://console.sermos.ai/api/v1/")
DEFAULT_DEPLOY_URL = urljoin(DEFAULT_BASE_URL, 'deploy')
DEFAULT_GET_MODEL_URL = urljoin(DEFAULT_BASE_URL, 'models/store-credentials')
DEFAULT_STORE_MODEL_URL = urljoin(DEFAULT_BASE_URL, 'models/store-credentials')
DEFAULT_SEARCH_MODEL_URL = urljoin(DEFAULT_BASE_URL, 'models')
S3_MODEL_BUCKET = 'sermos-client-models'
