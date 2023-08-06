# coding=utf-8
import json
import logging

__author__ = 'ThucNC'

import configparser
import os
from typing import List, Union

import magic
import requests
from ucode.helpers.clog import CLog
from ucode.helpers.misc import make_slug
from ucode.models.problem import Problem, TestCase
from ucode.models.question import Question, QuestionType
from ucode.services.dsa.problem_service import ProblemService

_logger = logging.getLogger(__name__)


class UCode:
    def __init__(self, base_url, token):
        self.s = requests.session()
        self.api_base_url = base_url
        self.token = token
        self._headers = {
            'access-token': self.token
        }

    def upload_file(self, file_path, upload_folder):
        url = self.get_api_url(f"/general/upload-file?folder={upload_folder}")
        # url = "https://httpbin.org/post"
        with open(file_path, 'rb') as f:
            file_name = os.path.basename(file_path)
            print(file_name)
            # content_type = "application/binary"
            content_type = magic.from_file(file_path, mime=True)
            print("Content-Type:", content_type)
            files = {'file': (file_name, f, content_type)}
            response = self.s.post(url, files=files, headers=self._headers)
            # file_content = open(file_path, 'rb').read()
            # data = {'file': file_content}
            # response = self.s.post(url, data=data, headers=self._headers)
            # print("url:", url)
            # print("payload:", json.dumps(data))
            print("status code", response.status_code)
            print(response.text)
            if response.ok:
                return response.json().get("data")
        return None

    def upload_and_replace_problem_resource(self, problem: Problem, upload_folder="problem_resources"):
        if not problem.resource_files:
            return

        for resource in problem.resource_files:
            filename = os.path.basename(resource)
            print("resource:", filename, resource)
            remote_url = self.upload_file(resource, upload_folder)
            if not remote_url:
                CLog.error(f"Cannot upload file `{resource}`")
            ProblemService.replace_image_urls(problem, filename, remote_url)

    def get_api_url(self, path):
        return self.api_base_url + path

    def create_problem(self, lesson_id, problem: Union[Question, Problem, str],
                       score=100, xp=100, lang='vi', statement_format="markdown", question_type='code',
                       is_server_judge=True, status="published", visibility="public"):
        """

        :param lesson_id:
        :param problem:
        :param score:
        :param xp: -1 để tự động tính theo độ khó
        :param lang:
        :param statement_format:
        :param question_type: multiple_choice, short_answer, code, turtle, sport
        :return:
        """
        if isinstance(problem, str):
            problem: Problem = ProblemService.load(problem, load_testcase=True)

        if isinstance(problem, Problem):
            self.upload_and_replace_problem_resource(problem)

            ucoin = xp
            if ucoin < 0:
                ucoin = int(round(50 * problem.difficulty**1.5, -2))
            if ucoin <= 0:
                ucoin = 100
            data = {
                "name": problem.name,
                "slug": problem.slug,
                "type": question_type,
                "statement": problem.statement,
                "statement_format": statement_format,
                "input_desc": problem.input_format,
                "output_desc": problem.output_format,
                "constraints": problem.constraints,
                "compiler": "python",
                "statement_language": lang,
                "score": score,
                "solution": problem.solution,
                "difficulty": problem.difficulty,
                "status": status,
                "visibility": visibility,
                "ucoin": ucoin,
                "source": problem.src_url if problem.src_url else "",
                'is_server_judge': is_server_judge
            }
            if not lesson_id:
                data['tags'] = problem.tags
        elif isinstance(problem, Question):
            question: Question = problem
            data = {
                "name": question.src_name,
                "type": question.type.value or question_type,
                "statement": question.statement,
                "statement_format": statement_format,
                "statement_language": lang,
                "score": score,
                "status": status,
                "visibility": visibility,
                "ucoin": xp,
                "constraints": "base_question" if question.base_question else
                                               ("sub_question" if question.sub_question else "")
            }

            new_option_format = True
            # new_option_format = False
            # if not isinstance(question.options, list):
            #     new_option_format = True
            # else:
            #     for i, option in enumerate(question.options):
            #         if not isinstance(option, QuestionOption):
            #             # CLog.error("Option not valid:")
            #             # print(question.to_json())
            #             new_option_format = True
            #             break
            #         if not option.content:
            #             new_option_format = True
            #             break
            #         data[f"option{i + 1}"] = option.content
            #         if option.is_correct:
            #             data['answer'] = f"{i + 1}"

            question_json = json.loads(question.to_json())
            if question.solution:
                data['solution'] = question.solution
            elif question.solutions:
                data['solutions'] = json.dumps(question_json['solutions'])

            if question.hint:
                data['hint'] = json.dumps(question_json["hint"])

            if question.statement_media:
                data['statement_media'] = json.dumps(question_json["statement_media"])

            if question.option_display:
                data['option_display'] = json.dumps(question_json["option_display"])

            if question.source:
                data['source'] = json.dumps(question_json["source"])

            if new_option_format:
                data['options'] = json.dumps(question_json["options"])

            if question.answer is not None:
                data['answers'] = question.answer
            if question.type == QuestionType.SHORT_ANSWER:
                print("data:", data)
        else:
            raise Exception(f"Unsupported problem type {type(problem)}")

        if lesson_id:
            url = self.get_api_url(f"/lesson-item/{lesson_id}/question")
        else:
            url = self.get_api_url(f"/problems")
            data['slug'] = make_slug(problem.name)

        response = self.s.post(url, json=data, headers=self._headers)
        # print("url:", url)
        # print("payload:", json.dumps(data))
        print("status code", response.status_code)
        # print(response.text)
        res = response.json()
        # print(res)
        if res['success']:
            question_id = res['data']['id']
            print("question_id:", question_id)
        else:
            raise Exception("Cannot create question:" + json.dumps(res))

        if isinstance(problem, Problem):
            # upload testcase
            # for i, testcase in enumerate(problem.testcases):
            #     self.upload_testcase(question_id, testcase, is_sample=i<2)
            self.upload_testcases(question_id, ProblemService.join_testcases(problem))

        if isinstance(problem, Problem):
            if problem.translations:
                for tran_lang, tran_problem in problem.translations.items():
                    CLog.info(f"Creating translation {tran_lang} for question #{question_id}...")
                    data = {
                        "name": tran_problem.name,
                        "type": "code",
                        "root_question_id": question_id,
                        "statement": tran_problem.statement,
                        "statement_language": tran_lang,
                        "input_desc": tran_problem.input_format,
                        "output_desc": tran_problem.output_format,
                        "constraints": tran_problem.constraints,
                        "status": status,
                        "visibility": visibility,

                    }
                    # print("url:", url)
                    # print("payload:", json.dumps(data))

                    response = self.s.post(url, json=data, headers=self._headers)
                    print("status code", response.status_code)
                    # print(response.text)
                    res = response.json()
                    if res['success']:
                        tran_question_id = res['data']['id']
                        print("translated question_id:", tran_question_id)
                    else:
                        raise Exception("Cannot create question:" + json.dumps(res))

        return question_id

    def create_problems(self, lesson_id, problems: List[Problem], score=10, xp=100, lang="vi"):
        question_ids = []
        for problem in problems:
            q_id = self.create_problem(self, lesson_id=lesson_id,
                                       problem=problem,
                                       score=score, xp=xp, lang=lang)
            question_ids.append(q_id)

        return question_ids

    def upload_testcases(self, problem_id, testcases: List[TestCase], samples=None, score=10):
        url = self.get_api_url(f"/question/{problem_id}/upload-testcases")
        testcase_data = []
        for i, testcase in enumerate(testcases):
            t = {
                "name": testcase.name,
                "explanation": testcase.explanation,
                "input": testcase.input,
                "output": testcase.output,
                "score": score,
                "is_sample": testcase.sample
            }
            testcase_data.append(t)
        payload = {
            "testcases": testcase_data
        }

        response = self.s.post(url, json=payload, headers=self._headers)
        print("status_code:", response.status_code)
        print(response.text)
        res = response.json()
        # print(res)
        if res['success']:
            print(len(testcases), "testcase(s) upload successfully")
        else:
            CLog.error("Cannot create testcase:" + json.dumps(res))

    def upload_testcase(self, problem_id, testcase: TestCase, is_sample=True, score=10):
        url = self.get_api_url(f"/question/{problem_id}/testcase")
        data = {
            "name": testcase.name,
            "explanation": testcase.explanation,
            "input": testcase.input,
            "output": testcase.output,
            "score": score,
            "is_sample": bool(is_sample)
        }

        response = self.s.post(url, json=data, headers=self._headers)
        print(response.status_code)
        res = response.json()
        print(res)
        if res['success']:
            testcase_id = res['data']['id']
            print("testcase_id:", testcase_id)
        else:
            CLog.error("Cannot create testcase:" + json.dumps(res))

    @staticmethod
    def read_credential(credential_file):
        config = configparser.ConfigParser()
        config.read(credential_file)
        if not config.has_section('UCODE'):
            CLog.error(f'Section `UCODE` should exist in {credential_file} file')
            return None, None
        if not config.has_option('UCODE', 'api_url') or not config.has_option('UCODE', 'token'):
            CLog.error(f'api_url and/or token are missing in {credential_file} file')
            return None, None

        api_url = config.get('UCODE', 'api_url')
        token = config.get('UCODE', 'token')

        return api_url, token

    def create_chapter(self, course_id, chapter_name, slug=None, parent_id=None,
                       status="draft", _type="chapter", is_free=True):
        if not slug:
            slug = make_slug(chapter_name)

        data = {
            "parent_id": parent_id if parent_id else 0,
            "item_type": _type,
            "name": chapter_name,
            "is_preview": False,
            # "content_type": "video",
            "is_free": is_free,
            "slug": slug,
            "status": status
        }

        url = self.get_api_url(f"/curriculum/{course_id}/course-items")

        response = self.s.post(url, json=data, headers=self._headers)

        print(response.status_code)
        res = response.json()
        print(res)
        if res['success']:
            return res['data']['id']
        else:
            raise Exception("Cannot create chapter:" + json.dumps(res))

    def create_lesson_item(self, course_id, chapter_id, lesson_name, slug=None,
                           desciption="", content="",
                           type="video", video_url="",
                           status="draft", is_free=True, visibility="public", ucoin=100):
        if not slug:
            slug = make_slug(lesson_name)

        data = {
            "parent_id": chapter_id,
            "item_type": "lesson_item",
            "name": lesson_name,
            "is_preview": False,
            "content_type": type,
            "is_free": is_free,
            "slug": slug,
            "status": status
        }

        url = self.get_api_url(f"/curriculum/{course_id}/course-items")

        response = self.s.post(url, json=data, headers=self._headers)
        print(response.status_code)
        res = response.json()
        # print(res)
        if not res['success']:
            raise Exception("Cannot create course item for lesson:" + json.dumps(res))

        course_item_id = res['data']['id']
        print("course_item_id:", course_item_id)
        lesson_item_id = res['data']['lesson_item_id']
        print("lesson_item_id:", lesson_item_id)
        # if type == "video":
        if video_url or content or desciption:
            url = self.get_api_url(f"/lesson-item/{lesson_item_id}")
            data = {
                "description": desciption,
                "video_url": video_url,
                "content": content,
                "content_format": "markdown",
                "slug": slug,
                "is_free": is_free,
                "is_preview": False,
                "visibility": visibility,
                "ucoin": ucoin
            }

            response = self.s.put(url, json=data, headers=self._headers)
            print(response.status_code)
            res = response.json()
            print(res)
            if not res['success']:
                raise Exception("Cannot lesson item:" + json.dumps(res))
        return lesson_item_id


def create_chapters_mc1():
    ucode = UCode("https://dev-api.ucode.vn/api", "72821b59462c5fdb552a049c1caed85c")

    course_id = 7
    for w in range(1, 13):
        chapter_name = "Thử thách %02d" % w
        chapter_id = ucode.create_chapter(course_id=course_id, chapter_name=chapter_name)


def create_public_problem():
    problems = ProblemService.read_all_problems_v1("/home/thuc/projects/ucode/weekly-algorithm-problems/week13",
                                                   translations=["vi"], load_testcase=True)

    ucode = UCode("https://dev-api.ucode.vn/api", "743c1fce2615a4cb569dd57f86b73898")

    print(len(problems))
    for i, (problem_folder, problem) in enumerate(problems):
        print(i+1, problem.name)
        # print(problem.tags)
        # print(problem.translations['vi'].statement)
        print("Testcases: ", len(problem.testcases))
        res = ucode.create_problem(lesson_id=None, problem=problem, lang="en", xp=-1, status="draft", is_server_judge=True)
        print("res:", res)
        # break


def upload_all_problems_in_folder():
    # lession_id = 4046
    lession_id = 0 # public problem
    base_folder = "D:\\projects\\ucode\\dsa-thematic-problems\\BaDinh_2021_9"
    problems = ProblemService.read_all_problems(base_folder, nested_folder=False)
    print("Total problems:", len(problems))

    ucode = UCode("https://dev-api.ucode.vn/api", "26fd9211ce59375f5f01987bb868d170")
    # ucode = UCode("https://api.ucode.vn/api", "88a6973b6288aa09ba01767e8bd4ab94")

    for i, (problem_folder, problem) in enumerate(problems):
        problem = ProblemService.load(problem_folder, load_testcase=True)
        print(i + 1, problem.name)
        # ucode.create_problem(lesson_id=lession_id, problem=problem, xp=200)
        print("testcases:", len(problem.testcases), len(problem.testcases_sample))
        ucode_id = ucode.create_problem(lesson_id=lession_id, problem=problem, xp=-1)
        print("uCode problem created: ", ucode_id)


def create_problems_to_lesson_ucode_live():
    base_folder = "D:\\projects\\ucode\\repl_backup\\ThucNguyen1\\py1-2-lesson-1-review"
    problems = ProblemService.read_all_problems(base_folder, nested_folder=False)

    lesson_id = 4052
    ucode = UCode("https://api.ucode.vn/api", "88a6973b6288aa09ba01767e8bd4ab94")
    #
    # lesson_id = 4622
    # ucode = UCode("https://dev-api.ucode.vn/api", "26fd9211ce59375f5f01987bb868d170")

    for i, (problem_folder, problem) in enumerate(problems):
        problem = ProblemService.load(problem_folder, load_testcase=True)
        print(i + 1, problem.name)
        prob_id = ucode.create_problem(lesson_id=lesson_id, problem=problem, xp=-1)
        print(f"Problem uploaded with id #{prob_id}")

    print("Total problems:", len(problems))


if __name__ == "__main__":
    # create_problems_to_lesson_ucode_live()
    # upload_all_problems_in_folder()

    # lession_id = 4051
    lession_id = 0
    #
    # # ucode = UCode("https://dev-api.ucode.vn/api", "26fd9211ce59375f5f01987bb868d170")
    ucode = UCode("https://api.ucode.vn/api", "88a6973b6288aa09ba01767e8bd4ab94")

    problem_folder = "../../problems/a_plus_b"
    problem: Problem = ProblemService.load(problem_folder, load_testcase=True)

    # problem = ProblemService.load("D:\\projects\\ucode\\dsa-thematic-problems\\competitive_programing_topics\\"
    #                               "maths\\fundamentals\\gcd_lcm\\fnum",
    #                               load_testcase=True)
    ucode.create_problem(lesson_id=lession_id, problem=problem, xp=-1)

    print(problem.name)
    print(len(problem.testcases))
    print(len(problem.testcases_sample))
    print(problem.tags)
    print(problem.resource_files)
    #
    # ucode_id = ucode.create_problem(lesson_id=0, problem=problem, xp=-1)
    # print("uCode problem created: ", ucode_id)
    # print(problem.statement)
    # print(problem.translations['en'].statement)


    # img_file = "C:/Users/thucnguyen/Downloads/FB Posts.png"
    # img_file = "C:/Users/thucnguyen/Downloads/z2154907105699_598b6d3a26a9aa817fc97c2c8079d261.jpg"
    # upload_url = ucode.upload_file(img_file, "thuc_test")
    # print(upload_url)
    # create_public_problem()
    # ucode_courses = {
    #     2: 42,
    #     3: 43,
    #     4: 44,
    #     5: 45,
    #     6: 46,
    #     7: 47,
    #     8: 48,
    #     9: 49,
    #     10: 50,
    #     11: 51
    # }
    # ucode_courses = {
    #     2: 46
    # }
    # for y, course_id in ucode_courses.items():
    #     iqsha(y, course_id)

    # create_chapters_mc1()

    # ucode = UCode("https://dev-api.ucode.vn/api", "72821b59462c5fdb552a049c1caed85c")
    # # problem_folder = "../../problems/domino_for_young"
    # problem_folder = "/home/thuc/projects/ucode/courses/course-py101/lesson2/c1_input/p13_chao_ban"
    # ucode_lesson_id = 172
    #
    # problem: Problem = ProblemService.load(problem_folder, load_testcase=True)
    # #
    # # print(problem)
    # #
    # print(len(problem.testcases))
    # for testcase in problem.testcases:
    #     print(testcase)

    # ucode.create_problem(lesson_id=172, problem=problem_folder)

    # beestar = Beestar()
    #
    # files = beestar.read_quizzes_files_from_folder(
    #     "/home/thuc/projects/ucode/content_crawler/data/beestar/*grade-4-math*_ans.html"
    # )
    # course_id = 17
    # # chappter_id = 413  # GT Math 2
    # # chappter_id = 630  # GT Math 5
    # chappter_id = 735
    # # chappter_id = 619  # problems
    #
    # ucode = UCode("https://dev-api.ucode.vn/api", "df12e0548fbba3e6f48f9df2b78c3df2")
    # # for file in files:
    # #     ucode.create_lesson_item_from_beestar_file(course_id=course_id, chapter_id=chappter_id, beestar_file=file)
    # file = "../../problems/bs/_bs_ans.html"
    # ucode.create_lesson_item_from_beestar_file(course_id=course_id, chapter_id=chappter_id, beestar_file=file)

    # problem_folder = "/home/thuc/projects/ucode/problemtools/problems/cs/Arcade_TheCore/p001_Intro_Gates__addTwoDigits"
    # problem = ProblemService.load(problem_folder, load_testcase=True)
    #
    # hr = HackerRank()
    # hr.login('thucngch', '15041985')
    # # prepare_testcases("/home/thuc/projects/ucode/problemtools/problems/cs/Arcade_TheCore/p001_Intro_Gates__addTwoDigits")
    # hr.upload_testcases(163975, "/home/thuc/projects/ucode/problemtools/problems/cs/Arcade_TheCore/p001_Intro_Gates__addTwoDigits/testcases_hackerrank.zip")
    # # hr_prob = hr.create_problem(problem)
    # # print(json.dumps(hr_prob))
    #
    # "https://www.hackerrank.com/rest/administration/contests/46715/challenge?slug=add-two-digits&track_id=0&chapter_id=0&weight=100"
    #
    #
    # ucode = UCode("https://dev-api.ucode.vn/api", "df12e0548fbba3e6f48f9df2b78c3df2")
    # # print(problem)
    # # print(problem.name)
    # # print(len(problem.testcases))
    # #
    # # ucode.create_problem(lesson_id=None, problem=problem, question_type='code', lang="en")





