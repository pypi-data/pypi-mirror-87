#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys
import pwd
import re
import time
import datetime
import git
#from persistent_bhub_config import PersistentBinderSpawner
from jupyterhub.spawner import LocalProcessSpawner
from traitlets import Unicode, Bool
import git
from git import Repo


def get_lockfile(path):
    is_locked = False
    locked_by = ""
    locked_when = ""

    lockfile_path = os.path.join(path, '.lockfile')
    if os.path.isfile(lockfile_path):
        is_locked = True
        with open(lockfile_path, 'r') as fh:
            locked_by = fh.readline().strip()
        locked_when = time.ctime(os.path.getmtime(lockfile_path))

    return (is_locked, locked_by, locked_when)

def get_commit_status(path):
    is_locked = False
    locked_by = ""
    locked_when = ""

    repo = None
    try:
        repo = Repo(path)
    except git.NoSuchPathError as e:
        # TODO: handle nonexisting path
        print(e)
        return
    except git.InvalidGitRepositoryError:
        # TODO: handle invalid git repo
        print(e)
        return

    branch_name = repo.head.ref.name 
    if branch_name == 'master':
        print(f"{path} is on MASTER - is_locked=False")
        is_locked = False
    else:
        print(f"{path} is on {branch_name} - is_locked=True")
        is_locked = True
        print(branch_name)
        match = re.search(r'^(?P<username>.*?)\/(?P<timestamp>.*)', branch_name)
        if match:
            print("MATCHED")
            d = match.groupdict()
            locked_by = d['username']
            dt_obj = datetime.datetime.strptime(d['timestamp'], '%Y-%m-%d_%H.%M.%S')
            #locked_when = d['timestamp']
            locked_when = str(dt_obj)
            print(d)
        else:
            print(f"NOT MATCHED: {branch_name}") 

    return (is_locked, locked_by, locked_when)

def get_git_commit(path):
    try:
        repo = Repo(path)
    except git.NoSuchPathError:
        repo = None
        pass
    except git.InvalidGitRepositoryError:
        repo = None
        pass
        
    commit = repo.commit()
    git_commit = {
        "commit_hash": commit.hexsha,
        "commit_date": time.ctime(commit.committed_date),
        "commit_name": commit.committer.name,
        "commit_message": commit.message,
        "active_branch": repo.active_branch.name,
    }
    return git_commit


def vol_name(folder_name: str):
    """Volume names only may container lower case alphanumeric chars.
    To prevent collisions, we build a hex representation of the original
    name"""
    return "vol-" + folder_name.encode().hex().lower()


class RRPPersistentBinderSpawner(LocalProcessSpawner):
    # the main project dir can be defined in the jupyterhub_config.py
    # c.RRPPersistentBinderSpawner.projects_dir = '/path/to/projects'

    projects_dir = Unicode(
        config=True,
        help='Directory of projects'
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user.project_dirs = self.get_project_dirs(self.projects_dir)
        return
        
    def get_state(self):
        _state = self.orm_spawner.state
        state = super().get_state()
        return state

    def get_project_dirs(self, project_dir):
        def _get_project_dirs():
            project_dirs = [] 
            for f in os.scandir(project_dir):
                if f.is_dir():
                    #(is_locked, locked_by, locked_when) = get_lockfile(f.path) 
                    (is_locked, locked_by, locked_when) = get_commit_status(f.path) 
                    git_commit = get_git_commit(f.path) or {}
                    project_dirs.append(
                        {
                            #"repo_url": f.path,
                            "repo_url": 'project://stelling/vermeul/{}'.format(f.name),
                            "display_name": f.name,
                            "image": "",
                            "ref": git_commit.get('commit_hash'),
                            "git_commit": git_commit,
                            "is_locked": is_locked,
                            "locked_by": locked_by,
                            "locked_when": locked_when,
                        }
                    )
            return project_dirs
        return _get_project_dirs
