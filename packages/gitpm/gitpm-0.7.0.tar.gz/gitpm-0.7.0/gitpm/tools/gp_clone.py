#! /usr/bin/python3

import argparse, sys, os
from cliprint import color

from ..core import Project


class GitPMClone:

    """
    'gitpm clone' is a tool to preserve metadata when cloning git projects.
    """

    @staticmethod
    def error(e):
        GitPMClone.parser.error(e)

    @staticmethod
    def generateParser():

        """
        Generate the ArgumentParser for 'gitpm clone'.
        """

        GitPMClone.parser = argparse.ArgumentParser(
            prog="gitpm clone",
            description="Clone (git) projects with metadata.",
            epilog="More details at https://github.com/finnmglas/gitPM.",
        )
        GitPMClone.parser.add_argument("selector", help="select a project to be cloned")
        GitPMClone.parser.add_argument(
            "dest", nargs="?", help="where to clone the project"
        )

        return GitPMClone.parser

    @staticmethod
    def main(args=None, path=os.getcwd()):

        """
        The main program of 'gitpm clone'.
        """

        if args == None:  # parse args using own parser
            GitPMClone.generateParser()
            args = GitPMClone.parser.parse_args(sys.argv[1:])

        oldproject = Project.fromSelector(args.selector.rstrip("/"), path)
        oldpath = oldproject.path
        newpath = args.selector.rstrip("/") + "-clone"

        if args.dest:
            newpath = args.dest

        # clone project (git)
        os.system('git clone "' + oldpath + '" "' + newpath + '"')

        # clone metadata (gitpm)
        newproject = Project(newpath)
        newproject.setName(oldproject.getName(), rename_dir=False)
        newproject.setId(oldproject.getId())
        newproject.setTags(oldproject.getTags())
        newproject.setDescription(oldproject.getDescription())
        newproject.setStatus(oldproject.getStatus())


if __name__ == "__main__":
    GitPMClone.main()
