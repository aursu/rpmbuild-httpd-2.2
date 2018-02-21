%define contentdir /var/www
%define mmn 20051115
%if 0%{?fedora}
%define mmnisa %{mmn}%{__isa_name}%{__isa_bits}
%else
%define mmnisa %{mmn}-%{__isa_name}-%{__isa_bits}
%endif

%if 0%{?rhel} >= 7
%define vstring %(source /etc/os-release; echo ${REDHAT_SUPPORT_PRODUCT})
%else
%define vstring centos
%endif

%define aprver 1
%define apuver 1

%global rpmrel 5

Summary: Apache HTTP Server
Name: httpd
Version: 2.2.34
Release: %{rpmrel}%{?dist}
URL: http://httpd.apache.org/
Source0: http://www.apache.org/dist/httpd/httpd-%{version}.tar.bz2
Source1: index.html
Source3: httpd.logrotate
Source5: httpd.sysconf
Source10: httpd.conf
Source11: ssl.conf

# files for virtual hosts and cluster specific settings
Source17: httpd.init

# Documentation
Source31: httpd.mpm.xml
Source33: README.confd

Source40: mod_remoteip.c
Source41: remoteip.conf

Source42: info.conf

# build/scripts patches
Patch2: httpd-2.1.10-apxs.patch
Patch5: httpd-2.2.22-layout.patch

# compile apache statically with apr and apr-util
Patch55: httpd-2.2.26-static.patch

# compile apache with bundled APR and APR-Util
Patch56: httpd-2.2.26-apr.patch

# Set POSIX Semaphores as default
Patch57: httpd-2.2.26-sem.patch

# Add mod_remoteip to httpd
Patch58: httpd-2.2.25-mod-remoteip.patch

# Decreased log level of several messages
Patch59: httpd-2.2.26-logging.patch

# Try to add OpenSSL 1.1.0 support
Patch60: httpd-2.2.34-openssl-1.1.0.patch

# Add DUMP_CONFIG into info_module
Patch61: httpd-2.2.34-dump-config.patch

# Disable Handler server-info
Patch62: httpd-2.2.34-no-server-info.patch

# mod_substitute from 2.4.29
Patch63: httpd-2.2.34-regsub_core-2.4.29.patch
Patch64: httpd-2.2.34-mod_substitute-2.4.29.patch

# Bug fixes
Patch130: httpd-2.2.15-r1667676.patch

# Security fixes
Patch227: CVE-2017-9798-patch-2.2.patch

License: ASL 2.0
Group: System Environment/Daemons
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: autoconf, perl, pkgconfig, findutils, xmlto, libtool
BuildRequires: zlib-devel
Obsoletes: httpd-suexec
Provides: webserver
Provides: httpd-mmn = %{mmn}, httpd-mmn = %{mmnisa}
Requires: httpd-tools = %{version}-%{release}
Requires: /etc/mime.types, system-logos >= 7.92.1-1
#Requires: apr >= 1.2.0, apr-util >= 1.2.0
Requires(pre): /usr/sbin/groupadd /usr/sbin/usermod

%description
The Apache HTTP Server is a powerful, efficient, and extensible
web server.

%package devel
Group: Development/Libraries
Summary: Development interfaces for the Apache HTTP server
Obsoletes: secureweb-devel, apache-devel, stronghold-apache-devel
#Requires: apr-devel, apr-util-devel, pkgconfig
Requires: pkgconfig
Requires: httpd = %{version}-%{release}
Requires: httpd-apr = %{version}-%{release}
Requires: httpd-apr-util = %{version}-%{release}
BuildConflicts: apr-devel
BuildConflicts: apr-util-devel

%description devel
The httpd-devel package contains the APXS binary and other files
that you need to build Dynamic Shared Objects (DSOs) for the
Apache HTTP Server.

If you are installing the Apache HTTP server and you want to be
able to compile or develop additional modules for Apache, you need
to install this package.

%package tools
Group: System Environment/Daemons
Summary: Tools for use with the Apache HTTP Server

%description tools
The httpd-tools package contains tools which can be used with
the Apache HTTP Server.

%package apr
Group: System Environment/Libraries
Summary: Apache Portable Runtime library
Requires: httpd = %{version}-%{release}
Conflicts: apr, apr-devel

%description apr
The mission of the Apache Portable Runtime (APR) is to provide a
free library of C data structures and routines, forming a system
portability layer to as many operating systems as possible,
including Unices, MS Win32, BeOS and OS/2.

%package apr-util
Group: System Environment/Libraries
Summary: Apache Portable Runtime Utility library
BuildRequires: expat-devel
Requires: httpd = %{version}-%{release}
Requires: httpd-apr = %{version}-%{release}
Conflicts: apr-util, apr-util-devel

%description apr-util
The mission of the Apache Portable Runtime (APR) is to provide a
free library of C data structures and routines.  This library
contains additional utility interfaces for APR; including support
for XML, LDAP, database interfaces, URI parsing and more.

%package -n mod_ssl
Group: System Environment/Daemons
Summary: SSL/TLS module for the Apache HTTP Server
Epoch: 1
BuildRequires: openssl-devel >= 1.0.1e
Requires(pre): httpd
Requires: httpd = 0:%{version}-%{release}, httpd-mmn = %{mmnisa}, openssl >= 1.0.1e
Obsoletes: stronghold-mod_ssl

%description -n mod_ssl
The mod_ssl module provides strong cryptography for the Apache Web
server via the Secure Sockets Layer (SSL) and Transport Layer
Security (TLS) protocols.

%package -n mod_remoteip
Group: System Environment/Daemons
Summary: Replaces the original client with the useragent IP address
Epoch: 1
Requires(pre): httpd
Requires: httpd = 0:%{version}-%{release}, httpd-mmn = %{mmnisa}

%description -n mod_remoteip
This module is used to treat the useragent which initiated the request as
the originating useragent as identified by httpd for the purposes of
authorization and logging, even where that useragent is behind a load
balancer, front end server, or proxy server.

%package -n mod_info
Group: System Environment/Daemons
Summary: Provides a comprehensive overview of the server configuration
Epoch: 1
Requires(pre): httpd
Requires: httpd = 0:%{version}-%{release}, httpd-mmn = %{mmnisa}

%description -n mod_info
Provides a comprehensive overview of the server configuration
If the config define -DDUMP_CONFIG is set, mod_info will dump the
pre-parsed configuration to stdout during server startup.
Pre-parsed means that directives like <IfDefine> and <IfModule> are
evaluated and environment variables are replaced. However it does not
represent the final state of the configuration. In particular, it does
not represent the merging or overriding that may happen for repeated
directives.

%prep
%setup -q
%patch2 -p1 -b .apxs
%patch5 -p1 -b .layout

%patch55 -p1 -b .static
%patch56 -p1 -b .apr
%patch57 -p1 -b .sem
%patch58 -p1 -b .rip
%if 0%{?fedora} >= 26
%patch60 -p1
%endif
%patch61 -p1
%patch62 -p1
%patch63 -p1
%patch64 -p1

# bug fixes
%patch130 -p1 -b .r1667676

# security fixes
%patch227 -p1 -b .cve9798

cp %{SOURCE40} modules/metadata/

# Safety check: prevent build if defined MMN does not equal upstream MMN.
vmmn=`echo MODULE_MAGIC_NUMBER_MAJOR | cpp -include include/ap_mmn.h |
sed -n '/^2/p'`
if test "x${vmmn}" != "x%{mmn}"; then
   : Error: Upstream MMN is now ${vmmn}, packaged MMN is %{mmn}
   : Update the mmn macro and rebuild.
   exit 1
fi

: Building with MMN %{mmn}, MMN-ISA %{mmnisa} and vendor string '%{vstring}'

%build
# reconfigure to enable wired minds module
./buildconf --reconf

# regenerate configure scripts
autoheader && autoconf || exit 1

# Before configure; fix location of build dir in generated apxs
%{__perl} -pi -e "s:\@exp_installbuilddir\@:%{_libdir}/httpd/build:g" \
    support/apxs.in

export CFLAGS=$RPM_OPT_FLAGS
export LDFLAGS="-Wl,-z,relro,-z,now"

# Hard-code path to links to avoid unnecessary builddep
export LYNX_PATH=/usr/bin/links

function mpmbuild()
{
mpm=$1; shift

# Build the daemon
mkdir $mpm; pushd $mpm
../configure \
    --prefix=%{_sysconfdir}/httpd \
    --exec-prefix=%{_prefix} \
    --bindir=%{_bindir} \
    --sbindir=%{_sbindir} \
    --mandir=%{_mandir} \
    --libdir=%{_libdir} \
    --sysconfdir=%{_sysconfdir}/httpd/conf \
    --includedir=%{_includedir}/httpd \
    --libexecdir=%{_libdir}/httpd/modules \
    --datadir=%{contentdir} \
    --with-installbuilddir=%{_libdir}/httpd/build \
    --with-mpm=$mpm \
    --with-pcre \
    $*

make %{?_smp_mflags}
popd
}

# Build everything and the kitchen sink with the prefork build
mpmbuild prefork \
    --enable-so \
    --enable-vhost-alias --with-ssl --enable-ssl=shared \
    --enable-expires --enable-speling --enable-deflate \
    --enable-headers --disable-status --enable-proxy \
    --enable-proxy-connect --enable-proxy-ftp --enable-proxy-http \
    --enable-proxy-scgi --enable-proxy-ajp --enable-proxy-balancer \
    --enable-rewrite \
    --enable-substitute=shared \
    --enable-remoteip=shared \
    --enable-info=shared

%install
rm -rf $RPM_BUILD_ROOT

pushd prefork
make DESTDIR=$RPM_BUILD_ROOT install
popd

# install conf file/directory
mkdir $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d
install -m 644 $RPM_SOURCE_DIR/README.confd \
    $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/README

install -m 644 -p $RPM_SOURCE_DIR/ssl.conf \
    $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/05-ssl.conf
install -m 644 -p $RPM_SOURCE_DIR/remoteip.conf \
    $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/04-remoteip.conf
install -m 644 -p $RPM_SOURCE_DIR/info.conf \
    $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/09-info.conf

rm $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf/*.conf
install -m 644 -p $RPM_SOURCE_DIR/httpd.conf \
   $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf/httpd.conf

mkdir $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
install -m 644 -p $RPM_SOURCE_DIR/httpd.sysconf \
   $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/httpd

# create a prototype session cache
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/cache/mod_ssl
touch $RPM_BUILD_ROOT%{_localstatedir}/cache/mod_ssl/scache.{dir,pag,sem}

# create cache root
mkdir $RPM_BUILD_ROOT%{_localstatedir}/cache/mod_proxy

# move utilities to /usr/bin
mv $RPM_BUILD_ROOT%{_sbindir}/{ab,htdbm,logresolve,htpasswd,htdigest} \
   $RPM_BUILD_ROOT%{_bindir}

# move sslpass
mkdir -p $RPM_BUILD_ROOT/%{_libexecdir}

# Make the MMN accessible to module packages
echo %{mmnisa} > $RPM_BUILD_ROOT%{_includedir}/httpd/.mmn
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/rpm
cat > $RPM_BUILD_ROOT%{_sysconfdir}/rpm/macros.httpd <<EOF
%%_httpd_mmn %{mmnisa}
%%_httpd_apxs %%{_sbindir}/apxs
%%_httpd_modconfdir %%{_sysconfdir}/httpd/conf.d
%%_httpd_confdir %%{_sysconfdir}/httpd/conf.d
%%_httpd_contentdir %{contentdir}
%%_httpd_moddir %%{_libdir}/httpd/modules
EOF

# docroot
mkdir $RPM_BUILD_ROOT%{contentdir}/html
install -m 644 -p $RPM_SOURCE_DIR/index.html \
        $RPM_BUILD_ROOT%{contentdir}/error/noindex.html

# Symlink for the powered-by-$DISTRO image:
ln -s ../../..%{_datadir}/pixmaps/poweredby.png \
        $RPM_BUILD_ROOT%{contentdir}/icons/poweredby.png

# symlinks for /etc/httpd
ln -s ../..%{_localstatedir}/log/httpd $RPM_BUILD_ROOT/etc/httpd/logs
ln -s ../..%{_localstatedir}/run/httpd $RPM_BUILD_ROOT/etc/httpd/run
ln -s ../..%{_libdir}/httpd/modules $RPM_BUILD_ROOT/etc/httpd/modules

# install log rotation stuff
mkdir -p $RPM_BUILD_ROOT/etc/logrotate.d
install -m 644 -p $RPM_SOURCE_DIR/httpd.logrotate \
    $RPM_BUILD_ROOT/etc/logrotate.d/httpd

# Make ap_config_layout.h libdir-agnostic
sed -i '/.*DEFAULT_..._LIBEXECDIR/d;/DEFAULT_..._INSTALLBUILDDIR/d' \
    $RPM_BUILD_ROOT%{_includedir}/httpd/ap_config_layout.h

# Fix path to instdso in special.mk
sed -i '/instdso/s,top_srcdir,top_builddir,' \
    $RPM_BUILD_ROOT%{_libdir}/httpd/build/special.mk

# Remove unpackaged files
rm -f $RPM_BUILD_ROOT%{_libdir}/*.exp \
      $RPM_BUILD_ROOT/etc/httpd/conf/mime.types \
      $RPM_BUILD_ROOT%{_libdir}/httpd/modules/*.exp \
      $RPM_BUILD_ROOT%{_libdir}/httpd/build/config.nice \
      $RPM_BUILD_ROOT%{_bindir}/ap?-config \
      $RPM_BUILD_ROOT%{_sbindir}/{checkgid,dbmmanage,envvars*} \
      $RPM_BUILD_ROOT%{contentdir}/htdocs/* \
      $RPM_BUILD_ROOT%{_mandir}/man1/dbmmanage.* \
      $RPM_BUILD_ROOT%{contentdir}/cgi-bin/*

rm -rf $RPM_BUILD_ROOT/etc/httpd/conf/{original,extra}

# install SYSV init stuff
mkdir -p $RPM_BUILD_ROOT/etc/rc.d/init.d
install -m755 %{SOURCE17} \
        $RPM_BUILD_ROOT/etc/rc.d/init.d/httpd

%check
# Check the built modules are all PIC
if readelf -d $RPM_BUILD_ROOT%{_libdir}/httpd/modules/*.so | grep TEXTREL; then
   : modules contain non-relocatable code
   exit 1
fi

%pre
#/usr/sbin/useradd -c "Apache" -u 48 \
#	-s /sbin/nologin -r -d %{contentdir} apache 2> /dev/null || :
# Add the "nogroup" group to be compatible with old configs
if ! grep -q ^nogroup: /etc/group; then
    /usr/sbin/groupadd -o -g 65534 nogroup
fi
/usr/bin/pkill -u nobody && /usr/sbin/usermod -u 65534 -o nobody ||
/usr/sbin/usermod -u 65534 -o nobody

%post
# Register the httpd service
/sbin/chkconfig --add httpd

%preun
if [ $1 = 0 ]; then
        /sbin/service httpd stop > /dev/null 2>&1
        /sbin/chkconfig --del httpd
fi


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)

%dir %{_sysconfdir}/httpd
%{_sysconfdir}/httpd/modules
%{_sysconfdir}/httpd/logs
%{_sysconfdir}/httpd/run
%dir %{_sysconfdir}/httpd/conf
%config(noreplace) %{_sysconfdir}/httpd/conf/httpd.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/magic
%config(noreplace) %{_sysconfdir}/logrotate.d/httpd

%dir %{_sysconfdir}/httpd/conf.d
%{_sysconfdir}/httpd/conf.d/README

%config(noreplace) %{_sysconfdir}/sysconfig/httpd
%config %{_sysconfdir}/rc.d/init.d/httpd

%{_sbindir}/ht*
%{_sbindir}/apachectl
%{_sbindir}/rotatelogs

%dir %{_libdir}/httpd
%dir %{_libdir}/httpd/modules
%{_libdir}/httpd/modules/mod*.so
%exclude %{_libdir}/httpd/modules/mod_ssl.so

%dir %{contentdir}
%dir %{contentdir}/cgi-bin
%dir %{contentdir}/html
%dir %{contentdir}/icons
%dir %{contentdir}/error
%dir %{contentdir}/error/include
%{contentdir}/icons/*
%{contentdir}/error/README
%{contentdir}/error/noindex.html
%config %{contentdir}/error/*.var
%config %{contentdir}/error/include/*.html

%attr(0710,root,nogroup) %dir %{_localstatedir}/run/httpd
%attr(0700,root,root) %dir %{_localstatedir}/log/httpd
%attr(0700,nobody,nogroup) %dir %{_localstatedir}/cache/mod_proxy

%exclude %{_mandir}/man1
%exclude %{_mandir}/man8
%exclude %{contentdir}/manual

%files tools
%defattr(-,root,root)
%{_bindir}/*
%doc LICENSE NOTICE

%files apr
%defattr(-,root,root,-)
%{_libdir}/libapr-%{aprver}.so.*

%{_bindir}/apr-%{aprver}-config
%{_libdir}/libapr-%{aprver}.*a
%{_libdir}/libapr-%{aprver}.so
%{_libdir}/pkgconfig/apr-%{aprver}.pc
%dir %{_libdir}/apr-%{aprver}
%dir %{_libdir}/apr-%{aprver}/build
%{_libdir}/apr-%{aprver}/build/*
%dir %{_includedir}/apr-%{aprver}
%{_includedir}/apr-%{aprver}/*.h

%files apr-util
%defattr(-,root,root,-)
%{_libdir}/libaprutil-%{apuver}.so.*
#%dir %{_libdir}/apr-util-%{apuver}

%{_bindir}/apu-%{apuver}-config
#%{_libdir}/apr-util-%{apuver}/*
%{_libdir}/libaprutil-%{apuver}.*a
%{_libdir}/libaprutil-%{apuver}.so
%{_libdir}/pkgconfig/apr-util-%{apuver}.pc


%files -n mod_ssl
%defattr(-,root,root)
%{_libdir}/httpd/modules/mod_ssl.so
%config(noreplace) %{_sysconfdir}/httpd/conf.d/05-ssl.conf
%attr(0700,nobody,root) %dir %{_localstatedir}/cache/mod_ssl
%attr(0600,nobody,root) %ghost %{_localstatedir}/cache/mod_ssl/scache.dir
%attr(0600,nobody,root) %ghost %{_localstatedir}/cache/mod_ssl/scache.pag
%attr(0600,nobody,root) %ghost %{_localstatedir}/cache/mod_ssl/scache.sem

%files devel
%defattr(-,root,root)
%{_includedir}/httpd
%{_sbindir}/apxs
%dir %{_libdir}/httpd/build
%{_libdir}/httpd/build/*.mk
%{_libdir}/httpd/build/*.sh
%{_sysconfdir}/rpm/macros.httpd

%files -n mod_remoteip
%defattr(-,root,root)
%{_libdir}/httpd/modules/mod_remoteip.so
%config(noreplace) %{_sysconfdir}/httpd/conf.d/04-remoteip.conf

%files -n mod_info
%defattr(-,root,root)
%{_libdir}/httpd/modules/mod_info.so
%config(noreplace) %{_sysconfdir}/httpd/conf.d/09-info.conf

%changelog
* Wed Feb 07 2018 Alexander Ursu <alexander.ursu@gmail.com> - 2.2.34-5
- ported variable length buffer library from 2.4
- ported mod_substitute from 2.4.29

* Tue Jan 16 2018 Alexander Ursu <alexander.ursu@gmail.com> - 2.2.34-4
- Resolves: #1493061 - CVE-2017-9798 httpd: various flaws

* Sat Nov 18 2017 Alexander Ursu <alexander.ursu@gmail.com> - 2.2.34-2
- added adoptation patch for OpenSSL 1.1.0
- added handler for -DDUMP_CONFIG CLI option (provided by
  mod_info)

* Thu Nov 09 2017 Alexander Ursu <alexander.ursu@gmail.com> - 2.2.34-1
- update to 2.2.34

* Mon Sep 18 2017 Alexander Ursu <alexander.ursu@gmail.com> - 2.2.26-11
- added logging adjustments for some type of error messages

* Mon Mar 16 2015 Alexander Ursu <alexander.ursu@gmail.com> - 2.2.26-8
- added old custom path for libmysqlclient.so library

* Thu Mar 12 2015 Alexander Ursu <alexander.ursu@gmail.com> - 2.2.26-7
- added nobody user modification
- modified startup scripts (added stack size rlimit setting)

* Tue Oct  7 2014 Alexander Ursu <alexander.ursu@gmail.com> - 2.2.26-6
- add mod_remoteip

* Thu Jul  3 2014 Alexander Ursu <alexander.ursu@gmail.com> - 2.2.26-5
- switch to bundled versions of APR and Ap-Util libs
- compiled httpd statically with APR and Apr-Util libs
- all Apr stuff moved to separate packages httpd-apr and httpd-
  apr-util; added related conflicts

* Thu Mar 20 2014 Alexander Ursu <alexander.ursu@gmail.com> - 2.2.26-3
- switch mod_substitute as shared and enabled by default

* Wed Feb 26 2014 Alexander Ursu <alexander.ursu@gmail.com> - 2.2.26-2
- switch to nobody/nogroup
