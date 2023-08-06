"""
Trace module
"""

import json
import logging
from retry import retry
from concurrent.futures import ThreadPoolExecutor, wait
from functools import partial
from typing import Callable
import requests
from requests import Session
from superwise.exceptions.superwise_exceptions import SuperwiseDataError
from superwise.validations.superwise_validator import *


class Trace:

    def __init__(self, session: Session, token: str, host: str, protocol: str, customer:str):
        self._logger = logging.getLogger(__name__)
        self._session = session
        self._token = token
        self._host = host
        if customer:
            self._uri = f"{protocol}://{host}/{customer}" + "/trace/v1/task/{task_id}/"
        else:
            self._uri = f"{protocol}://{host}" + "/trace/v1/task/{task_id}/"

    def prediction_emit(self, data, task_id: str, version_id: str):
        """
        send trace prediction single record(single mode)
        """
        url = str(self._uri.format(task_id=task_id) + 'prediction/emit')
        body = dict(record=data, version_id=version_id)
        validator = valid_trace_prediction_emit
        return self._prediction_helper_func(url=url, body=body, validator=validator, chunk_size=-1, is_label=False)

    def prediction_batch(self, data, task_id: str, version_id: str, chunk_size: int = 10, category='D'):
        """
        send trace prediction records(batch mode)
        """
        url = str(self._uri.format(task_id=task_id) + 'prediction/batch')
        body = dict(records=data, version_id=version_id, category=category)
        validator = valid_trace_prediction_batch
        return self._prediction_helper_func(url=url, body=body, validator=validator, chunk_size=chunk_size,
                                            is_label=False)

    def prediction_file(self, file_url: str, task_id: str, version_id: str):
        """
        send trace batch request with path to file in s3.
        """
        url = str(self._uri.format(task_id=task_id) + 'prediction/file')
        body = dict(file_url=file_url, version_id=version_id)
        validator = valid_trace_prediction_file
        return self._prediction_helper_func(url=url, body=body, validator=validator, chunk_size=-1, is_label=False)

    def label_emit(self, data, task_id: str):
        """
        send trace label prediction single record(single mode)
        """
        url = str(self._uri.format(task_id=task_id) + 'label/emit')
        validator = valid_trace_label_emit
        return self._prediction_helper_func(url=url, body=data, validator=validator, chunk_size=-1, is_label=True)

    def label_batch(self, data, task_id: str, chunk_size: int = 100, category='D'):
        """
        send trace label prediction records(batch mode)
        """
        url = str(self._uri.format(task_id=task_id) + 'label/batch')
        body = dict(records=data, category=category)
        validator = valid_trace_label_batch
        return self._prediction_helper_func(url=url, body=body, validator=validator, chunk_size=chunk_size,
                                            is_label=True)

    def label_file(self, file_url: str, task_id: str):
        """
        send trace batch request with path to file in s3.
        """
        url = str(self._uri.format(task_id=task_id) + 'label/file')
        body = dict(file_url=file_url)
        validator = valid_trace_label_file
        return self._prediction_helper_func(url=url, body=body, validator=validator, chunk_size=-1, is_label=True)

    def _prediction_helper_func(self, url: str, body: dict, validator: Callable, chunk_size: int, is_label: bool):
        """
        Centralize function to send post request to the server
        :param url: end point URI
        :param body: request body
        :param validator: validate the body structure
        :param _retry: amount of times try to send post
        :return: Error or Response Code of the request
        """
        headers = {'Content-Type': 'application/json',
                  'Authorization': self._session.headers.get('Authorization')}
        self._logger.info(f" send {url} request")
        if validator(data=body):
            if chunk_size == -1:
                res = self._session.post(url=url, data=json.dumps(body), headers=headers)
                self._logger.info(
                    f"request {url}  return with status code {res.status_code}")
                return res.status_code
            else:
                chunks = []
                for i in range(0, len(body["records"]), chunk_size):
                    if not is_label:
                        chunks.append({"records": body["records"][i:i + chunk_size],
                                       "version_id": body["version_id"],
                                       "category": body.get("category", "D")})
                    else:
                        chunks.append({"records": body["records"][i:i + chunk_size],
                                       "category": body.get("category", "D")})

                with ThreadPoolExecutor(max_workers=20) as executor:
                    futures = [executor.submit(partial(self._send_data, url,headers),chunk) for chunk in chunks]
                wait(futures)
                try:
                    [res.result() for res in futures]
                    return 201
                except:
                    raise SuperwiseDataError("problem send data to superwise")
        self._logger.info(f"request {url}  with wrong data format")
        raise SuperwiseDataError("data don't in the right format")

    @retry(SuperwiseDataError, tries=3, delay=3)
    def _send_data(self, url, headers,chunk):
        res = self._session.post(url=url, data=json.dumps(chunk), headers=headers)
        if res.status_code != 201:
            raise SuperwiseDataError("problem send data to superwise")
        return True
