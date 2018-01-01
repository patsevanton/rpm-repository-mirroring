%global _prefix /usr/local

Name:    rpm-repository-mirroring
Version: 0.1
#Release: 1%{?dist}
Release: 1
Summary: RPM repository mirroring script using reposync

Group:   Development Tools
License: ASL 2.0
Source0: rpm-repository-mirroring.sh

%description

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p %{buildroot}/%{_bindir}
%{__install} -m 755 %{SOURCE0} %{buildroot}/%{_bindir}/%{name}

%files
%{_bindir}/%{name}
