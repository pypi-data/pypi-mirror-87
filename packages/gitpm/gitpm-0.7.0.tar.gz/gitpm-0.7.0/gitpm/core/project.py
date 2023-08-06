import os, subprocess, cliprint, string
from cliprint import color


class Project:

    """
    Git-repositories are called projects, when managed with GitPM.
    This is because we include additional metadata and management possibilities.
    """

    ## --- STATIC VARIABLES --- ##

    types = ["repo", "bare"]
    status_set = ["new", "maintained", "discontinued", "completed", "undefined"]
    status_colors = {
        "new": color.foreground.YELLOW,
        "maintained": color.foreground.GREEN,
        "discontinued": color.foreground.RED,
        "completed": color.foreground.BLUE,
        "undefined": "",  # the status meaning "no status defined"
    }

    id_width = 4
    hash_abbr_len = 8

    git_file_id = "project-id"
    git_file_name = "description"
    git_file_about = "social-description"
    git_file_status = "maintainance"
    git_file_tags = "social-tags"

    git_argument_set = [
        "branch",
        "tag",
        "commit",
        "status",
        "remote",
        "ls-tree",
        "ls-remote",
        "ls-files",
        "show",
        "config",
        "checkout",
        "add",
        "fetch",
        "merge",
        "pull",
        "push",
        "reset",
        "rev-list",
        "switch",
        "rebase",
        "log",
        "grep",
        "diff",
        "bisect",
        "mv",
        "restore",
        "rm",
        "sparse-checkout",
        "init",
    ]

    ## --- STATIC METHODS --- ##

    @staticmethod
    def git_repo_at(path):

        """
        Check if a folder contains a normal git repository.
        """

        return os.path.isdir(path) and os.path.isdir(os.path.join(path, ".git"))

    @staticmethod
    def git_bare_at(path):

        """
        Check if a folder contains a bare git repository.
        """

        return (
            os.path.isdir(path)
            and not path.split("/")[-1] == ".git"
            and not os.path.isdir(os.path.join(path, ".git"))
            and os.path.isdir(os.path.join(path, "objects"))
            and os.path.isdir(os.path.join(path, "refs"))
        )

    @staticmethod
    def at(path):

        """
        Check if a folder contains a git repository of any type.
        """

        return Project.git_repo_at(path) or Project.git_bare_at(path)

    @staticmethod
    def list(
        path,
        type="all",
        amount="all",
        status="all",
        status_inverse=False,
        id_required=False,
        in_name="",
        is_name=None,
    ):

        """
        List repositories.
        """

        dirs = os.listdir(path)

        if type == "all":
            projects = [
                Project(os.path.join(path, d))
                for d in dirs
                if Project.at(os.path.join(path, d))
            ]
        elif type == "repo":
            projects = [
                Project(os.path.join(path, d))
                for d in dirs
                if Project.git_repo_at(os.path.join(path, d))
            ]
        elif type == "bare":
            projects = [
                Project(os.path.join(path, d))
                for d in dirs
                if Project.git_bare_at(os.path.join(path, d))
            ]
        else:
            raise ValueError("Unknown GitPM project type: '" + type + "'")

        if id_required:
            projects = [p for p in projects if p.getId(allow_empty=True)]

        if is_name:
            projects = [p for p in projects if p.getName() == is_name]
        elif in_name:
            projects = [p for p in projects if in_name.lower() in p.getName().lower()]

        projects = sorted(projects, key=lambda p: p.getId())
        projects.reverse()

        if amount in ["all", "", None]:
            amount = len(projects)

        projects = [
            p
            for p in projects
            if (status == "all" or ((p.getStatus() == status) ^ status_inverse))
        ][0:amount]

        return projects

    @staticmethod
    def table(*projects):
        return cliprint.table(
            [Project.id_width + 4, 32, 14, Project.hash_abbr_len + 4],
            [
                [
                    color.f.bold + p.getId() + color.end,
                    p.getName(),
                    Project.status_colors[p.getStatus()] + p.getStatus() + color.end,
                    p.getLastCommit()[0 : Project.hash_abbr_len],
                ]
                for p in projects
            ],
        )

    @staticmethod
    def listIds(path):
        return [project.getId() for project in Project.list(path)]

    @staticmethod
    def isId(hexId):
        return all(c in set(string.hexdigits) for c in hexId)

    @staticmethod
    def formatId(id):
        if isinstance(id, str):
            id = int(id, 16)

        formatedId = hex(id)[2:]

        while Project.id_width > len(formatedId):
            formatedId = "0" + formatedId

        return formatedId

    @staticmethod
    def listSelectors(path=os.getcwd()):
        return [
            (p.path, p.getName(), p.getId(allow_empty=True)) for p in Project.list(path)
        ]

    @staticmethod
    def listNonUniqueIds(path=os.getcwd()):
        ids = [s[2] for s in Project.listSelectors(path)]
        return list(set([i for i in ids if ids.count(i) > 1 and i != ""]))

    @staticmethod
    def listNonUniqueNames(path=os.getcwd()):
        names = [s[1] for s in Project.listSelectors(path)]
        return list(set([i for i in names if names.count(i) > 1 and i != ""]))

    @staticmethod
    def hasSelector(s, path=os.getcwd()):
        return len(
            [
                d
                for d in Project.listSelectors(path)
                if s in d or os.path.join(path, s) == d[0]
            ]
        )

    @staticmethod
    def fromSelector(s, path=os.getcwd()):
        sel_count = Project.hasSelector(s)

        if sel_count == 0:
            raise ValueError("Project selector '" + s + "' not matched.")
        elif sel_count > 1:
            raise ValueError("Project selector '" + s + "' not uniquely defined.")

        sel = Project.listSelectors(path)

        if len([d for d in sel if s == d[0] or os.path.join(path, s) == d[0]]):  # path
            return Project(s)
        elif len([d for d in sel if s == d[1]]):  # name
            return Project([d for d in sel if s == d[1]][0][0])
        else:  # id
            return Project([d for d in sel if s == d[2]][0][0])

    ## --- DATA MODEL METHODS --- ##

    def __init__(self, path, setup=None):
        if Project.git_repo_at(path) or setup == "repo":
            self.path = path
            self.meta_path = self.path + "/.git"
            self.type = "repo"
        elif Project.git_bare_at(path) or setup == "bare":
            self.path = path
            self.meta_path = self.path
            self.type = "bare"
            # self.setId(path.split("/")[-1]) # Used to update base
        else:
            raise ValueError("No project recognized at '" + path + "'")

    @staticmethod
    def create(path, name="", id=None, bare=False):
        repositories = Project.list(path, id_required=True)

        if id == None:
            if len(repositories) == 0:
                newId = Project.formatId(0)
            else:
                newId = int(repositories[0].getId(), 16) + 1
                newId = Project.formatId(newId)
        else:
            newId = id

        os.mkdir(name)
        p = Project(name, setup={False: "repo", True: "bare"}[bare])

        if bare:
            p.execute(["git", "init", "--bare"])
        else:
            p.execute(["git", "init"])

        p.writeFile(Project.git_file_id, newId)
        p.writeFile(Project.git_file_name, name)
        p.writeFile(Project.git_file_status, "new")

        return p

    ## --- CLASS METHODS --- ##

    def delete(self):
        for root, dirs, files in os.walk(self.path, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(self.path)

    def execute(self, command):
        try:
            output = str(
                subprocess.check_output(
                    command,
                    cwd=self.path,
                    stderr=open(os.devnull, "w"),
                ),
                "utf-8",
            ).strip()
        except subprocess.CalledProcessError:
            output = ""
        return output

    def readFile(self, f):
        try:
            with open(self.meta_path + "/" + f) as fh:
                content = fh.read()
        except IOError:
            content = ""

        return content.strip()

    def writeFile(self, f, data):
        with open(self.meta_path + "/" + f, "w") as fh:
            fh.write(data)

    ## --- --- Getters and Setters --- --- ##

    def setName(self, name, rename_dir=False):
        self.writeFile(Project.git_file_name, name)
        if rename_dir:
            os.rename(self.path, name)
            self = Project(name)

    def getName(self):
        name = self.readFile(Project.git_file_name)

        if name in [
            "Unnamed repository; edit this file 'description' to name the repository.",
            "",
        ]:
            name = self.path.split("/")[-1]  # folder name => project name

        return name

    def setStatus(self, status):
        self.writeFile(Project.git_file_status, status)

    def getStatus(self):
        status = self.readFile(Project.git_file_status)
        if status not in Project.status_set:
            status = "undefined"
        return status

    def setDescription(self, description):
        self.writeFile(Project.git_file_about, description)

    def getDescription(self):
        return self.readFile(Project.git_file_about)

    def setTags(self, tags):
        self.writeFile(Project.git_file_tags, tags)

    def getTags(self):
        return self.readFile(Project.git_file_tags)

    def getCurrentBranch(self):
        # git 2.22: self.execute(["git", "branch", "--show-current"])
        return self.execute(["git", "rev-parse", "--abbrev-ref", "HEAD"])

    def getLastCommit(self, branch=None):
        if branch == None:
            branch = self.getCurrentBranch()

        try:
            commit = self.execute(["git", "rev-parse", branch])
        except:
            commit = "-"

        return commit

    def countCommits(self, branch=None):
        if branch == None:
            branch = self.getCurrentBranch()

        try:
            return int(self.execute(["git", "rev-list", branch, "--count"]))
        except:
            return 0

    def listCommits(self, branch=None):
        if branch == None:
            branch = self.getCurrentBranch()

        return self.execute(["git", "rev-list", branch]).split("\n")

    def getId(self, allow_empty=False):
        id = self.readFile(Project.git_file_id)
        if id == "" and not allow_empty:
            id = "-" * Project.id_width
        return id

    def setId(self, id):
        self.writeFile(Project.git_file_id, id)
