Name:           mpv
Version:        0.40.0
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
# Required by xpresent:
BuildRequires:  libXfixes-devel
BuildRequires:  meson >= 1.3.0
BuildRequires:  python3-docutils
BuildRequires:  rst2pdf

BuildRequires:  pkgconfig(alsa) >= 1.0.18
BuildRequires:  pkgconfig(caca) >= 0.99.beta18
BuildRequires:  pkgconfig(dvdnav) >= 4.2.0
BuildRequires:  pkgconfig(dvdread) >= 4.1.0
BuildRequires:  pkgconfig(egl) >= 1.4.0
BuildRequires:  pkgconfig(ffnvcodec) >= 11.1.5.1
BuildRequires:  pkgconfig(gbm) >= 17.1.0
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(jack)
BuildRequires:  pkgconfig(lcms2) >= 2.6
BuildRequires:  pkgconfig(libarchive) >= 3.4.0
BuildRequires:  pkgconfig(libavcodec) >= 60.31.102
BuildRequires:  pkgconfig(libavdevice) >= 60.3.100
BuildRequires:  pkgconfig(libavfilter) >= 9.12.100
BuildRequires:  pkgconfig(libavformat) >= 60.16.100
BuildRequires:  pkgconfig(libavutil) >= 58.29.100
BuildRequires:  pkgconfig(libass) >= 0.12.2
BuildRequires:  pkgconfig(libbluray) >= 0.3.0
BuildRequires:  pkgconfig(libcdio) >= 0.90
BuildRequires:  pkgconfig(libcdio_paranoia)
BuildRequires:  pkgconfig(libdisplay-info) >= 0.1.1
BuildRequires:  pkgconfig(libdrm) >= 2.4.105
BuildRequires:  pkgconfig(libjpeg)
BuildRequires:  pkgconfig(libpipewire-0.3) >= 0.3.57
BuildRequires:  pkgconfig(libplacebo) >= 6.338.2
BuildRequires:  pkgconfig(libpulse) >= 1.0
BuildRequires:  pkgconfig(libsixel) >= 1.5
BuildRequires:  pkgconfig(libswresample) >= 4.12.100
BuildRequires:  pkgconfig(libswscale) >= 7.5.100
BuildRequires:  pkgconfig(libv4l2)
BuildRequires:  pkgconfig(libva) >= 1.1.0
BuildRequires:  pkgconfig(libva-drm) >= 1.1.0
BuildRequires:  pkgconfig(libva-x11) >= 1.1.0
BuildRequires:  pkgconfig(libva-wayland) >= 1.1.0
BuildRequires:  pkgconfig(lua-5.1)
BuildRequires:  pkgconfig(mujs) >= 1.0.0
BuildRequires:  pkgconfig(openal) >= 1.13
BuildRequires:  pkgconfig(rubberband) >= 3.0.0
BuildRequires:  pkgconfig(sdl2)
#BuildRequires:  pkgconfig(shaderc)
#BuildRequires:  pkgconfig(sndio) >= 1.9.0
#BuildRequires:  pkgconfig(spirv-cross-c-shared)
BuildRequires:  pkgconfig(uchardet)
BuildRequires:  pkgconfig(vapoursynth) >= 56
BuildRequires:  pkgconfig(vapoursynth-script) >= 56
BuildRequires:  pkgconfig(vdpau) >= 0.2
BuildRequires:  pkgconfig(vulkan) >= 1.3.238
BuildRequires:  pkgconfig(wayland-client) >= 1.21.0
BuildRequires:  pkgconfig(wayland-cursor) >= 1.21.0
BuildRequires:  pkgconfig(wayland-egl) >= 9.0.0
BuildRequires:  pkgconfig(wayland-protocols) >= 1.31
BuildRequires:  pkgconfig(wayland-scanner)
BuildRequires:  pkgconfig(x11) >= 1.0.0
BuildRequires:  pkgconfig(xext) >= 1.0.0
BuildRequires:  pkgconfig(xinerama) >= 1.0.0
BuildRequires:  pkgconfig(xkbcommon) >= 0.3.0
BuildRequires:  pkgconfig(xpresent) >= 1.0.0
BuildRequires:  pkgconfig(xrandr) >= 1.4.0
BuildRequires:  pkgconfig(xscrnsaver) >= 1.0.0
BuildRequires:  pkgconfig(xv)
BuildRequires:  pkgconfig(zimg) >= 2.9
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(mujs) >= 1.0.0
BuildRequires:  pkgconfig(wayland-egl) >= 9.0.0

Requires:           bash-completion
Requires(post):     desktop-file-utils
Requires(postun):   desktop-file-utils
Requires:           hicolor-icon-theme

Provides:       mplayer-backend

Obsoletes:      mpv-zsh < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       mpv-zsh = %{?epoch:%{epoch}:}%{version}-%{release}

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

%package        devel
Summary:        Development package for libmpv
Requires:       mpv-libs%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       mpv-libs-devel = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      mpv-libs-devel < %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       pkgconfig

%description    devel
Libmpv development header files and libraries.

%prep
%autosetup -p1

%build
# Must explicitly disable all the stuff for other OSes (!):
%meson \
  -D alsa=enabled \
  -D avfoundation=disabled \
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
  -D dmabuf-wayland=enabled \
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
  -D lua=enabled \
  -D macos-10-15-4-features=disabled \
  -D macos-11-features=disabled \
  -D macos-11-3-features=disabled \
  -D macos-12-features=disabled \
  -D macos-cocoa-cb=disabled \
  -D macos-media-player=disabled \
  -D macos-touchbar=disabled \
  -D manpage-build=enabled \
  -D openal=enabled \
  -D opensles=disabled \
  -D oss-audio=disabled \
  -D pdf-build=enabled \
  -D pipewire=enabled \
  -D plain-gl=enabled \
  -D pulse=enabled \
  -D rubberband=enabled \
  -D sdl2-audio=enabled \
  -D sdl2-gamepad=enabled \
  -D sdl2=enabled \
  -D sdl2-video=enabled \
  -D shaderc=disabled \
  -D sixel=enabled \
  -D sndio=disabled \
  -D spirv-cross=disabled \
  -D swift-build=disabled \
  -D uchardet=enabled \
  -D vaapi-drm=enabled \
  -D vaapi=enabled \
  -D vaapi-wayland=enabled \
  -D vaapi-win32=disabled \
  -D vaapi-x11=enabled \
  -D vapoursynth=enabled \
  -D vdpau-gl-x11=enabled \
  -D vdpau=enabled \
  -D vector=enabled \
  -D videotoolbox-gl=disabled \
  -D videotoolbox-pl=disabled \
  -D vulkan=enabled \
  -D wasapi=disabled \
  -D wayland=enabled \
  -D win32-threads=disabled \
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
%{_datadir}/icons/hicolor/*/apps/%{name}*.*
%{_metainfodir}/%{name}.metainfo.xml
%{_mandir}/man1/%{name}.*
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/encoding-profiles.conf
%{bash_completions_dir}/%{name}
%{fish_completions_dir}/%{name}.fish
%{zsh_completions_dir}/_%{name}

%files libs
%license LICENSE.* Copyright
%{_libdir}/libmpv.so.*

%files devel
%{_includedir}/%{name}
%{_libdir}/libmpv.so
%{_libdir}/pkgconfig/mpv.pc

%changelog
* Mon Mar 31 2025 Simone Caronni <negativo17@gmail.com> - 1:0.40.0-1
- Update to 0.40.0.
- Update shell completion installation.

* Wed Oct 16 2024 Simone Caronni <negativo17@gmail.com> - 1:0.39.0-1
- Update to 0.39.0.

* Wed Apr 24 2024 Simone Caronni <negativo17@gmail.com> - 1:0.38.0-1
- Update to 0.38.0.
- Momentarily disable shaderc as it's not compatible with version 2024+.

* Thu Apr 04 2024 Simone Caronni <negativo17@gmail.com> - 1:0.37.0-1
- Update to 0.37.0.

* Wed Feb 07 2024 Simone Caronni <negativo17@gmail.com> - 1:0.36.0-2
- Rename libs-devel subpackage to devel.

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
