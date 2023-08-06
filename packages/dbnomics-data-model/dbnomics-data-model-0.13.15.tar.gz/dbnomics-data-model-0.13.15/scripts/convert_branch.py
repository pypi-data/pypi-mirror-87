#! /usr/bin/env python3

# dbnomics-data-model -- Define, validate and transform DBnomics data.
# By: Christophe Benz <christophe.benz@cepremap.org>
#
# Copyright (C) 2017-2018 Cepremap
# https://git.nomics.world/dbnomics/dbnomics-data-model
#
# dbnomics-data-model is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# dbnomics-data-model is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


"""Convert all the commits of a source data Git repository, and create all the corresponding commits
in the JSON data Git repository of the DBnomics project.

The existing commits of the JSON data Git repository are kept in order to keep SHA-1 references.
A new branch named `convert-branch` is created.

Warning: this script works only with non-bare Git repositories. Another script could be written to handle them.
"""


import argparse
import datetime
import logging
import os
import subprocess
import sys

from dulwich.repo import Repo

args = None  # Will be defined by main().
log = logging.getLogger(__name__)


def convert_commit(source_repo_commit):
    global args

    source_repo_commit_id = source_repo_commit.id.decode('utf-8')

    log.info("Checkout branch {!r} at {!r} in source repository".format(
        args.convert_branch_name, source_repo_commit_id))
    # Move branch if it already exists (-B option).
    subprocess.run(
        ["git", "checkout", "-B", args.convert_branch_name, source_repo_commit_id],
        check=True,
        cwd=args.source_repo_dir,
    )

    log.info("Delete files in target repository")
    # Command is the same than in `.gitlab-ci.yml` jobs.
    subprocess.run(
        'find -not -path "./.git/*" -not -name ".git" -delete',
        check=True,
        cwd=args.target_repo_dir,
        shell=True,
    )

    log.info("Running convert script...")
    subprocess.run(
        [args.convert_script, args.source_repo_dir, args.target_repo_dir],
        check=True,
        # shell=True,
    )
    log.info("Convert script ended")

    log.info("Commit converted files in target repository")
    subprocess.run(
        ["git", "add", "--all"],
        check=True,
        cwd=args.target_repo_dir,
    )
    commit_author = "Convert branch script <convert-branch@db.nomics.world>"
    commit_message = "New conversion...\n\nfrom commit {} in source data repository".format(
        source_repo_commit_id).encode('utf-8')
    subprocess.run(
        [
            "git", "commit",
            "--quiet",
            "-m", commit_message,
            "--date", str(source_repo_commit.author_time),
            "--author", commit_author,
        ],
        check=False,  # Git returns an error status code if there is nothing to commit. Ignore it and continue.
        cwd=args.target_repo_dir,
    )


def warn_if_repo_is_not_clean(dir_path):
    process = subprocess.run(['git', 'status', '--porcelain'], cwd=dir_path, stdout=subprocess.PIPE)
    if process.stdout:
        log.warning("{}: Git repository working tree is not clean. The script will ignore non-committed data.".format(
            dir_path))


def main():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='display debug logging messages')
    parser.add_argument('convert_script', help='path to the convert script of the fetcher')
    parser.add_argument('source_repo_dir', help='path of the Git repository containing source data')
    parser.add_argument('target_repo_dir', help='path of the Git repository containing JSON and TSV data')
    parser.add_argument('--convert-branch-name', default="convert-branch",
                        help='name of the temporary branch used in source and target repositories')
    parser.add_argument('--read-from', default=None,
                        help='commit of the source repo to start reading from (by default, find start commit automatically')
    parser.add_argument('--write-on', default=None,
                        help='commit of the target repo to start writing at (by default, create an orphan branch)')
    args = parser.parse_args()
    args.source_repo_dir = os.path.abspath(args.source_repo_dir)
    args.target_repo_dir = os.path.abspath(args.target_repo_dir)

    logging.basicConfig(
        format="%(levelname)s:%(asctime)s:%(message)s",
        level=logging.DEBUG if args.verbose else logging.INFO,
    )

    warn_if_repo_is_not_clean(args.source_repo_dir)
    warn_if_repo_is_not_clean(args.target_repo_dir)

    # Create a new branch in target repo starting from "--write-on" commit, or orphan.
    log.info("Creating branch {!r} in target repository".format(args.convert_branch_name))
    subprocess.run(
        ["git", "checkout", "-b", args.convert_branch_name, args.write_on]
        if args.write_on is not None
        else ["git", "checkout", "--orphan", args.convert_branch_name],
        check=True,
        cwd=args.target_repo_dir,
    )

    source_repo = Repo(args.source_repo_dir)

    start_commit_found = args.read_from is None
    source_repo_commits = list(map(lambda w: w.commit, source_repo.get_walker(reverse=True)))
    for source_repo_commit_idx, source_repo_commit in enumerate(source_repo_commits):
        source_repo_commit_id = source_repo_commit.id.decode('utf-8')
        if not start_commit_found:
            assert args.read_from is not None
            if source_repo_commit_id == args.read_from:
                start_commit_found = True
            else:
                continue

        log.info("Converting commit {!r} of source repository ({}/{})".format(
            source_repo_commit_id, source_repo_commit_idx + 1, len(source_repo_commits)))
        convert_commit(source_repo_commit)

    # Clean temporary branches.

    log.info("Delete branch {!r} in source repository".format(args.convert_branch_name))
    subprocess.run(
        ["git", "checkout", "master"],
        check=True,
        cwd=args.source_repo_dir,
    )
    subprocess.run(
        ["git", "branch", "-d", args.convert_branch_name],
        cwd=args.source_repo_dir,
    )

    new_master_branch_name = "master-{}".format(str(datetime.datetime.now().date()))
    log.info("Rename target repository 'master' branch to {!r}".format(new_master_branch_name))
    subprocess.run(
        ["git", "checkout", "master"],
        check=True,
        cwd=args.target_repo_dir,
    )
    subprocess.run(
        ["git", "branch", "--move", new_master_branch_name],
        check=True,
        cwd=args.target_repo_dir,
    )

    log.info("Rename target repository {!r} branch to 'master'".format(args.convert_branch_name))
    subprocess.run(
        ["git", "checkout", args.convert_branch_name],
        check=True,
        cwd=args.target_repo_dir,
    )
    subprocess.run(
        ["git", "branch", "--move", "master"],
        check=True,
        cwd=args.target_repo_dir,
    )

    log.info(("A new 'master' branch exists in target repository, old 'master' branch was archived to {!r}. "
              "All you have to do now is decide whether to force the push to origin.").format(new_master_branch_name))

    return 0


if __name__ == '__main__':
    sys.exit(main())
