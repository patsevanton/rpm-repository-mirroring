# rpm-repository-mirroring - Скрипт для скачивания RPM пакетов из репозиториев, для которых нельзя сделать RPM зеркало

## Установка и запуск rpm-repository-mirroring (epel-release нужен для nginx)
```
yum install -y epel-release
yum -y install yum-plugin-copr
yum copr enable antonpatsev/rpm-repository-mirroring
yum -y install rpm-repository-mirroring
```

## Настройка rpm-repository-mirroring (пример с репозиторием grafana)
Редактируем файл `/etc/rpm-repository-mirroring.conf`
В нем все подробно описано.

### Grafana

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

Например, если мы хотим скачивать только rpm пакеты из репозитория grafana, то конфиг будет такой:
```
# Директория, в которых будут создаваться rpm репозитории
DOWNLOAD_DIR=/var/www/repos

# репозитории, rpm которых будут скачиваться начиная с определенной версии, указаной в значении
REPOS={"grafana":"6.5.3"}
```

Запускаем скрипт
```
rpm-repository-mirroring
```

После запуска скрипта в директории /var/www/repos должна появится директория grafana, содержащая rpm репозиторий.

### Kubernetes

Создадим /etc/yum.repos.d/kubernetes.repo со следующим содержимым:

```
[kubernetes]
name=Kubernetes
baseurl=https://packages.cloud.google.com/yum/repos/kubernetes-el7-x86_64
enabled=1
gpgcheck=1
repo_gpgcheck=1
gpgkey=https://packages.cloud.google.com/yum/doc/yum-key.gpg https://packages.cloud.google.com/yum/doc/rpm-package-key.gpg
```

Если мы хотим скачивать только rpm пакеты из репозитория kubernetes, то конфиг будет такой:
```
# Директория, в которых будут создаваться rpm репозитории
DOWNLOAD_DIR=/var/www/repos

# репозитории, rpm которых будут скачиваться начиная с определенной версии, указаной в значении
REPOS={"kubernetes":"1.17.6"}

# Для всех репозиторией, в которых есть rpm-пакет, совпадающий с ключом, необходимо скачать последние N версии этих rpm пакетов.
# Где N указываетя в значении.
CUT_AFTER={"rkt":2,"kubernetes-cni":2,"cri-tools":2}
```

Диаграмма для репо kubernetes и grafana
![](https://habrastorage.org/webt/wd/8f/dj/wd8fdjxo6a-j1fevwuuiz8lkp4u.png)
