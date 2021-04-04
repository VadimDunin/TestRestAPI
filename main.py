import requests, os
from subprocess import Popen
from subprocess import PIPE

debug = True

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


class MyRequests(Utils):
    def __init__(self, base_url, port, credentials):
        self.base_url = base_url
        self.port = port
        self.username = credentials.username
        self.password = credentials.password

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
            # full_request = "curl -k -X {}".format(req)
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

    def exec_request(self):
        pass


class TerminalRequests(MyRequests):
    def __init__(self, base_url=base_url, port=port, credentials=Credentials):
        super().__init__(base_url, port, credentials)
        self.base_url = base_url
        self.auth_segment = "auth/session"
        self.auth_login = ' -H  "accept: application/json" -H  "Content-Type: application/json" -d "{\"username\": \"admin\",  \"password\": \"admin\"}\"'
        self.auth_request = "https://{}/{}\"".format(self.base_url, self.auth_segment) + self.auth_login

    def request_auth(self):
        print(self.request_via_curl(self.auth_request))


if __name__ == '__main__':
    TR = TerminalRequests()
    # TR.response_parser(TR.request_post(TR.auth_request))
    # TR.request_auth()
    auth_req = 'curl -k -X POST "https://'+base_url+'/auth/session" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{  \"username\": \"admin\",  \"password\": \"admin\"}"'
    output = TR.request_via_curl(auth_req)
    print(output)

    # url = 'http://ES_search_demo.com/document/record/_search?pretty=true'
    # data = '''{
    #   "query": {
    #     "bool": {
    #       "must": [
    #         {
    #           "text": {
    #             "record.document": "SOME_JOURNAL"
    #           }
    #         },
    #         {
    #           "text": {
    #             "record.articleTitle": "farmers"
    #           }
    #         }
    #       ],
    #       "must_not": [],
    #       "should": []
    #     }
    #   },
    #   "from": 0,
    #   "size": 50,
    #   "sort": [],
    #   "facets": {}
    # }'''
#    response = requests.post(url, data=data)

# curl -X POST "https://192.168.111.170:8090/auth/session" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{  \"username\": \"admin\",  \"password\": \"admin\"}"


# url='https://192.168.111.170:8090/auth/session" -H  "accept: application/json" -H  "Content-Type: application/json" -d '
# data='''
# {  \"username\": \"admin\",
#   \"password\": \"admin\"}"
# '''

# response = requests.post(url, data, verify=False)
# print(response)