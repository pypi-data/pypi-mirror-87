#! /usr/bin/python3

import argparse, sys, os
from cliprint import color

from ..core import Project


class GitPMList:

    """
    List (git) projects.
    """

    @staticmethod
    def error(e):
        GitPMList.parser.error(e)

    @staticmethod
    def generateParser():

        """
        Generate the ArgumentParser for 'gitpm list'.
        """

        GitPMList.parser = argparse.ArgumentParser(
            prog="gitpm list",
            description="List (git) projects.",
            epilog="More details at https://github.com/finnmglas/gitPM.",
        )
        GitPMList.parser.add_argument(
            "-s",
            "--status",
            default="all",
            choices=Project.status_set,
            help="filter projects by maintainance status",
        )
        GitPMList.parser.add_argument(
            "-i",
            dest="inverse_selection",
            action="store_true",
            default=False,
            help="invert status selection (with -s)",
        )
        GitPMList.parser.add_argument(
            "-t",
            "--type",
            default="all",
            choices=Project.types,
            help="filter projects by repository type",
        )
        GitPMList.parser.add_argument(
            "-n",
            dest="number",
            type=int,
            help="limit list to display NUMBER results",
        )
        GitPMList.parser.add_argument(
            "-f",
            "--find",
            help="filter projects by name",
        )

        return GitPMList.parser

    @staticmethod
    def main(args=None, path=os.getcwd()):

        """
        The main program of 'gitpm list'. List projects.
        """

        if args == None:  # parse args using own parser
            GitPMList.generateParser()
            args = GitPMList.parser.parse_args(sys.argv[1:])

        projects = Project.list(
            path,
            type=args.type,
            amount=args.number,
            status=args.status,
            status_inverse=args.inverse_selection,
            in_name=args.find,
        )

        # Print it

        if len(projects) == 0:
            print(color.f.bold + "No repositories found.\n" + color.end)
            return

        bare_projects = [p for p in projects if p.type == "bare"]
        repo_projects = [p for p in projects if p.type == "repo"]

        if len(repo_projects):
            print(color.f.bold + "GitPM found these repositories:\n" + color.end)
            print(Project.table(*repo_projects))

        if len(bare_projects):

            if len(repo_projects):
                start_str = "And "
            else:
                start_str = "GitPM found "

            print(
                color.f.bold
                + start_str
                + "these "
                + color.f.red
                + "bare"
                + color.end
                + color.f.bold
                + " repositories:\n"
                + color.end
            )
            print(Project.table(*bare_projects))


if __name__ == "__main__":
    GitPMList.main()
