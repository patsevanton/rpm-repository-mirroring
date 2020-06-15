# rpm-repository-mirroring - Скрипт для скачивания RPM пакетов из репозиториев, для которых нельзя сделать RPM зеркало

## Установка или создание репозиториев в директории yum.repos.d, откуда нужно скачивать RPM пакеты.

Для примера будем использовать репозиторий Grafana.
Создадим /etc/yum.repos.d/grafana.repo со следующим содержимым:
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

## Установка и запуск rpm-repository-mirroring
```
yum -y install yum-plugin-copr
yum copr enable antonpatsev/rpm-repository-mirroring
yum -y install rpm-repository-mirroring
Run rpm-repository-mirroring in cron OR run rpm-repository-mirroring manual
```

## После запуска скрипта в директории /var/www/repos должна появится директория grafana, содержащая rpm репозиторий.

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
