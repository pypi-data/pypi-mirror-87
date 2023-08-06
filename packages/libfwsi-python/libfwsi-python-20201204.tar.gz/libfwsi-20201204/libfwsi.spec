Name: libfwsi
Version: 20201204
Release: 1
Summary: Library to access the Windows Shell Item format
Group: System Environment/Libraries
License: LGPLv3+
Source: %{name}-%{version}.tar.gz
URL: https://github.com/libyal/libfwsi
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
          
BuildRequires: gcc          

%description -n libfwsi
Library to access the Windows Shell Item format

%package -n libfwsi-static
Summary: Library to access the Windows Shell Item format
Group: Development/Libraries
Requires: libfwsi = %{version}-%{release}

%description -n libfwsi-static
Static library version of libfwsi.

%package -n libfwsi-devel
Summary: Header files and libraries for developing applications for libfwsi
Group: Development/Libraries
Requires: libfwsi = %{version}-%{release}

%description -n libfwsi-devel
Header files and libraries for developing applications for libfwsi.

%package -n libfwsi-python2
Obsoletes: libfwsi-python < %{version}
Provides: libfwsi-python = %{version}
Summary: Python 2 bindings for libfwsi
Group: System Environment/Libraries
Requires: libfwsi = %{version}-%{release} python2
BuildRequires: python2-devel

%description -n libfwsi-python2
Python 2 bindings for libfwsi

%package -n libfwsi-python3
Summary: Python 3 bindings for libfwsi
Group: System Environment/Libraries
Requires: libfwsi = %{version}-%{release} python3
BuildRequires: python3-devel

%description -n libfwsi-python3
Python 3 bindings for libfwsi

%prep
%setup -q

%build
%configure --prefix=/usr --libdir=%{_libdir} --mandir=%{_mandir} --enable-python2 --enable-python3
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
%make_install

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -n libfwsi
%defattr(644,root,root,755)
%license COPYING COPYING.LESSER
%doc AUTHORS README
%attr(755,root,root) %{_libdir}/*.so.*

%files -n libfwsi-static
%defattr(644,root,root,755)
%license COPYING COPYING.LESSER
%doc AUTHORS README
%attr(755,root,root) %{_libdir}/*.a

%files -n libfwsi-devel
%defattr(644,root,root,755)
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/*.la
%{_libdir}/*.so
%{_libdir}/pkgconfig/libfwsi.pc
%{_includedir}/*
%{_mandir}/man3/*

%files -n libfwsi-python2
%defattr(644,root,root,755)
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/python2*/site-packages/*.a
%{_libdir}/python2*/site-packages/*.la
%{_libdir}/python2*/site-packages/*.so

%files -n libfwsi-python3
%defattr(644,root,root,755)
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/python3*/site-packages/*.a
%{_libdir}/python3*/site-packages/*.la
%{_libdir}/python3*/site-packages/*.so

%changelog
* Fri Dec  4 2020 Joachim Metz <joachim.metz@gmail.com> 20201204-1
- Auto-generated

