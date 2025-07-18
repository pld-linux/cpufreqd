#
# TODO:
#   - loading modules in init-script, if needed
#   - missing plugin: nvclock
#   - move plugins into separate packages? (some is needed, because of additional deps)
#   - update Polish translations
#
Summary:	Fully configurable daemon for dynamic frequency and voltage scaling
Summary(pl.UTF-8):	Skalowanie częstotliwości procesora
Name:		cpufreqd
Version:	2.4.2
Release:	4
License:	GPL v2
Group:		Applications/System
Source0:	http://dl.sourceforge.net/cpufreqd/%{name}-%{version}.tar.bz2
# Source0-md5:	2ca80a77849c9a69b81e27c1843c97f5
Source1:	%{name}.init
Patch0:		%{name}-battery.patch
URL:		http://www.linux.it/~malattia/wiki/index.php/Cpufreqd
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	cpufrequtils-devel
BuildRequires:	libtool
BuildRequires:	lm_sensors-devel
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	sysfsutils-devel
Requires(post):	sed >= 4.0
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A small daemon to adjust cpu speed and voltage (and not only) for
kernels using any of the cpufreq drivers available. Cpufreqd is not a
userspace governor.
Cpufreqd allows you to apply governor profiles from rules based on
battery level, ac status, temperature (ACPI or sensors), running
programs, cpu usage and (maybe) more. You can also change your nforce
FSB clock and video card frequency (NVidia only) or execute arbitrary
commands when a specific rule is applied.
You need a CPU with frequency and voltage scaling capabilities and a
Linux kernel with cpufreq support.

%description -l pl.UTF-8
Ten demon monitoruje stan baterii przez /proc/apm i skaluje
częstotliwość procesora zgodnie z zestawem reguł. Jest bardzo
przydatny do zapewniania maksymalnego czasu życia baterii, a
jednocześnie dobrej szybkości procesora.

%prep
%setup -q
%patch -P0 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--libdir=%{_libdir}/%{name} \
	--enable-sensors
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add cpufreqd
%service cpufreqd restart "CPU FREQ daemon"

%preun
if [ "$1" = "0" ]; then
	%service cpufreqd stop
	/sbin/chkconfig --del cpufreqd
fi

%files
%defattr(644,root,root,755)
%doc README TODO
%attr(754,root,root) %{_sbindir}/*
%attr(755,root,root) %{_bindir}/*
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*.conf
%{_mandir}/man?/*
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/*
