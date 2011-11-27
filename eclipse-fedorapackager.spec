%global eclipse_base   %{_libdir}/eclipse
%global install_loc    %{_datadir}/eclipse/dropins/packager

Name:           eclipse-fedorapackager
Version:        0.1.12
Release:        3
Summary:        Fedora Packager Tools

Group:          Development/Java
License:        EPL
URL:            http://fedorahosted.org/eclipse-fedorapackager
# Tar file generated from Git repository (tag 0.1.12)
# by:
#   bash get-eclipse-fedorapackager-sources.sh 0.1.12
Source0:        %{name}.tar.xz
Source1:        get-eclipse-fedorapackager-sources.sh
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch: noarch

BuildRequires: java-devel
BuildRequires: eclipse-pde >= 0:3.4.0
BuildRequires: not-yet-commons-ssl
BuildRequires: json >= 3-3
BuildRequires: eclipse-changelog
BuildRequires: eclipse-rpm-editor
BuildRequires: jakarta-commons-codec
BuildRequires: jakarta-commons-httpclient >= 3.1
BuildRequires: xmlrpc3-client
BuildRequires: xmlrpc3-common
BuildRequires: ws-commons-util
# Note: As of 0.1.10 we require >= 0.10.0 due to
# API changes.
BuildRequires: eclipse-egit >= 0.10.0
Requires: eclipse-platform >= 3.4.0
Requires: json >= 3-3
Requires: not-yet-commons-ssl
Requires: eclipse-rpm-editor
Requires: eclipse-changelog
Requires: jakarta-commons-httpclient >= 3.1
Requires: jakarta-commons-codec
Requires: xmlrpc3-client
Requires: xmlrpc3-common
Requires: ws-commons-util
# Note: As of 0.1.10 we require >= 0.10.0 due to
# API changes.
Requires: eclipse-egit >= 0.10.0

%description
Eclipse Fedora Packager is an Eclipse plug-in, which helps
Fedora contributors to interact with Fedora infrastructure
such as Koji, Bodhi and Git.

%prep
%setup -q -n eclipse-fedorapackager
rm -fr org.apache*
rm -fr org.json*
mkdir orbit
pushd orbit
ln -s %{_javadir}/xmlrpc3-client.jar
ln -s %{_javadir}/xmlrpc3-common.jar
ln -s %{_javadir}/json.jar org.json.jar
ln -s %{_javadir}/ws-commons-util.jar
ln -s %{_javadir}/not-yet-commons-ssl.jar commons-ssl.jar
popd

%build
%{eclipse_base}/buildscripts/pdebuild \
                -f org.fedoraproject.eclipse.packager \
                -o `pwd`/orbit \
                -d "rpm-editor changelog jgit egit"

%install
%{__rm} -rf %{buildroot}
install -d -m 755 %{buildroot}%{install_loc}

%{__unzip} -q -d %{buildroot}%{install_loc} \
     build/rpmBuild/org.fedoraproject.eclipse.packager.zip

# Remove old and create new symlinks to Import-Packages 
# in %%{_datadir}/eclipse/dropins/packager
pushd $RPM_BUILD_ROOT%{install_loc}/eclipse/plugins
rm -rf xmlrpc3-client.jar xmlrpc3-common.jar org.json.jar \
       ws-commons-util.jar commons-ssl.jar
ln -s %{_javadir}/xmlrpc3-client.jar
ln -s %{_javadir}/xmlrpc3-common.jar
ln -s %{_javadir}/json.jar org.json.jar
ln -s %{_javadir}/ws-commons-util.jar
ln -s %{_javadir}/not-yet-commons-ssl.jar commons-ssl.jar
popd 

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{install_loc}
%doc org.fedoraproject.eclipse.packager-feature/*.html

