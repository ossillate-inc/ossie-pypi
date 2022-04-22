#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import os
import sys
from pathlib import Path
sys.path[0] = str(Path(sys.path[0]).parent)

from .Options.options import Options
from .Config.config import Config
from .Logger.logger import Logger

from .Authentication.creds import Creds
from .Authentication.auth import Auth

from .Commands.command_check_all import CheckAll
from .Commands.command_check_project import CheckProject
from .Commands.command_check_package import CheckPackage

from .Utils.utils import parse_url
from .Monitor.monitor import *

############################################################################
# Init
############################################################################

def audit_request(creds, auth, env, args):
	attempts = 3
	token = None
	expired = False
	while attempts and (not token or expired):

		# current state
		token = creds.get_cred('token')
		if not token:
			if env != 'CICD':
				print('User not authenticated. You need to authenticate the user first.')
		elif auth.token_expired(creds, token):
			print('User access tokens have expired. Fetching new tokens.')
			expired = True
		else:
			break

		# fix tokens
		if env == "CICD":
			creds.add_or_update_cred('id', args['id'])
		auth.create_or_refresh_session(creds, expired=expired)

		# check if fixed
		attempts -= 1
		if not attempts:
			raise Exception('could not authenticate user!')

	if args['all']:
		site_package_checker = CheckAll(auth=auth, creds=creds)
		return site_package_checker.run()

	elif args['package']:
		package_checker = CheckPackage(args['package'], auth=auth, creds=creds)
		return package_checker.run()

	elif args['project']:
		project_checker = CheckProject(args['project'], auth=auth, creds=creds)
		return project_checker.run()

def cleanup(env, auth, creds):
	if env == "CICD":
		creds.delete_cred('token')
		creds.delete_cred('id')
		creds.delete_cred('auth_url')
	else:
		saved_url = creds.get_cred('auth_url')
		if not saved_url:
			creds.delete_cred('token')
		else:
			saved_url_info = parse_url(saved_url)
			if not saved_url_info:
				creds.delete_cred('token')
			url = saved_url_info['scheme'] + '://' + saved_url_info['netloc']
			if url != auth.base_url():
				creds.delete_cred('token')

def main(mode:str=None, args:dict=None):

	if not mode and not args:
		# parse args
		try:
			opts = Options(sys.argv[1:])
		except Exception as e:
			print("Failed: %s. Use --help." % (str(e)))
			exit(1)

		# get args
		mode = opts.mode()
		args = opts.args()

	# derive deployment env
	if 'id' in args and args['id']:
		env = 'CICD'
	else:
		env = 'CLI'

	if env == "CICD" and mode == "Authenticate":
		print("User authentication is not supported in CI/CD env!")
		exit(1)

	# get configuration
	try:
		cfg_file_path = os.path.join(os.path.dirname(__file__), "config.ini")
		config = Config(file_path=cfg_file_path)
	except Exception as e:
		print("Error getting config parser: %s" % (str(e)))
		exit(1)

	# user config filepath
	try:
		filepath = config.get('USER_CONFIG_FILEPATH', env, str)
		user_creds_filepath = os.path.expanduser(filepath)
	except Exception as e:
		print("Failed to get user config filepath from config. Defaulting to ~/.ossie.yaml: %s. Exiting." % (str(e)))
		exit(1)

	# debugging configuration
	try:
		debug = config.get('DEBUG', env, bool)
	except:
		debug = False

	# logging infrastructure
	try:
		logfile_path = config.get('LOGFILE_PATH', env, str)
	except:
		logfile_path = None
	try:
		logger = Logger("Logger",path=logfile_path, debug=bool(debug))
	except Exception as e:
		print("Failed to setup logging module: %s" % (str(e)))
		exit(1)

	try:
		creds = Creds(user_creds_filepath, logger)
	except Exception as e:
		print("Failed to init user credentials module: %s" % (str(e)))
		exit(1)

	try:
		auth = Auth(config, logger, env)
	except Exception as e:
		print("Failed to init user authentication module: %s" % (str(e)))
		exit(1)

	# remove stale credentials
	cleanup(env, auth, creds)

	if mode == "Authenticate":
		try:
			force = args['force']
			token = creds.get_cred('token')
			if not token or force:
				return auth.create_or_refresh_session(creds, expired=False)
			else:
				expired = auth.token_expired(creds, token)
				if not expired:
					print("User is already authenticated. Nothing to do")
					return True
				else:
					return auth.create_or_refresh_session(creds, expired=expired)
		except Exception as e:
			print("Failed to authenticate user: %s" % (str(e)))

	elif mode == "Audit":
		try:
			audit_request(creds, auth, env, args)
			return 0
		except Exception as e:
			print("Failed to audit (%s): %s" % (env, str(e)))

	elif mode == "Monitor":
		try:
			if args['status']:
				activate_pip_wrapper()
			else:
				deactivate_pip_wrapper()
		except Exception as e:
			print("Failed to monitor: %s" % (str(e)))
	else:
		raise Exception("Bad option")

if __name__ == "__main__":
	main()
