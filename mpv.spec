# Todo:
# - sixel support

Name:           mpv
Version:        0.36.0
Release:        1%{?dist}
Epoch:          1
Summary:        Movie player playing most video formats and DVDs
License:        GPLv2+ and LGPLv2+
URL:            http://%{name}.io/

Source0:        https://github.com/%{name}-player/%{name}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
BuildRequires:  libatomic
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  libshaderc-devel
# Required by xpresent:
BuildRequires:  libXfixes-devel
BuildRequires:  luajit-devel
BuildRequires:  meson >= 0.60.3
BuildRequires:  python3-docutils
BuildRequires:  rst2pdf

BuildRequires:  pkgconfig(alsa) >= 1.0.18
BuildRequires:  pkgconfig(caca) >= 0.99.beta18
BuildRequires:  pkgconfig(dvdnav) >= 4.2.0
BuildRequires:  pkgconfig(dvdread) >= 4.1.0
BuildRequires:  pkgconfig(egl) >= 1.5
BuildRequires:  pkgconfig(ffnvcodec) >= 11.1.5.1
BuildRequires:  pkgconfig(gbm) >= 17.1.0
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(jack)
BuildRequires:  pkgconfig(lcms2) >= 2.6
BuildRequires:  pkgconfig(libarchive) >= 3.4.0
BuildRequires:  pkgconfig(libavcodec) >= 60.3.100
BuildRequires:  pkgconfig(libavdevice) >= 60.1.100
BuildRequires:  pkgconfig(libavfilter) >= 9.3.100
BuildRequires:  pkgconfig(libavformat) >= 60.3.100
BuildRequires:  pkgconfig(libavutil) >= 58.2.100
BuildRequires:  pkgconfig(libass) >= 0.12.2
BuildRequires:  pkgconfig(libbluray) >= 0.3.0
BuildRequires:  pkgconfig(libcdio)
BuildRequires:  pkgconfig(libcdio_paranoia)
BuildRequires:  pkgconfig(libdrm) >= 2.4.75
BuildRequires:  pkgconfig(libjpeg)
BuildRequires:  pkgconfig(libpipewire-0.3) >= 0.3.48
BuildRequires:  pkgconfig(libplacebo) >= 5.264.0
BuildRequires:  pkgconfig(libpulse) >= 1.0
#BuildRequires:  pkgconfig(libsixel) >= 1.5
BuildRequires:  pkgconfig(libswresample) >= 4.10.100
BuildRequires:  pkgconfig(libswscale) >= 7.1.100
BuildRequires:  pkgconfig(libv4l2)
BuildRequires:  pkgconfig(libva) >= 1.1.0
BuildRequires:  pkgconfig(libva-drm) >= 1.1.0
BuildRequires:  pkgconfig(libva-x11) >= 1.1.0
BuildRequires:  pkgconfig(libva-wayland) >= 1.1.0
BuildRequires:  pkgconfig(lua-5.1)
BuildRequires:  pkgconfig(openal) >= 1.13
BuildRequires:  pkgconfig(rubberband) >= 1.8.0
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(shaderc)
BuildRequires:  pkgconfig(smbclient)
#BuildRequires:  pkgconfig(spirv-cross-c-shared)
BuildRequires:  pkgconfig(uchardet)
BuildRequires:  pkgconfig(vapoursynth) >= 24
BuildRequires:  pkgconfig(vapoursynth-script) >= 23
BuildRequires:  pkgconfig(vdpau) >= 0.2
BuildRequires:  pkgconfig(vulkan)
BuildRequires:  pkgconfig(wayland-client) >= 1.20.0
BuildRequires:  pkgconfig(wayland-cursor) >= 1.20.0
BuildRequires:  pkgconfig(wayland-protocols) >= 1.25
BuildRequires:  pkgconfig(wayland-scanner)
BuildRequires:  pkgconfig(x11) >= 1.0.0
BuildRequires:  pkgconfig(xext) >= 1.0.0
BuildRequires:  pkgconfig(xinerama) >= 1.0.0
BuildRequires:  pkgconfig(xkbcommon) >= 0.3.0
BuildRequires:  pkgconfig(xpresent) >= 1.0.0
BuildRequires:  pkgconfig(xrandr) >= 1.2.0
BuildRequires:  pkgconfig(xscrnsaver) >= 1.0.0
BuildRequires:  pkgconfig(xv)
BuildRequires:  pkgconfig(zimg) >= 2.9
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(mujs) >= 1.0.0
BuildRequires:  pkgconfig(wayland-egl) >= 9.0.0
BuildRequires:  pkgconfig(wayland-protocols) >= 1.15

Requires:       bash-completion
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils
Requires:       hicolor-icon-theme

Provides:       mplayer-backend

%description
Mpv is a movie player based on MPlayer and mplayer2. It supports a wide variety
of video file formats, audio and video codecs, and subtitle types. Special
input URL types are available to read input from a variety of sources other
than disk files. Depending on platform, a variety of different video and audio
output methods are supported.

%package        libs
Summary:        Dynamic library for Mpv frontends 
Provides:       libmpv = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      libmpv < %{?epoch:%{epoch}:}%{version}-%{release}

%description    libs
This package contains the dynamic library libmpv, which provides access to Mpv.

%package        libs-devel
Summary:        Development package for libmpv
Requires:       mpv-libs%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       libmpv-devel = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      libmpv-devel < %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       pkgconfig

%description    libs-devel
Libmpv development header files and libraries.

%package zsh
Summary:        zsh completion functions for MPV
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       zsh

%description zsh
zsh completion functions for MPV.

%prep
%autosetup -p1

%build
export CFLAGS="%{optflags} -I%{_includedir}/cuda"
export CCFLAGS="%{optflags} -I%{_includedir}/cuda"

# Must explicitly disable all the stuff for other OSes (!):
%meson \
  -D alsa=enabled \
  -D android-media-ndk=disabled \
  -D audiounit=disabled \
  -D build-date=true \
  -D caca=enabled \
  -D cdda=enabled \
  -D cocoa=disabled \
  -D coreaudio=disabled \
  -D cplayer=true \
  -D cplugins=enabled \
  -D cuda-hwaccel=enabled \
  -D cuda-interop=enabled \
  -D d3d11=disabled \
  -D d3d-hwaccel=disabled \
  -D d3d9-hwaccel=disabled \
  -D direct3d=disabled \
  -D drm=enabled \
  -D dvbin=enabled \
  -D dvdnav=enabled \
  -D egl-drm=enabled \
  -D egl=enabled \
  -D egl-android=disabled \
  -D egl-angle=disabled \
  -D egl-angle-lib=disabled \
  -D egl-angle-win32=disabled \
  -D egl-wayland=enabled \
  -D egl-x11=enabled \
  -D gbm=enabled \
  -D gl=enabled \
  -D gl-cocoa=disabled \
  -D gl-dxinterop=disabled \
  -D gl-dxinterop-d3d9=disabled \
  -D gl-win32=disabled \
  -D gl-x11=enabled \
  -D html-build=enabled \
  -D iconv=enabled \
  -D ios-gl=disabled \
  -D jack=enabled \
  -D javascript=enabled \
  -D jpeg=enabled \
  -D lcms2=enabled \
  -D libarchive=enabled \
  -D libavdevice=enabled \
  -D libbluray=enabled \
  -D libmpv=true \
  -D libplacebo=enabled \
  -D libplacebo-next=enabled \
  -D lua=enabled \
  -D macos-10-11-features=disabled \
  -D macos-10-12-2-features=disabled \
  -D macos-10-14-features=disabled \
  -D macos-cocoa-cb=disabled \
  -D macos-media-player=disabled \
  -D macos-touchbar=disabled \
  -D manpage-build=enabled \
  -D openal=enabled \
  -D opensles=disabled \
  -D oss-audio=disabled \
  -D pdf-build=enabled \
  -D pipewire=enabled \
  -D pulse=enabled \
  -D rpi-mmal=disabled \
  -D rubberband=enabled \
  -D sdl2-audio=enabled \
  -D sdl2-gamepad=enabled \
  -D sdl2=enabled \
  -D sdl2-video=enabled \
  -D shaderc=enabled \
  -D sixel=disabled \
  -D sndio=disabled \
  -D spirv-cross=disabled \
  -D swift-build=disabled \
  -D uchardet=enabled \
  -D vaapi-drm=enabled \
  -D vaapi=enabled \
  -D vaapi-wayland=enabled \
  -D vaapi-x11=enabled \
  -D vaapi-x-egl=enabled \
  -D vapoursynth=enabled \
  -D vdpau-gl-x11=enabled \
  -D vdpau=enabled \
  -D videotoolbox-gl=disabled \
  -D vulkan=enabled \
  -D vulkan-interop=disabled \
  -D wasapi=disabled \
  -D wayland=enabled \
  -D win32-internal-pthreads=disabled \
  -D x11=enabled \
  -D xv=enabled \
  -D zimg=enabled \
  -D zlib=enabled

%meson_build

%install
%meson_install

%check
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{name}.metainfo.xml
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

%files
%license LICENSE.* Copyright
%docdir %{_docdir}/%{name}
%{_docdir}/%{name}
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/bash-completion/completions/%{name}
%{_datadir}/icons/hicolor/*/apps/%{name}*.*
%{_metainfodir}/%{name}.metainfo.xml
%{_mandir}/man1/%{name}.*
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/encoding-profiles.conf

%files libs
%license LICENSE.* Copyright
%{_libdir}/libmpv.so.*

%files libs-devel
%{_includedir}/%{name}
%{_libdir}/libmpv.so
%{_libdir}/pkgconfig/mpv.pc

%files zsh
%{_datadir}/zsh/site-functions/_%{name}

%changelog
* Sun Oct 08 2023 Simone Caronni <negativo17@gmail.com> - 1:0.36.0-1
- Update to 0.36.0.

* Tue Apr 11 2023 Simone Caronni <negativo17@gmail.com> - 1:0.35.1-2
- Rebuild for updated dependencies.

* Sat Feb 04 2023 Simone Caronni <negativo17@gmail.com> - 1:0.35.1-1
- Update to 0.35.1.
- Switch to meson.
- Build also PDF documentation.

* Wed Apr 06 2022 Simone Caronni <negativo17@gmail.com> - 1:0.34.1-3
- Rebuild for updated dependencies.

* Sun Mar 13 2022 Simone Caronni <negativo17@gmail.com> - 1:0.34.1-2
- Rebuild for updated dependencies.

* Tue Feb 15 2022 Simone Caronni <negativo17@gmail.com> - 1:0.34.1-1
- Update to 0.34.1.

* Tue Nov 02 2021 Simone Caronni <negativo17@gmail.com> - 1:0.34.0-1
- Update to 0.34.0.

* Fri Sep 24 2021 Simone Caronni <negativo17@gmail.com> - 1:0.33.1-4
- Add patch from upstream to fix DVB build with kernel 5.14+.

* Tue Jul 27 2021 Simone Caronni <negativo17@gmail.com> - 1:0.33.1-3
- Rebuild for updated dependencies.

* Tue Apr 27 2021 Simone Caronni <negativo17@gmail.com> - 1:0.33.1-2
- Rebuild for updated FFMpeg.

* Sun Apr 11 2021 Simone Caronni <negativo17@gmail.com> - 1:0.33.1-1
- Update to 0.33.1.

* Wed Mar 24 2021 Simone Caronni <negativo17@gmail.com> - 1:0.33.0-3
- Rebuild for updated dependencies.

* Mon Mar 01 2021 Simone Caronni <negativo17@gmail.com> - 1:0.33.0-2
- Rebuild for updated dependencies.

* Mon Feb 15 2021 Simone Caronni <negativo17@gmail.com> - 1:0.33.0-1
- Update to 0.33.0.
