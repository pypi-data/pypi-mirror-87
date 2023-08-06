#! /usr/bin/python3

import argparse, sys, os

from ..core import Project
from cliprint import *


class GitPMRemove:

    """
    'gitpm remove' deletes projects.
    """

    @staticmethod
    def error(e):
        GitPMRemove.parser.error(e)

    @staticmethod
    def generateParser():

        """
        Generate the ArgumentParser for 'gitpm remove'.
        """

        GitPMRemove.parser = argparse.ArgumentParser(
            prog="gitpm remove",
            description="Delete (git) projects.",
            epilog="More details at https://github.com/finnmglas/gitPM.",
        )
        GitPMRemove.parser.add_argument(
            "name",
            choices=[p.getName() for p in Project.list(os.getcwd())],
            metavar="name",
            help="specify a project name",
        ).required = True

        return GitPMRemove.parser

    @staticmethod
    def main(args=None, path=os.getcwd()):

        """
        The main program of 'gitpm remove'.
        """

        if args == None:  # parse args using own parser
            GitPMRemove.generateParser()
            args = GitPMRemove.parser.parse_args(sys.argv[1:])

        project = Project.fromSelector(args.name)

        try:
            if input("Delete project? (y / n) ") == "y":
                name = project.getName()
                id = project.getId()
                project.delete()
                print(
                    "Deleted project "
                    + color.f.bold
                    + name
                    + color.end
                    + " with id "
                    + id
                    + ".\n"
                )
            else:
                raise KeyboardInterrupt
        except KeyboardInterrupt:
            print("Canceled deletion.\n")


if __name__ == "__main__":
    GitPMRemove.main()
