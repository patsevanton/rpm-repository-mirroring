#!/usr/bin/env python

import json
import sys
import yum
from distutils.version import LooseVersion

config = "rpm-repository-mirroring.conf"


def get_list_repo(config):
	with open(config, "r") as f:
		for line in f:
			if "REPOS" in line:
				fields = line.strip().split("=")
				list_repo=json.loads(fields[1])
				return list_repo

def get_dict_cut(config):
	with open(config, "r") as f:
		for line in f:
			if "CUT_AFTER" in line:
				fields = line.strip().split("=")
				name_count=json.loads(fields[1])
				return name_count


name_count = get_dict_cut(config)
repo_name_ver = {}
for repo in get_list_repo(config):
	yb = yum.YumBase()
	if not yb.setCacheDir(force=True, reuse=False):
		print >>sys.stderr, "Can't create a tmp. cachedir. "
		sys.exit(1)

	yb.repos.disableRepo('*')
	yb.repos.enableRepo(repo)
	repo_name_ver[repo] = {}
	ignore = False
	prev_name = None
	for pkg in sorted(yb.pkgSack.returnPackages(), reverse=True):
		if ignore == True and prev_name == pkg.name:
			continue
		if prev_name != pkg.name:
			ignore = False
		if pkg.name in name_count:
			if name_count[pkg.name] > 0:
				if pkg.name in repo_name_ver[repo]:
					repo_name_ver[repo][pkg.name].append(pkg.version + '-' + pkg.release)
				else:
					repo_name_ver[repo][pkg.name] = [pkg.version +  '-' + pkg.release]
				name_count[pkg.name] -= 1
			else:
				name_count.pop(pkg.name, None)
				ignore = True
		else:
			if pkg.name in repo_name_ver[repo]:
				if LooseVersion(pkg.version) >= LooseVersion(get_list_repo(config)[repo]):
					repo_name_ver[repo][pkg.name].append(pkg.version + '-' + pkg.release)
			else:
				if LooseVersion(pkg.version) >= LooseVersion(get_list_repo(config)[repo]):
					repo_name_ver[repo][pkg.name] = [pkg.version + '-' + pkg.release]
		prev_name = pkg.name


def pretty(d, indent=0):
   for key, value in d.items():
      print('\t' * indent + str(key))
      if isinstance(value, dict):
         pretty(value, indent+1)
      else:
         print('\t' * (indent+1) + str(value))

pretty(repo_name_ver)
#print repo_name_ver

