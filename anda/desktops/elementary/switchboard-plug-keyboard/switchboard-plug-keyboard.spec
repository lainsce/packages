%global __provides_exclude_from ^%{_libdir}/switchboard/.*\\.so$

%global srcname switchboard-plug-keyboard

%global plug_type hardware
%global plug_name keyboard
%global plug_rdnn io.elementary.switchboard.keyboard

Name:           switchboard-plug-keyboard
Summary:        Switchboard Keyboard plug
Version:        2.7.0
Release:        %autorelease
License:        GPLv3+

URL:            https://github.com/elementary/switchboard-plug-keyboard
Source0:        %{url}/archive/%{version}/%{srcname}-%{version}.tar.gz

# upstream patch to support screenshot keyboard shortcut changes in gala
Patch:          %{url}/commit/6ebd576.patch

BuildRequires:  gettext
BuildRequires:  libappstream-glib
BuildRequires:  meson
BuildRequires:  vala >= 0.22.0

BuildRequires:  pkgconfig(glib-2.0) >= 2.32
BuildRequires:  pkgconfig(granite) >= 6.0.0
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(ibus-1.0) >= 1.5.19
BuildRequires:  pkgconfig(libgnomekbd)
BuildRequires:  pkgconfig(libgnomekbdui)
BuildRequires:  pkgconfig(libhandy-1) >= 0.90.0
BuildRequires:  pkgconfig(switchboard-2.0)
BuildRequires:  pkgconfig(xkeyboard-config)

Requires:       gala
Requires:       switchboard%{?_isa}
Supplements:    switchboard%{?_isa}

%description
This plug can be used to change several keyboard settings, for example
the delay and speed of the key repetition, or the cursor blinking speed.
You can change your keyboard layout, and use multiple layouts at the
same time. Keyboard shortcuts are also part of this plug.


%prep
%autosetup -n %{srcname}-%{version} -p1


%build
%meson
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
