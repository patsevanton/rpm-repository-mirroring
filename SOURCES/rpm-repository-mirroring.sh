#!/bin/bash

# based on: http://blog.kagesenshi.org/2007/06/fedora-repository-mirroring-script.html

yum -y makecache

source /etc/rpm-repository-mirroring.conf

downrepo () {
    cd $MROOT
    echo "Sychronizing Repositories"
    reposync --download-metadata --gpgcheck --plugins --repoid=$1 --arch=$2 --newest-only -t /tmp/reposync-cache
    STAT=$?
    if [ "$STAT" == "0" ];then
        cd $1
        #echo "Cleaning old packages"
        # dont delete old kernels
        #repomanage --old . | grep -v 'kernel\-' | xargs rm -rf
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
