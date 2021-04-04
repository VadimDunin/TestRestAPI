import requests

from main import Utils, base_url, port, Credentials, BadResponses, use_curl, use_requests_lib
from req_lib import TerminalRequests


class RestAPI(Utils):
    def __init__(self, base_url=base_url, port=port, credentials=Credentials):
        self.base_url = base_url
        self.port = port
        self.username = credentials.username
        self.password = credentials.password
        self.tr = TerminalRequests(self)

    def request_post(self, req):
        try:
            self.debug_msg(req)
            response = requests.post(req)
            print(response)
            return response
        except requests.exceptions.SSLError:
            self.debug_msg("Ошибка SSL - сертификата")
        finally:
            response = requests.post(req, verify=False)
            print(response)
            return response

    def request_via_curl(self, req=None):
        if req is not None:
            full_request = req
            self.debug_msg(full_request)
            return self.run_cmd(full_request)[1]

    def request_get(self, req):
        try:
            self.debug_msg(req)
            response = requests.get(req)
            print(response)
            return response
        except requests.exceptions.SSLError:
            self.debug_msg("Ошибка SSL - сертификата")
        finally:
            response = requests.get(req, verify=False)
            print(response)
            return response

    def response_parser(self, response):
        for value in BadResponses.response_list:
            if str(response) == str(value):
                print("Возникла ошибка при выполнении запроса: {}".format(response))

    def exec_request(self, request):
        if use_curl:
            self.request_via_curl(req=request)
        elif use_requests_lib:
            self.request_get(req=request)