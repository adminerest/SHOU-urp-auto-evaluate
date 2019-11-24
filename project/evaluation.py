import io
from typing import Tuple

import requests
from PIL import Image, ImageTk

from lesson import Lesson


# @Author:adminerest


class Evaluation:
    def __init__(self, error):
        self.session = requests.session()  # 初始化个session
        self.error = error  # 传入信息显示模块

    '''
    进行评教
    '''

    def evaluate(self):
        try:
            lessons = self.get_unfinished_lessons()  # 获取未评教课程列表
            count = 0
            self.error.set("登录成功！\n正在评教...请稍等")
            for les in lessons:
                if les.evaluate():  # 每门课程进行评教，返回是否评教成功
                    count += 1
            if count == len(lessons):  # 判断多少课程评教成功
                self.error.set("全部课程评教成功！")
            elif count == 0:
                self.error.set("没有课程评教成功！")
            else:
                self.error.set("部分课程评教成功！")
        except:
            return False

    '''
    获取需要评教的课程基本信息
    '''

    def get_unfinished_lessons(self):
        lessons = []
        list_url = "https://urp.shou.edu.cn/student/teachingEvaluation/teachingEvaluation/search"
        try:
            html = self.session.post(url=list_url, timeout=5)  # 获取评教列表
        except requests.ConnectionError:
            self.error.set("获取待评教列表失败！连接错误！")
            raise
        except requests.HTTPError:
            self.error.set("获取待评教列表失败！请求网页有问题！")
            raise
        except requests.Timeout:
            self.error.set("获取待评教列表失败！请求超时！")
            raise
        if html.url == "https://urp.shou.edu.cn/login?errorCode=concurrentSessionExpired":
            self.error.set("请勿在程序运行时登录！")
            raise
        info = html.content
        lessons_list = eval(info)["data"]
        for lesson_info in lessons_list:
            if lesson_info["isEvaluated"] == "否":  # 为未评教的课程创建对象
                lesson_data = Lesson(self.session,
                                     lesson_info["evaluatedPeople"],
                                     lesson_info["id"]["evaluatedPeople"],
                                     lesson_info["id"]["questionnaireCoding"],
                                     lesson_info["questionnaire"]["questionnaireName"],
                                     lesson_info["id"]["evaluationContentNumber"],
                                     lesson_info["evaluationContent"],
                                     self.error)
                lessons.append(lesson_data)
        return lessons

    def get_login_img(self):
        """
        获取验证码图片
        :return:
        """
        flag, pil_image, message = self.get_verification_code_image()
        if not flag:
            self.error.set(message)
            return None
        tk_image = ImageTk.PhotoImage(pil_image)
        return tk_image

    def get_verification_code_image(self):
        """
        获取验证码图片请求
        :return: image, error message
        """
        try:
            login_img = self.session.get("https://urp.shou.edu.cn/img/captcha.jpg", timeout=5)
        except requests.ConnectionError:
            return False, None, "获取验证码失败！连接错误！"
        except requests.HTTPError:
            return False, None, "获取验证码失败！请求网页有问题！"
        except requests.Timeout:
            return False, None, "获取验证码失败！请求超时！"
        else:
            image_bytes = login_img.content
            data_stream = io.BytesIO(image_bytes)
            pil_image = Image.open(data_stream)
            return True, pil_image, "获取验证码成功"

    def login(self, user, password, code) -> bool:
        """
        登录
        :param user: username
        :param password: password
        :param code: verify code
        :return: login result :`True` or `False`
        """
        flag, message = self.login_request(username=user, password=password, code=code)
        if not flag:
            self.error.set(message)
        return flag

    def login_request(self, username, password, code) -> Tuple[bool, str]:
        """
        登录请求
        :param username: username
        :param password: password
        :param code: verificationCode
        :return: login result and error message
        """
        data = {
            "j_username": username,
            "j_password": password,
            "j_captcha": code,
            "_spring_security_remember_me": "on"
        }
        try:
            rp = self.session.post(url="https://urp.shou.edu.cn/j_spring_security_check", data=data, timeout=5)
        except requests.ConnectionError:
            return False, "登录失败！连接错误！"
        except requests.HTTPError:
            return False, "登录失败！请求网页有问题！"
        except requests.Timeout:
            return False, "登录失败！请求超时！"
        else:
            if rp.url == "https://urp.shou.edu.cn/login?errorCode=badCaptcha":
                return False, "验证码输入错误！"
            elif rp.url == "https://urp.shou.edu.cn/login?errorCode=badCredentials":
                return False, "用户名或密码输入错误！"
        return True, "登录成功"
