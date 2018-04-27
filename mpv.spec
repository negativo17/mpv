#Todo
#Checking for VapourSynth filter bridge (Python)    : no ('vapoursynth >= 24 vapoursynth-script >= 23' not found)
#Checking for VapourSynth filter bridge (Lazy Lua)  : no ('vapoursynth >= 24' not found)
#Checking for VapourSynth filter bridge (core)      : not found any of vapoursynth-lazy, vapoursynth

Name:           mpv
Version:        0.28.2
Release:        1%{?dist}
Epoch:          1
Summary:        Movie player playing most video formats and DVDs
License:        GPLv2+ and LGPLv2+
URL:            http://%{name}.io/

Source0:        https://github.com/%{name}-player/%{name}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch0:         %{name}-config.patch
Patch1:         %{name}-do-not-fail-with-minor-ffmpeg-updates.patch

BuildRequires:  desktop-file-utils
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  luajit-devel
BuildRequires:  perl(Encode)
BuildRequires:  perl(Math::BigInt)
BuildRequires:  perl(Math::BigRat)
BuildRequires:  python-docutils
BuildRequires:  waf

%if 0%{?fedora}
BuildRequires:  rst2pdf
%endif

%ifarch x86_64
BuildRequires:  nvidia-driver-devel
BuildRequires:  cuda-devel >= 7.5
%endif

BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(caca) >= 0.99.beta18
BuildRequires:  pkgconfig(dvdnav)
BuildRequires:  pkgconfig(dvdread)
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(jack)
BuildRequires:  pkgconfig(lcms2)
BuildRequires:  pkgconfig(libarchive) >= 3.0.0
BuildRequires:  pkgconfig(libavcodec) >= 58.7.100
BuildRequires:  pkgconfig(libavfilter) >= 7.0.101
BuildRequires:  pkgconfig(libavformat) >= 58.0.102
BuildRequires:  pkgconfig(libavutil) >= 56.6.100
BuildRequires:  pkgconfig(libass)
BuildRequires:  pkgconfig(libbluray)
BuildRequires:  pkgconfig(libcdio)
BuildRequires:  pkgconfig(libcdio_paranoia)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(libswresample) >= 3.0.100
BuildRequires:  pkgconfig(libswscale) >= 5.0.101
BuildRequires:  pkgconfig(libv4l2)
BuildRequires:  pkgconfig(libva)
BuildRequires:  pkgconfig(openal) >= 1.13
BuildRequires:  pkgconfig(rubberband)
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(smbclient)
BuildRequires:  pkgconfig(uchardet)
BuildRequires:  pkgconfig(vdpau)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xinerama)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  pkgconfig(xscrnsaver)
BuildRequires:  pkgconfig(xv)
BuildRequires:  pkgconfig(zlib)

%if 0%{?fedora}
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-cursor)
BuildRequires:  pkgconfig(wayland-egl)
BuildRequires:  pkgconfig(wayland-scanner)
%endif

%if 0%{?fedora} || 0%{?rhel} ==7
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils
%endif

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

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
export CFLAGS="%{optflags} -I%{_includedir}/cuda"
export CCFLAGS="%{optflags} -I%{_includedir}/cuda"
waf configure \
    --bindir=%{_bindir} \
    --confdir=%{_sysconfdir}/%{name} \
    --disable-build-date \
    --docdir=%{_docdir}/%{name} \
    --enable-cplugins \
    --enable-dvbin \
    --enable-encoding \
    --enable-libarchive \
    --enable-libmpv-shared \
    --enable-html-build \
    --enable-openal \
%if 0%{?fedora}
    --enable-pdf-build \
%endif
    --enable-sdl2 \
    --libdir=%{_libdir} \
    --mandir=%{_mandir} \
    --prefix=%{_prefix}

waf build %{?_smp_mflags}

%install
waf install --destdir=%{buildroot}

desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop
install -Dpm 644 README.md etc/input.conf etc/mpv.conf -t %{buildroot}%{_docdir}/%{name}

%post
%if 0%{?rhel} ==7
/usr/bin/update-desktop-database &> /dev/null || :
/bin/touch --no-create %{_datadir}/icons/hicolor &> /dev/null || :
%endif

%postun
%if 0%{?rhel} ==7
/usr/bin/update-desktop-database &> /dev/null || :
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &> /dev/null || :
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :
%endif

%ldconfig_scriptlets libs

%files
%docdir %{_docdir}/%{name}
%{_docdir}/%{name}
%license LICENSE.* Copyright RELEASE_NOTES
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}*.*
%{_mandir}/man1/%{name}.*
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/encoding-profiles.conf

%files libs
%license LICENSE.* Copyright RELEASE_NOTES
%{_libdir}/libmpv.so.*

%files libs-devel
%{_includedir}/%{name}
%{_libdir}/libmpv.so
%{_libdir}/pkgconfig/mpv.pc

%changelog
* Thu Apr 26 2018 Simone Caronni <negativo17@gmail.com> - 1:0.28.2-1
- Update to 0.28.2.
- Update SPEC file.

* Wed Apr 11 2018 Simone Caronni <negativo17@gmail.com> - 1:0.27.2-1
- Update to 0.27.2.

* Thu Oct 26 2017 Simone Caronni <negativo17@gmail.com> - 1:0.27.0-1
- Update to 0.27.0.

* Tue Oct 03 2017 Simone Caronni <negativo17@gmail.com> - 1:0.26.0-2
- Enable DVB support that had been disabled by default in mpv 0.26 (thanks Jens
  Peters).
- Sort build requirements.

* Tue Sep 12 2017 Simone Caronni <negativo17@gmail.com> - 1:0.26.0-1
- Update to 0.26.0.

* Thu Jun 08 2017 Simone Caronni <negativo17@gmail.com> - 1:0.25.0-2
- Enable C plugins.

* Thu Jun 01 2017 Simone Caronni <negativo17@gmail.com> - 1:0.25.0-1
- Update to 0.25.0.
- Adjust epoch requirements.
- Require at least FFmpeg 3.3 to build, for dynamic CUDA loading.

* Thu Mar 23 2017 Simone Caronni <negativo17@gmail.com> - 1:0.24.0-2
- Rebuild for libbluray update.

* Tue Feb 14 2017 Simone Caronni <negativo17@gmail.com> - 1:0.24.0-1
- Update to 0.24.0.
- Disable CUDA support until FFmpeg 3.4, it does not work without the new
  dynamic CUDA library loading introduced in FFmpeg 3.4.

* Tue Jan 03 2017 Simone Caronni <negativo17@gmail.com> - 1:0.23.0-1
- Update to 0.23.0.
- Bump up FFmpeg build requirements to pull in newest FFmpeg at build time.

* Tue Nov 29 2016 Simone Caronni <negativo17@gmail.com> - 1:0.22.0-3
- Patch so minimal updates to FFmpeg will not require a rebuild

* Tue Nov 29 2016 Simone Caronni <negativo17@gmail.com> - 1:0.22.0-2
- MPV triggers a warning even if the sahred object major version to which it is
  linked against is the same. Rebuild for FFMpeg 3.2.1.

* Fri Nov 25 2016 Simone Caronni <negativo17@gmail.com> - 1:0.22.0-1
- Update to 0.22.0.

* Fri Nov 11 2016 Simone Caronni <negativo17@gmail.com> - 1:0.21.0-1
- Update to 0.21.0, enable CUDA support for x86_64.

* Wed Sep 14 2016 Simone Caronni <negativo17@gmail.com> - 1:0.20.0-2
- Adjust Lua build requirements.

* Sat Aug 27 2016 Simone Caronni <negativo17@gmail.com> - 1:0.20.0-1
- Update to 0.20.0, update build requirements.
- Enable building on CentOS/RHEL 7.
- Enable PDF/HTML docs.
- Enable libarchive, OpenAL, Colour Ascii Art (caca) support.
- Do not run update-desktop-database on Fedora 25+ as per packaging guidelines.

* Wed Aug 17 2016 Simone Caronni <negativo17@gmail.com> - 1:0.19.0-1
- Update to 0.19.0, bump Epoch.

* Sat Jul 30 2016 Julian Sikorski <belegdol@fedoraproject.org> - 0.18.1-2
- Rebuilt for ffmpeg-3.1.1

* Tue Jul 26 2016 Miro Hrončok <mhroncok@redhat.com> - 0.18.1-1
- Update to 0.18.1
- Remove patch for Fedora < 22

* Sun Jul 03 2016 Sérgio Basto <sergio@serjux.com> - 0.18.0-3
- BRs in alphabetical order, rename of sub-packages libs and other improvements

* Thu Jun 30 2016 Sérgio Basto <sergio@serjux.com> - 0.18.0-2
- Add BR perl(Encode) to build on F24 (merge from Adrian Reber PR)

* Tue Jun 28 2016 Sérgio Basto <sergio@serjux.com> - 0.18.0-1
- Update to 0.18.0
