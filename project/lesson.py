from re import compile
from time import sleep

import requests
from bs4 import BeautifulSoup


class Lesson:
    """
    author: adminerest
    """

    def __init__(self,
                 session,
                 evaluated_people,
                 evaluated_people_number,
                 questionnaire_code,
                 questionnaire_name,
                 evaluation_content_number,
                 evaluation_content,
                 error):
        self.session = session
        self.evaluated_people_number = evaluated_people_number
        self.questionnaire_code = questionnaire_code
        self.evaluation_content_number = evaluation_content_number
        self.questionnaire_name = questionnaire_name
        self.evaluated_people = evaluated_people
        self.evaluation_content = evaluation_content
        self.error = error

    def single_lesson_evaluate(self):

        """
        单门课程进行评教
        :return: flag
        """
        self.error.set("正在评价" + self.evaluation_content)
        flag, message, single_lesson_evaluation_page = self.get_evaluation_page_request()
        if not flag:
            self.error.set(message)
            return False
        evaluation_values = self.get_evaluation_values(single_lesson_evaluation_page)
        flag, message = self.submit_results_request(evaluation_values)
        return flag

    def submit_results_request(self, evaluation_values):
        """
        提交课程评教结果
        :param evaluation_values:
        :return: flag, message
        """
        url = "https://urp.shou.edu.cn/student/teachingEvaluation/teachingEvaluation/evaluation"
        sleep(30)  # 后端强制限时30秒后才能提交。。。这个坑了我一整天。。。2019-11-22-22:00:00
        try:
            rq = self.session.post(url=url, data=evaluation_values, timeout=5)  # 提交评价
        except requests.ConnectionError:
            return False, "提交评价失败！连接错误！"
        except requests.HTTPError:
            return False, "提交评价失败！请求网页有问题！"
        except requests.Timeout:
            return False, "提交评价失败！请求超时！"
        if rq.url == "https://urp.shou.edu.cn/login?errorCode=concurrentSessionExpired":
            return False, "请勿在程序运行时登录！"
        elif "success" in rq.text:  # 判断后端返回参数
            return True, "提交成功"
        else:
            return False, "提交失败"

    def get_evaluation_page_request(self):
        """
        获取一门课的评教页面
        :return: flag, message, html page
        """
        data = {
            "evaluatedPeopleNumber": self.evaluated_people_number,
            "questionnaireCode": self.questionnaire_code,
            "evaluationContentNumber": self.evaluation_content_number,
            "questionnaireName": self.questionnaire_name,
            "evaluatedPeople": self.evaluated_people,
            "evaluationContentContent": ""
        }
        url = "https://urp.shou.edu.cn/student/teachingEvaluation/teachingEvaluation/evaluationPage"
        try:
            single_lesson_evaluation_page = self.session.post(url=url, data=data, timeout=5)
        except requests.ConnectionError:
            return False, "获取评教页面失败！连接错误！", None
        except requests.HTTPError:
            return False, "获取评教页面失败！请求网页有问题！", None
        except requests.Timeout:
            return False, "获取评教页面失败！请求超时！", None
        if single_lesson_evaluation_page.url == "https://urp.shou.edu.cn/login?errorCode=concurrentSessionExpired":
            return False, "请勿在程序运行时登录！", None
        return True, "获取评教页面成功", single_lesson_evaluation_page

    def get_evaluation_values(self, single_lesson_evaluation_page):
        """
        使用bs抓取页面内容
        :param single_lesson_evaluation_page:
        :return: dict
        """
        data = {
            "questionnaireCode": self.questionnaire_code,
            "evaluationContentNumber": self.evaluation_content_number,
            "evaluatedPeopleNumber": self.evaluated_people_number,
            "zgpj": "老师非常好",
            "count": ""
        }
        bs = BeautifulSoup(single_lesson_evaluation_page.text, "html.parser")
        token_value = bs.find(name="input", attrs={"type": "hidden", "name": "tokenValue", "id": "tokenValue"})["value"]
        data["tokenValue"] = token_value
        # 寻找最高评价radio并获取参数
        buttons = bs.find_all(name="input", attrs={"type": "radio", "class": "ace", "value": compile(".*_1")})
        for button in buttons:  # 将选好的选项放入表单中，默认最高评教
            data[button["name"]] = button["value"]
        return data
