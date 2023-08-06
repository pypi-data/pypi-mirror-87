"""Default dispatcher implementation using Requests."""

import json
import logging
import mimetypes
import os
import time
from datetime import datetime
from json.decoder import JSONDecodeError

from dateutil.tz import UTC
from requests import Session


class Dispatcher(object):
    def __init__(self, backend):
        self.raw_results = False
        self.backend = backend
        self.backend.login()

    def send(
        self,
        method,
        path,
        params=None,
        data=None,
        file=None,
        filename=None,
        mimetype=None,
        rclass=None,
        rlist=False,
        rpartial=True,
    ):
        if method == "GET":
            result = self.backend.get(path, params=params)

        elif method == "POST":
            if file is None:
                result = self.backend.post(path, data=data)
            else:
                result = self.backend.upload(
                    path, file, filename=filename, mimetype=mimetype
                )

        elif method == "PUT":
            result = self.backend.put(path, data=data)

        elif method == "DELETE":
            result = self.backend.delete(path, params=params, data=data)

        else:
            raise ValueError(f"unknown method {method}")

        if self.raw_results:
            return result

        if rclass:
            class_result = rclass.from_data(result, partial=rpartial)

            if rlist and not isinstance(class_result, list):
                return [class_result]
            else:
                return class_result

        return result


class RequestsBackend(object):
    """Send/Receive data via TeamDynamix WebApi with Requests library."""

    def __init__(self, organization, beid, wskey, use_sandbox, json_encoder):
        """Initialize dispatcher backend."""
        if use_sandbox:
            api_base = "SBTDWebApi"
        else:
            api_base = "TDWebApi"

        self.base_url = f"https://{organization.lower()}.teamdynamix.com/{api_base}"
        self.beid = beid
        self.wskey = wskey
        self.json_encoder = json_encoder
        self.logger = logging.getLogger("tdxapi-dispatcher")

        # initialize requests Session
        self.session = Session()
        self.session.headers.update({"Content-Type": "application/json"})

    def login(self):
        """Admin login using BEID and WebServicesKey."""
        url = self.base_url + "/api/auth/loginadmin"
        payload = {"BEID": self.beid, "WebServicesKey": self.wskey}

        self.logger.debug(f"Sending POST request to {url}")
        response = self.session.post(
            url, headers={"Authorization": None}, data=json.dumps(payload)
        )

        if response.ok:
            self.session.headers.update({"Authorization": f"Bearer {response.text}"})
            self.logger.debug(
                f"Response {response.status_code}: Authorization successful"
            )
        else:
            raise PermissionError("Authorization Failed")

    def get(self, path, params=None):
        """Send HTTP GET request."""
        url = self.base_url + path

        self.logger.debug(f"Sending GET request to {url} with {params}")
        r = self.session.get(url, params=params)

        return self.process(r)

    def post(self, path, data=None):
        """Send HTTP POST request."""
        url = self.base_url + path
        json_data = json.dumps(data, cls=self.json_encoder)

        self.logger.debug(f"Sending POST request to {url} with {json_data}")
        r = self.session.post(url, data=json_data)

        return self.process(r)

    def put(self, path, data=None):
        """Send HTTP PUT request."""
        url = self.base_url + path
        json_data = json.dumps(data, cls=self.json_encoder)

        self.logger.debug(f"Sending PUT request to {url} with {json_data}")
        r = self.session.put(url, data=json_data)

        return self.process(r)

    def delete(self, path, params=None, data=None):
        """Send HTTP DELETE request."""
        url = self.base_url + path
        json_data = json.dumps(data, cls=self.json_encoder)

        self.logger.debug(
            f"Sending DELETE request to {url} with {params} and {json_data}"
        )
        r = self.session.delete(url, params=params, data=json_data)

        return self.process(r)

    def upload(self, path, file, filename=None, mimetype=None):
        """Post a multipart-encoded file."""
        if filename is None:
            filename = os.path.basename(file)

        if mimetype is None:
            mimetype = mimetypes.guess_type(file)[0]

        url = self.base_url + path
        files = {"file": (filename, open(file, "rb"), mimetype)}

        # Override session Content-Type to let Requests handle it
        headers = {"Content-Type": None}

        self.logger.debug(f"Sending POST request to {url} with file data")
        r = self.session.post(url, headers=headers, files=files)

        return self.process(r)

    def process(self, response, retry=1):
        """Process response based on status code."""
        self.logger.debug(f"Response {response.status_code}: {response.text}")

        # OK - 200 - Return response
        if response.status_code == 200 or response.status_code == 201:
            if response.text:
                try:
                    return response.json()
                except JSONDecodeError:
                    return response.text
            else:
                return None

        # Too Many Requests - 429 - Wait until we can start requests again
        elif response.status_code == 429:
            # Get UTC datetime when requests can begin again
            reset_utc = datetime.strptime(
                response.headers["X-RateLimit-Reset"], "%a, %d %b %Y %H:%M:%S GMT"
            ).replace(tzinfo=UTC)

            # Get current UTC datetime
            now_utc = datetime.strptime(
                response.headers["Date"], "%a, %d %b %Y %H:%M:%S GMT"
            ).replace(tzinfo=UTC)

            # Sleep for the number of seconds between now and the reset datetime
            sleep_for = int((reset_utc - now_utc).total_seconds()) + 5
            self.logger.info(f"Rate limit exceeded, waiting {sleep_for} seconds")
            time.sleep(sleep_for)

            # Retry the request
            self.logger.debug("Retrying previously failed request")
            response = self.session.send(response.request)

            return self.process(response)

        # Unauthorized - 401 - Retry request with fresh token before raising error
        elif response.status_code == 401:
            if retry > 0:
                # Get a new token
                self.login()

                # Update auth header on prepared request
                response.request.headers.update(
                    {"Authorization": self.session.headers["Authorization"]}
                )

                # Retry request
                self.logger.debug("Retrying previously failed request")
                return self.process(self.session.send(response.request), retry=0)
            else:
                raise PermissionError("Unauthorized")

        # Not Found - 404 - Return None
        elif response.status_code == 404:
            return None

        # Raise exception for any other status codes
        else:
            try:
                msg = response.json()
                raise Exception(
                    f"{response.status_code}: {msg['Message']} (ID: {msg['ID']})"
                )
            except (JSONDecodeError, KeyError, TypeError):
                raise Exception(f"{response.status_code}: {response.text}")
