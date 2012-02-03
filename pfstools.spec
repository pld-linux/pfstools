#
# TODO:
# - jpeghdr
# - gdal
# - octave
# - split progs package by libraries required
#
Summary:	pfstools for High Dynamic Range Images and Video
Summary(pl.UTF-8):	Narzędzia do obrazów i wideo o dużym zakresie luminancji
Name:		pfstools
Version:	1.8.5
Release:	1
License:	LGPL
Group:		Libraries
Source0:	http://downloads.sourceforge.net/pfstools/%{name}-%{version}.tar.gz
# Source0-md5:	80dac70bfb6359a6749453477e74b112
URL:		http://pfstools.sourceforge.net/
BuildRequires:	ImageMagick-c++-devel >= 6.0
BuildRequires:	OpenEXR-devel >= 1.0
BuildRequires:	OpenGL-GLU-devel
BuildRequires:	OpenGL-glut-devel
BuildRequires:	QtGui-devel >= 4
BuildRequires:	autoconf >= 2.59-9
BuildRequires:	automake
BuildRequires:	libtiff-devel
BuildRequires:	libtool >= 2:2.0
BuildRequires:	netpbm-devel
BuildRequires:	qt4-build >= 4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
pfstools package is a set of command line (and one GUI) programs for
reading, writing, manipulating and viewing high-dynamic range (HDR)
images and video frames. All programs in the package exchange data
using Unix pipes and a simple generic HDR image format (pfs). The
concept of the pfstools is similar to netpbm package for low-dynamic
range images.

%description -l pl.UTF-8
Pakiet pfstools jest zestawiem programów służących do odczytu,
zapisu, obróbki i wyświetlania obrazów i klatek wideo o wysokim
zakresie dynamiki (HDR). Wszystkie programy wymieniają dane za
pomocą uniksowych rurek i prostego ogólnego formatu obrazów HDR
(pfs). Idea pfstools jest podobna do pakietu netpbm, używanego do
obrazów o niskim zakresie dynamiki.

%package devel
Summary:	Header files for pfstools
Summary(pl.UTF-8):	Pliki nagłówkowe pfstools
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
The header files are only needed for development of programs using the
pfstools.

%description devel -l pl.UTF-8
W pakiecie tym znajdują się pliki nagłówkowe, przeznaczone dla
programistów używających bibliotek pfstools.

%package static
Summary:	Static pfstools libraries
Summary(pl.UTF-8):	Biblioteki statyczne pfstools
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static pfstools libraries.

%description static -l pl.UTF-8
Biblioteki statyczne pfstools.

%package progs
Summary:	pfstools utility programs
Summary(pl.UTF-8):	Narzędzia pfstools
Group:		Applications/Graphics

%description progs
This package contains pfstools utility programs.

%description progs -l pl.UTF-8
Pakiet zawiera narzędzia pfstools.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}

%configure \
	--disable-matlab \
	--disable-octave \
	%{?debug:--enable-debug}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libpfs-1.2.la

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README TODO doc/faq.txt doc/pfs_format_spec.pdf
%attr(755,root,root) %{_libdir}/libpfs-1.2.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpfs-1.2.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpfs-1.2.so
%{_pkgconfigdir}/pfs.pc
%{_includedir}/pfs-1.2

%files static
%defattr(644,root,root,755)
%{_libdir}/libpfs-1.2.a

%files progs
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/pfs*
%{_datadir}/pfstools
%{_mandir}/man1/pfs*.1*
