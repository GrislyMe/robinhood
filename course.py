from ssl import PEM_cert_to_DER_cert
from user import CCU_User
from debug import Error
from bs4 import BeautifulSoup as bs
import requests
import logging

class Get_Course():
    def __init__(self, user: CCU_User):
        self.user = user

    def request_course_form(self, subcate: int):

        if not self.user.is_login:
            logging.error("user is not log in")
            return Error.LOGIN_FAIL

        url = r"http://kiki.ccu.edu.tw/~ccmisp06/cgi-bin/class/Add_Course01.cgi"

        data = {
                "session_id": self.user.session_id,
                "use_cge_new_cate": [
                    "1",
                    "$use_cge_new_cate"
                ],
                "page": "0",
                "e": "0",
                "grade": "1",
                "grade2": "1",
                "cge_cate": "2",
                "cge_subcate": subcate,
                "dept": "I001"
                }

        page = requests.post(url, data, headers = self.user.headers)
        if page == None:
            logging.error("can't get page")
            return Error.POST_REQUEST_FAIL

        courses_list = self.__get_course_table(page)

        logging.debug(courses_list)
        return courses_list

    def request_page_in_form(self, cge_cate: int, page_index: int):
        url = r"http://kiki.ccu.edu.tw/~ccmisp06/cgi-bin/class/Add_Course01.cgi"
        params = {
                "session_id": self.user.session_id,
                "use_cge_new_cate": 1,
                "m": 0,
                "dept": "I001",
                "grade": 1,
                "page": page_index,
                "cge_cate": 2,
                "cge_subcate": cge_cate
                }

        page = requests.get(url, params=params, headers=self.user.headers)
        if not page:
            logging.error("fail to requests page after first request")
            return Error.GET_REQUEST_FAIL

        courses_list = self.__get_course_table(page)
        if not courses_list:
            return Error.NO_FORM_IN_PAGE
        else:
            logging.debug(courses_list)

        return courses_list

    def send_submit(self, page: int, course_id: int, subcate: int):
        url = r"http://kiki.ccu.edu.tw/~ccmisp06/cgi-bin/class/Add_Course01.cgi"

        data = {
                "session_id": self.user.session_id,
                "dept": "I001",
                "grade": "1",
                "cge_cate": "2",
                "cge_subcate": subcate,
                "page": page,
                "e": "0",
                "m": "0",
                "SelectTag": "1",
                "course": f"{course_id}_01",
                f"{course_id}_01": "3"
                }

        ret = requests.post(url, data, headers=self.user.headers)
        ret.encoding = "utf-8"

        return 0

    def __get_course_table(self, page: requests.Response):
        page.encoding = "utf-8"

        form = bs(page.text, "html.parser").find("form")
        if not form:
            logging.error("no form found in page")
            return Error.NO_FORM_IN_PAGE

        table = form.find("table").find("table")
        if not table:
            logging.error("no table found in form")
            return Error.NO_TABLE_IN_FORM

        rows = table.find_all('tr')[1:]
        if not rows:
            logging.error("no data in table")
            return Error.EMPTY_TABLE

        courses_list = []
        for row in rows:
            cols = row.find_all('th')
            courses_list += [Course(cols[1: 9])]

        return courses_list

class Course():
    def __init__(self, course: list):
        try:
            self.current = int(course[0].text)
            self.empty = int(course[1].text)
        except ValueError:
            logging.error("courses info error")

        self.name = str(course[2].text)
        self.course_id = int(self.name[:7])
        self.teacher = course[3].text
        self.time = course[7].text

    def __str__(self):
        return f"{self.current}, {self.empty}, {self.course_id}, {self.name}, {self.time}"

    def __repr__(self):
        return f"{self.current}--{self.empty}--{self.course_id}--{self.name}--{self.time}"

