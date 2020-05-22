#!/usr/bin/env python

import sys
import yum

config = "rpm-repository-mirroring.conf"
name_count = {'rkt':5,'kubernetes-cni':5,'cri-tools':5}


def get_list_repo(config):
	with open(config) as f:
		for line in f:
			if "REPOS" in line:
				fields = line.strip().split("=")
				list_repo=fields[1][1:-1].split()
				return list_repo

repo_name_ver = {}
for repo in get_list_repo(config):
	yb = yum.YumBase()
	if not yb.setCacheDir(force=True, reuse=False):
		print >>sys.stderr, "Can't create a tmp. cachedir. "
		sys.exit(1)

	yb.repos.disableRepo('*')
	yb.repos.enableRepo(repo)
	repo_name_ver[repo] = {}
	for pkg in sorted(yb.pkgSack.returnPackages()):
		if pkg.name in name_count:
#			i = 0
			for num in range(0, int(name_count[pkg.name])):
#				print pkg
#				i += 1
#				print i
				if pkg.name in repo_name_ver[repo]:
					repo_name_ver[repo][pkg.name].append(pkg.version + '-' + pkg.release)
				else:
					repo_name_ver[repo][pkg.name] = [pkg.version +  '-' + pkg.release]
				break
		else:
			if pkg.name in repo_name_ver[repo]:
				repo_name_ver[repo][pkg.name].append(pkg.version + '-' + pkg.release)
			else:
				repo_name_ver[repo][pkg.name] = [pkg.version + '-' + pkg.release]

def pretty(d, indent=0):
   for key, value in d.items():
      print('\t' * indent + str(key))
      if isinstance(value, dict):
         pretty(value, indent+1)
      else:
         print('\t' * (indent+1) + str(value))

pretty(repo_name_ver)
#print repo_name_ver
