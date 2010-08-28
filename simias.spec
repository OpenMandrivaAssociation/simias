%define buildnum 10090

Name:           simias
Version:        1.8.3.10090.1
Release:        %mkrel 1
Url:            http://www.ifolder.com
License:        GPLv2
Group:          System/Libraries
Summary:        Collection-Oriented Data Storage
Source:         simias.tar.gz
Patch:          simias-lib64.patch
Patch1:         simias-libflaim.patch
Patch2:         simias-buildfix.patch
Patch3:         simias-make.patch
Patch4:         simias-warnings.patch
Patch5:         simias-fix-format-errors.patch
Patch6:         simias-fix-linking.patch
Patch7:         simias-use-external-gsoap.patch
Requires:       mono-data >= 1.2.2
Requires:       mono-web >= 1.2.2
Requires:       log4net >= 1.2.9
Requires:       xsp >= 1.2.5
BuildRequires:  flex
BuildRequires:  bison
BuildRequires:  e2fsprogs-devel
BuildRequires:  glib2-devel
BuildRequires:  libflaim-devel
BuildRequires:  libxml2-devel
BuildRequires:  log4net-devel
BuildRequires:  ncurses-devel
BuildRequires:  libuuid-devel
BuildRequires:  mono-data
BuildRequires:  mono-devel
BuildRequires:  mono-web
BuildRequires:  xsp
BuildRoot:      %{_tmppath}/%{name}-%{version}

%description
Simias is a technology that will allow various types of data to be
stored and related in what is known as a collection.  Initially Simias
is the underlying data store for the iFolder project, although it has
potential to do much more.

%package devel
License:        GPLv2
Summary:        Development files for simias
Group:          Development/Libraries/C and C++
Requires:       %{name} = %{version}

%description devel
Development files for simias. Simias is a technology that will allow
various types of data to be stored and related in what is known as a
collection. Initially Simias is the underlying data store for the
iFolder project, although it has potential to do much more.

%prep
%setup -q -n %{name}
%patch
%patch1
%patch2 
%patch3
%patch4
%patch5 -p 1
%patch6 -p 1

%build
export BUILDNUM=%{buildnum}
autoreconf -i
%configure2_5x --with-runasclient

# rebuild shipped gsoap
rm dependencies/external/tools/gsoap/linux-2.7/soapcpp2  
rm dependencies/external/tools/gsoap/linux-2.7/wsdl2h  
pushd dependencies/external/tools/gsoap/linux-2.7  
cd src
make -f MakefileMacOSX COFLAGS="%{optflags} -fno-strict-aliasing" LIBS=""
cp soapcpp2 ..  
cd ..  
cd wsdl  
make -f MakefileSolaris COFLAGS="%{optflags} -fno-strict-aliasing" LIBS="-lnsl"
cd ..
popd

# parallel build is broken
make

%install
rm -rf %{buildroot}
export BUILDNUM=%{buildnum}
%makeinstall_std

mv %{buildroot}%{_bindir}/SimiasDirectoryMapping \
    %{buildroot}%{_sysconfdir}/simias

chmod 644 %{buildroot}%{_sysconfdir}/simias/*
chmod 644 %{buildroot}%{_libdir}/pkgconfig/*
find %{buildroot}%{_libdir}/web -type f | xargs chmod 644

rm -rf %{buildroot}%{_datadir}/simias/COPYING

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc COPYING
%{_bindir}/*
%dir %{_sysconfdir}/simias
%config %{_sysconfdir}/simias/Simias.config
%config %{_sysconfdir}/simias/Simias.log4net
%config %{_sysconfdir}/simias/defaults.config
%config %{_sysconfdir}/simias/SimiasDirectoryMapping
%{_libdir}/libFlaimWrapper.so
%{_libdir}/libFlaimWrapper.so.0
%{_libdir}/libFlaimWrapper.so.0.0.0
%{_libdir}/libsimias-event.so
%{_libdir}/libsimias-event.so.0
%{_libdir}/libsimias-event.so.0.0.0
%{_libdir}/libsimias-manager.so.0
%{_libdir}/libsimias-manager.so.0.0.0
%{_libdir}/libsimias.so
%{_libdir}/libsimias.so.0
%{_libdir}/libsimias.so.0.0.0
%{_libdir}/web

%files devel
%defattr(-,root,root)
%{_libdir}/libFlaimWrapper.so
%{_libdir}/libsimias-event.so
%{_libdir}/libsimias-manager.so
%{_libdir}/libsimias.so
%{_libdir}/pkgconfig/*
%{_includedir}/simias

