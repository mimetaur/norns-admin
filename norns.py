#!/usr/bin/env python3

import fire
import subprocess
import configparser

config = configparser.ConfigParser()
config.read('norns.ini')

from os.path import expanduser
home = expanduser("~")

# local config
dev_path = home + "/" + config['LOCAL']['DEV_PATH']
exclude_file = home + "/" + config['LOCAL']['RSYNC_EXCLUDES']

# remote config
norns_url = config['REMOTE']['URL']
norns_code_path = config['REMOTE']['CODE_PATH']


class DocCommand(object):
    """Document subcommands for Norns scripts"""

    def open(self, script):
        subprocess.run(["open", f"{dev_path}/{script}/doc.index.html"])

    def build(self, script):
        subprocess.run(["cd", f"{dev_path}/{script}"])
        subprocess.run(["ldoc", "."])


class SyncCommand(object):
    """rsync files between Norns and local machine."""

    def up(self, script):
        """rsync script folder up to Norns"""

        local_path = f"{dev_path}/{script}/"
        remote_path = f"{norns_url}:/{norns_code_path}/{script}"

        rsync_cmd = f"rsync -avz --exclude-from '{exclude_file}' {local_path} {remote_path}"
        print(rsync_cmd)
        # subprocess.run(rsync_cmd)


class Norns(object):
    """A command line tool to work with the Norns from your local dev machine."""

    def __init__(self):
        self.doc = DocCommand()
        self.sync = SyncCommand()

    def shell(self):
        """SSH into Norns with we/sleep credentials."""
        subprocess.run(["ssh", norns_url])


if __name__ == '__main__':
    fire.Fire(Norns)
