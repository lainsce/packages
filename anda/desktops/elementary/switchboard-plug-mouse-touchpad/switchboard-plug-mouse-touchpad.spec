%global __provides_exclude_from ^%{_libdir}/switchboard/.*\\.so$

%global srcname switchboard-plug-mouse-touchpad

%global plug_type hardware
%global plug_name mouse-touchpad
%global plug_rdnn io.elementary.switchboard.mouse-touchpad

Name:           switchboard-plug-mouse-touchpad
Summary:        Switchboard Mouse and Touchpad plug
Version:        6.1.0
Release:        %autorelease
License:        GPLv3+

URL:            https://github.com/elementary/switchboard-plug-mouse-touchpad
Source0:        %{url}/archive/%{version}/%{srcname}-%{version}.tar.gz

BuildRequires:  gettext
BuildRequires:  libappstream-glib
BuildRequires:  meson
BuildRequires:  vala >= 0.22.0

BuildRequires:  pkgconfig(glib-2.0) >= 2.32
BuildRequires:  pkgconfig(granite)
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(switchboard-2.0)
BuildRequires:  pkgconfig(libxml-2.0)

Requires:       switchboard%{?_isa}
Supplements:    switchboard%{?_isa}

%description
A switchboard plug to configure the behavior of mice and touchpads.


%prep
%autosetup -n %{srcname}-%{version} -p1


%build
%meson -Dgnome_40=true
%meson_build


%install
%meson_install

%find_lang %{plug_name}-plug


%check
appstream-util validate-relax --nonet \
    %{buildroot}/%{_datadir}/metainfo/%{plug_rdnn}.appdata.xml


%files -f %{plug_name}-plug.lang
%doc README.md
%license COPYING

%{_libdir}/switchboard/%{plug_type}/lib%{plug_name}.so

%{_datadir}/metainfo/%{plug_rdnn}.appdata.xml


%changelog
* Sat Oct 15 2022 windowsboy111 <windowsboy111@fyralabs.com>
- Repackaged for Terra
