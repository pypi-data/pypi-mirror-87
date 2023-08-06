# coding=utf-8
import logging

__author__ = 'ThucNC'
_logger = logging.getLogger(__name__)


class LessonService:
    @staticmethod
    def read_quiz(quiz_file):
        pass


if __name__ == "__main__":
    base_folder = "../problems/lessons"
    quiz_file = "/home/thuc/projects/ucode/ucode-cli/problems/lessons/math4/gia_thiet_tam/quiz_gia_thiet_tam.md"
    LessonService.read_quiz(quiz_file)