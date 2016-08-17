Name:           mpv
Version:        0.19.0
Release:        1%{?dist}
Epoch:          1
Summary:        Movie player playing most video formats and DVDs
License:        GPLv2+
URL:            http://%{name}.io/

Source0:        https://github.com/%{name}-player/%{name}/archive/v%{version}.tar.gz

# set defaults for Fedora
Patch0:         %{name}-config.patch

BuildRequires:  desktop-file-utils
BuildRequires:  ffmpeg-devel
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  perl(Encode)
BuildRequires:  perl(Math::BigInt)
BuildRequires:  perl(Math::BigRat)
BuildRequires:  python-docutils
BuildRequires:  waf

BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(dvdnav)
BuildRequires:  pkgconfig(dvdread)
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(enca)
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(jack)
BuildRequires:  pkgconfig(lcms2)
BuildRequires:  pkgconfig(libarchive)
BuildRequires:  pkgconfig(libass)
BuildRequires:  pkgconfig(libbluray)
BuildRequires:  pkgconfig(libcdio)
BuildRequires:  pkgconfig(libcdio_paranoia)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libguess)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(libquvi-0.9)
BuildRequires:  pkgconfig(libv4l2)
BuildRequires:  pkgconfig(libva)
BuildRequires:  pkgconfig(lua-5.1)
BuildRequires:  pkgconfig(rubberband)
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(smbclient)
BuildRequires:  pkgconfig(uchardet) >= 0.0.5
BuildRequires:  pkgconfig(vdpau)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-cursor)
BuildRequires:  pkgconfig(wayland-egl)
BuildRequires:  pkgconfig(wayland-scanner)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xinerama)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  pkgconfig(xscrnsaver)
BuildRequires:  pkgconfig(xv)
BuildRequires:  pkgconfig(zlib)

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

%build
CCFLAGS="%{optflags}" \
waf configure \
    --prefix=%{_prefix} \
    --bindir=%{_bindir} \
    --libdir=%{_libdir} \
    --mandir=%{_mandir} \
    --docdir=%{_docdir}/%{name} \
    --confdir=%{_sysconfdir}/%{name} \
    --disable-build-date \
    --enable-libmpv-shared \
    --enable-sdl2 \
    --enable-encoding

waf build %{?_smp_mflags}

%install
waf install --destdir=%{buildroot}

desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop
install -Dpm 644 README.md etc/input.conf etc/mpv.conf -t %{buildroot}%{_docdir}/%{name}

%post
/usr/bin/update-desktop-database &> /dev/null || :
/bin/touch --no-create %{_datadir}/icons/hicolor &> /dev/null || :

%postun
/usr/bin/update-desktop-database &> /dev/null || :
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
* Wed Aug 17 2016 Simone Caronni <negativo17@gmail.com> - 0.19.0-1
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
