#! /usr/bin/python3

import argparse, sys, os
from cliprint import color

from ..core import Project

from .gp_list import GitPMList
from .gp_create import GitPMCreate
from .gp_remove import GitPMRemove
from .gp_loop import GitPMLoop

from .gp_stat import GitPMStat
from .gp_sync import GitPMSync

from .gp_set import GitPMSet
from .gp_details import GitPMDetails
from .gp_clone import GitPMClone
from .gp_git import GitPMGit
from .gp_update import GitPMUpdate


class GitPM:

    """
    The 'gitpm' cli simplifies repository management.
    """

    general_tools = {
        "list": GitPMList,
        "create": GitPMCreate,
        "remove": GitPMRemove,
        "loop": GitPMLoop,
        "stat": GitPMStat,
        "clone": GitPMClone,
        "sync": GitPMSync,
    }
    project_tools = {
        "details": GitPMDetails,
        "set": GitPMSet,
        "git": GitPMGit,
        "update": GitPMUpdate,
    }

    tools = {**general_tools, **project_tools}

    @staticmethod
    def error(e):
        GitPM.parser.error(e)

    @staticmethod
    def generateParser():

        """
        Generate the ArgumentParser for 'gitpm'.
        """

        GitPM.parser = argparse.ArgumentParser(
            description="Manage multiple git projects and their metadata.",
            epilog="More details at https://github.com/finnmglas/gitpm.",
            formatter_class=argparse.RawTextHelpFormatter,
        )
        GitPM.parser.add_argument(
            "-v",
            "--version",
            dest="show_version",
            action="store_true",
            help="show the current version and exit",
        )
        GitPM.parser.add_argument(
            "-c",
            "--cwd",
            dest="cwd",
            default=os.getcwd(),
            help="modify the current working directory",
        )
        GitPM.parser.add_argument(
            "project",
            nargs="?",
            help="specify a project name",
        )
        subparsers = GitPM.parser.add_subparsers(
            dest="tool",
            metavar="tool",
            help="select a GitPM tool"
            + "\nif no project was specified:  "
            + str(set(GitPM.general_tools.keys())).replace("'", "")
            + "\nif a project was specified:   "
            + str(set(GitPM.project_tools.keys())).replace("'", ""),
        )

        for name in GitPM.tools:
            tool = GitPM.tools[name]
            # Import Parser --- ledgerman [name]
            toolParser = subparsers.add_parser(name)
            toolParser.__dict__ = tool.generateParser().__dict__

        return GitPM.parser

    @staticmethod
    def main(path=os.getcwd()):
        # --- generate parser
        GitPM.generateParser()

        argv = sys.argv[1:]

        # --- argparse preparation
        if len(argv) == 1 and Project.hasSelector(argv[0].rstrip("/"), path):
            argv += ["details"]

        if (
            len(argv) >= 2
            and argv[0].rstrip("/") in [p.getName() for p in Project.list(path)]
            and argv[1] in Project.git_argument_set
        ):
            argv = [argv[0], "git"]
        elif len(argv) >= 3 and argv[1] == "git":
            argv = argv[:2]

        if len(argv) and argv[0] in GitPM.general_tools:
            argv = [None, *argv]

        if not len(argv):
            argv += ["list"]

        # --- argparse
        args = GitPM.parser.parse_args(argv)

        if args.project and not Project.hasSelector(args.project.rstrip("/"), path):
            GitPM.error(
                "Project " + color.f.bold + args.project + color.end + " not found."
            )

        # check validity of [project] combined with [tool]
        if args.project == None and args.tool in GitPM.project_tools:
            GitPM.error("Expected argument [project] for tool '" + args.tool + "'.")
        elif args.project != None and args.tool in GitPM.general_tools:
            GitPM.error("Unexpected argument [project] for tool '" + args.tool + "'.")

        # show version (`gitpm --version`)
        if args.show_version:
            import pkg_resources

            print(pkg_resources.require("gitpm")[0].version)
            return

        # forward args to a tool
        try:
            GitPM.tools[args.tool].main(args, args.cwd)
        except KeyboardInterrupt:
            print()


if __name__ == "__main__":
    GitPM.main()
