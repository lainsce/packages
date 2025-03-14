%global DEPOT_COMMIT 1f511020737b695f4cbb3260fdaef78a29acdd35
%global commit d010bcca8659825705dd34061d7e1bfc7ea81934

%global builddir out/Release
%global headlessbuilddir out/Headless
%global remotingbuilddir out/Remoting

%global _chromiumver 109.0.5375.1
Name:           electron
Version:        20.3.3
Release:        %autorelease
Summary:        Build cross-platform desktop apps with JavaScript, HTML, and CSS
URL:            https://electronjs.org
# Source0:        https://chromium.googlesource.com/chromium/src.git/+archive/refs/tags/%{_chromiumver}.tar.gz
# Source0:        https://commondatastorage.googleapis.com/chromium-browser-official/chromium-%{_chromiumver}.tar.xz
Source0:        https://github.com/electron/electron/archive/refs/tags/v%{version}.tar.gz
Source1:        https://chromium.googlesource.com/chromium/tools/depot_tools.git/+archive/%{DEPOT_COMMIT}.tar.gz

# nodejs source
Source3:        https://github.com/nodejs/node/archive/refs/tags/v19.0.0.tar.gz

Requires:       ffmpeg gtk3 libevent libxslt minizip nss re2 snappy c-ares
License:        MIT
BuildRequires:  clang
BuildRequires:  dbus-devel
BuildRequires:  gperf
BuildRequires:  gtk3-devel
BuildRequires:  libnotify-devel
BuildRequires:  libgnome-keyring-devel
BuildRequires:  libcap-devel
BuildRequires:  cups-devel
BuildRequires:  libXtst-devel
BuildRequires:  alsa-lib-devel
BuildRequires:  libXrandr-devel
BuildRequires:  nss-devel
BuildRequires:  python-dbusmock
BuildRequires:  git-core
BuildRequires:  python3.7
BuildRequires:  python3-httplib2
BuildRequires:  nodejs
BuildRequires:  libcxx-devel
BuildRequires:  libcxxabi-devel
BuildRequires:	gcc-c++

BuildRequires:	alsa-lib-devel
BuildRequires:	atk-devel
BuildRequires:	bison
BuildRequires:	cups-devel
BuildRequires:	dbus-devel
BuildRequires:	desktop-file-utils
BuildRequires:	expat-devel
BuildRequires:	flex
BuildRequires:	fontconfig-devel
BuildRequires:	glib2-devel
BuildRequires:	glibc-devel
BuildRequires:	gperf
BuildRequires:	libusb-compat-0.1-devel
BuildRequires:	libutempter-devel
BuildRequires:	libXdamage-devel
BuildRequires:	libXtst-devel
BuildRequires:	xcb-proto
BuildRequires:	mesa-libgbm-devel

BuildRequires:  libstdc++-static
BuildRequires:	libstdc++-devel, openssl-devel
BuildRequires:	bzip2-devel
BuildRequires:	dbus-glib-devel
BuildRequires:	elfutils
BuildRequires:	elfutils-libelf-devel
BuildRequires:	flac-devel
BuildRequires:  libva-devel
%description
The Electron framework lets you write cross-platform desktop applications using JavaScript, HTML and CSS. It is based on Node.js and Chromium and is used by the Atom editor and many other apps.

%prep
%setup -q -T -c -n depot_tools -a 1
#git clone --depth 1 https://chromium.googlesource.com/chromium/src.git --branch %_chromiumver %{_builddir}/chromium-%{_chromiumver}
# %%autosetup -c chromium-%{_chromiumver} -p1 -v

# pushd %{_builddir}/chromium-%{_chromiumver}

# # git checkout %{_chromiumver}

# # export PATH=%{_builddir}/depot_tools:$PATH
# # mkdir -p %{_builddir}/electron
# # pushd %{_builddir}/electron

# mkdir -p electron
# tar -xvf %{SOURCE1} --strip-components=1 -C electron



# popd

cd %{_builddir}
echo $PWD
#%{_builddir}/depot_tools/gclient config -v --name "src" --unmanaged https://chromium.googlesource.com/chromium/src
#%{_builddir}/depot_tools/gclient sync --force -v --nohooks --shallow --deps=linux
%{_builddir}/depot_tools/gclient config -vvv --name "src/electron" --unmanaged https://github.com/electron/electron@%{version}
%{_builddir}/depot_tools/gclient sync --force -vvv --nohooks --with_branch_heads --with_tags --deps=linux

#mkdir -p third_party/electron_node
#tar -xvf %{SOURCE3} --strip-components=1 -C third_party/electron_node


%build
cd %{_builddir}/src


# build/landmines.py
# build/util/lastchange.py -o build/util/LASTCHANGE
# electron/script/apply_all_patches.py \
#     electron/patches/config.json

export CC="gcc"
export CXX="g++"
export AR="ar"
export RANLIB="ranlib"
# gclient sync -f -v

export CHROMIUM_BUILDTOOLS_PATH=`pwd`/buildtools

build/landmines.py
build/util/lastchange.py -o build/util/LASTCHANGE

%{_builddir}/depot_tools/download_from_google_storage.py \
    --no_resume --extract --no_auth --bucket chromium-nodejs \
    -s third_party/node/node_modules.tar.gz.sha1

CHROMIUM_CORE_GN_DEFINES=""
CHROMIUM_CORE_GN_DEFINES+=' is_debug=false dcheck_always_on=false dcheck_is_configurable=false'
%ifarch x86_64 aarch64
CHROMIUM_CORE_GN_DEFINES+=' system_libdir="lib64"'
%endif
#CHROMIUM_CORE_GN_DEFINES+=' ffmpeg_branding="ChromeOS" proprietary_codecs=true'
CHROMIUM_CORE_GN_DEFINES+=' use_custom_libcxx=false'
CHROMIUM_CORE_GN_DEFINES+=' enable_ppapi=true'
CHROMIUM_CORE_GN_DEFINES+=' is_clang=false use_sysroot=false disable_fieldtrial_testing_config=true use_lld=false rtc_enable_symbol_export=true'
#CHROMIUM_CORE_GN_DEFINES+=' exec_script_whitelist=exec_script_whitelist+["//electron/BUILD.gn"]'
# allow //electron to use exec_script
echo '   + ["//electron/BUILD.gn"]' >> .gn

# remove first line of .gn
# sed -i '1d' .gn
# sed -i 's|import("//third_party/angle/dotfile_settings.gni")||g' .gn
# sed -i 's|angle_dotfile_settings.exec_script_whitelist +||g' .gn

# CHROMIUM_CORE_GN_DEFINES+=' is_official_build=true use_thin_lto=false is_cfi=false chrome_pgo_phase=0 use_debug_fission=true'
#sed -i 's|OFFICIAL_BUILD|GOOGLE_CHROME_BUILD|g' tools/generate_shim_headers/generate_shim_headers.py

export CHROMIUM_CORE_GN_DEFINES


CHROMIUM_BROWSER_GN_DEFINES=""
CHROMIUM_BROWSER_GN_DEFINES+=' use_gio=true use_pulseaudio=true icu_use_data_file=true'
CHROMIUM_BROWSER_GN_DEFINES+=' enable_nacl=false'
CHROMIUM_BROWSER_GN_DEFINES+=' enable_widevine=true'
CHROMIUM_BROWSER_GN_DEFINES+=' use_vaapi=true'

export CHROMIUM_BROWSER_GN_DEFINES

mkdir -p third_party/node/linux/node-linux-x64/bin
ln -sf %{_bindir}/node third_party/node/linux/node-linux-x64/bin/node

sed -i 's|arm-linux-gnueabihf-|arm-linux-gnu-|g' build/toolchain/linux/BUILD.gn

%ifarch aarch64
# We don't need to cross compile while building on an aarch64 system.
sed -i 's|aarch64-linux-gnu-||g' build/toolchain/linux/BUILD.gn

# Correct the ninja file to check for aarch64, not just x86.
sed -i '/${LONG_BIT}/ a \      aarch64)\' ../depot_tools/ninja
sed -i '/aarch64)/ a \        exec "/usr/bin/ninja-build" "$@";;\' ../depot_tools/ninja
%endif

# Get rid of the pre-built eu-strip binary, it is x86_64 and of mysterious origin
rm -rf buildtools/third_party/eu-strip/bin/eu-strip
# Replace it with a symlink to the Fedora copy
ln -sf %{_bindir}/eu-strip buildtools/third_party/eu-strip/bin/eu-strip

# is_mas_build fails to build and we're not on a mac
sed -i 's|is_mas_build|is_mac|g' electron/BUILD.gn
sed -i 's|enable_ppapi|true|g' electron/BUILD.gn
# tools/gn/bootstrap/bootstrap.py -v --no-clean --gn-gen-args="$CHROMIUM_CORE_GN_DEFINES $CHROMIUM_BROWSER_GN_DEFINES $GN_EXTRA_ARGS"
mkdir -p %{builddir}
ln -sf /usr/bin/gn buildtools/linux64/gn
gn --script-executable=/usr/bin/python3 gen --args="import(\"//electron/build/args/release.gn\") $CHROMIUM_CORE_GN_DEFINES $CHROMIUM_BROWSER_GN_DEFINES $GN_EXTRA_ARGS" %{builddir}



export PATH=%{_builddir}/depot_tools:$PATH
# ln -s /usr/bin/python3.7 /usr/bin/python
# cd src/electron
export CHROMIUM_BUILDTOOLS_PATH=`pwd`/buildtools
export CC="gcc"
export CXX="g++"
export AR="ar"
export RANLIB="ranlib"

# gn gen %{builddir} --args="import(\"//electron/build/args/release.gn\")"
ninja -C %{builddir} electron

%install
electron/script/strip-binaries.py -d out/Release
install electron ./out/Release/electron

%files
%{_bindir}/electron
%doc electron/src/README.md
%license electron/src/LICENSE

%changelog
* Sun Oct 23 2022 windowsboy111 <windowsboy111@fyralabs.com>
- Initial package