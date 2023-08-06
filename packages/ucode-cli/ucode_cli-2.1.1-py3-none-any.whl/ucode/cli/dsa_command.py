from pathlib import Path

import typer

from ucode.models.problem import ProblemFolderFormat
from ucode.services.dsa.problem_service import ProblemService

app = typer.Typer()


@app.command(name="create")
def create_dsa_problem(
        problem_name: str = typer.Argument(..., help='The name of the problem to be created, put in "..." '
                                                     'if there are spaces in the name.'),
        dir: Path = typer.Option(".", "--dir", "-d",
                                 help="Parent folder that contains new problem, default to current folder.",
                                 exists=True, file_okay=False),
        lang: str = typer.Option("vi", "--lang", "-l",
                                 help='Main problem statement language, default to "vi" for Vietnamese'),
        code: str = typer.Option("cpp", "--code", "-c",
                                 help='Programming language for solution and testcase, default to "cpp" for C++, '
                                      'available option: cpp|pas|py'),
        trans: str = typer.Option("", "--trans", "-t",
                                  help='List of additional statement languages, separated by commas, ex.: "en,ru"'),
        overwrite: bool = typer.Option(False, "--overwrite", "-F",
                                       help='Force overwriting existing folder')):
    """
    Create a problem boilerplate

    Syntax:
    ucode dsa create [-d {folder}] {problem name} [--overwrite]

    Ex.:
    ucode dsa create "Race Condition" -c py

    ucode dsa create -d problems -l en "Race Condition" --overwrite

    """
    tran_langs = []
    if trans.strip():
        tran_langs = trans.strip().split(",")
    ProblemService.create_problem(dir, problem_name, lang=lang, translations=tran_langs, overwrite=overwrite,
                                  programming_language=code)
    # print("DSA create"))


@app.command(name="check")
def check_dsa_problem(problem_folder: Path = typer.Argument(".", help="Problem folder, default to current folder.",
                                                            exists=True, file_okay=False),
                      load: bool = False):
    """
    Check problem folder for proper format

    Syntax:
    ucode dsa check {problem-folder}

    Ex.:
    ucode dsa check ../problems/prob2

    """
    ProblemService.check_problem(str(problem_folder))
    if load:
        ProblemService.load(str(problem_folder), load_testcase=True)


@app.command(name="convert")
def convert_dsa_problem(problem_folder: Path = typer.Argument(".", help="Problem folder to be converted",
                                                              exists=True, file_okay=False),
                        _from: ProblemFolderFormat = typer.Option(ProblemFolderFormat.themis, "--from", "-f",
                                                                  help="From format"),
                        _to: ProblemFolderFormat = typer.Option(ProblemFolderFormat.ucode, "--to", "-t",
                                                                  help="To format"),
                        output: Path = typer.Option(None, "--output", "-o",
                                                    help="Output problem folder to be written to, "
                                                         "default to problem_folder"),
                        overwrite: bool = typer.Option(False, "--overwrite", "-F",
                                                       help='Force overwriting existing folder'),
                        testcases_only: bool = typer.Option(False, "--testcases_only", "-T",
                                                            help='Force overwriting existing folder')
                        ):
    if not output:
        output = ""
    ProblemService.convert(str(problem_folder), _from, _to, str(output),
                           overwrite=overwrite, convert_testcases_only=testcases_only)


if __name__ == "__main__":
    app()
