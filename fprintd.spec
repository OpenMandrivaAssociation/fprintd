%define with_doc 1
%{?_with_doc: %{expand: %%global with_doc 1}}

Summary:	D-Bus service for Fingerprint reader access
Name:		fprintd
Version:	0.4.1
Release:	2
Group:		System/Kernel and hardware
License:	GPLv2+
Url:		http://www.freedesktop.org/wiki/Software/fprint/fprintd
# download here:
# http://cgit.freedesktop.org/libfprint/fprintd/
# then rename and re-pack
Source0:	fprintd-%{version}.tar.bz2
Patch1:		fprintd-0.4.1-fix-doc.patch

BuildRequires:	intltool
BuildRequires:	libtool
BuildRequires:	pam-devel
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(libfprint) >= 0.4.0
BuildRequires:	pkgconfig(polkit-agent-1)
%if %{with_doc}
BuildRequires:	gtk-doc
%endif

%description
D-Bus service to access fingerprint readers.

%files -f %{name}.lang
%doc README COPYING AUTHORS TODO
%{_bindir}/fprintd-*
%{_libexecdir}/fprintd
# FIXME This file should be marked as config when it does something useful
%{_sysconfdir}/fprintd.conf
%{_sysconfdir}/dbus-1/system.d/net.reactivated.Fprint.conf
%{_datadir}/dbus-1/system-services/net.reactivated.Fprint.service
%{_datadir}/polkit-1/actions/net.reactivated.fprint.device.policy
%{_localstatedir}/lib/fprint
%{_mandir}/man1/fprintd.*

#--------------------------------------------------------------------

%package pam
Summary:	PAM module for fingerprint authentication
Group:		System/Kernel and hardware
Requires:	%{name} = %{version}-%{release}

%description pam
PAM module that uses the fprintd D-Bus service for fingerprint
authentication.

%files pam
%doc pam/README
/%{_lib}/security/pam_fprintd.so

#--------------------------------------------------------------------

%package devel
Summary:	Development files for %{name}
Group:		Development/Other
Requires:	%{name} = %{version}-%{release}
Requires:	gtk-doc

%description devel
Development documentation for fprintd, the D-Bus service for
fingerprint readers access.

%files devel
%if %{with_doc}
%{_datadir}/gtk-doc/html/fprintd
%endif
%{_datadir}/dbus-1/interfaces/net.reactivated.Fprint.Device.xml
%{_datadir}/dbus-1/interfaces/net.reactivated.Fprint.Manager.xml

#--------------------------------------------------------------------

%prep
%setup -q
%patch1 -p0

autoreconf -fi

%if %{with_doc}
cp doc/fprintd-sections.txt doc/html-sections.txt
%endif

%build
%configure2_5x \
%if %{with_doc}
	--enable-gtk-doc \
%endif
	--enable-pam \
	--libdir=/%{_lib}/

%make

%install
%makeinstall_std
mkdir -p %{buildroot}/%{_localstatedir}/lib/fprint

rm -f %{buildroot}/%{_lib}/security/pam_fprintd.{a,la,so.*}

%find_lang %{name}

