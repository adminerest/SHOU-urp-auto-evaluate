import requests
from bs4 import BeautifulSoup
from re import compile
from time import sleep

# @Author:adminerest


class Lesson:

    def __init__(self,
                 session,
                 evaluatedPeople,
                 evaluatedPeopleNumber,
                 questionnaireCode,
                 questionnaireName,
                 evaluationContentNumber,
                 evaluationContent,
                 error):
        self.session = session
        self.evaluatedPeopleNumber = evaluatedPeopleNumber
        self.questionnaireCode = questionnaireCode
        self.evaluationContentNumber = evaluationContentNumber
        self.questionnaireName = questionnaireName
        self.evaluatedPeople = evaluatedPeople
        self.evaluationContent = evaluationContent
        self.error = error

    '''单门课程进行评教'''

    def evaluate(self):
        data = {"evaluatedPeopleNumber": self.evaluatedPeopleNumber,
                "questionnaireCode": self.questionnaireCode,
                "evaluationContentNumber": self.evaluationContentNumber,
                "questionnaireName": self.questionnaireName,
                "evaluatedPeople": self.evaluatedPeople,
                "evaluationContentContent": ""}
        self.error.set("正在评价" + self.evaluationContent)
        url = "https://urp.shou.edu.cn/student/teachingEvaluation/teachingEvaluation/evaluationPage"
        try:
            html = self.session.post(url=url, data=data, timeout=5)
        except requests.ConnectionError:
            self.error.set("获取评教页面失败！连接错误！")
            raise
        except requests.HTTPError:
            self.error.set("获取评教页面失败！请求网页有问题！")
            raise
        except requests.Timeout:
            self.error.set("获取评教页面失败！请求超时！")
            raise
        if html.url == "https://urp.shou.edu.cn/login?errorCode=concurrentSessionExpired":
            self.error.set("请勿在程序运行时登录！")
            raise
        data = {"questionnaireCode": self.questionnaireCode,
                "evaluationContentNumber": self.evaluationContentNumber,
                "evaluatedPeopleNumber": self.evaluatedPeopleNumber,
                "zgpj": "老师非常好",
                "count": ""}
        bs = BeautifulSoup(html.text, "html.parser")
        token_value = bs.find(name="input", attrs={"type": "hidden", "name": "tokenValue", "id": "tokenValue"})["value"]
        data["tokenValue"] = token_value
        # 寻找最高评价radio并获取参数
        buttons = bs.find_all(name="input", attrs={"type": "radio", "class": "ace", "value": compile(".*_1")})
        for button in buttons:  # 将选好的选项放入表单中，默认最高评教
            data[button["name"]] = button["value"]
        url = "https://urp.shou.edu.cn/student/teachingEvaluation/teachingEvaluation/evaluation"
        sleep(30)  # 后端强制限时30秒后才能提交。。。这个坑了我一整天。。。2019-11-22-22:00:00
        try:
            rq = self.session.post(url=url, data=data, timeout=5)  # 提交评价
        except requests.ConnectionError:
            self.error.set("提交评价失败！连接错误！")
            raise
        except requests.HTTPError:
            self.error.set("提交评价失败！请求网页有问题！")
            raise
        except requests.Timeout:
            self.error.set("提交评价失败！请求超时！")
            raise
        if rq.url == "https://urp.shou.edu.cn/login?errorCode=concurrentSessionExpired":
            self.error.set("请勿在程序运行时登录！")
            raise
        elif "success" in rq.text:  # 判断后端返回参数
            return True
        else:
            return False
