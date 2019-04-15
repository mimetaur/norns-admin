#!/usr/bin/env python3

import fire
import subprocess
import os

import configparser
config = configparser.ConfigParser()
config.read('norns.ini')

from os.path import expanduser
home = expanduser("~")

# local config
dev_path = home + "/" + config['LOCAL']['DEV_PATH']
exclude_file = home + "/" + config['LOCAL']['RSYNC_EXCLUDES']
invalid_script_names = config['LOCAL']['INVALID_SCRIPTS'].split(",")
editor_cmd = config['LOCAL']['EDITOR']

# remote config
norns_url = config['REMOTE']['URL']
norns_code_path = config['REMOTE']['CODE_PATH']


def norns_script_folders():
    scripts = []
    with os.scandir(dev_path) as it:
        for entry in it:
            if not entry.name.startswith('.') and entry.is_dir():
                if entry.name not in invalid_script_names:
                    scripts.append(entry.name)
    return scripts


valid_scripts = norns_script_folders()


def is_valid(script_name):
    valid = False
    if script_name in valid_scripts:
        valid = True
    return valid


def rsync_up(script):
    if not is_valid(script):
        raise ValueError('Not a valid Norns script.')

    print(f"Syncing {script} to Norns.")

    local_path = f"{dev_path}/{script}/"
    remote_path = f"{norns_url}:/{norns_code_path}/{script}"

    rsync_cmd = f"rsync -avz --exclude-from {exclude_file} {local_path} {remote_path}"
    subprocess.run(rsync_cmd, shell=True)


class DocCommand(object):
    """Document subcommands for Norns scripts"""

    def open(self, script):
        subprocess.run(["open", f"{dev_path}/{script}/doc.index.html"])

    def build(self, script):
        subprocess.run(["cd", f"{dev_path}/{script}"])
        subprocess.run(["ldoc", "."])


class Norns(object):
    """A command line tool to work with the Norns from your local dev machine."""

    def __init__(self):
        self.doc = DocCommand()

    def sync(self, script):
        """rsync script folder up to Norns"""
        if script == "all":
            for a_script in valid_scripts:
                rsync_up(a_script)
        else:
            rsync_up(script)

    def shell(self):
        """SSH into Norns with we/sleep credentials."""
        subprocess.run(["ssh", norns_url])

    def list(self):
        """List all valid Norns scripts."""
        print("*** Valid scripts ***")
        return valid_scripts

    def cd(self, script):
        """cd to a Norns script folder."""
        subprocess.run(["cd", f"{dev_path}/{script}"])

    def open(self, script):
        """open a Norns script folder."""
        subprocess.run(["open", f"{dev_path}/{script}"])

    def edit(self, script):
        """edit a Norns script folder."""
        subprocess.run([editor_cmd, f"{dev_path}/{script}"])


if __name__ == '__main__':
    fire.Fire(Norns)
