# rpm-repository-mirroring

Fork from https://gist.github.com/piotr1212/9135754
RPM repository mirroring is script for RPM repository mirroring.
Required: nginx, createrepo.

After install change:
1) server_name in /etc/nginx/conf.d/nginx-rpm-repository-mirroring.conf
2) REPOS in /etc/rpm-repository-mirroring.conf
3) run rpm-repository-mirroring manual
