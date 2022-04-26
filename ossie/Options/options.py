#!/usr/bin/env python

import argparse

class Options():
	__mode = None
	__args = None

	def args(self):
		return self.__args

	def mode(self):
		return self.__mode

	def __init__(self, argv):
		self.__mode = None
		self.__args = {}

		parser = argparse.ArgumentParser(prog="main v1.0",
										 usage="usage: main cmd [options] args",
										 description="Audit PyPi packages, including all dependencies")
		subparsers = parser.add_subparsers(title="actions", dest='cmd', help='Command (e.g. auth, audit, monitor)') 

		# Audit sub-command
		audit_parser = subparsers.add_parser('audit', help='Audit a project or package(s).')
		audit_parser.add_argument('--id', dest='id', action='store', help='ID')
		#audit_parser.add_argument('--secret', dest='secret', action='store', required='--id', help='Secret')
	
		audit_group = audit_parser.add_mutually_exclusive_group(required=True)
		audit_group.add_argument('--all', help='Audit all installed packages and dependencies.', action='store_true')
		audit_group.add_argument('--project', help='Audit all deps of a project.', action='store')
		audit_group.add_argument('--package', help='Audit a package, including all deps (e.g., dateutils==0.6.12).', action='store')
		audit_group.add_argument('--deps', help='Audit all deps specified in a file (e.g., requirements.txt).', action='store')

		# Authenticate sub-command
		auth_parser = subparsers.add_parser('auth', help='Authenticate user with the server.')
		auth_parser.add_argument('--force', help='Force user re-authentication', dest="force", action='store_true')

		# Monitor sub-command
		monitor_parser = subparsers.add_parser('monitor', help='Monitor package installations and alert user in real time.')
		monitor_group = monitor_parser.add_mutually_exclusive_group()
		monitor_group.add_argument('--start', help='Start monitoring', dest="status", action='store_true', default=True)
		monitor_group.add_argument('--stop', help='Stop monitoring', dest="status", action='store_false')

		args = parser.parse_args(argv)

		if args.cmd == "auth":
			self.__mode = "Authenticate"
			self.__args = {'force': args.force}

		elif args.cmd == "audit":
			self.__mode = "Audit"
			self.__args = {
				'id'		: args.id,
				'all'		: args.all,
				'project'	: args.project,
				'package'	: args.package,
				'deps'		: args.deps,
			}

		elif args.cmd == "monitor":
			self.__mode = "Monitor"
			self.__args = {
				'status' : args.status,
			}

		else:
			raise Exception("Bad option")

if __name__ == '__main__':
	import sys
	opts = Options(sys.argv[1:])
	print(opts.args())
