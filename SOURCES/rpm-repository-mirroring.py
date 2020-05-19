#!/usr/bin/env python

import subprocess

config = "rpm-repository-mirroring.conf"
begin_version_package_at_repo = {'kubernetes':1.15.9-0,}

def get_list_repo(config):
	with open(config) as f:
	    for line in f:
	        if "REPOS" in line:
	        	fields = line.strip().split("=")
	        	list_repo=fields[1][1:-1].split()
	        	return list_repo

def command_yum_available_package_in_repo(repo):
	return "yum -q --showduplicates --disablerepo=\* --enablerepo={0} list available".format(repo)

def command_yum_last_version_for_package(package):
	return "yum -q --showduplicates list available {0}".format(package)

def get_uniq_package_in_repo(config):
	array_uniq_package = []
	for repo in get_list_repo(config):
		process = subprocess.Popen(command_yum_available_package_in_repo(repo), shell=True, stdout=subprocess.PIPE)
		output, error = process.communicate()
		for line in output.splitlines():
			if "REPOS" not in line:
				if "Available" not in line:
					package = line.strip().split()[0].split('.')[0]
					if package not in array_uniq_package:
						array_uniq_package.append(package)
	return array_uniq_package

def get_last_version_for_package(package, begin_version_package_at_repo):
	array_last_version_package = []
	process = subprocess.Popen(command_yum_last_version_for_package(package), shell=True, stdout=subprocess.PIPE)
		output, error = process.communicate()
		for line in output.splitlines():
			print(line)


get_last_version_for_uniq_package(config)

def main(config):
	list_uniq_package = get_uniq_package_in_repo(config)
	for package in list_uniq_package:
		get_last_version_for_package(package, begin_version_package_at_repo)

