#Module-Specific definitions
%define mod_name mod_ldap_userdir
%define mod_conf A37_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Look up user home directories (for /~user URLs) from an LDAP directory
Name:		apache-%{mod_name}
Version:	1.1.10
Release:	%mkrel 3
Group:		System/Servers
License:	GPL
URL:		http://horde.net/~jwm/software/mod_ldap_userdir/
Source0:	http://horde.net/~jwm/software/mod_ldap_userdir/%{mod_name}-%{version}.tar.bz2
Source1:	%{mod_conf}.bz2
Patch0:		mod_ldap_userdir-anonbind.diff
BuildRequires:	openssl-devel
BuildRequires:	openldap-devel
Requires:	openldap
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= 2.2.0
Requires(pre):	apache-mpm-prefork >= 2.2.0
Requires:	apache-conf >= 2.2.0
Requires:	apache-mpm-prefork >= 2.2.0
BuildRequires:	apache-devel >= 2.2.0
BuildRequires:	file
Conflicts:	apache-mod_userdir
Epoch:		1
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
mod_ldap_userdir is a module that enables the Apache web server to
look up user home directories (for /~user URLs) from an LDAP
directory.

%prep

%setup -q -n %{mod_name}-%{version}
%patch0 -p0 -b .anonbind

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

%build

%configure2_5x \
    --with-apxs=%{_sbindir}/apxs \
    --with-tls

#%%make

%{_sbindir}/apxs -DTLS=1 -L%{_libdir} -lldap -llber -c mod_ldap_userdir.c

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d

install -m0755 .libs/*.so %{buildroot}%{_libdir}/apache-extramodules/
bzcat %{SOURCE1} > %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

install -d %{buildroot}%{_var}/www/html/addon-modules
ln -s ../../../..%{_docdir}/%{name}-%{version} %{buildroot}%{_var}/www/html/addon-modules/%{name}-%{version}

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f %{_var}/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart 1>&2
    fi
fi

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc DIRECTIVES README posixAccount-objectclass user-ldif
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}
%{_var}/www/html/addon-modules/*

