#!/usr/bin/env python

import json
import os
import shutil
import sys
import yum
from distutils.version import LooseVersion

config = "rpm-repository-mirroring.conf"

def get_dict_repo(config):
	with open(config, "r") as f:
		for line in f:
			if "REPOS" in line:
				fields = line.strip().split("=")
				dict_repo=json.loads(fields[1])
				return dict_repo

def get_dict_cut(config):
	with open(config, "r") as f:
		for line in f:
			if "CUT_AFTER" in line:
				fields = line.strip().split("=")
				name_count=json.loads(fields[1])
				return name_count

def get_download_dir(config):
	with open(config) as f:
		for line in f:
			if "DOWNLOAD_DIR" in line:
				fields = line.strip().split("=")
				dir=fields[1]
				return dir

def save_po(pkg):
	remote = pkg.returnSimple('relativepath')
	local = os.path.basename(remote)
	local = os.path.join(download_dir, local)
	pkg.localpath = local
	path = pkg.repo.getPackage(pkg, copy_local=1, cache = False)
	if not os.path.exists(local) or not os.path.samefile(path, local):
		shutil.copy2(path, local)	

name_count = get_dict_cut(config)
repo_name_ver = {}
repo_ver = get_dict_repo(config)
download_dir = get_download_dir(config)

for repo in repo_ver:
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

		pkg.repo.copy_local = True
		pkg.repo.cache = 0

		if pkg.name in name_count:
			if name_count[pkg.name] > 0:
				if pkg.name not in repo_name_ver[repo]:
					repo_name_ver[repo][pkg.name] = []
				repo_name_ver[repo][pkg.name].append(pkg.version + '-' + pkg.release)
				name_count[pkg.name] -= 1
				save_po(pkg)
			else:
				name_count.pop(pkg.name, None)
				ignore = True
		else:
			if LooseVersion(pkg.version) >= LooseVersion(repo_ver[repo]):
				if pkg.name not in repo_name_ver[repo]:
					repo_name_ver[repo][pkg.name] = []
				repo_name_ver[repo][pkg.name].append(pkg.version + '-' + pkg.release)
				save_po(pkg)
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
