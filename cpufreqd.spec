Summary:	Scales your cpu frequency
Summary(pl):	Skalowanie czêstotliwo¶ci procesora
Name:		cpufreqd
Version:	1.0
%define	_pre	beta1
Release:	1.%{_pre}.1
License:	GPL v2
Group:		Applications/System
Source0:	http://dl.sourceforge.net/sourceforge/%{name}/%{name}-%{version}-%{_pre}.tar.gz
# Source0-md5:	d712993e5dfbe18f7111c56127919d82
Source1:	%{name}.init
Patch0:		%{name}-am.patch
URL:		http://www.brodo.de/cpufreq/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This daemon monitors /proc/apm for the battery status and scales your
cpu frequency according to a set of rules. It is very useful for
providing maximum battery life but good cpu speed at the same time.

%description -l pl
Ten demon monitoruje stan baterii przez /proc/apm i skaluje
czêstotliwo¶æ procesora zgodnie z zestawem regu³. Jest bardzo
przydatny do zapewniania maksymalnego czasu ¿ycia baterii, a
jednocze¶nie dobrej szybko¶ci procesora.

%prep
%setup -q -n %{name}-%{version}-%{_pre}
%patch0 -p1

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
install -d $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/%{name}
install *.conf $RPM_BUILD_ROOT%{_sysconfdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add cpufreqd
if [ -f /var/lock/subsys/cpufreqd ]; then
	/etc/rc.d/init.d/cpufreqd restart >&2
else
	echo "Run \"/etc/rc.d/init.d/cpufreqd start\" to start CPU FREQ daemon."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/cpufreqd ]; then
		/etc/rc.d/init.d/cpufreqd stop>&2
	fi
	/sbin/chkconfig --del cpufreqd
fi

%files
%defattr(644,root,root,755)
%doc README TODO
%attr(754,root,root) %{_bindir}/*
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/*.conf
%{_mandir}/man?/*
%attr(754,root,root) %{_sysconfdir}/rc.d/init.d/%{name}
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/*
