%global _enable_debug_package 0
%global debug_package %{nil}
%global __os_install_post /usr/lib/rpm/brp-compress %{nil}

Name:           Atlas
Version:        2.2.1
Release:        3%{?dist}
Summary:        A Proxy for the MySQL Client/Server protocol

License:        GPL
URL:            https://github.com/Qihoo360/Atlas

Source0:        %{name}-%{version}.tar.gz
Source1:        mysql-proxy.cnf
Source2:        mysql-proxy.service
Source3:        mysql-proxy.sysconfig

PATCH0:         mysql-5.7.patch

BuildRequires:  flex
BuildRequires:  libtool
BuildRequires:  glib2-devel >= 2.50.0
BuildRequires:  jemalloc-devel
BuildRequires:  libevent-devel
BuildRequires:  lua-devel >= 5.1
BuildRequires:  mysql-devel
BuildRequires:  openssl-devel
BuildRequires:  pkgconfig

Requires:       openssl
Requires:       jemalloc
Requires:       mysql
Requires:       lua >= 5.1
Requires:       glib2 >= 2.50.0


Conflicts:      mysql-proxy
ExcludeArch:    x86

%description
Atlas is a MySQL protocol-based database middleware project developed 
and maintained by infrastructure team of  the Web platform  Department 
in QIHU 360 SOFTWARE CO. LIMITED(NYSE:QIHU). It fixed lots of bugs and 
added lot of new functions on the basis of MySQL-Proxy 0.8.2. 
Currently the project has been widely applied in QIHU, 
many MySQL business has connected to the Atlas platform. 
The number of read and write requests forwarded by Atlas has reached billions.

%package devel
Summary:    Development files for Atlas
Requires:   atlas-mysql-proxy = %{version}-%{release}

%description devel
Development files for Atlas


%prep
%setup -q
%patch0 -p1

%build
%configure -with-lua CFLAGS="$CFLAGS -DHAVE_LUA_H" LDFLAGS="$LDFLAGS -lm -ldl -lcrypto -ljemalloc" 
make %{?_smp_mflags}


%install
%{__make} DESTDIR=%{buildroot} install
install -d -m 0755 %{buildroot}%{_sysconfdir}/mysql-proxy
install -D -p -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/mysql-proxy/mysql-proxy.cnf
install -D -p -m 0644 %{SOURCE2} %{buildroot}%{_unitdir}/mysql-proxy.service
install -d -m 0755 %{buildroot}%{_sysconfdir}/sysconfig
install -D -p -m 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/sysconfig/mysql-proxy
install -d -m 0755 %{buildroot}%{_localstatedir}/log/mysql-proxy
#ln -sf %{_libdir}/mysql-proxy %{buildroot}/usr/lib/mysql-proxy

%clean
rm -rf %{buildroot}%

%pre
getent group  mysql >/dev/null || groupadd -g 27 -o -r mysql
getent passwd mysql >/dev/null || useradd -u 27 -M -N -o -r -g mysql -s /bin/bash -d /var/lib/mysql mysql

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun %{name}.service


%files
%defattr(-,root,root,-)
%{_bindir}/mysql-proxy
%{_bindir}/encrypt
%{_bindir}/mysql-binlog-dump
%{_bindir}/mysql-myisam-dump
%exclude %{_bindir}/mysql-proxyd
%config(noreplace) %{_sysconfdir}/mysql-proxy/mysql-proxy.cnf
%config(noreplace) %{_sysconfdir}/sysconfig/mysql-proxy
%{_unitdir}/mysql-proxy.service
%dir %attr(0755,mysql,mysql) %{_localstatedir}/log/mysql-proxy
%dir %{_libdir}/mysql-proxy
%{_libdir}/mysql-proxy/lua/*
%{_libdir}/mysql-proxy/plugins/*
%{_libdir}/libmysql-*
%{_libdir}/libsql-*
%doc examples/

%files devel
%defattr(-,root,root,-)
%{_includedir}/*.h
%{_libdir}/pkgconfig/mysql-chassis.pc
%{_libdir}/pkgconfig/mysql-proxy.pc

%changelog
* Tue Nov 07 2017 Allan Hung <hung.allan@gmail.com> - 2.2.1-3
- First Release
