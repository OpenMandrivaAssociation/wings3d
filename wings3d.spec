%define oname wings
%define erlangdir %{_libdir}/erlang
%define wingsdir %{erlangdir}/lib/%{oname}-%{version}
%define esdldir %{erlangdir}/lib/esdl-0.96-0626
%define esdl_ver 0.96.0626

Summary: 	A 3D subdivision modeler
Name: 		wings3d
Version: 	0.99.01
Release: 	%mkrel 1
License: 	BSD-like
Group: 		Graphics
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Url: 		http://www.wings3d.com
Source0: 	http://prdownloads.sourceforge.net/wings/%{oname}-%{version}.tar.bz2
Source1:   	%{name}.png
Source2:	%{name}_manual1.6.1.pdf
Source3:	wingspov-0.98.28_v1.tgz
Patch0:		%{oname}-0.99.01-accel-optflags.patch
Patch2:		%{oname}-0.99.01-plugins_src-makefile.patch
BuildRequires:	erlang-compiler
BuildRequires:	erlang-esdl-devel	>= %{esdl_ver}-4
BuildRequires:	imagemagick
BuildRequires:	libjpeg-devel
Requires:	erlang-esdl		>= %{esdl_ver}-4

%description
Wings 3D is a free and open source polygon mesh subdivision 
modeller inspired by Nendo and Mirai from Izware, all using 
the winged edge data structure.Wings 3D is ideally suited for 
modeling and texturing low to medium density polygon meshes. 
It has a wide range of very effective tools optimised for these 
tasks hidden behind its 'minimalistic' interface.

%package povray
Summary:	Povray import/export plug-in for Wings 3D
Group:		Graphics
Requires:	%{name} = %{version}-%{release}
Requires:	povray

%description povray
Povray import/export plug-in for Wings 3D.


%prep
%setup -qn %{oname}-%{version}
%patch0 -p1
%patch2 -p1

tar zxf %{SOURCE3}

%build
export CFLAGS="%{optflags}"
export PATH=%{erlangdir}/bin:$PATH
export ESDL_PATH=%{erlangdir}/lib/esdl-0.96.0626

%(echo %make|perl -pe 's/-j\d+/-j1/g')

%install
rm -rf %{buildroot}

install -d -m 755 %{buildroot}/%{wingsdir}
cat %{SOURCE2} > ./%{name}_manual1.6.1.pdf

# remove unneeded files
rm -rf src/*.erl

# install files, also those missing
mv -f ebin %{buildroot}/%{wingsdir}
mv -f fonts_src/*.beam %{buildroot}/%{wingsdir}/ebin/
mv -f icons/*.beam %{buildroot}/%{wingsdir}/ebin/
mv -f intl_tools/*.beam %{buildroot}/%{wingsdir}/ebin/
mv -f fonts %{buildroot}/%{wingsdir}
mv -f plugins %{buildroot}/%{wingsdir}
mv -f plugins_src/commands/*.lang %{buildroot}/%{wingsdir}/plugins/commands/
mv -f plugins_src/import_export/*.lang %{buildroot}/%{wingsdir}/plugins/import_export/
mv -f plugins_src/primitives/*.lang %{buildroot}/%{wingsdir}/plugins/primitives/
mv -f plugins_src/*.lang %{buildroot}/%{wingsdir}/plugins/
mv -f src %{buildroot}/%{wingsdir}
mv -f vsn.mk %{buildroot}/%{wingsdir}

# executable script
install -d -m 755 %{buildroot}/%{_bindir}

cat > %{buildroot}/%{_bindir}/%{name} << "EOF"
#!/bin/sh
export ESDL_PATH=%{esdldir}
erl -pa $ESDL_PATH/ebin %{wingsdir}/ebin -noinput -smp disable -run wings_start start_halt "$@"
EOF

# icons
install -d %{buildroot}%{_iconsdir}/hicolor/{16x16,32x32,48x48}/apps
convert %{SOURCE1} -size 16x16 %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png
convert %{SOURCE1} -size 32x32 %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
convert %{SOURCE1} -size 48x48 %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png

# menu
mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << EOF
[Desktop Entry]
Name=Wings 3D
Comment=%{summary}
Exec=%{_bindir}/%{name} 
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=true
Categories=Graphics;3DGraphics;
EOF

%post
%{update_menus}
%update_icon_cache hicolor

%postun
%{clean_menus}
%clean_icon_cache hicolor

%clean
rm -rf %{buildroot}

%files
%defattr(644,root,root,755)
%doc AUTHORS license.terms README
%doc *.pdf NOTES
%attr(755,root,root) %{_bindir}/*
%{wingsdir}
%{_iconsdir}/hicolor/*/apps/%{name}.png
%{_datadir}/applications/*.desktop
%exclude %{wingsdir}/plugins/import_export/kayos_utils.beam
%exclude %{wingsdir}/plugins/import_export/pov_exp.beam
%exclude %{wingsdir}/plugins/import_export/pov_ui.beam
%exclude %{wingsdir}/plugins/import_export/wpc_pov.beam

%files povray
%defattr(644,root,root,755)
%{wingsdir}/plugins/import_export/kayos_utils.beam
%{wingsdir}/plugins/import_export/pov_exp.beam
%{wingsdir}/plugins/import_export/pov_ui.beam
%{wingsdir}/plugins/import_export/wpc_pov.beam
