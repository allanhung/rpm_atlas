export RPMBUILDROOT=/root/rpmbuild

yum -y install epel-release
yum -y install yum-utils rpm-build rpmdevtools make patch git

mkdir -p $RPMBUILDROOT/SOURCES && mkdir -p $RPMBUILDROOT/SPECS && mkdir -p $RPMBUILDROOT/SRPMS
# fix rpm marcos
sed -i -e "s#.centos##g" /etc/rpm/macros.dist

# mysql-proxy
git clone https://github.com/Qihoo360/Atlas Atlas-2.2.1
tar -zcf $RPMBUILDROOT/SOURCES/Atlas-2.2.1.tar.gz Atlas-2.2.1
rpm -i /usr/local/src/build/mysql-community-common-* /usr/local/src/build/mysql-community-libs-* /usr/local/src/build/mysql-community-devel-*
/bin/cp -f /usr/local/src/build/Atlas.spec $RPMBUILDROOT/SPECS/
/bin/cp -f /usr/local/src/build/mysql-5.7.patch $RPMBUILDROOT/SOURCES/
/bin/cp -f /usr/local/src/build/mysql-proxy.service $RPMBUILDROOT/SOURCES/
/bin/cp -f /usr/local/src/build/mysql-proxy.sysconfig $RPMBUILDROOT/SOURCES/
/bin/cp -f /usr/local/src/build/mysql-proxy.cnf $RPMBUILDROOT/SOURCES/
yum-builddep -y $RPMBUILDROOT/SPECS/Atlas.spec
rpmbuild -bb $RPMBUILDROOT/SPECS/Atlas.spec
