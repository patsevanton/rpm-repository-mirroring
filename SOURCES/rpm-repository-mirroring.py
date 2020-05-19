#!/usr/bin/env python

import subprocess
from pprint import pprint

path_to_storage = "/var/www/repos"
config = "rpm-repository-mirroring.conf"
begin_version_package_at_repo = {'kubernetes':'1.15.12-0','grafana':'5.4.5-1'}
last_count_version_specific_package = {'rkt':5,'kubernetes-cni':5,'cri-tools':5}

def get_list_repo(config):
	with open(config) as f:
	    for line in f:
	        if "REPOS" in line:
	        	fields = line.strip().split("=")
	        	list_repo=fields[1][1:-1].split()
	        	return list_repo

def command_yum_available_package_in_repo(repo):
	return "yum -q --showduplicates --disablerepo=\* --enablerepo={0} list available".format(repo)

def command_yum_available_version_for_package(package,count_version):
	return "yum -q --showduplicates list available {0} | tail -n {1}".format(package, count_version)

def get_dict_uniq_packages_in_repo():
	dict_uniq_packages_in_repo = {}
	for repo in list_repo:
		list_uniq_packages_custom_repo = []
		process = subprocess.Popen(command_yum_available_package_in_repo(repo), shell=True, stdout=subprocess.PIPE)
		output, error = process.communicate()
		for line in output.splitlines():
			if "REPOS" not in line:
				if "Available" not in line:
					package = line.strip().split()[0].split('.')[0]
					if package not in list_uniq_packages_custom_repo:
						list_uniq_packages_custom_repo.append(package)
		if repo not in dict_uniq_packages_in_repo:
			dict_uniq_packages_in_repo[repo] = list_uniq_packages_custom_repo
	return dict_uniq_packages_in_repo

# def get_dict_version_for_package(package, begin_version_package_at_repo,last_count_version_specific_package):
def dict_version_of_package_uniq_packages_in_repo(dict_uniq_packages_in_repo):
	for repo, list_uniq_packages in dict_uniq_packages_in_repo.iteritems():
		for package,count_version in last_count_version_specific_package.iteritems():
			if package in list_uniq_packages:
				process = subprocess.Popen(command_yum_available_version_for_package(package,count_version), shell=True, stdout=subprocess.PIPE)
				output, error = process.communicate()
				print(output)
				for line in output.splitlines():
					if "REPOS" not in line:
						if "Available" not in line:
							package = line.strip().split()[0].split('.')[0]
							version = line.strip().split()[1]
							print("{0}-{1}".format(package, version))


def check_package_in_storage(package_with_version):
	path_to_storage


# pprint(list_repo)
# pprint(dict_uniq_packages_in_repo)
# get_dict_version_for_package('kubelet')

# def main(config):
# 	list_uniq_package = get_uniq_package_in_repo(config)
# 	for package in list_uniq_package:
# 		get_last_version_for_package(package, begin_version_package_at_repo)

list_repo = get_list_repo(config)
dict_uniq_packages_in_repo = get_dict_uniq_packages_in_repo()
# print(dict_uniq_packages_in_repo)
# dict_version_of_package_uniq_packages_in_repo = 
dict_version_of_package_uniq_packages_in_repo(dict_uniq_packages_in_repo)