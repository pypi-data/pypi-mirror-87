import eventlet
requests = eventlet.import_patched('requests')
from deezer.gw import GW
from deezer.api import API
import json

__version__ = "0.0.10"

class TrackFormats():
    """Number associtation for formats"""
    FLAC    = 9
    MP3_320 = 3
    MP3_128 = 1
    MP4_RA3 = 15
    MP4_RA2 = 14
    MP4_RA1 = 13
    DEFAULT = 8
    LOCAL   = 0

class Deezer:
    def __init__(self):
        self.http_headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                          "Chrome/79.0.3945.130 Safari/537.36",
            "Accept-Language": None
        }
        self.session = requests.Session()
        self.session.mount('http://', requests.adapters.HTTPAdapter(pool_maxsize=100))
        self.session.mount('https://', requests.adapters.HTTPAdapter(pool_maxsize=100))

        self.logged_in = False
        self.current_user = {}
        self.childs = []
        self.selected_account = 0

        self.api = API(self.session, self.http_headers)
        self.gw = GW(self.session, self.http_headers)

    def set_accept_language(self, lang):
        self.http_headers['Accept-Language'] = lang

    def get_accept_language(self):
        return self.http_headers['Accept-Language']

    def login(self, email, password, re_captcha_token, child=0):
        # Check if user already logged in
        user_data = self.gw.get_user_data()
        if user_data['USER']['USER_ID'] == 0:
            self.logged_in = False
            return False
        # Get the checkFormLogin
        check_form_login = user_data['checkFormLogin']
        login = self.session.post(
            "https://www.deezer.com/ajax/action.php",
            data={
                'type': 'login',
                'mail': email,
                'password': password,
                'checkFormLogin': check_form_login,
                'reCaptchaToken': re_captcha_token
            },
            headers={'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', **self.http_headers}
        )
        # Check if user logged in
        if 'success' not in login.text:
            self.logged_in = False
            return False
        user_data = self.gw.get_user_data()
        self._post_login(user_data)
        self.change_account(child)
        self.logged_in = True
        return True

    def login_via_arl(self, arl, child=0):
        arl = arl.strip()
        cookie_obj = requests.cookies.create_cookie(
            domain='.deezer.com',
            name='arl',
            value=arl,
            path="/",
            rest={'HttpOnly': True}
        )
        self.session.cookies.set_cookie(cookie_obj)
        user_data = self.gw.get_user_data()
        # Check if user logged in
        if user_data["USER"]["USER_ID"] == 0:
            self.logged_in = False
            return False
        self._post_login(user_data)
        self.change_account(child)
        self.logged_in = True
        return True

    def _post_login(self, user_data):
        self.childs = []
        family = user_data["USER"]["MULTI_ACCOUNT"]["ENABLED"]
        if family:
            childs = self.gw.get_child_accounts()
            for child in childs:
                self.childs.append({
                    'id': child["USER_ID"],
                    'name': child["BLOG_NAME"],
                    'picture': child.get("USER_PICTURE", "")
                })
        else:
            self.childs.append({
                'id': user_data["USER"]["USER_ID"],
                'name': user_data["USER"]["BLOG_NAME"],
                'picture': user_data["USER"].get("USER_PICTURE", "")
            })

    def change_account(self, child_n):
        if len(self.childs)-1 >= child_n:
            self.current_user =self.childs[child_n]
            self.selected_account = child_n
        else:
            self.current_user = self.childs[0]
            self.selected_account = 0
        return (self.current_user, self.selected_account)
