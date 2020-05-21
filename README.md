# rpm-repository-mirroring

Fork from https://gist.github.com/piotr1212/9135754
RPM repository mirroring is script for RPM repository mirroring.
Required: nginx, createrepo.

After install change:
1) server_name in /etc/nginx/conf.d/nginx-rpm-repository-mirroring.conf
2) REPOS in /etc/rpm-repository-mirroring.conf
3) run rpm-repository-mirroring manual

rpm-repository-mirroring.py делает словарь где ключ является репозиторием, а значение явлется словать, у которрого ключ является название пакета, а значение является список последних доступных версий.

Для репозиториев kubernetes и grafana нужно добавить их репозитории:

```
[grafana]
name=grafana
baseurl=https://packages.grafana.com/oss/rpm
repo_gpgcheck=1
enabled=1
gpgcheck=0
gpgkey=https://packages.grafana.com/gpg.key
sslverify=1
sslcacert=/etc/pki/tls/certs/ca-bundle.crt
```

```
[kubernetes]
name=Kubernetes
baseurl=https://packages.cloud.google.com/yum/repos/kubernetes-el7-x86_64
enabled=1
gpgcheck=1
repo_gpgcheck=1
gpgkey=https://packages.cloud.google.com/yum/doc/yum-key.gpg https://packages.cloud.google.com/yum/doc/rpm-package-key.gpg
```

Диаграмма для репо kubernetes и grafana
![](https://habrastorage.org/webt/wd/8f/dj/wd8fdjxo6a-j1fevwuuiz8lkp4u.png)
