#! /usr/bin/python3

import argparse, sys, os
from cliprint import color, print_table

from ..core import Project


class GitPMStat:

    """
    'gitpm stat' is a tool to get details about a gitpm repobase.
    """

    @staticmethod
    def error(e):
        GitPMStat.parser.error(e)

    @staticmethod
    def generateParser():

        """
        Generate the ArgumentParser for 'gitpm stat'.
        """

        GitPMStat.parser = argparse.ArgumentParser(
            prog="gitpm stat",
            description="Get stats about gitpm repobases.",
            epilog="More details at https://github.com/finnmglas/gitPM.",
        )

        return GitPMStat.parser

    @staticmethod
    def main(args=None, path=os.getcwd()):

        """
        The main program of 'gitpm stat'.
        """

        if args == None:  # parse args using own parser
            GitPMStat.generateParser()
            args = GitPMStat.parser.parse_args(sys.argv[1:])

        projects = Project.list(path)

        if len(projects) == 0:
            print(
                color.f.bold
                + "Folder without git projects, not a codebase.\n"
                + color.end
            )
            exit()

        print("Codebase at", color.f.bold + path + color.end + ":\n")

        # --- Project types

        print(
            "Contains " + color.f.bold,
            len(projects),
            "projects" + color.end + ": ",
            len(Project.list(path, type="repo")),
            "regular ones and",
            len(Project.list(path, type="bare")),
            "bares.",
        )

        # --- Maintainance Stats

        print("Maintainance:", end=" ")
        status_amount_tuples = [
            (s, len([p for p in projects if p.getStatus() == s]))
            for s in Project.status_set
            if len([p for p in projects if p.getStatus() == s])
        ]
        iterations = len(status_amount_tuples)
        for i in range(iterations):
            s, n = status_amount_tuples[i]

            print(Project.status_colors[s], end="")
            print(str(n), end=" ")
            print(s + color.end, end="")
            if i == iterations - 1:
                print(".\n")
            elif i == iterations - 2:
                print(" and ", end="")
            else:
                print(",", end=" ")
            i += 1

        # --- Commits

        commitCounts = [p.countCommits() for p in projects]
        commitCount = sum(commitCounts)
        maximum = max(commitCounts)
        print(
            "In total" + color.f.bold,
            commitCount,
            "Commits" + color.end + ", on average",
            str(int(commitCount / len(projects))) + ".",
        )
        print(
            "A maximum of",
            maximum,
            "Commits in '" + projects[commitCounts.index(maximum)].getName() + "'.\n",
        )

        # --- Metadata stats

        count_id = len([p for p in projects if "-" not in p.getId()])
        count_tags = len([p for p in projects if p.getTags() != ""])
        count_descr = len([p for p in projects if p.getDescription() != ""])
        if count_id == count_tags == count_descr == len(projects):
            print("All projects have complete metadata.")
        else:
            print(
                count_id,
                "projects have an id,",
                count_tags,
                "have tags and",
                count_descr,
                "have a project description.",
            )
        print()

        # --- Check uniqueness of selectors

        id_nonunique = Project.listNonUniqueIds(path)
        name_nonunique = Project.listNonUniqueNames(path)
        nonunique_selectors = True

        if len(id_nonunique):
            print(
                color.f.red + "[Warning]" + color.end,
                "Non-unique ids found:",
                id_nonunique,
            )
        elif len(name_nonunique):
            print(
                color.f.red + "[Warning]" + color.end,
                "Non-unique names found:",
                name_nonunique,
            )
        else:
            nonunique_selectors = False

        if nonunique_selectors:
            print()


if __name__ == "__main__":
    GitPMStat.main()
