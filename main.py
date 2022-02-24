#!/usr/bin/env python3
from user import CCU_User
from course import Get_Course
#from course import Course
from debug import logger_init
from debug import Error
import time

def one_cycle():
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

    counter = 0
    select = 0
    while counter < 100:
        for i in range(1, page_max + 1):
            courses = crawler.request_page_in_form(sub_cate, i)
            if type(courses) is not list:
                return Error.GET_REQUEST_FAIL
            for course in courses:
                if course.course_id in target and course.empty:
                    ret = crawler.send_submit(i, course.course_id, sub_cate)
                    if ret == 0:
                        select += 1
                        print("got it")
            time.sleep(5)
            counter += 1

    user.logout()
    return str(select)

def main():
    logger_init(enable_debug=True)

    #account = "407410001"
    #passwd = "NpFcD02-15"
    select = 0
    while(1):
        select = one_cycle()
        if type(select) is str:
            with open("result", "w") as op:
                op.write(select)

    #alive_daemon.join()

if __name__ == "__main__":
    main()
