from logging import Logger as __Logger
from logging import getLogger

import vcr as __vcr

# Centralized instance of vcr. Use this in test cases to avoid leaking keys.
vcr = __vcr.VCR(filter_query_parameters=["api-key"])

# Main logger during test-cases.
LOGGER: __Logger = getLogger(__name__)
