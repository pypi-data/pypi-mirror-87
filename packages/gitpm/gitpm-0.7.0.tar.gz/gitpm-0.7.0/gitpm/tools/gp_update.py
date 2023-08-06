#! /usr/bin/python3

import argparse, sys, os
from cliprint import color, print_table, table

from ..core import Project


class GitPMUpdate:

    """
    'gitpm update' is a tool to get two projects to have the same progress.
    """

    @staticmethod
    def error(e):
        GitPMUpdate.parser.error(e)

    @staticmethod
    def generateParser():

        """
        Generate the ArgumentParser for 'gitpm update'.
        """

        GitPMUpdate.parser = argparse.ArgumentParser(
            prog="gitpm update",
            description="Compare and update a project clone with the original.",
            epilog="More details at https://github.com/finnmglas/gitPM.",
        )
        GitPMUpdate.parser.add_argument(
            "original", help="The project to update (from or to depends)"
        )
        GitPMUpdate.parser.add_argument(
            "-v",
            "--verbose",
            action="store_true",
            help="Display an extensive update log",
        )

        return GitPMUpdate.parser

    @staticmethod
    def format_short(msg, length=16, end="..."):
        msg = str(msg)
        if len(msg) < length:
            return msg
        else:
            return msg[: length - 3] + end

    @staticmethod
    def isEqual(name, a, b, verbose=False):

        length = 24
        sign_equals = {
            True: color.f.green + "==" + color.end,
            False: color.f.red + "!=" + color.end,
        }

        equality = a == b
        if not verbose:
            return equality

        print(
            table(
                [16, length + 2, 4, length + 2],
                [
                    [
                        color.f.bold + name + (":" if name else "") + color.end,
                        GitPMUpdate.format_short(a, length),
                        sign_equals[equality],
                        GitPMUpdate.format_short(b, length),
                    ],
                ],
            ),
            end="",
        )

        return equality

    @staticmethod
    def askUpdateMetadata(name, option_1, option_2, set_action_p1, set_action_p2):
        update_input = input("Update " + name + "? (y/n) ").lower()

        if update_input and update_input[0] == "y":

            if option_1 in ["undefined", ""]:
                update_input = "2"
            elif option_2 in ["undefined", ""]:
                update_input = "1"
            else:
                update_input = input(
                    "1: '" + option_1 + "' or\n2: '" + option_2 + "'? (1/2) "
                ).lower()

            if update_input == "1":
                set_action_p1(option_1)
                set_action_p2(option_1)
            elif update_input == "2":
                set_action_p1(option_2)
                set_action_p2(option_2)

    # returns 0 if nothing was to be updated, else 1
    @staticmethod
    def updateProjects(project_1, project_2, path=os.getcwd(), verbose=False, end=True):
        if verbose:
            print(
                color.f.bold
                + "Comparing project at '"
                + project_1.path
                + "' and at '"
                + project_2.path
                + "':\n"
                + color.end
            )

        # --- Compare Metadata
        name_1 = project_1.getName()
        name_2 = project_2.getName()
        equality_name = GitPMUpdate.isEqual("Name", name_1, name_2, verbose)

        id_1 = project_1.getId()
        id_2 = project_2.getId()
        equality_id = GitPMUpdate.isEqual("Id", id_1, id_2, verbose)

        status_1 = project_1.getStatus()
        status_2 = project_2.getStatus()
        equality_status = GitPMUpdate.isEqual("Status", status_1, status_2, verbose)

        description_1 = project_1.getDescription()
        description_2 = project_2.getDescription()
        equality_description = GitPMUpdate.isEqual(
            "Description", description_1, description_2, verbose
        )

        tags_1 = project_1.getTags()
        tags_2 = project_2.getTags()
        equality_tags = GitPMUpdate.isEqual("Tags", tags_1, tags_2, verbose)

        # --- Compare commitlogs

        commitlog_1 = project_1.listCommits()
        commitlog_2 = project_2.listCommits()
        equality_commitcount = GitPMUpdate.isEqual(
            "Commits", len(commitlog_1), len(commitlog_2), verbose
        )
        equality_commits = GitPMUpdate.isEqual("", commitlog_1, commitlog_2, verbose)

        if verbose:
            print()

        # --- Equal commitlogs and equal projects -> done

        if equality_commits:
            if (
                equality_name
                and equality_id
                and equality_status
                and equality_description
                and equality_tags
            ):
                if end:
                    print(color.f.bold + "Equal projects. Nothing to do." + color.end)
                return 0
            else:
                if end:
                    print(color.f.bold + "Equal commit-logs." + color.end)

        # --- Unequal commitlogs -> push commits

        else:
            common_history = [c for c in commitlog_1 if c in commitlog_2]

            if common_history == []:
                if end:
                    print(
                        color.f.bold + "No common commit history. Aborting." + color.end
                    )
                return 0

            if common_history == commitlog_2[0 : len(common_history)]:
                ahead_project = project_1
                behind_project = project_2
                ahead_amount = len(commitlog_1) - len(common_history)
            elif common_history == commitlog_1[0 : len(common_history)]:
                ahead_project = project_2
                behind_project = project_1
                ahead_amount = len(commitlog_2) - len(common_history)
            else:
                if end:
                    print(
                        color.f.bold
                        + "Weird things happening. Resolve it manually with git."
                        + color.end
                    )
                return 0

            print(
                "Project at '" + ahead_project.path + "' is",
                ahead_amount,
                "commit" + ("" if ahead_amount == 1 else "s") + " ahead.",
            )

            push_input = input("Update? (y/n) ").lower()
            if push_input and push_input[0] == "y":
                if behind_project.type == "repo":
                    behind_project.execute(
                        ["git", "pull", os.path.join(path, ahead_project.path)]
                    )
                else:
                    if ahead_project.type == "bare":
                        ahead_project.execute(
                            [
                                "git",
                                "push",
                                "--set-upstream",
                                os.path.join(path, behind_project.path),
                                ahead_project.getCurrentBranch(),
                            ]
                        )
                    else:
                        ahead_project.execute(
                            ["git", "push", os.path.join(path, behind_project.path)]
                        )

        # --- update metadata if needed

        if not equality_name:
            GitPMUpdate.askUpdateMetadata(
                "Name",
                name_1,
                name_2,
                project_1.setName,
                project_2.setName,
            )
        if not equality_id:
            GitPMUpdate.askUpdateMetadata(
                "Id",
                id_1,
                id_2,
                project_1.setId,
                project_2.setId,
            )
        if not equality_status:
            GitPMUpdate.askUpdateMetadata(
                "Status",
                status_1,
                status_2,
                project_1.setStatus,
                project_2.setStatus,
            )
        if not equality_description:
            GitPMUpdate.askUpdateMetadata(
                "Description",
                description_1,
                description_2,
                project_1.setDescription,
                project_2.setDescription,
            )
        if not equality_tags:
            GitPMUpdate.askUpdateMetadata(
                "Tags",
                tags_1,
                tags_2,
                project_1.setTags,
                project_2.setTags,
            )

        return 1

    @staticmethod
    def main(args=None, path=os.getcwd()):

        """
        The main program of 'gitpm update'.
        """

        if args == None:  # parse args using own parser
            GitPMUpdate.generateParser()
            args = GitPMUpdate.parser.parse_args(sys.argv[1:])

        GitPMUpdate.updateProjects(
            Project.fromSelector(args.project),
            Project(args.original),
            path=path,
            verbose=args.verbose,
        )


if __name__ == "__main__":
    GitPMUpdate.main()
