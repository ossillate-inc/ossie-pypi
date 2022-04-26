#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from __future__ import generators

import socket

from .command_base import CommandBase

class CheckPackage(CommandBase):
	def __init__(self, name, auth, creds, env):
		self.package_name = name.split('==')[0] if '==' in name else name
		self.version = name.split('==')[1] if '==' in name else None
		print("[+] Auditing package %s (version %s)" % \
			(self.package_name, self.version if self.version else 'latest'))
		super().__init__("package", name, auth, creds, env)

	def get_packages(self):
		return [{
			"name": f"{self.package_name}",
			"version": f"{self.version}" if self.version else None,
		}]


