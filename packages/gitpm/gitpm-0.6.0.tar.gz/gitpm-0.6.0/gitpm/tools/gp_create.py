#! /usr/bin/python3

import argparse, sys, os
from cliprint import color

from ..core import Project


class GitPMCreate:

    """
    'gitpm create' is a commandline tool to create new git projects.
    """

    @staticmethod
    def error(e):
        GitPMCreate.parser.error(e)

    @staticmethod
    def generateParser():

        """
        Generate the ArgumentParser for 'gitpm create'.
        """

        GitPMCreate.parser = argparse.ArgumentParser(
            prog="gitpm create",
            description="Create (git) projects.",
            epilog="More details at https://github.com/finnmglas/gitPM.",
        )
        GitPMCreate.parser.add_argument(
            "-n",
            "--name",
            help="specify a project name",
        ).required = True
        GitPMCreate.parser.add_argument(
            "-i",
            "--id",
            help="specify a project id",
        )
        GitPMCreate.parser.add_argument(
            "-b",
            "--bare",
            action="store_true",
            default=False,
            help="create a bare git repository",
        )

        return GitPMCreate.parser

    @staticmethod
    def main(args=None, path=os.getcwd()):

        """
        The main program of 'gitpm create'.
        """

        if args == None:  # parse args using own parser
            GitPMCreate.generateParser()
            args = GitPMCreate.parser.parse_args(sys.argv[1:])

        project = Project.create(
            path,
            name=args.name,
            id=args.id,
            bare=args.bare,
        )

        print(
            "New project "
            + color.f.bold
            + project.getName()
            + color.end
            + " with id "
            + project.getId()
            + ".\n"
        )


if __name__ == "__main__":
    GitPMCreate.main()
