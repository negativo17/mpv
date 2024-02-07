Name:           mpv
Version:        0.34.1
Release:        5%{?dist}
Epoch:          1
Summary:        Movie player playing most video formats and DVDs
License:        GPLv2+ and LGPLv2+
URL:            http://%{name}.io/

Source0:        https://github.com/%{name}-player/%{name}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  desktop-file-utils
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  luajit-devel
BuildRequires:  perl(Encode)
BuildRequires:  perl(Math::BigInt)
BuildRequires:  perl(Math::BigRat)
BuildRequires:  python3-docutils
BuildRequires:  waf

BuildRequires:  pkgconfig(alsa) >= 1.0.18
BuildRequires:  pkgconfig(caca) >= 0.99.beta18
BuildRequires:  pkgconfig(dvdnav) >= 4.2.0
BuildRequires:  pkgconfig(dvdread) >= 4.1.0
BuildRequires:  pkgconfig(egl) >= 1.5
BuildRequires:  pkgconfig(ffnvcodec) >= 8.2.15.7
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(jack)
BuildRequires:  pkgconfig(lcms2) >= 2.6
BuildRequires:  pkgconfig(libavcodec) >= 58.16.100
BuildRequires:  pkgconfig(libavdevice) >= 58.0.0
BuildRequires:  pkgconfig(libavfilter) >= 7.14.100
BuildRequires:  pkgconfig(libavformat) >= 58.9.100
BuildRequires:  pkgconfig(libavutil) >= 56.12.100
BuildRequires:  pkgconfig(libass) >= 0.12.1
BuildRequires:  pkgconfig(libbluray) >= 0.3.0
BuildRequires:  pkgconfig(libcdio)
BuildRequires:  pkgconfig(libcdio_paranoia)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libpulse) >= 1.0
BuildRequires:  pkgconfig(libswresample) >= 3.0.100
BuildRequires:  pkgconfig(libswscale) >= 5.0.101
BuildRequires:  pkgconfig(libv4l2)
BuildRequires:  pkgconfig(libva) >= 1.1.0
BuildRequires:  pkgconfig(libva-drm) >= 1.1.0
BuildRequires:  pkgconfig(libva-x11) >= 1.1.0
BuildRequires:  pkgconfig(libva-wayland) >= 1.1.0
BuildRequires:  pkgconfig(openal) >= 1.13
BuildRequires:  pkgconfig(rubberband) >= 1.8.0
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(smbclient)
BuildRequires:  pkgconfig(uchardet)
BuildRequires:  pkgconfig(vapoursynth) >= 24
BuildRequires:  pkgconfig(vapoursynth-script) >= 23
BuildRequires:  pkgconfig(vdpau) >= 0.2
BuildRequires:  pkgconfig(vulkan)
BuildRequires:  pkgconfig(wayland-client) >= 1.15.0
BuildRequires:  pkgconfig(wayland-cursor) >= 1.15.0
BuildRequires:  pkgconfig(wayland-scanner)
BuildRequires:  pkgconfig(x11) >= 1.0.0
BuildRequires:  pkgconfig(xext) >= 1.0.0
BuildRequires:  pkgconfig(xinerama) >= 1.0.0
BuildRequires:  pkgconfig(xkbcommon) >= 0.3.0
BuildRequires:  pkgconfig(xrandr) >= 1.2.0
BuildRequires:  pkgconfig(xscrnsaver) >= 1.0.0
BuildRequires:  pkgconfig(xv)
BuildRequires:  pkgconfig(zimg) >= 2.9
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(mujs) >= 1.0.0
BuildRequires:  pkgconfig(wayland-egl) >= 9.0.0
BuildRequires:  pkgconfig(wayland-protocols) >= 1.14

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

%package        devel
Summary:        Development package for libmpv
Requires:       mpv-libs%{_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       mpv-libs-devel = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      mpv-libs-devel < %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       pkgconfig

%description    devel
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
waf configure \
    --bindir=%{_bindir} \
    --confdir=%{_sysconfdir}/%{name} \
    --disable-build-date \
    --docdir=%{_docdir}/%{name} \
    --enable-cdda \
    --enable-cplugins \
    --enable-dvbin \
    --enable-dvdnav \
    --enable-gl-x11 \
    --enable-libmpv-shared \
    --enable-html-build \
    --enable-openal \
    --enable-sdl2 \
    --libdir=%{_libdir} \
    --mandir=%{_mandir} \
    --prefix=%{_prefix}

waf build %{?_smp_mflags}

%install
waf install --destdir=%{buildroot}

desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop
install -Dpm 644 README.md etc/input.conf etc/mpv.conf -t %{buildroot}%{_docdir}/%{name}

%files
%license LICENSE.* Copyright RELEASE_NOTES
%docdir %{_docdir}/%{name}
%{_docdir}/%{name}
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/bash-completion/completions/%{name}
%{_datadir}/icons/hicolor/*/apps/%{name}*.*
%{_mandir}/man1/%{name}.*
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/encoding-profiles.conf

%files libs
%license LICENSE.* Copyright RELEASE_NOTES
%{_libdir}/libmpv.so.*

%files devel
%{_includedir}/%{name}
%{_libdir}/libmpv.so
%{_libdir}/pkgconfig/mpv.pc

%files zsh
%{_datadir}/zsh/site-functions/_%{name}

%changelog
* Wed Feb 07 2024 Simone Caronni <negativo17@gmail.com> - 1:0.34.1-5
- Rename libs-devel subpackage to devel.

* Sun Feb 12 2023 Simone Caronni <negativo17@gmail.com> - 1:0.34.1-4
- First build on el8.
- Trim changelog.

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
