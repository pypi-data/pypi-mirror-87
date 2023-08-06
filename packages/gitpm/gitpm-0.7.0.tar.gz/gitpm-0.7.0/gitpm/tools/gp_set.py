#! /usr/bin/python3

import argparse, sys, os

from ..core import Project
from cliprint import *


class GitPMSet:

    """
    'gitpm set' is a tool to modify git projects.
    """

    project_set_variables = {
        "id": Project.setId,
        "status": Project.setStatus,
        "name": Project.setName,
        "description": Project.setDescription,
        "tags": Project.setTags,
    }

    @staticmethod
    def error(e):
        GitPMSet.parser.error(e)

    @staticmethod
    def generateParser():

        """
        Generate the ArgumentParser for 'gitpm set'.
        """

        GitPMSet.parser = argparse.ArgumentParser(
            prog="gitpm [project] set",
            description="Set (git) project metadata.",
            epilog="More details at https://github.com/finnmglas/gitPM.",
        )

        GitPMSet.parser.add_argument(
            "variable",
            choices=GitPMSet.project_set_variables.keys(),
            metavar="variable",
            help="choose a variable from {%(choices)s}",
        )

        GitPMSet.parser.add_argument(
            "value",
            help="specify a new value",
        )

        return GitPMSet.parser

    @staticmethod
    def main(args=None, path=os.getcwd()):

        """
        The main program of 'gitpm set'.
        """

        if args == None:  # parse args using own parser
            GitPMSet.generateParser()
            args = GitPMSet.parser.parse_args(sys.argv[1:])

        project = Project.fromSelector(args.project)

        kwargs = {}
        if args.variable == "name":
            rename_dir_input = input("Rename folder (default: no)? (y/n) ").lower()
            if rename_dir_input and rename_dir_input[0] == "y":
                kwargs["rename_dir"] = True

        GitPMSet.project_set_variables[args.variable](project, args.value, **kwargs)


if __name__ == "__main__":
    GitPMSet.main()
