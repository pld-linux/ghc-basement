#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	basement
Summary:	Foundation scrap box of array & string
Name:		ghc-%{pkgname}
Version:	0.0.11
Release:	2
License:	BSD
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/basement
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	dc1ffab6a43e42f147769af6fe564742
URL:		http://hackage.haskell.org/package/basement
BuildRequires:	ghc >= 6.12.3
%if %{with prof}
BuildRequires:	ghc-prof
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
%requires_eq	ghc
Requires(post,postun):	/usr/bin/ghc-pkg
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
Foundation most basic primitives without any dependencies.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description prof
Profiling %{pkgname} library for GHC.  Should be installed when
GHC's profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.hs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.hs build
LANG=C.UTF-8 LC_ALL=C.UTF-8 runhaskell Setup.hs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc %{name}-%{version}-doc/*
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.so
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.a
%exclude %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*_p.a

%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Basement
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Basement/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Basement/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Basement/Alg
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Basement/Alg/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Basement/Alg/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Basement/Bindings
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Basement/Bindings/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Basement/Bindings/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Basement/Block
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Basement/Block/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Basement/Block/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Basement/Compat
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Basement/Compat/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Basement/Compat/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Basement/Compat/C
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Basement/Compat/C/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Basement/Compat/C/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Basement/Numerical
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Basement/Numerical/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Basement/Numerical/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Basement/Sized
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Basement/Sized/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Basement/Sized/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Basement/String
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Basement/String/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Basement/String/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Basement/String/Encoding
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Basement/String/Encoding/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Basement/String/Encoding/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Basement/Terminal
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Basement/Terminal/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Basement/Terminal/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Basement/Types
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Basement/Types/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Basement/Types/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Basement/UArray
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Basement/UArray/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Basement/UArray/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Basement/UTF8
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Basement/UTF8/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Basement/UTF8/*.dyn_hi

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Basement/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Basement/Alg/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Basement/Bindings/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Basement/Block/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Basement/Compat/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Basement/Compat/C/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Basement/Numerical/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Basement/Sized/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Basement/String/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Basement/String/Encoding/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Basement/Terminal/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Basement/Types/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Basement/UArray/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Basement/UTF8/*.p_hi
%endif
