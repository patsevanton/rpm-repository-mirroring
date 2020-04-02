#!/bin/bash

# based on: http://blog.kagesenshi.org/2007/06/fedora-repository-mirroring-script.html

yum -y makecache fast

source /etc/rpm-repository-mirroring.conf

downrepo () {
    cd $MROOT
    echo "Sychronizing Repositories"
    reposync --download-metadata --cachedir=/var/cache/rpm-repository-mirroring --plugins --repoid=$1 --arch=$2 --allow-path-traversal
    STAT=$?
    echo $1
    if [[ $1 == *"kubernetes"* ]]; then
        pwd
        cd ../pool
        cp -a *.rpm $MROOT/kubernetes
        change-name-rpm-kubernetes -path $MROOT/kubernetes
        cd $MROOT
    fi
    if [ "$STAT" == "0" ];then
        cd $1
        repomanage --keep=5 --old . |  xargs rm -rf
        echo "Recreating repodata"
        if [ -f comps.xml ]; then
                echo "comps.xml found"
                createrepo --workers 2 -g comps.xml .
        else
                echo "comps.xml not found, creating without groups"
            createrepo .
        fi

        if [ -f *-updateinfo.xml.gz ]; then
                zcat *-updateinfo.xml.gz > updateinfo.xml
                modifyrepo updateinfo.xml ./repodata/
                rm *-updateinfo.xml.gz
        fi
    fi
    cd $MROOT
}

for REPO in $REPOS;do
  downrepo $REPO $ARCH
done
