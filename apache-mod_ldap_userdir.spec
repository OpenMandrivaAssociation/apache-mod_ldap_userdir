#Module-Specific definitions
%define mod_name mod_ldap_userdir
%define mod_conf A37_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Look up user home directories (for /~user URLs) from an LDAP directory
Name:		apache-%{mod_name}
Version:	1.1.18
Release:	5
Group:		System/Servers
License:	GPL
URL:		https://horde.net/~jwm/software/mod_ldap_userdir/
Source0:	http://horde.net/~jwm/software/mod_ldap_userdir/%{mod_name}-%{version}.tar.gz
Source1:	%{mod_conf}
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

%description
mod_ldap_userdir is a module that enables the Apache web server to look up user
home directories (for /~user URLs) from an LDAP directory.

%prep

%setup -q -n %{mod_name}-%{version}

cp %{SOURCE1} %{mod_conf}

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

%build

%configure2_5x --localstatedir=/var/lib \
    --with-apxs=%{_bindir}/apxs \
    --with-tls

#%%make

%{_bindir}/apxs -DTLS=1 -L%{_libdir} -lldap -llber -c mod_ldap_userdir.c

%install

install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d

install -m0755 .libs/*.so %{buildroot}%{_libdir}/apache-extramodules/
install -m0644 %{mod_conf} %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

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

%files
%doc DIRECTIVES README user-ldif
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}


%changelog
* Sat Feb 11 2012 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.18-4mdv2012.0
+ Revision: 772672
- rebuild

* Tue May 24 2011 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.18-3
+ Revision: 678331
- mass rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.18-2mdv2011.0
+ Revision: 588015
- rebuild

* Sun Oct 17 2010 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.18-1mdv2011.0
+ Revision: 586379
- 1.1.18

* Fri Apr 23 2010 Funda Wang <fwang@mandriva.org> 1:1.1.17-3mdv2010.1
+ Revision: 538087
- rebuild

* Mon Mar 08 2010 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.17-2mdv2010.1
+ Revision: 516133
- rebuilt for apache-2.2.15

* Wed Dec 09 2009 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.17-1mdv2010.1
+ Revision: 475236
- 1.1.17

* Sat Aug 01 2009 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.16-2mdv2010.0
+ Revision: 406602
- rebuild

* Sun Jun 21 2009 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.16-1mdv2010.0
+ Revision: 387753
- fix build
- 1.1.16

* Tue Jan 06 2009 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.14-2mdv2009.1
+ Revision: 325802
- rebuild

* Thu Oct 16 2008 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.14-1mdv2009.1
+ Revision: 294278
- 1.1.14

* Fri Oct 10 2008 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.13-1mdv2009.1
+ Revision: 291383
- 1.1.13

* Mon Jul 14 2008 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.12-3mdv2009.0
+ Revision: 234966
- rebuild

* Thu Jun 05 2008 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.12-2mdv2009.0
+ Revision: 215594
- fix rebuild
- hard code %%{_localstatedir}/lib to ease backports

* Fri May 09 2008 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.12-1mdv2009.0
+ Revision: 205213
- 1.2.12
- drop the anonbind patch as it won't apply, this might bring back #22294

* Fri Mar 07 2008 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.11-4mdv2008.1
+ Revision: 181792
- rebuild

* Mon Dec 24 2007 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.11-3mdv2008.1
+ Revision: 137499
- rebuilt against openldap-2.4.7 libs

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sat Sep 08 2007 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.11-2mdv2008.0
+ Revision: 82601
- rebuild

* Sun Jul 15 2007 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.11-1mdv2008.0
+ Revision: 52254
- 1.1.11


* Sat Mar 10 2007 Oden Eriksson <oeriksson@mandriva.com> 1.1.10-3mdv2007.1
+ Revision: 140708
- rebuild

* Thu Nov 09 2006 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.10-2mdv2007.0
+ Revision: 79447
- Import apache-mod_ldap_userdir

* Sun Jul 30 2006 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.10-2mdv2007.0
- permit anonymous bind (Scott Karns, fixes #22294)

* Fri May 05 2006 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.10-1mdk
- 1.1.10 (Minor bugfixes)

* Mon Apr 24 2006 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.9-1mdk
- 1.1.9

* Wed Dec 14 2005 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.8-2mdk
- rebuilt against apache-2.2.0

* Mon Nov 28 2005 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.8-1mdk
- fix versioning

* Wed Aug 31 2005 Oden Eriksson <oeriksson@mandriva.com> 2.0.54_1.1.8-2mdk
- rebuilt against new openldap-2.3.6 libs

* Sun Jul 31 2005 Oden Eriksson <oeriksson@mandriva.com> 2.0.54_1.1.8-1mdk
- 1.1.8 (Major feature enhancements)
- fix deps

* Fri Jun 03 2005 Oden Eriksson <oeriksson@mandriva.com> 2.0.54_1.1.6-1mdk
- initial Mandriva package

