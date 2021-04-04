import os
from subprocess import Popen
from subprocess import PIPE
from rest_api import RestAPI

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


if __name__ == '__main__':
    TR = RestAPI()
    TR.tr.request_auth()
