import logging
import pathlib
import sys

import git


def is_git_repo(path):
    try:
        _ = git.Repo(path).git_dir
        return True
    except git.InvalidGitRepositoryError:
        return False


async def clone_or_pull_project(path: pathlib.Path, url):
    if is_git_repo(path):
        pull_repo(path)
    else:
        clone_project(path, url)


def clone_project(path, url):
    logging.info(f"cloning project: { path.absolute()}")
    try:
        git.Repo.clone_from(url, path)
    except KeyboardInterrupt:
        logging.error("User interrupted")
        sys.exit(0)
    except Exception as e:
        logging.error("Error cloning project %s", path)
        logging.error(e)


def pull_repo(path):
    logging.info("updating existing project %s", path)
    try:
        repo = git.Repo(path)
        repo.remotes.origin.pull()
        logging.info("done updating project  %s", path)

    except KeyboardInterrupt:
        logging.error("User interrupted")
        sys.exit(0)
    except Exception as e:
        logging.error("Error pulling project %s", path)
        logging.error(e)


