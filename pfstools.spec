# TODO:
# - jpeghdr (libjpeghdr doesn't seem to be freely available; was attached to some book?); not supported by CMakeLists
# - split progs package by libraries required
#
# Conditional build:
%bcond_with	opencv	# pfsalign utility (using OpenCV)

Summary:	pfstools for High Dynamic Range Images and Video
Summary(pl.UTF-8):	Narzędzia do obrazów i wideo o dużym zakresie luminancji
Name:		pfstools
Version:	2.2.0
Release:	7
License:	LGPL v2.1+
Group:		Libraries
Source0:	http://downloads.sourceforge.net/pfstools/%{name}-%{version}.tgz
# Source0-md5:	8f026213e567bc72dd23253ced5417a4
Patch0:		imagemagick7.patch
Patch1:		%{name}-glut.patch
URL:		http://pfstools.sourceforge.net/
BuildRequires:	ImageMagick-c++-devel >= 6.0
BuildRequires:	OpenEXR-devel >= 1.0
BuildRequires:	OpenGL-GLU-devel
BuildRequires:	OpenGL-glut-devel
BuildRequires:	Qt5Widgets-devel >= 5
BuildRequires:	cmake >= 2.8.8
BuildRequires:	fftw3-devel >= 3
BuildRequires:	fftw3-single-devel >= 3
# pfsingdal not supported in CMakeLists
#BuildRequires:	gdal-devel
BuildRequires:	gsl-devel
BuildRequires:	libexif-devel
BuildRequires:	libgomp-devel
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	libtiff-devel
BuildRequires:	netpbm-devel
BuildRequires:	octave-devel
%{?with_opencv:BuildRequires:	opencv-devel}
BuildRequires:	perl-base
BuildRequires:	pkgconfig
BuildRequires:	qt5-build >= 5
BuildRequires:	texlive-format-pdflatex
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		octave_m_dir	%(octave-config --m-site-dir)
%define		octave_oct_dir	%(octave-config --oct-site-dir)

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
Obsoletes:	pfstools-static < 2

%description devel
The header files are only needed for development of programs using the
pfstools.

%description devel -l pl.UTF-8
W pakiecie tym znajdują się pliki nagłówkowe, przeznaczone dla
programistów używających bibliotek pfstools.

%package progs
Summary:	pfstools utility programs
Summary(pl.UTF-8):	Narzędzia pfstools
Group:		Applications/Graphics
Requires:	%{name} = %{version}-%{release}
Obsoletes:	pfscalibration < 2
Obsoletes:	pfstmo < 2

%description progs
This package contains pfstools utility programs.

%description progs -l pl.UTF-8
Pakiet zawiera narzędzia pfstools.

%package -n octave-pfstools
Summary:	Octave bindings for pfstools
Summary(pl.UTF-8):	Wiązania języka Octave do pfstools
Group:		Development/Languages
Requires:	%{name} = %{version}-%{release}

%description -n octave-pfstools
Octave bindings for pfstools.

%description -n octave-pfstools -l pl.UTF-8
Wiązania języka Octave do pfstools.

%prep
%setup -q
%patch -P0 -p1
%patch -P1 -p1

%build
install -d build
cd build
export CXXFLAGS="%{rpmcxxflags} -std=c++11"
%cmake .. \
	%{!?with_opencv:-DWITH_OpenCV=OFF}

%{__make}

cd ../doc
pdflatex pfs_format_spec.tex

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README doc/faq.txt doc/pfs_format_spec.pdf
%attr(755,root,root) %{_libdir}/libpfs.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpfs.so.2

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpfs.so
%{_pkgconfigdir}/pfs.pc
%{_includedir}/pfs

%files progs
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/pfs*
%attr(755,root,root) %{_bindir}/*2hdrgen
%{_datadir}/pfstools
%{_mandir}/man1/pfs*.1*
%{_mandir}/man1/*2hdrgen.1*

%files -n octave-pfstools
%defattr(644,root,root,755)
%dir %{octave_oct_dir}/pfstools
%attr(755,root,root) %{octave_oct_dir}/pfstools/pfs*.oct
%{octave_m_dir}/pfstools
