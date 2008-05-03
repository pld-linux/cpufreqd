# TODO:
# - loading modules in init-script, if needed
# - missing plugin: nvclock, sensors
# - move plugins into separate packages? (some is needed, because of additional deps)
Summary:	Scales your cpu frequency
Summary(pl.UTF-8):	Skalowanie częstotliwości procesora
Name:		cpufreqd
Version:	2.2.1
Release:	2
License:	GPL v2
Group:		Applications/System
Source0:	http://dl.sourceforge.net/cpufreqd/%{name}-%{version}.tar.bz2
# Source0-md5:	e66f22915c8ce609cd0c8f254da11c08
Source1:	%{name}.init
URL:		http://cpufreqd.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	cpufrequtils-devel
BuildRequires:	libtool
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	sysfsutils-devel
Requires(post):	sed >= 4.0
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This daemon monitors /proc/apm for the battery status and scales your
cpu frequency according to a set of rules. It is very useful for
providing maximum battery life but good cpu speed at the same time.

%description -l pl.UTF-8
Ten demon monitoruje stan baterii przez /proc/apm i skaluje
częstotliwość procesora zgodnie z zestawem reguł. Jest bardzo
przydatny do zapewniania maksymalnego czasu życia baterii, a
jednocześnie dobrej szybkości procesora.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--libdir=%{_libdir}/%{name}
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
if [ "$1" = 1 ]; then
	# Modify config file for 2.6
	if [ -d /sys/devices/system/cpu/cpu0/cpufreq ] ; then
		# translate percentages in integer values
		CPUFREQD_MAX_SPEED=`cat /sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_max_freq`
		CPUFREQD_MIN_SPEED=`cat /sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_min_freq`
		CPUFREQD_MHIGH_SPEED=$(( $CPUFREQD_MAX_SPEED / 100 * 66 ))
		CPUFREQD_MLOW_SPEED=$(( $CPUFREQD_MAX_SPEED / 100 * 33 ))
		sed -i -e "s/100%/$CPUFREQD_MAX_SPEED/; \
			s/66%/$CPUFREQD_MHIGH_SPEED/; \
			s/33%/$CPUFREQD_MLOW_SPEED/;  \
			s/0%/$CPUFREQD_MIN_SPEED/;" \
			%{_sysconfdir}/cpufreqd.conf
	fi
fi

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
