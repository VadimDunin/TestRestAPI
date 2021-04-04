class TerminalRequests:
    def __init__(self, app):
        self.app = app
        self.base_url = self.app.base_url
        self.auth_segment = "auth/session"
        self.auth_login = ' -H  "accept: application/json" -H  "Content-Type: application/json" -d "{\"username\": \"admin\",  \"password\": \"admin\"}\"'
        self.auth_request = "https://{}/{}\"".format(self.base_url, self.auth_segment) + self.auth_login

    def request_auth(self):
        print(self.app.exec_request(self.auth_request))