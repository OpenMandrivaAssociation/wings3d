%define erlangdir %{_libdir}/erlang
%define oname wings

Summary: 	A subdivision modeler
Name: 		wings3d
Version: 	0.98.36
Release: 	%mkrel 1
License: 	BSD-like
Group: 		Graphics
Url: 		http://www.wings3d.org/
Source0: 	http://prdownloads.sourceforge.net/wings/%{oname}-%{version}.tar.bz2
Source1:   	%{name}.png
Source2:	%{name}_manual1.6.1.pdf
BuildRequires:	erlang-base		>= R11B-6
BuildRequires:	erlang-compiler
BuildRequires:	erlang-devel
BuildRequires:	erlang-esdl-devel	>= 0.96.0626-3
BuildRequires:	mesa-common-devel
BuildRequires:	SDL-devel
BuildRequires:	imagemagick
BuildRoot: 	%{_tmppath}/%{name}-%{version}-buildroot

%description
Wings 3D is a subdivision modeler inspired by Nendo and Mirai from Izware.

%prep
%setup -qn %{oname}-%{version}

%build
ERL_FLAGS="%{optflags}"
PATH=%{erlangdir}/bin:$PATH make

%install
rm -rf %{buildroot}

install -d -m 755 %{buildroot}/%{_datadir}/wings
cp -r * %{buildroot}/%{_datadir}/wings
cat %{SOURCE2} > ./%{name}_manual1.6.1.pdf

install -d -m 755 %{buildroot}/%{_bindir}

cat > %{buildroot}/%{_bindir}/%{name} << "EOF"
#!/bin/sh
export ESDL_PATH=/usr/lib/erlang/lib/esdl-*
erl -pa $ESDL_PATH/ebin /usr/share/wings/ebin  -run wings_start start_halt
EOF

install -d %{buildroot}{%{_liconsdir},%{_iconsdir},%{_miconsdir}}
convert %{SOURCE1} -size 16x16 %{buildroot}%{_miconsdir}/%{name}.png
convert %{SOURCE1} -size 32x32 %{buildroot}%{_iconsdir}/%{name}.png
convert %{SOURCE1} -size 48x48 %{buildroot}%{_liconsdir}/%{name}.png

%post
%{update_menus}

%postun
%{clean_menus}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS license.terms README
%doc *.pdf
%attr(755,root,root) %{_bindir}/*
%{_datadir}/%{oname}/*
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
