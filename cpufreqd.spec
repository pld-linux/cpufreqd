Summary:	Scales your cpu frequency
Summary(pl):	Skalowanie czêstotliwo¶ci procesora
Name:		cpufreqd
Version:	1.0
%define	_pre	pre1
Release:	0.%{_pre}.1
License:	GPL v2
Group:		Applications/System
Source0:	http://www.staikos.net/~staikos/cpufreqd/%{name}-%{version}-%{_pre}.tar.gz
# Source0-md5:	3596674f1c36b85f7c05c8a4adf14a3d
URL:		http://www.brodo.de/cpufreq/
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
%setup  -q -n %{name}-%{version}-%{_pre}

%build
%{__make} CFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_sbindir},%{_mandir}/{man1,man5}}

install %{name} $RPM_BUILD_ROOT%{_sbindir}
install cpufreqd.conf $RPM_BUILD_ROOT%{_sysconfdir}
install *.1  $RPM_BUILD_ROOT%{_mandir}/man1
install *.5  $RPM_BUILD_ROOT%{_mandir}/man5

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README TODO
%attr(754,root,root) %{_sbindir}/*
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/*
%{_mandir}/man1/*.1*
%{_mandir}/man5/*.5*
