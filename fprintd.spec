%bcond_without doc

Name:       fprintd
Version:    0.5.1
Release:    8
Summary:    D-Bus service for Fingerprint reader access

Group:      System/Kernel and hardware
License:    GPLv2+
Source0:    http://people.freedesktop.org/~hadess/fprintd-%{version}.tar.xz
Patch0:     0001-data-Fix-syntax-error-in-fprintd.pod.patch
Url:        http://www.freedesktop.org/wiki/Software/fprint/fprintd

BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(gio-2.0) >= 2.26
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gmodule-2.0)
BuildRequires:	pkgconfig(libfprint) > 0.1.0
BuildRequires:	pkgconfig(polkit-gobject-1) >= 0.91
BuildRequires:  pkgconfig(udev)
BuildRequires:  pkgconfig(systemd)
BuildRequires:  pam-devel
BuildRequires:	gettext-devel
%if %{with doc}
BuildRequires:  gtk-doc
%endif
BuildRequires:  intltool

%description
D-Bus service to access fingerprint readers.

%files -f %name.lang
%doc README COPYING AUTHORS TODO
%{_bindir}/fprintd-*
%{_libexecdir}/fprintd
# FIXME This file should be marked as config when it does something useful
%{_sysconfdir}/fprintd.conf
%{_sysconfdir}/dbus-1/system.d/net.reactivated.Fprint.conf
%{_unitdir}/fprintd.service
%{_datadir}/dbus-1/system-services/net.reactivated.Fprint.service
%{_datadir}/polkit-1/actions/net.reactivated.fprint.device.policy
%{_localstatedir}/lib/fprint
%_mandir/man1/fprintd.*

#--------------------------------------------------------------------

%package    pam
Summary:    PAM module for fingerprint authentication
Requires:   %{name} = %{version}-%{release}
# Note that we obsolete pam_fprint, but as the configuration
# is different, it will be mentioned in the release notes
Provides:   pam_fprint = %{version}-%{release}
Obsoletes:  pam_fprint < 0.2-5

Group:      System/Kernel and hardware
License:    GPLv2+

%description pam
PAM module that uses the fprintd D-Bus service for fingerprint
authentication.

%files pam
%doc pam/README
/%{_lib}/security/pam_fprintd.so

#--------------------------------------------------------------------

%package devel
Summary:    Development files for %{name}
Requires:   %{name} = %{version}-%{release}
Requires:   gtk-doc
Group:      Development/Other
License:    GFDLv1.1+

%description devel
Development documentation for fprintd, the D-Bus service for
fingerprint readers access.

%files devel
%if %{with doc}
%{_datadir}/gtk-doc/html/fprintd
%endif
%{_datadir}/dbus-1/interfaces/net.reactivated.Fprint.Device.xml
%{_datadir}/dbus-1/interfaces/net.reactivated.Fprint.Manager.xml

#--------------------------------------------------------------------

%prep
%setup -q -n %{name}-%{version}
%apply_patches

autoreconf -i -f

%if %{with doc}
#%__cp doc/fprintd-sections.txt doc/html-sections.txt
%endif

%build

%configure --disable-static \
%if %{with doc}
           --enable-gtk-doc \
%endif
           --enable-pam --libdir=/%{_lib}/

make

%install
%makeinstall_std
mkdir -p %{buildroot}/%{_localstatedir}/lib/fprint

rm -f %{buildroot}/%{_lib}/security/pam_fprintd.{a,la,so.*}
%find_lang %name
