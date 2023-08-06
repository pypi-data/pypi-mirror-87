#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

"""Command line interface for GitLab CI."""

import argparse
import os
import sys
from time import sleep

import keyring
from tabulate import tabulate
from termcolor import colored, cprint

import gitlabcicli as info
from gitlabcicli.gitlabapiwrapper import GitLabApiClient
from gitlabcicli.gitwrapper import (
    get_current_commit,
    get_long_commit_sha,
    get_project_name,
    get_server_url,
    get_shas,
)
from gitlabcicli.script_helpers import debug, error, set_verbosity

try:
    import argcomplete
except ImportError:
    argcomplete = None

KNOWN_STATES = {
    "unknown": {
        "color": "yellow",
        "severity": 0,
    },
    "success": {
        "color": "green",
        "severity": 1,
    },
    "pending": {
        "color": "magenta",
        "severity": 2,
    },
    "running": {
        "color": "blue",
        "severity": 3,
    },
    "canceled": {
        "color": "grey",
        "severity": 4,
    },
    "failed": {
        "color": "red",
        "severity": 5,
    },
    "created": {
        "color": "yellow",
        "severity": 2,
    },
    "skipped": {"color": "blue", "severity": 2},
    "manual": {"color": "red", "severity": 4},
}

COMMAND_ALIASES_MAP = {
    "show": {"status"},
    "raw": {"log"},
    "do": {"action"},
    "lint": {"validate"},
    "open": {"web"},
}

KEYRING_SERVICE_NAME = "gitlabcicli"


def sha_completer(prefix, **kwargs):
    """tab completion shas in current git"""

    return (s[:8] for s in get_shas() if s.startswith(prefix))


def gitlabciyml_completer(prefix, **_):
    """tab completion for .gitlab-ci.yml"""
    files = argcomplete.completers.FilesCompleter()(prefix)
    print(files)

    return [
        fn
        for fn in files
        if (os.path.isdir(fn) or ".gitlab-ci.yml".startswith(fn.split("/")[-1]))
    ]


def parse_args():
    """Return the parsed arguments as object (see argparse doc)."""
    parser = argparse.ArgumentParser(description=info.__doc__)
    parser.add_argument(
        "--version", action="version", version="%(prog)s {info.__version__}"
    )
    parser.add_argument(
        "-v",
        dest="verbosity",
        action="count",
        default=0,
        help="Be more verbose (up to -vvvvv)",
    )
    parser.add_argument("-t", "--token", help="The token from gitlab to query the API")
    parser.add_argument(
        "-s",
        "--server",
        metavar="URL",
        dest="server_url",
        help="The gitlab server url"
        + "(e.g.: https://gitlab.com/, default: parsed from remote)",
    )
    parser.add_argument(
        "-p",
        "--project",
        help="The project name or id (e.g. foo/bar, default: current project)",
    )

    subparsers = parser.add_subparsers(
        title="actions",
        dest="action",
        # required=False, TODO
    )

    # show
    parser_show = subparsers.add_parser(
        "show",
        aliases=COMMAND_ALIASES_MAP["show"],
        help="Show the current job status",
    )
    parser_show.add_argument(
        "-c",
        "--commit",
        type=get_long_commit_sha,
        metavar="SHA",
        dest="commit_hash",
        help="The commit id to check (default: the current id)",
    ).completer = sha_completer
    parser_show.add_argument(
        "-j",
        "--job",
        metavar="ID",
        dest="job_ids",
        type=int,
        action="append",
        default=[],
        help="The job id to inspect",
    )

    # raw
    parser_raw = subparsers.add_parser(
        "raw",
        aliases=COMMAND_ALIASES_MAP["raw"],
        help="Get or watch the output of a job",
    )
    parser_raw.add_argument(
        "-f",
        "--follow",
        action="store_true",
        default=False,
        help="Follow running jobs (default: false)",
    )
    parser_raw.add_argument(
        "-c",
        "--commit",
        type=get_long_commit_sha,
        metavar="SHA",
        dest="commit_hash",
        help="The commit id to inspect (default: the current id)",
    ).completer = sha_completer
    parser_raw.add_argument(
        "-j",
        "--job",
        metavar="ID",
        dest="job_ids",
        type=int,
        action="append",
        default=[],
        help="The job id to inspect",
    )

    # do
    parser_do = subparsers.add_parser(
        "do",
        aliases=COMMAND_ALIASES_MAP["do"],
        help="Run actions on jobs [cancel, retry, erase]",
    )
    parser_do.add_argument(
        "job_action",
        metavar="action",
        choices=("cancel", "retry", "erase"),
        help="What to do with the job [cancel, retry, erase]",
    )
    parser_do.add_argument(
        "-j",
        "--job",
        metavar="ID",
        dest="job_ids",
        type=int,
        action="append",
        required=True,
        help="The job id to inspect",
    )

    # lint
    parser_lint = subparsers.add_parser(
        "lint",
        aliases=COMMAND_ALIASES_MAP["lint"],
        help="Validate the gitlab-ci.yml",
    )
    parser_lint.add_argument(
        "file",
        type=argparse.FileType("r"),
        default=".gitlab-ci.yml",
        nargs="?",
        help="The gitlab-ci.yml",
    ).completer = gitlabciyml_completer

    # open
    parser_open = subparsers.add_parser(
        "open",
        aliases=COMMAND_ALIASES_MAP["open"],
        help="Open the current project in your browser",
    )

    if argcomplete:
        argcomplete.autocomplete(parser)

    args = parser.parse_args()

    if args.verbosity > 5:
        args.verbosity = 5
    set_verbosity(args.verbosity)

    if not args.action:
        args.action = "show"

    if args.action not in COMMAND_ALIASES_MAP:
        for command, aliases in COMMAND_ALIASES_MAP.items():
            if args.action in aliases:
                args.action = command

                break

    return args


def fetch_token(args):
    """Retreive the token for current server from keyring."""

    if not args.token:
        try:
            args.token = keyring.get_password(KEYRING_SERVICE_NAME, args.server_url)
        except Exception as exc:
            error("No token found in wallet. Please use --token to specify your token.")
            error(str(exc))
            sys.exit(500)


def _color_job_status(status):
    """Return the colored job status as string"""

    return colored(status, attrs=["bold"], color=KNOWN_STATES[status]["color"])


def _color_coverage(coverage):
    """Return the colored coverage as string"""

    if coverage:
        color = "red"

        if coverage > 90:
            color = "green"
        elif coverage > 75:
            color = "yellow"

        return colored(f"{coverage:.1f}%", color=color)
    else:
        debug("No coverage found", min_debug_level=5)

        return ""


def print_job_table(jobs):
    """Print information about the jobs to stdout."""
    table_jobs = []
    table_headers = [
        "id",
        "status",
        "stage",
        "commit hash",
        "commit title",
        "author",
        "coverage",
    ]

    for job in jobs:
        debug(job["status"], 5)

        if job["status"] not in KNOWN_STATES.keys():
            error(f'[!] Status "{job["status"]}" is unknown!')

            continue
        table_job = [
            job["id"],
            _color_job_status(job["status"]),
            job["stage"],
            job["commit"]["short_id"],
            job["commit"]["title"],
            job["commit"]["author_name"],
            _color_coverage(job["coverage"]),
        ]
        table_jobs.append(table_job)
    print(tabulate(table_jobs, headers=table_headers, disable_numparse=True))


class GitLabCiCli(object):
    """A Cli class."""

    def __init__(self, server_url, token, **kwargs):
        self.api_client = GitLabApiClient(
            server_url=server_url,
            token=token,
        )
        self.args = kwargs

        self.project_id = self.api_client.get_project_id(self.args["project"])

        if self.project_id == -1:
            error("Could not determine the project ID.")

        if self.args["action"] in {"raw"}:
            self.project_path = self.api_client.get_project_path(self.project_id)

            if not self.project_path:
                error("Could not determine the project path.")

    def get_jobs(self):
        """Return a list of jobs to handle."""

        if "job_ids" in self.args and self.args["job_ids"]:
            jobs = []

            for jid in self.args["job_ids"]:
                job = self.api_client.get_job_for_id(
                    project_id=self.project_id,
                    job_id=jid,
                )

                if job:
                    jobs.append(job)
        else:
            pipeline_id = self.api_client.get_pipeline_for_commit(
                project_id=self.project_id,
                commit_hash=self.args["commit_hash"],
            )

            if not pipeline_id:
                error(f"No pipeline found for commit {self.args['commit_hash']}")
                exit(404)
            jobs = self.api_client.get_pipeline_jobs(
                project_id=self.project_id,
                pipeline_id=pipeline_id,
            )
            jobs = sorted(jobs, key=lambda v: v["id"])

        return jobs

    def show(self):
        """Run gitlabcicli show."""
        jobs = self.get_jobs()

        if not jobs:
            error("No jobs found.")

            return
        print_job_table(jobs)

    def raw(self):
        """run gitlabcicli raw"""
        jobs = self.get_jobs()

        for job in jobs:
            print()
            cprint(f" === Job output of job #{job['id']} === ", attrs=["bold"])
            print()
            raw_output = ""
            try:
                while True:
                    new_raw_output = self.api_client.get_raw_job_increment(
                        project_path=self.project_path,
                        job_id=job["id"],
                        oldraw=raw_output,
                    )

                    if new_raw_output:
                        print(new_raw_output, end="", flush=True)
                        raw_output += new_raw_output

                    if job["status"] in ["pending", "running", "created"]:
                        if not self.args["follow"]:
                            # not following
                            print()
                            cprint(
                                "...still running... (use --follow to follow the output)",
                                color="yellow",
                                attrs=["bold"],
                            )

                            break
                        else:
                            # follow
                            sleep(0.5)
                            # update job information
                            job = self.api_client.get_job_for_id(
                                project_id=self.project_id,
                                job_id=job["id"],
                            )
                    else:
                        # job has finished

                        break
            except KeyboardInterrupt:
                pass
            print()

    def do(self):
        """Run gitlabcicli do."""

        for job_id in self.args["job_ids"]:
            response = self.api_client.run_action_on_job(
                action=self.args["job_action"],
                job_id=job_id,
                project_id=self.project_id,
            )
            debug(response, 5)

            if not response:
                error(
                    f"Could not {self.args['job_action']} job #{job_id} for project '{self.args['project']}'."
                )
            else:
                past = {"cancel": "canceled", "retry": "retried", "erase": "erased"}
                cprint(
                    f"Successfully {self.args['job_action']} job #{job_id} for project '{self.args['project']}'",
                    color="green",
                    attrs=["bold"],
                )

                if self.args["job_action"] == "retry":
                    cprint(
                        f"New job id is #{response['id']}",
                        color="green",
                        attrs=["bold"],
                    )

    def lint(self):
        """Run gitlabcicli lint."""
        gitlabciyml_text = self.args["file"].read()
        debug(f"gitlabci.yml content:\n{gitlabciyml_text}", 5)
        api = self.api_client.validate_ciyml(gitlabciyml_text=gitlabciyml_text)

        if api["status"] == "valid":
            cprint(
                ".gitlab-ci.yml is valid",
                color="green",
                attrs=["bold"],
            )
        else:
            cprint(
                ".gitlab-ci.yml is invalid",
                color="red",
                attrs=["bold"],
            )
            print("List of errors:")

            for error_description in api["errors"]:
                print(f" - {error_description}")

    def open(self):
        """Open the current project in browser."""
        url = self.api_client.get_project_url(self.project_id)
        os.system(f"xdg-open {url}")


def main():
    """The main function"""
    args = parse_args()

    if args.action in {"show", "raw", "lint", "do", "open"}:
        if not getattr(args, "server_url", None):
            debug("Try to get server url from remote of local git repo...", 2)
            args.server_url = get_server_url()
            debug(f"Using server {args.server_url}", 1)

    if args.action in {"show", "raw", "lint", "do", "open"}:
        if not getattr(args, "project", None):
            debug("Try to get project from remote of local git repo...", 2)
            args.project = get_project_name()
            debug(f"Using project {args.project}", 1)

    if args.action in {"show", "raw"} and ("job_ids" not in args or not args.job_ids):

        if not getattr(args, "commit_hash", None):
            # ref is better than commit
            debug("Try to get commit from remote of local git repo...", 2)
            args.commit_hash = get_current_commit()
            debug(f"Using commit {args.commit_hash}", 1)

    if args.action in {"show", "raw", "lint", "do", "open"}:
        if not getattr(args, "token", None):
            debug("Try to get token for server from config...", 2)
            fetch_token(args)
            debug(f"Using token {args.token}", 1)

    cli = GitLabCiCli(**args.__dict__)

    if args.action == "show":
        cli.show()
    elif args.action == "raw":
        cli.raw()
    elif args.action == "do":
        cli.do()
    elif args.action == "lint":
        cli.lint()
    elif args.action == "open":
        cli.open()

    # After successful run

    if args.token:
        keyring.set_password(KEYRING_SERVICE_NAME, args.server_url, args.token)


if __name__ == "__main__":
    main()
