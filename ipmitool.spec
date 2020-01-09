Name:         ipmitool
Summary:      Utility for IPMI control
Version:      1.8.11
Release:      28%{?dist}
License:      BSD
Group:        System Environment/Base
URL:          http://ipmitool.sourceforge.net/
Source0:      http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
Source1:      openipmi-ipmievd.sysconf
Source2:      set-bmc-url.sh
Source3:      ipmitool-modalias.conf
Buildroot:    %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: openssl-devel readline-devel ncurses-devel
Requires(post): chkconfig
Requires(preun): chkconfig
Requires: net-tools
Requires: OpenIPMI
Requires: gettext
Obsoletes: OpenIPMI-tools < 2.0.14-3
Provides: OpenIPMI-tools = 2.0.14-3

Patch1: ipmitool-1.8.10-ipmievd-init.patch
Patch2: ipmitool-1.8.10-ipmievd-condrestart.patch
Patch3: ipmitool-1.8.11-ipmieved-pidfile.patch
Patch4: ipmitool-1.8.11-dell-oem.patch
Patch5: ipmitool-1.8.11-dell-setled.patch
Patch6: ipmitool-1.8.10-k-option.patch
Patch7: ipmitool-1.8.11-set-kg-key.patch
Patch8: ipmitool-1.8.11-set-kg-key2.patch
Patch9: ipmitool-1.8.11-sol-payload-size.patch
Patch10: ipmitool-1.8.11-dell-setled-updates.patch
Patch11: ipmitool-1.8.11-dell-big-endian.patch
Patch12: ipmitool-1.8.11-sol-leak.patch
Patch13: ipmitool-1.8.11-remove-umask0.patch
Patch14: ipmitool-1.8.11-retransmit.patch
Patch15: ipmitool-1.8.11-dell-addons.patch
Patch16: ipmitool-1.8.11-o-exitcode.patch
Patch17: ipmitool-1.8.11-cmdline-checks.patch
Patch18: ipmitool-1.8.11-no-work-setaccess.patch
Patch19: ipmitool-1.8.11-tout-retry.patch
Patch20: ipmitool-1.8.11-ipv6env.patch
Patch21: ipmitool-1.8.14-dell13g.patch
Patch22: ipmitool-1.8.14-unienv.patch
Patch23: ipmitool-1.8.14-optenvre.patch
Patch24: ipmitool-1.8.13-envarg.patch
Patch25: ipmitool-1.8.15-bz1194420-ddr4.patch
Patch26: ipmitool-1.8.11-bz1126333-slowswid.patch
Patch27: ipmitool-1.8.11-bz878614-overname.patch

%description
This package contains a utility for interfacing with devices that support
the Intelligent Platform Management Interface specification.  IPMI is
an open standard for machine health, inventory, and remote power control.

This utility can communicate with IPMI-enabled devices through either a
kernel driver such as OpenIPMI or over the RMCP LAN protocol defined in
the IPMI specification.  IPMIv2 adds support for encrypted LAN
communications and remote Serial-over-LAN functionality.

It provides commands for reading the Sensor Data Repository (SDR) and
displaying sensor values, displaying the contents of the System Event
Log (SEL), printing Field Replaceable Unit (FRU) information, reading and
setting LAN configuration, and chassis power control.

%prep

%setup -q
%patch1 -p1 -b .ipmievd-init
%patch2 -p0 -b .condrestart
%patch3 -p1 -b .ipmievd-pidfile
%patch4 -p1 -b .delloem
%patch5 -p1 -b .setled
%patch6 -p1 -b .k-option
%patch7 -p1 -b .set-kg
%patch8 -p1 -b .set-kg2
%patch9 -p1 -b .sol-payload-size
%patch10 -p1 -b .setled-updates
%patch11 -p1 -b .fixes
%patch12 -p1 -b .sol-leak
%patch13 -p1 -b .umask0
%patch14 -p1 -b .retransmit
%patch15 -p1 -b .dell-addons
%patch16 -p1 -b .o-exitcode
%patch17 -p1 -b .cmdline-checks
%patch18 -p1 -b .no-work-setaccess
%patch19 -p1 -b .tout-retry
%patch20 -p1 -b .ipv6env
%patch21 -p1 -b .13g
%patch22 -p0 -b .unienv
%patch23 -p1 -b .optenvre
%patch24 -p1 -b .envarg
%patch25 -p1 -b .ddr4
%patch26 -p1 -b .slowswid
%patch27 -p1 -b .overname


for f in AUTHORS ChangeLog; do
    iconv -f iso-8859-1 -t utf8 < ${f} > ${f}.utf8
    mv ${f}.utf8 ${f}
done

cp -p %SOURCE3 .

%build
# --disable-dependency-tracking speeds up the build
# --enable-file-security adds some security checks
# --disable-intf-free disables FreeIPMI support - we don't want to depend on
#   FreeIPMI libraries, FreeIPMI has its own ipmitoool-like utility.
%configure --disable-dependency-tracking --enable-file-security --disable-intf-free
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

install -Dpm 755 contrib/ipmievd.init.redhat %{buildroot}%{_initrddir}/ipmievd
install -Dpm 644 %SOURCE1 %{buildroot}%{_sysconfdir}/sysconfig/ipmievd
install -Dm 644 contrib/exchange-bmc-os-info.sysconf %{buildroot}%{_sysconfdir}/sysconfig/exchange-bmc-os-info
install -Dm 644 %SOURCE2 %{buildroot}%{_sysconfdir}/profile.d/set-bmc-url.sh
install -Dm 755 contrib/exchange-bmc-os-info.init.redhat %{buildroot}%{_initddir}/exchange-bmc-os-info

install -Dm 644 contrib/bmc-snmp-proxy.sysconf %{buildroot}%{_sysconfdir}/sysconfig/bmc-snmp-proxy
install -Dm 755 contrib/bmc-snmp-proxy         %{buildroot}%{_initddir}/bmc-snmp-proxy

install -d -m 755 ${RPM_BUILD_ROOT}%{_sysconfdir}/modprobe.d
install -m 644 %SOURCE3 ${RPM_BUILD_ROOT}%{_sysconfdir}/modprobe.d/ipmitool-modalias.conf
%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add ipmievd

%preun
if [ $1 = 0 ]; then
   service ipmievd stop >/dev/null 2>&1
   /sbin/chkconfig --del ipmievd
fi

%postun
if [ "$1" -ge "1" ]; then
    service ipmievd condrestart >/dev/null 2>&1 || :
fi

%files
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/modprobe.d/ipmitool-modalias.conf
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/sysconfig/ipmievd
%config(noreplace) %{_sysconfdir}/sysconfig/exchange-bmc-os-info
%config(noreplace) %{_sysconfdir}/sysconfig/bmc-snmp-proxy
%{_sysconfdir}/profile.d/set-bmc-url.sh
%{_initddir}/exchange-bmc-os-info
%{_initddir}/bmc-snmp-proxy
%{_initrddir}/ipmievd
%{_bindir}/*
%{_sbindir}/*
%{_mandir}/man*/*
%doc %{_datadir}/doc/ipmitool
%{_datadir}/ipmitool

%changelog
* Mon Apr 20 2015 Ales Ledvinka <aledvink@redhat.com> - 1.8.11-28
- (#1085072) Correct init paths.

* Wed Mar 04 2015 Ales Ledvinka <aledvink@redhat.com> - 1.8.11-25
- (#878614)  SDR long sensor names.

* Tue Feb 24 2015 Ales Ledvinka <aledvink@redhat.com> - 1.8.11-23
- (#1194420) Fix DDR4 SDR crash.
- (#1170266) Wrong version reported.
- (#1162175) Extra dependency.
- (#1126333) Very slow response from SDR owner type SW ID
- (#903019)  SDR lists x4600m2 fan units as unspecified

* Mon Sep 15 2014 Ales Ledvinka <aledvink@redhat.com> - 1.8.11-21
- (#1028163) Fix environment variable parsing.

* Mon Sep 15 2014 Ales Ledvinka <aledvink@redhat.com> - 1.8.11-20
- (#1056581) IPv6 connectivity support.
- (#1029529) Fix dependency for kernel module loading.

* Tue Jun 25 2013 Ales Ledvinka <aledvink@redhat.com> - 1.8.11-16
- (#923192) ipmi command retry no longer shifts replies

* Tue Feb 05 2013 Petr Hracek <phracek@redhat.com> - 1.8.11-15
- (#903251) - link=on and ipmi=on no longer work for setaccess

* Wed May 30 2012 Jan Safranek <jsafrane@redhat.com> - 1.8.11-13.1
- fixed retransmissions of lanplus requests, broken in previous release
  (#826027)

* Mon Feb 20 2012 Jan Safranek <jsafrane@redhat.com> - 1.8.11-13
- added new options to configure retransmissions on lan/lanplus interfaces
  (#748073)
- updated dellem command (#739358)
- fixed exit code of ipmitool -o list (#715615)
- improved checking of command line arguments (#725993)

* Thu Nov 24 2011 Jan Safranek <jsafrane@redhat.com> - 1.8.11-12
- fixed wrong permissions on ipmievd.pid (#756685)

* Thu Aug 18 2011 Jan Safranek <jsafrane@redhat.com> - 1.8.11-11
- fixed delloem powermonitor on bigendian systems (#731718)
- fixed memory leak in Serial-over-Lan module (#731977)

* Wed Aug 10 2011 Jan Safranek <jsafrane@redhat.com> - 1.8.11-10
- added -Y option for ipmitool to hide Kg key from cmdline (#698647)
- added 'channel setkg' command to set Kg encryption key on remote machine
  (#726390)

* Thu Aug  4 2011 Jan Safranek <jsafrane@redhat.com> - 1.8.11-10
- updated 'delloem setled' command to indicate SES status and drive
  activities for a PCI-e SSD (#727314)

* Mon Jul 25 2011 Jan Safranek <jsafrane@redhat.com> - 1.8.11-9
- rebuilt for RHEL 6.2 Fastrack

* Thu Jul 14 2011 Jan Safranek <jsafrane@redhat.com> - 1.8.11-8
- fixed 'ipmi sol' sending wrong packets due to miscalculation of SOL
  payload size (#675975)

* Mon Feb  7 2011 Jan Safranek <jsafrane@redhat.com> - 1.8.11-7
- added 'delloem' command for Dell-specific IPMI extensions (#631649, #63793)

* Wed Jun  2 2010 Jan Safranek <jsafrane@redhat.com> - 1.8.11-6
- Changed ipmievd to use /var/run/ipmievd.pid file by default (#596809)

* Wed Mar  3 2010 Jan Safranek <jsafrane@redhat.com> - 1.8.11-5
- Fixed exit code of ipmievd initscript with wrong arguments (#562186)

* Fri Dec 11 2009 Dennis Gregorovic <dgregor@redhat.com> - 1.8.11-4.1
- Rebuilt for RHEL 6

* Mon Nov  2 2009 Jan Safranek  <jsafrane@redhat.com> 1.8.11-4
- fix ipmievd initscript 'condrestart' action (#532188)

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 1.8.11-3
- rebuilt with new openssl

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Jan Safranek <jsafrane@redhat.com> 1.8.11-1
- updated to new version

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jan 17 2009 Tomas Mraz <tmraz@redhat.com> 1.8.10-3
- rebuild with new openssl

* Tue Oct 14 2008 Jan Safranek <jsafrane@redhat.com> 1.8.10-2
- fix issues found during package review:
  - clear Default-Start: line in the init script, the service should be 
    disabled by default
  - added Obsoletes: OpenIPMI-tools
  - compile with --disable-dependency-tracking to speed things up
  - compile with --enable-file-security
  - compile with --disable-intf-free, don't depend on FreeIPMI libraries
    (FreeIPMI has its own ipmitool-like utility)

* Mon Oct 13 2008 Jan Safranek <jsafrane@redhat.com> 1.8.10-1
- package created, based on upstream .spec file
