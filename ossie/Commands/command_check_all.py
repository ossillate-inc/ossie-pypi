from .command_base import CommandBase
import subprocess
import re
import socket

class CheckAll(CommandBase):
	def __init__(self, auth, creds, env):
		super().__init__('all', 'system', auth, creds, env)

	def get_packages(self):
		pipreqs_command = ['pip', 'freeze']
		tmpfile = '/tmp/audit_req.txt'
		with open(tmpfile, 'w') as tmpf:
			subprocess.run(pipreqs_command, stdout=tmpf)
		packages = self.get_packages_from_file(tmpfile)
		print("[+] Auditing all installed packages")
		return packages
