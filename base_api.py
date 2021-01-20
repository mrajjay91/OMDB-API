#!/usr/bin/env python
# -- coding: utf-8 --
"""
Generic class for API related request
"""

import requests
from requests.exceptions import HTTPError


class BaseAPI:
    def _init_(self, url, params):
        self.url = url
        self.params = params

    def get_request(self):
        """
        GET request for API
        :return:
        """
        try:
            response = requests.get(url=self.url, params=self.params, timeout=10)
            response.raise_for_status()
        except HTTPError as http_err:
            raise http_err
        except Exception as err:
            raise err
        else:
            return response.json()
