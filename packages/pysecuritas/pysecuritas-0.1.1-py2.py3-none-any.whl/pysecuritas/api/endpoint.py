# -*- coding: utf-8 -*-
"""
    :copyright: © pysecuritas, All Rights Reserved
"""
import time
from typing import Dict

from pysecuritas.core.utils import clean_response, get_response_value

DEFAULT_TIMEOUT = 60
RATE_LIMIT = 1


def handle_result(status, result):
    """
    Handle different status of an async request

    :param status current status
    :param result current result

    :return: the cleaned result if it's ok, if waiting, returns None
    """

    if status == "WAIT":
        return

    if status == "ERROR":
        raise RequestException(result["PET"]["MSG"])

    if status == "OK":
        return clean_response(result)


class Endpoint:
    """
    The entrypoint to perform any action on an alarm such as arm and disarm
    """

    def __init__(self, session, timeout=DEFAULT_TIMEOUT):
        """
        Initializes endpoint api with a session

        :param session session to access securitas api
        :param timeout timeout before given up on a request attempt
        """

        self.session = session
        self.timeout = timeout

    def get_inf(self) -> Dict:
        """
        Waits for signal 16 and gets the result from INF command

        :return: a response or nothing if timeout happens
        """

        payload = self.session.build_payload(ID=self.session.generate_request_id())
        payload.update(request="ACT_V2")
        self.session.validate_connection()
        threshold = time.time() + self.timeout
        while time.time() < threshold:
            time.sleep(RATE_LIMIT)
            result = self.session.get(payload)
            print(result)
            log = result["LIST"]["REG"][0]
            if log["@signaltype"] == "16":
                payload.update(request="INF", idsignal=log["@idsignal"], signaltype="16")
                result = self.session.get(payload)
                return handle_result(get_response_value(result)[0], result)

    def async_request(self, action, **params) -> Dict:
        """
        Performs a double request
        The first request is sent asynchronously with a given id
        That same id is then used to get the result

        :param action action to be performed
        :param params additional parameters for the request

        :return: a response or nothing if timeout happens
        """

        payload = self.session.build_payload(request=action, ID=self.session.generate_request_id(), **params)
        print(payload)
        self.session.validate_connection()
        payload["request"] = action + "1"
        self.session.get(payload)
        time.sleep(RATE_LIMIT)
        payload["request"] = action + "2"
        threshold = time.time() + self.timeout
        while time.time() < threshold:
            time.sleep(RATE_LIMIT)
            result = self.session.get(payload)
            result = handle_result(get_response_value(result)[0], result)
            if result:
                return result

    def request(self, action, **params) -> Dict:
        """
        Performs a simple request

        :param action action to be performed
        :param params additional parameters for the request

        :return: a response or nothing if timeout happens
        """

        payload = self.session.build_payload(request=action, ID=self.session.generate_request_id(), **params)
        self.session.validate_connection()
        result = self.session.get(payload)
        result = handle_result(get_response_value(result)[0], result)
        if result:
            return result


class RequestException(Exception):
    """
    Exception when unable to perform an action
    """

    def __init__(self, *args):
        super(RequestException, self).__init__(*args)
