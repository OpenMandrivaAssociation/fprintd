%bcond_without doc

Summary:    D-Bus service for Fingerprint reader access
Name:       fprintd
Version:	1.94.2
Release:	1
Group:      System/Kernel and hardware
License:    GPLv2+
Source0:    https://gitlab.freedesktop.org/libfprint/fprintd/uploads/9dec4b63d1f00e637070be1477ce63c0/%{name}-v%{version}.tar.bz2
Url:        http://www.freedesktop.org/wiki/Software/fprint/fprintd
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(gio-2.0) >= 2.26
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gmodule-2.0)
BuildRequires:	pkgconfig(libfprint-2) > 0.1.0
BuildRequires:	pkgconfig(polkit-gobject-1) >= 0.91
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  meson
BuildRequires:  pam-devel
BuildRequires:	gettext-devel
BuildRequires:	pkgconfig(pam_wrapper)
BuildRequires:	python-dbusmock
BuildRequires:	python-libpamtest
BuildRequires:	python-cairo
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
%{_datadir}/dbus-1/system.d/net.reactivated.Fprint.conf
%{_unitdir}/fprintd.service
%{_datadir}/dbus-1/services/net.reactivated.Fprint.service
%{_datadir}/polkit-1/actions/net.reactivated.fprint.device.policy
%{_localstatedir}/lib/fprint
%doc %{_mandir}/man1/fprintd.*

#--------------------------------------------------------------------

%package pam
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
%doc %{_mandir}/man8/pam_fprintd.8.*
%{_libdir}/security/pam_fprintd.so

#--------------------------------------------------------------------

%package devel
Summary:    Development files for %{name}
Requires:   %{name} = %{version}-%{release}
Group:      Development/Other
BuildArch:	noarch

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
%autosetup -p1 -n %{name}-v%{version}


%if %{with doc}
#%%__cp doc/fprintd-sections.txt doc/html-sections.txt
%endif

%build
%meson 	\
		-Ddbus_service_dir="%{_datadir}/dbus-1/services" \
%if %{with doc}
        -Dgtk_doc=true \
%endif
         -Dpam=true \
		 -Dpam_modules_dir=%{_libdir}/security

%meson_build
 
%install
%meson_install
mkdir -p %{buildroot}/%{_localstatedir}/lib/fprint

rm -f %{buildroot}/%{_libdir}/security/pam_fprintd.{a,la,so.*}
%find_lang %name
