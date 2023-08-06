#  Copyright (c) 2020 Data Spree GmbH - All Rights Reserved
#  Unauthorized copying of this file, via any medium is strictly prohibited.
#  Proprietary and confidential.

from requests.auth import AuthBase


class HTTPTokenAuth(AuthBase):
    """Attaches Token Authentication to the given Request object."""
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        # add authentication header with token
        r.headers['Authorization'] = 'Token {}'.format(self.token)
        return r
