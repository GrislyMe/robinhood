#!/usr/bin/env python3
from user import CCU_User
from course import Get_Course
#from course import Course
from debug import logger_init
from debug import Error
import time


def main():
    logger_init(enable_debug=True)

    #account = "407410001"
    #passwd = "NpFcD02-15"
    account = "407530012"
    passwd = "andy0707"
    user = CCU_User(account, passwd)
    user.login()

    #try to keep the connection
    #alive_daemon = threading.Thread(target = user.stay_alive, args = "")
    #alive_daemon.start()
    crawler = Get_Course(user)
    crawler.request_course_form(2)
    course = []

    sub_cate = 2
    page_max = 2
    with open("target", "r") as t:
        target = t.readlines()
        target = [i[:-1] for i in target]

    while 1:
        for i in range(1, page_max + 1):
            courses = crawler.request_page_in_form(sub_cate, i)
            if type(courses) is not list:
                return Error.GET_REQUEST_FAIL
            for course in courses:
                if course.course_id in target and course.empty:
                    ret = crawler.send_submit(i, course.course_id, sub_cate)
                    if ret == 0:
                        print("got it")
            time.sleep(5)

    #alive_daemon.join()

if __name__ == "__main__":
    main()
