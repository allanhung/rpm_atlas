RPMBUILD for Atlas
=========================

Atlas is a MySQL protocol-based database middleware project developed and maintained by infrastructure team of the Web platform Department in QIHU 360 SOFTWARE CO. LIMITED(NYSE:QIHU). It fixed lots of bugs and added lot of new functions on the basis of MySQL-Proxy 0.8.2. Currently the project has been widely applied in QIHU, many MySQL business has connected to the Atlas platform. The number of read and write requests forwarded by Atlas has reached billions.

How to Build
=========
    git clone https://github.com/allanhung/rpm_atlas
    cd rpm_atlas
    download mysql 5.7 rpm from website and put in scripts dir
    docker run --name=atlas_build --rm -ti -v $(pwd)/rpms:/root/rpmbuild/RPMS/x86_64 -v $(pwd)/rpms:/root/rpmbuild/RPMS/noarch -v $(pwd)/scripts:/usr/local/src/build centos:7 /bin/bash -c "/usr/local/src/build/build_atlas.sh"

# check
    docker run --name=atlas_check --rm -ti -v $(pwd)/rpms:/root/rpmbuild/RPMS centos:6 /bin/bash -c "yum localinstall -y /root/rpmbuild/RPMS/Atlas-*.rpm"

# Install
    yum install rpms/Atlas-*.rpm

# Reference #

  * [Atlas](https://github.com/Qihoo360/Atlas)
