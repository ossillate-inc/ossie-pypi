import json
class AuditStats:
	def __init__(self, audit_data):
		assert 'packages' in audit_data, "Unexpected error. Please report this bug"
		assert isinstance(audit_data['packages'], list), "Unexpected error. Please report this bug"
		self.audit_data = audit_data
		self._reported = []
		self._erroneous = []
		self._not_risky = []
		self._not_found = []
		self._risky = []
		self.aggregate_stats()

	def add_pkg(self, type, pkg):
		getattr(self,type).append(pkg)

	def __str__(self):
		for attr_name in dir(self):
			attribute = getattr(self, attr_name)
			if isinstance(list, attribute):
				if attr_name[0] == "_":
					print(attr_name[1:],":", len(attribute))

	# count: number of scanned packages
	def summary(self, requested_count:int):

		out = ""
		reported_count = len(self._reported)
		if not requested_count or reported_count > requested_count:
			print("Unexpected error occurred. Exiting.")
			exit(1)
		if requested_count > reported_count:
			out += "[WARNING]: only %d of %d package(s) were analyze(d)!" % \
					(reported_count, requested_count)

		errorenous_count = len(self._erroneous)
		if reported_count and errorenous_count:
			out += "[WARNING]: failed to analyze %d package(s)\n%s\n" % \
				(errorenous_count, [ (i['name'],i['version']) for i in self._erroneous])
			reported_count -= errorenous_count

		missing_count = len(self._not_found)
		if reported_count and missing_count:
			if reported_count == missing_count:
				out += "    [+] No package(s) were found"
			else:
				out += "    [+] %d package(s) were not found\n" % (missing_count)
				for i in self._not_found:
					out += "        [+] %s (version %s)\n" % (i['name'], i['version'])
			reported_count -= missing_count

		risky_count = len(self._risky)
		if reported_count and risky_count:
			out += "    [+] Found %d risky package(s)\n" % (risky_count)
			for i in self._risky:
				out += "        [+] %s (version %s) is %s\n" % \
					(i['name'], i['version'], ','.join(i['risks']))
			reported_count -= risky_count
		elif reported_count and reported_count == len(self._not_risky):
			out += "    [+] No risks found\n"

		not_risky_count = len(self._not_risky)
		if reported_count and not_risky_count:
			reported_count -= not_risky_count
		if reported_count:
			print("Unexpected error. Exiting!")
			exit(1)
		print(out.strip('\n'))
		return risky_count

	def create_issue(self):
		with open("/tmp/issue_title.txt", 'w') as f:
			f.write("Risky/Malicious/Undesirable Dependencies found")
		with open("/tmp/issue_body.txt", 'w') as f:
			issue = ''
			for p in self._risky:
				issue = issue+'\n'+p['name'] 
				for risk,reasons in p["risks"].items():
					issue += ","+risk+"," 
					for r in reasons:
						issue += r['details']
			f.write(issue)

	def aggregate_stats(self):
		for pkg in self.audit_data['packages']:
			self._reported.append(pkg)
			if 'risks' not in pkg or not pkg['risks']:
				self._erroneous.append(pkg)
				continue

			if isinstance(pkg['risks'], str):
				msg = pkg['risks']
				if msg == 'no risks found':
					self._not_risky.append(pkg)
				else:
					self._not_found.append(pkg)
				continue

			for cat in pkg['risks']:
				self._risky.append(pkg)
		if len(self._risky) > 0:
			with open("/tmp/issue_required.txt", 'w') as f:
				f.write("YES")
			self.create_issue()
		else:
			with open("/tmp/issue_required.txt", 'w') as f:
				f.write("NO")
			with open("/tmp/issue_title.txt", 'w') as f:
				f.write("NA")
			with open("/tmp/issue_body.txt", 'w') as f:
				f.write("NA")

