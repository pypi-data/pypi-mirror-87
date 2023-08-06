#! /usr/bin/python3

import argparse, sys, os
from cliprint import color, print_table

from .gp_update import GitPMUpdate

from ..core import Project


class GitPMSync:

    """
    'gitpm sync' is a tool to update gitpm repobases.
    """

    @staticmethod
    def error(e):
        GitPMSync.parser.error(e)

    @staticmethod
    def generateParser():

        """
        Generate the ArgumentParser for 'gitpm sync'.
        """

        GitPMSync.parser = argparse.ArgumentParser(
            prog="gitpm sync",
            description="Update changes between two gitpm repobases.",
            epilog="More details at https://github.com/finnmglas/gitPM.",
        )
        GitPMSync.parser.add_argument(
            "base", help="The repobase to update changes with"
        )
        GitPMSync.parser.add_argument(
            "-v",
            "--verbose",
            action="store_true",
            help="Display an extensive update log",
        )
        GitPMSync.parser.add_argument(
            "-s",
            "--sync-all",
            dest="sync_all",
            action="store_true",
            help="Sync all projects (copy new ones).",
        )

        return GitPMSync.parser

    @staticmethod
    def main(args=None, path=os.getcwd()):

        """
        The main program of 'gitpm sync'.
        """

        if args == None:  # parse args using own parser
            GitPMSync.generateParser()
            args = GitPMSync.parser.parse_args(sys.argv[1:])

        # assuming unique IDs

        # --- list projects with ids (and on -s, new ones)
        projects_ids_here = []
        if args.sync_all:
            ids_here = []
        for p in Project.list(path):
            id = p.getId(allow_empty=True)
            if id != "":
                projects_ids_here.append((id, p))
                if args.sync_all:
                    ids_here.append(id)

        projects_ids_there = []
        if args.sync_all:
            ids_there = []
        for p in Project.list(args.base):
            id = p.getId(allow_empty=True)
            if id != "":
                projects_ids_there.append((id, p))
                if args.sync_all:
                    ids_there.append(id)

        if args.sync_all:
            projects_ids_not_here = [
                tp[1] for tp in projects_ids_there if tp[0] not in ids_here
            ]
            projects_ids_not_there = [
                tp[1] for tp in projects_ids_here if tp[0] not in ids_there
            ]

        # --- find pairs to update
        projects_to_sync = []
        for project_here in projects_ids_here:
            for project_there in projects_ids_there:
                if project_here[0] == project_there[0]:
                    projects_to_sync.append((project_here[1], project_there[1]))

        # --- update pairs
        change_count = 0
        for tp in projects_to_sync:
            here, there = tp
            change_count += GitPMUpdate.updateProjects(
                here,
                there,
                path=path,
                verbose=args.verbose,
                end=False,  # no "doing nothing" messages
            )

        # --- copy new projects
        if args.sync_all:
            change_count = len(projects_ids_not_here) + len(projects_ids_not_there)

            for p in projects_ids_not_here:
                cp_input = input("Copy project at '" + p.path + "' here? (y/n) ")
                if cp_input and cp_input[0] == "y":
                    os.system('cp -r "' + p.path + '" "' + path + '"')
                    print("Copied.")

            for p in projects_ids_not_there:
                cp_input = input("Copy project at '" + p.path + "' there? (y/n) ")
                if cp_input and cp_input[0] == "y":
                    os.system('cp -r "' + p.path + '" "' + args.base + '"')
                    print("Copied.")

        if change_count == 0:
            print(color.f.bold + "Nothing found to be updated." + color.end)


if __name__ == "__main__":
    GitPMSync.main()
