import io
import requests
from PIL import Image, ImageTk
from lesson import Lesson

# @Author:admineres


class Evaluation:
    def __init__(self, error):
        self.session = requests.session()  # 初始化个session
        self.error = error  # 传入信息显示模块

    '''
    进行评教
    '''

    def evaluate(self):
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

    '''
    获取需要评教的课程基本信息
    '''

    def get_unfinished_lessons(self):
        lessons = []
        list_url = "https://urp.shou.edu.cn/student/teachingEvaluation/teachingEvaluation/search"
        try:
            info = self.session.post(url=list_url).content  # 获取评教列表
        except requests.ConnectionError:
            self.error.set("获取待评教列表失败！连接错误！")
            exit(0)
        except requests.HTTPError:
            self.error.set("获取待评教列表失败！请求网页有问题！")
            exit(0)
        except requests.Timeout:
            self.error.set("获取待评教列表失败！请求超时！")
            exit(0)
        lessons_list = eval(info)["data"]
        for lesson_info in lessons_list:
            if lesson_info["isEvaluated"] == "否":  # 为未评教的课程创建对象
                lesson_data = Lesson(self.session,
                                     lesson_info["evaluatedPeople"],
                                     lesson_info["id"]["evaluatedPeople"],
                                     lesson_info["id"]["questionnaireCoding"],
                                     lesson_info["questionnaire"]["questionnaireName"],
                                     lesson_info["id"]["evaluationContentNumber"],
                                     self.error)
                lessons.append(lesson_data)
        return lessons

    '''
    获取验证码图片
    '''

    def get_login_img(self):
        try:
            login_img = self.session.get("https://urp.shou.edu.cn/img/captcha.jpg")
        except requests.ConnectionError:
            self.error.set("获取验证码失败！连接错误！")
            return None
        except requests.HTTPError:
            self.error.set("获取验证码失败！请求网页有问题！")
            return None
        except requests.Timeout:
            self.error.set("获取验证码失败！请求超时！")
            return None
        else:
            image_bytes = login_img.content
            data_stream = io.BytesIO(image_bytes)
            pil_image = Image.open(data_stream)
            tk_image = ImageTk.PhotoImage(pil_image)
            return tk_image

    '''
    进行登录
    '''

    def login(self, user, password, code):
        data = {"j_username": user, "j_password": password, "j_captcha": code,
                "_spring_security_remember_me": "on"}
        try:
            rp = self.session.post(url="https://urp.shou.edu.cn/j_spring_security_check", data=data)
        except requests.ConnectionError:
            self.error.set("登录失败！连接错误！")
            return False
        except requests.HTTPError:
            self.error.set("登录失败！请求网页有问题！")
            return False
        except requests.Timeout:
            self.error.set("登录失败！请求超时！")
            return False
        else:
            if rp.url == "https://urp.shou.edu.cn/login?errorCode=badCaptcha":
                self.error.set("验证码输入错误！")
                return False
            elif rp.url == "https://urp.shou.edu.cn/login?errorCode=badCredentials":
                self.error.set("用户名或密码输入错误！")
                return False
        return True
