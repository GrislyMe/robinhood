from fake_useragent import UserAgent
from bs4 import BeautifulSoup as bs
from debug import Error
import logging
import requests
import time

class CCU_User:
    def __init__(self, account = "", passwd = ""):
        self.account = account
        self.passwd = passwd
        self.user_name = ""
        self.session_id = ""
        self.is_login = False
        self.is_alive = False
        self.is_idle = True

        self.headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "Host": "kiki.ccu.edu.tw",
                "Origin": "http://kiki.ccu.edu.tw",
                "User-Agent": UserAgent().random
                }

        self.params = {
                "session_id": self.session_id,
                "m": 0,
                "e": 0
                }
        return

    def set_userInfo(self, account: str, passwd: str):
        self.account = account
        self.passwd = passwd

    def stay_alive(self):
        url = r"http://kiki.ccu.edu.tw/~ccmisp06/cgi-bin/class/index.php"

        if self.session_id:
            while(self.is_alive and not self.is_idle):
                try:
                    requests.get(url, params = self.params, headers = self.headers)
                except:
                    logging.exception("can't send get request")
                    return Error.EXCEPTION_FATAL

                time.sleep(100)
        else:
            logging.warning("no session_id found, retry login...")
            return Error.NO_SESSION_ID
        return 0


    def login(self):
        url = r"http://kiki.ccu.edu.tw/~ccmisp06/cgi-bin/class/bookmark.php"

        data = {
                "version": 0,
                "id": self.account,
                "password": self.passwd,
                "term": "on",
                "m": 0
                }

        page = requests.post(url, headers = self.headers, data = data)
        page.encoding = "utf-8"

        #get session id
        self.session_id = page.url.split("session_id=")[1].split("&")[0]
        logging.debug(self.session_id)
        if self.session_id == None:
            logging.error("can't get session ID")
            return Error.LOGIN_FAIL

        #get user name
        self.user_name = bs(page.text, "html.parser").find("font", {"size": "2"})
        if self.user_name is None:
            logging.error("can't get user_name")
            return Error.LOGIN_FAIL
        else:
            self.user_name = self.user_name.text.split()[0]

        print(f"greeting {self.user_name}")

        self.is_login = True
        self.is_idle = True
        self.is_alive = True
        return 0

    def logout(self):
        url = rf"http://kiki.ccu.edu.tw/~ccmisp06/cgi-bin/class/logout.php?session_id={self.session_id}"

        ret = requests.get(url, headers=self.headers)
        ret.encoding = "utf-8"
        logging.debug(ret.text)

        return 0
