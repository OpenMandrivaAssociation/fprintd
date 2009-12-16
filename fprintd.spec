%define long_hash  04fd09cfa88718838e02f4419befc1a0dd4b5a0e
%define short_hash 04fd09cfa

Name:       fprintd
Version:    0.1
Release:    %mkrel 1.git%{short_hash}.1
Summary:    D-Bus service for Fingerprint reader access

Group:      System/Kernel and hardware
License:    GPLv2+
# git clone git://projects.reactivated.net/~dsd/fprintd.git
# cd fprintd
# git reset --hard %{long_hash}
# ./autogen.sh && make distcheck
# mv fprintd-0.1.tar.bz2 fprintd-0.1-%{short_hash}.tar.bz2
Source0:    fprintd-0.1-%{short_hash}.tar.bz2
Patch1:     0001-Detect-when-a-device-is-disconnected.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=498368
Patch2:     polkit1.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=543194
Patch3:     0001-Remove-all-use-of-g_error.patch
Url:        http://www.reactivated.net/fprint/wiki/Fprintd
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires:  dbus-glib-devel
BuildRequires:  pam-devel
BuildRequires:  libfprint-devel >= 0.1.0
BuildRequires:  polkit-devel
BuildRequires:  gtk-doc
BuildRequires:  intltool
BuildRequires:  autoconf 
BuildRequires:  automake 
BuildRequires:  libtool

%description
D-Bus service to access fingerprint readers.

%files
%defattr(-,root,root,-)
%doc README COPYING AUTHORS TODO
%{_bindir}/fprintd-*
%{_libexecdir}/fprintd
# FIXME This file should be marked as config when it does something useful
%{_sysconfdir}/fprintd.conf
%{_sysconfdir}/dbus-1/system.d/net.reactivated.Fprint.conf
%{_datadir}/dbus-1/system-services/net.reactivated.Fprint.service
%{_datadir}/polkit-1/actions/net.reactivated.fprint.device.policy
%{_localstatedir}/lib/fprint

#--------------------------------------------------------------------

%package pam
Summary:    PAM module for fingerprint authentication
Requires:   %{name} = %{version}-%{release}
# Note that we obsolete pam_fprint, but as the configuration
# is different, it will be mentioned in the release notes
Provides:   pam_fprint = %{version}-%{release}
Obsoletes:  pam_fprint < 0.2-3

Group:      System Environment/Base
License:    GPLv2+

%description pam
PAM module that uses the fprintd D-Bus service for fingerprint
authentication.

%files pam
%defattr(-,root,root,-)
%doc pam/README
/%{_lib}/security/pam_fprintd.so

#--------------------------------------------------------------------

%package devel
Summary:    Development files for %{name}
Requires:   %{name} = %{version}-%{release}
Requires:   gtk-doc
Group:      Development/Libraries
License:    GFDLv1.1+
BuildArch:  noarch

%description devel
Development documentation for fprintd, the D-Bus service for
fingerprint readers access.

%files devel
%defattr(-,root,root,-)
%{_datadir}/gtk-doc/html/fprintd
%{_datadir}/dbus-1/interfaces/net.reactivated.Fprint.Device.xml
%{_datadir}/dbus-1/interfaces/net.reactivated.Fprint.Manager.xml

#--------------------------------------------------------------------

%prep
%setup -q -n %{name}-%{version}
%patch1 -p1
%patch2 -p1 -b .polkit1
%patch3 -p1 -b .g_error

autoreconf -i -f

%build
%configure --enable-gtk-doc --enable-pam

%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std
mkdir -p $RPM_BUILD_ROOT/%{_localstatedir}/lib/fprint

rm -f $RPM_BUILD_ROOT/%{_lib}/security/pam_fprintd.{a,la,so.*}

%clean
rm -rf $RPM_BUILD_ROOT
