import os
import re
import platform
import subprocess

def find_executable(exg):
	try:
		(path, _) = subprocess.Popen(["which", exg], stdout=subprocess.PIPE).communicate()
		path = path.strip()
		if not os.path.exists(path):
			return None
		return path
	except:
		return None

def get_ossie_pip_alias(pip='pip'):
	"""Return the alias for ossie-pip.
	If pyenv is being used, return an alias to the current python installation's ossie-pip."""
	ossie_pip_alias = 'alias %s="ossie-pip"' % (pip)
	if find_executable('pyenv'):
		pyenv_version = os.popen('pyenv version').read().split('(')[0].strip()
		ossie_pip_alias = 'alias %s="~/.pyenv/versions/' + pyenv_version + '/bin/ossie-pip"' % (pip)
	return ossie_pip_alias

def install_alias(file_path, alias):
	"""Install the given alias to the given file.
	Add a comment above the alias so that users know what it's for."""
	try:
		with open(file_path, 'r') as read_f:
			contents = read_f.read()
			if alias in contents:
				return False
			out = open(file_path, 'a')
			out.write('\n')
			msg = '# Ossillate: pip alias to source the ossie-pip script'
			out.write(msg)
			out.write('\n')
			out.write(alias)
			out.write('\n')
			out.close()
			return True
	except:
		return False

def uninstall_alias(file_path, alias):
	"""Uninstall the given alias from the given file."""
	with open(file_path, 'r') as read_f:
		contents = read_f.read()
		if alias not in contents:
			return False
		contents = re.sub(".*"+alias+".*\n?","",contents)
		msg = '# Ossillate: pip alias to source the ossie-pip script'
		contents = re.sub(".*"+msg+".*\n?","",contents)
		out = open(file_path, 'w')
		out.write(contents)
		out.close()
		return True

def ensure_executable():
	"""Make sure pip wrapper is executable"""
	ossie_pip_path = find_executable("ossie-pip")
	if not ossie_pip_path:
		print("ossie-pip is not installed. Exiting.")
		exit(1)
	else:
		os.chmod(ossie_pip_path, int('755', 8))

def get_bash_file():
	try:
		current_platform = platform.system().lower()
		
		# if platform is Windows, use "~/.bash_profile"
		if current_platform == "windows":
			bash_file = "~/.bash_profile"
		
		# if platform is OS X use "~/.bash_profile"
		elif current_platform == "darwin":
			bash_file = "~/.bash_profile"
		
		# if platform is Linux use "~/.bashrc
		elif current_platform == "linux":
			bash_file = "~/.bashrc"
		
		# else discard
		else:
			print("Failed to install pip alias: platform not supported. Installations will not be monitored!")
			exit(1)

		bash_file = os.path.expanduser(bash_file)
		if not os.path.exists(bash_file):
			print("Failed to install pip alias: only 'bash' shell is supported. Installations will not be monitored!")
			exit(1)

		return bash_file
	except Exception as e:
		print("Failed to install pip alias: %s. Installations will not be monitored!" % (str(e)))
		exit(1)

def deactivate_pip_wrapper():
	try:
		# get ~/.bashrc or ~/.bash_profile
		bash_file = get_bash_file()

		# remove pip alias
		ossie_pip_alias = get_ossie_pip_alias()
		if ossie_pip_alias:
			uninstall_alias(bash_file, ossie_pip_alias)

		ossie_pip_alias = get_ossie_pip_alias(pip='pip3')
		if ossie_pip_alias:
			uninstall_alias(bash_file, ossie_pip_alias)

		# alert user
		print("<//> OssieBOT: to stop monitoring source %s file and set unalias:" % (bash_file))
		print("source %s; unalias pip; unalias pip3" % (bash_file))
	except Exception as e:
		print("Failed to remove pip alias: %s. Installations will CONTINUE to be monitored!" % (str(e)))

def activate_pip_wrapper():
	try:
		# get ~/.bashrc or ~/.bash_profile
		bash_file = get_bash_file()

		# make executable
		ensure_executable()

		# install for bash
		ossie_pip_alias = get_ossie_pip_alias()
		if ossie_pip_alias and install_alias(bash_file, ossie_pip_alias):
			ossie_pip_alias = get_ossie_pip_alias(pip='pip3')
			if ossie_pip_alias:
				install_alias(bash_file, ossie_pip_alias)
			# alert user
			print("<//> OssieBOT: to start monitoring source %s file:" % (bash_file))
			print("source %s" % (bash_file))
	except Exception as e:
		print("Failed to install pip-wrapper: %s" % (str(e)))
