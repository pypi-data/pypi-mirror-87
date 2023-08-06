#! /usr/bin/python3

import argparse, sys, os

from ..core import Project
from cliprint import *


class GitPMGit:

    """
    'gitpm git' is a tool to run git commands in git projects.
    """

    @staticmethod
    def error(e):
        GitPMGit.parser.error(e)

    @staticmethod
    def generateParser():

        """
        Generate the ArgumentParser for 'gitpm git'.
        """

        GitPMGit.parser = argparse.ArgumentParser(
            prog="gitpm git",
            description="Execute git commands.",
            epilog="More details at https://github.com/finnmglas/gitPM.",
        )

        return GitPMGit.parser

    @staticmethod
    def main(args=None, path=os.getcwd()):

        """
        The main program of 'gitpm git'.
        """

        if args == None:  # parse args using own parser
            GitPMGit.generateParser()
            args = GitPMGit.parser.parse_args(sys.argv[1:])

        project = Project.fromSelector(args.project)

        if sys.argv[2] == "git":
            output = project.execute(sys.argv[2:])
        else:
            output = project.execute(["git"] + sys.argv[2:])

        print(output)


if __name__ == "__main__":
    GitPMGit.main()
