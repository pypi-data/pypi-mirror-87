from builtins import staticmethod

from ucode.models.problem import Problem
from ucode.services.dsa.problem_service import ProblemService


class TestcaseService:
    @staticmethod
    def generate_testcases(problem_folder):
        problem: Problem = ProblemService.load(problem_folder)
        meta, folders = ProblemService.detect_problem_code_in_folder(problem_folder)
        print(problem)
        print(folders)


if __name__ == "__main__":
    folder = "../../../problems/big_mod_py"
    TestcaseService.generate_testcases(problem_folder=folder)
