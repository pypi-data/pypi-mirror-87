import base64
import time
import requests
import logging
import re
from Crypto.Hash import SHA1, HMAC

from pyvimond.utils import create_api_metadata


class VimondClient:

    def __init__(self, api_url, user, secret):
        self.api_url = api_url
        self.user = user
        self.secret = secret
        self.logger = logging.getLogger('VimondClient')

    def _get_auth_headers(self, method, path, user, secret):
        timestamp = time.strftime("%a, %d %b %Y %H:%M:%S %z")
        signature = self._get_signature(method, path, secret, timestamp)
        auth_header = "SUMO " + user + ":" + signature
        return {"Authorization": auth_header,
                "x-sumo-date": timestamp}

    @staticmethod
    def _get_signature(method, path, secret, timestamp):
        plain_path = re.sub(r"\?.*", "", path)
        string_to_sign = method + "\n" + plain_path + "\n" + timestamp
        sig_hash = HMAC.new(secret.encode('utf-8'), digestmod=SHA1)
        sig_hash.update(string_to_sign.encode('utf-8'))
        return base64.b64encode(sig_hash.digest()).decode("utf-8")

    def _admin_request_internal(self, api_url, method, path, user, secret, body=None):
        send_headers = self._get_auth_headers(method, path, user, secret)
        send_headers['Accept'] = 'application/json;v=3'
        send_headers['Content-Type'] = 'application/json;v=3'
        if method == "POST":
            response = requests.post(api_url + path,
                                     json=body,
                                     headers=send_headers,
                                     timeout=10)
        elif method == "PUT":
            response = requests.put(api_url + path,
                                    json=body,
                                    headers=send_headers,
                                    timeout=10)
        elif method == "GET":
            response = requests.get(api_url + path,
                                    headers=send_headers,
                                    timeout=10)
        if response.status_code == 404:
            return None
        if response.status_code == 200:
            return response.json()
        raise Exception('Request failed: status=' + str(response.status_code) + ": " + str(response.text))

    def _admin_request(self, method, path, body=None):
        return self._admin_request_internal(self.api_url, method, path, self.user, self.secret, body)

    def get_category(self, category_id):
        return self._admin_request("GET",
                                   f"/api/web/category/{str(category_id)}?expand=metadata&showHiddenMetadata=true")

    def get_asset(self, asset_id):
        return self._admin_request("GET", f"/api/web/asset/{str(asset_id)}?expand=metadata&showHiddenMetadata=true")

    def get_asset_metadata(self, asset_id):
        return self._admin_request("GET", f"/api/metadata/asset/{str(asset_id)}")

    def update_asset_metadata(self, asset_id, metadata):
        api_metadata = create_api_metadata(metadata)
        return self._admin_request("POST", f"/api/metadata/asset/{str(asset_id)}", api_metadata)

    def update_asset_data(self, asset_id, payload):
        return self._admin_request("PUT", f"/api/web/asset/{str(asset_id)}", payload)

    def update_category_metadata(self, category_id, metadata):
        api_metadata = create_api_metadata(metadata)
        return self._admin_request("POST", f"/api/metadata/category/{str(category_id)}", api_metadata)
