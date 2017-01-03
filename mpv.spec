#Todo
#Checking for VapourSynth filter bridge (Python)    : no ('vapoursynth >= 24 vapoursynth-script >= 23' not found)
#Checking for VapourSynth filter bridge (Lazy Lua)  : no ('vapoursynth >= 24' not found)
#Checking for VapourSynth filter bridge (core)      : not found any of vapoursynth-lazy, vapoursynth

Name:           mpv
Version:        0.22.0
Release:        3%{?dist}
Epoch:          1
Summary:        Movie player playing most video formats and DVDs
License:        GPLv2+
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

%if 0%{?rhel} ==7
BuildRequires:  ffmpeg
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
BuildRequires:  pkgconfig(enca)
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(jack)
BuildRequires:  pkgconfig(lcms2)
BuildRequires:  pkgconfig(libarchive) >= 3.0.0
BuildRequires:  pkgconfig(libavcodec) >= 56.1.0
BuildRequires:  pkgconfig(libavformat) >= 56.01.0
BuildRequires:  pkgconfig(libavutil) >= 54.02.0
BuildRequires:  pkgconfig(libass)
BuildRequires:  pkgconfig(libbluray)
BuildRequires:  pkgconfig(libcdio)
BuildRequires:  pkgconfig(libcdio_paranoia)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libguess)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(libswscale) >= 2.1.3
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

%if 0%{?fedora} == 24 || 0%{?fedora} == 23 || 0%{?rhel} ==7
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils
%endif

Requires:       hicolor-icon-theme

%description
Mpv is a movie player based on MPlayer and mplayer2. It supports a wide variety
of video file formats, audio and video codecs, and subtitle types. Special
input URL types are available to read input from a variety of sources other
than disk files. Depending on platform, a variety of different video and audio
output methods are supported.

%package        libs
Summary:        Dynamic library for Mpv frontends 
Provides:       libmpv = %{?epoch}:%{version}-%{release}
Obsoletes:      libmpv < %{?epoch}:%{version}-%{release}

%description    libs
This package contains the dynamic library libmpv, which provides access to Mpv.

%package        libs-devel
Summary:        Development package for libmpv
Requires:       mpv-libs%{_isa} = %{?epoch}:%{version}-%{release}
Provides:       libmpv-devel = %{?epoch}:%{version}-%{release}
Obsoletes:      libmpv-devel < %{?epoch}:%{version}-%{release}
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
    --enable-libarchive \
    --enable-libmpv-shared \
    --enable-html-build \
    --enable-openal \
    --enable-sdl2 \
    --enable-encoding \
    --libdir=%{_libdir} \
    --mandir=%{_mandir} \
    --prefix=%{_prefix} \
%if 0%{?fedora}
    --enable-pdf-build
%endif

waf build %{?_smp_mflags}

%install
waf install --destdir=%{buildroot}

desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop
install -Dpm 644 README.md etc/input.conf etc/mpv.conf -t %{buildroot}%{_docdir}/%{name}

%post
%if 0%{?fedora} == 24 || 0%{?fedora} == 23 || 0%{?rhel} ==7
/usr/bin/update-desktop-database &> /dev/null || :
%endif
/bin/touch --no-create %{_datadir}/icons/hicolor &> /dev/null || :

%postun
%if 0%{?fedora} == 24 || 0%{?fedora} == 23 || 0%{?rhel} ==7
/usr/bin/update-desktop-database &> /dev/null || :
%endif
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &> /dev/null || :
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%docdir %{_docdir}/%{name}
%{_docdir}/%{name}
%license LICENSE Copyright
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}*.*
%{_mandir}/man1/%{name}.*
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/encoding-profiles.conf

%files libs
%license LICENSE Copyright
%{_libdir}/libmpv.so.*

%files libs-devel
%{_includedir}/%{name}
%{_libdir}/libmpv.so
%{_libdir}/pkgconfig/mpv.pc

%changelog
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
