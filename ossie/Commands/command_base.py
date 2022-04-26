#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from __future__ import generators

from abc import ABC, abstractmethod

from ..AuditRequesters.PythonAuditRequester import PythonAuditRequester
from ..AuditProcessors.AuditStats import AuditStats

import re
import socket

class CommandBase:
	def __init__(self, cmd, name, auth, creds, env):
		self.req_type = cmd
		self.req_name = name
		self.creds = creds
		self.auth = auth
		self.env = env
		self.__packages = None

	@abstractmethod
	def get_packages(self):
		pass

	def summarize_audit_response(self, env):
		try:
			audit_data = self.pyAuditer.audit_data
			report = AuditStats(audit_data)
			if env == "CICD":
				return report.create_issue()
			return report.summary(len(self.__packages))
		except Exception as e:
			print("Failed to generate audit report: %s" % (str(e)))

	def __parse_string_for_pkg_info(self, line):
		try:
			if line == '':
				return None
			version_search_outcome = re.search(r'(.*)(==|>=|<=)(.*)', line)
			if version_search_outcome is not None:
				pkg = {
					"name": version_search_outcome.group(1),
					"version": version_search_outcome.group(3)
				}
			else:
				pkg = {
					"name": line
				}
			return pkg
		except Exception as e:
			raise Exception("Failed to parse %s: %s" % (line, str(e)))

	def get_packages_from_output(self, out):
		packages=[]
		try:
			for line in out.splitlines():
				pkg = self.__parse_string_for_pkg_info(line)
				if not pkg:
					break
				packages.append(pkg)
		except Exception as e:
			print("Failed to parse output %s for packages" % (output, str(e)))
			pass
		finally:
			return packages

	def get_packages_from_file(self, filepath):
		packages=[]
		try:
			with open(filepath) as f:
				while True:
					line = f.readline().strip()
					pkg = self.__parse_string_for_pkg_info(line)
					if not pkg:
						break
					packages.append(pkg)
			return packages
		except Exception as e:
			print("Failed to parse %s for packages" % (tmpfile, str(e)))
			pass
		finally:
			return packages

	def run(self):
		self.__packages = self.get_packages()
		self.pyAuditer = PythonAuditRequester(self.__packages, self.creds.creds_filepath(), self.auth, self.creds)
		self.pyAuditer.perform_audit(self.req_type, self.req_name)
		return self.summarize_audit_response(self.env)
