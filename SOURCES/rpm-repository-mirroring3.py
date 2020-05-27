#!/usr/bin/env python

import json
import sys
import yum
from distutils.version import LooseVersion
from pprint import pprint

config = "rpm-repository-mirroring.conf"


def get_dir_to_download(config):
	with open(config) as f:
		for line in f:
			if "DESTDIR" in line:
				fields = line.strip().split("=")
				dir_to_download=fields[1][1:-1].split()
				return dir_to_download


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

def get_dict_of_list_package_for_download(dict):
	dict_of_list_package_for_download = {}
	for repo, int_dict in dict.items():
		list_package_for_download = []
		for package, list_version in int_dict.items():
			for version in list_version:
				list_package_for_download.append(package + '-' +  version)
		dict_of_list_package_for_download[repo] = list_package_for_download
	return dict_of_list_package_for_download


def download_rpm_to_custom_dir(repo_name_ver):
	dict_of_list_package_for_download = get_dict_of_list_package_for_download(repo_name_ver)
	for repo in dict_of_list_package_for_download:
		yb = yum.YumBase()
		yb.downloadPkgs(dict_of_list_package_for_download[repo])



#pretty(repo_name_ver)


#print repo_name_ver
download_rpm_to_custom_dir(repo_name_ver)
