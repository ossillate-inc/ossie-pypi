#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from __future__ import generators

import os
import socket

from .command_base import CommandBase
import subprocess

class CheckProject(CommandBase):
	def __init__(self, path, auth, creds, env):
		if not os.path.exists(path):
			print("%s does not exist. Exiting." % (path))
			exit(1)
		if not os.path.isdir(path):
			print("%s is not a valid Python project. Exiting." % (path))
			exit(1)
		path = os.path.expanduser(path)
		path = os.path.abspath(path)
		self.project_path = path
		print("[+] Auditing Project @ ", self.project_path)
		name = os.path.basename(self.project_path)
		super().__init__("project", name, auth, creds, env)

	def get_packages(self):
		try:
			pipreqs_command = subprocess.Popen(["pipreqs", self.project_path, "--print", "--force"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			out, err = pipreqs_command.communicate()
			if err:
				err = err.decode('utf-8').strip()
				if err == 'INFO: Successfully output requirements':
					err = None
			if out:
				out = out.decode('utf-8').strip()
			if err or not out or len(out) < 20:
				raise Exception('invalid requirements!')
		except:
			print("%s is not a valid Python project. Exiting." % (self.project_path))
			exit(1)

		try:
			print("    [+] Gathered project requirements")
			packages = self.get_packages_from_output(out)
			if not packages or not len(packages):
				raise Exception("invalid requirements!")
			return packages
		except:
			print("Failed to audit. Exiting.")
			exit(1)
