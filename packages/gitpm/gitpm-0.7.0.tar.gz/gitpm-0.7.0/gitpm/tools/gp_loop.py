#! /usr/bin/python3

import argparse, sys, os

from cliprint import color

try:
    import readline
except:
    pass  # readline not available


class GitPMLoop:

    """
    'gitpm loop' is a tool that will help you enter the gitPM shell.
    """

    @staticmethod
    def error(e):
        GitPMLoop.parser.error(e)

    @staticmethod
    def generateParser():

        """
        Generate the ArgumentParser for 'gitpm loop'.
        """

        GitPMLoop.parser = argparse.ArgumentParser(
            prog="gitpm loop",
            description="The 'gipm-loop' tool runs the gitPM shell.",
            epilog="More details at https://github.com/finnmglas/gitPM.",
        )

        return GitPMLoop.parser

    @staticmethod
    def main(args=None, directory=os.getcwd()):

        """
        The main program of 'gitpm loop'.
        """

        if args == None:  # parse args using own parser
            GitPMLoop.generateParser()
            args = GitPMLoop.parser.parse_args(sys.argv[1:])

        GitPMLoop.loop(directory)

    @staticmethod
    def loop(directory=os.getcwd()):
        currentProject = ""  # checkout [id]
        prompt = "gitpm > "

        print("Starting a gitPM operation loop. Type 'quit' to exit.\n")
        while True:
            cmd = ""
            try:
                del cmd
                cmd = input(
                    color.foreground.BOLD + color.foreground.BLUE + prompt + color.END
                )
                cmd_argv = cmd.split(" ")

                if cmd.strip() == "":
                    continue
                else:
                    print()

                if cmd_argv[0] == "checkout":
                    if len(cmd_argv) == 1:
                        print("error: argument id: expected id after 'checkout'")
                    elif len(cmd_argv) > 2:
                        print("error: too many arguments for 'checkout'")
                    elif not Project.isId(
                        cmd_argv[1]
                    ) or Project.formatId(
                        cmd_argv[1]
                    ) not in Project.listIds(
                        directory
                    ):
                        print("error: argument id: can't check out invalid id")
                    else:
                        currentProject = cmd_argv[1]
                        prompt = (
                            "gitpm: " + Project.formatId(cmd_argv[1]) + " > "
                        )
                        continue
                elif cmd in ["quit", "q", "exit"]:
                    if currentProject == "":
                        raise KeyboardInterrupt()
                    else:
                        currentProject = ""
                        prompt = "gitpm > "
                        continue
                elif cmd in ["clear", "cls"]:
                    os.system("clear")
                    continue
                elif cmd == "loop":  # no looping in loops
                    print("Can't start a loop within a loop. Type 'quit' to exit.")
                else:
                    if currentProject != "":
                        cmd = currentProject + " " + cmd
                    # execute
                    os.system("gitpm " + cmd)

                print()
            except EOFError:
                print("\n")

                print("Exiting loop")
                break

            except KeyboardInterrupt:
                try:
                    cmd
                except UnboundLocalError:
                    print("\n")

                print("Exiting loop")
                break


if __name__ == "__main__":
    GitPMLoop.main()
