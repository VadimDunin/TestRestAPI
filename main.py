import requests, os
from subprocess import Popen
from subprocess import PIPE

debug = True
use_curl = False
use_requests_lib = True

base_url = "192.168.1.103:8090"
port = "8090"


class Utils:
    def debug_msg(self, msg):
        if debug:
            print("DEBUG: {}\n".format(msg))

    def run_cmd(self, cmd, lang="ru_RU.UTF8"):
        test_env = os.environ.copy()
        test_env["LANG"] = lang
        p = Popen(cmd, stdout=PIPE, shell=True, env=test_env)
        stdout = p.communicate()[0].decode("utf8").strip()
        return p.returncode, stdout


class Credentials:
    username = "admin"
    password = "admin"


class BadResponses:
    response_list = ["<Response [404]>"]


class RestAPI(Utils):
    def __init__(self, base_url=base_url, port=port, credentials=Credentials):
        self.base_url = base_url
        self.port = port
        self.username = credentials.username
        self.password = credentials.password
        self.terminal = TerminalRequests(self)

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


class TerminalRequests:
    def __init__(self, app):
        self.app = app
        self.base_url = self.app.base_url
        self.auth_segment = "auth/session"
        self.auth_login = ' -H  "accept: application/json" -H  "Content-Type: application/json" -d "{\"username\": \"admin\",  \"password\": \"admin\"}\"'
        self.auth_request = "https://{}/{}\"".format(self.base_url, self.auth_segment) + self.auth_login

    def request_auth(self):
        print(self.app.exec_request(self.auth_request))


if __name__ == '__main__':
    TR = RestAPI()
    TR.terminal.request_auth()
