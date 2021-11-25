#
# Conditional build:
%bcond_without	ocaml_opt	# native optimized binaries (bytecode is always built)
%bcond_without	apidocs		# API documentation

# not yet available on x32 (ocaml 4.02.1), update when upstream will support it
%ifnarch %{ix86} %{x8664} %{arm} aarch64 ppc sparc sparcv9
%undefine	with_ocaml_opt
%endif

Summary:	Non-blocking streaming Unicode codec for OCaml
Summary(pl.UTF-8):	Nieblokujący strumieniowy kodek Unicode dla OCamla
Name:		ocaml-uutf
Version:	1.0.2
Release:	1
License:	ISC
Group:		Libraries
Source0:	https://erratique.ch/software/uutf/releases/uutf-%{version}.tbz
# Source0-md5:	a7c542405a39630c689a82bd7ef2292c
# don't require uchar package, drop compatibility with ocaml < 4.03
Patch0:		%{name}-uchar.patch
Patch1:		%{name}-deprecated.patch
URL:		https://erratique.ch/software/uutf
BuildRequires:	ocaml >= 1:4.03
BuildRequires:	ocaml-cmdliner-devel >= 0.9.6
BuildRequires:	ocaml-findlib-devel
BuildRequires:	ocaml-ocamlbuild
%{?with_apidocs:BuildRequires:	ocaml-ocamldoc}
BuildRequires:	ocaml-topkg-devel
BuildRequires:	rpm-build >= 4.6
%requires_eq	ocaml-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		debug_package	%{nil}

%description
Uutf is a non-blocking streaming codec to decode and encode the UTF-8,
UTF-16, UTF-16LE and UTF-16BE encoding schemes. It can efficiently
work character by character without blocking on I/O. Decoders perform
character position tracking and support newline normalization.

%description -l pl.UTF-8
Uutf to nieblokujący strumieniowy kodek do dekodowania i kodowania
schematów UTF-8, UTF-16, UTF16LE i UTF-16BE. Potrafi efektywnie
działać znak po znaku bez blokowania na we/wy. Dekodery wykonują
śledzenie pozycji znaków i obsługują normalizację znaków nowego
wiersza.

%package devel
Summary:	Non-blocking streaming Unicode codec for OCaml - development part
Summary(pl.UTF-8):	Nieblokujący strumieniowy kodek Unicode dla OCamla - cześć programistyczna
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%requires_eq	ocaml

%description devel
This package contains files needed to develop OCaml programs using
uutf library.

%description devel -l pl.UTF-8
Pakiet ten zawiera pliki niezbędne do tworzenia programów w OCamlu
używających biblioteki uutf.

%package apidocs
Summary:	API documentation for OCaml uutf library
Summary(pl.UTF-8):	Dokumentacja API biblioteki OCamla uutf
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for OCaml uutf library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki OCamla uutf.

%prep
%setup -q -n uutf-%{version}
%patch0 -p1
%patch1 -p1

%build
ocaml pkg/pkg.ml build --with-cmdliner true

%if %{with apidocs}
install -d html
ocamldoc -html -d html -I _build/src _build/src/uutf.mli
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/uutf

cp -p _build/{opam,pkg/META} $RPM_BUILD_ROOT%{_libdir}/ocaml/uutf
cp -p _build/src/*.{cma,cmi,cmt,cmti,mli} $RPM_BUILD_ROOT%{_libdir}/ocaml/uutf
%if %{with ocaml_opt}
cp -p _build/src/*.{a,cmx,cmxa,cmxs} $RPM_BUILD_ROOT%{_libdir}/ocaml/uutf
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.md LICENSE.md README.md
%dir %{_libdir}/ocaml/uutf
%{_libdir}/ocaml/uutf/META
%{_libdir}/ocaml/uutf/*.cma
%if %{with ocaml_opt}
%attr(755,root,root) %{_libdir}/ocaml/uutf/*.cmxs
%endif

%files devel
%defattr(644,root,root,755)
%{_libdir}/ocaml/uutf/*.a
%{_libdir}/ocaml/uutf/*.cmi
%{_libdir}/ocaml/uutf/*.cmt
%{_libdir}/ocaml/uutf/*.cmti
%{_libdir}/ocaml/uutf/*.mli
%if %{with ocaml_opt}
%{_libdir}/ocaml/uutf/*.cmx
%{_libdir}/ocaml/uutf/*.cmxa
%endif
%{_libdir}/ocaml/uutf/opam

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc html/*
%endif
