%define		pkg	node-gyp
Summary:	Node.js native addon build tool
Name:		nodejs-gyp
Version:	0.9.5
Release:	2
License:	MIT
Group:		Development/Libraries
URL:		https://github.com/TooTallNate/node-gyp
Source0:	http://registry.npmjs.org/node-gyp/-/node-gyp-%{version}.tgz
# Source0-md5:	3d8a5cf4b5b92457af68035bb0e0e96f
Patch0:		jobs-alias.patch
Patch1:		system-gyp.patch
Patch2:		link-libnode.patch
BuildRequires:	sed >= 4.0
Requires:	gyp
Requires:	make
Requires:	nodejs
Requires:	nodejs-devel
Requires:	nodejs-fstream
Requires:	nodejs-glob < 4.0.0
Requires:	nodejs-glob >= 3.0.0
Requires:	nodejs-graceful-fs < 2.0.0
Requires:	nodejs-graceful-fs >= 1.0.0
Requires:	nodejs-minimatch
Requires:	nodejs-mkdirp
Requires:	nodejs-nopt < 3.0.0
Requires:	nodejs-nopt >= 2.0.0
Requires:	nodejs-npmlog < 1.0.0
Requires:	nodejs-osenv < 1.0.0
Requires:	nodejs-request < 3
Requires:	nodejs-request >= 2
Requires:	nodejs-rimraf < 3.0.0
Requires:	nodejs-rimraf >= 2.0.0
Requires:	nodejs-semver < 2.0.0
Requires:	nodejs-semver >= 1.0.0
Requires:	nodejs-tar
Requires:	nodejs-which < 2.0.0
Requires:	nodejs-which >= 1.0.0
Requires:	python
Obsoletes:	node-node-gyp
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
node-gyp is a cross-platform command-line tool written in Node.js for
compiling native addon modules for Node.js, which takes away the pain
of dealing with the various differences in build platforms. It is the
replacement to the node-waf program which is removed for node v0.8.

%prep
%setup -qc
mv package/* .
%patch0 -p1
%patch1 -p1
%patch2 -p1

# fix shebangs
%{__sed} -i -e '1s,^#!.*node,#!/usr/bin/node,' \
	bin/node-gyp.js

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{nodejs_libdir}/%{pkg}
cp -pr bin lib legacy package.json $RPM_BUILD_ROOT%{nodejs_libdir}/%{pkg}
cp -pr *.gyp* $RPM_BUILD_ROOT%{nodejs_libdir}/%{pkg}

install -d $RPM_BUILD_ROOT%{_bindir}
ln -s %{nodejs_libdir}/%{pkg}/bin/node-gyp.js $RPM_BUILD_ROOT%{_bindir}/node-gyp

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md LICENSE
%attr(755,root,root) %{_bindir}/node-gyp
%dir %{nodejs_libdir}/%{pkg}
%{nodejs_libdir}/%{pkg}/package.json
%{nodejs_libdir}/%{pkg}/addon.gypi
%{nodejs_libdir}/%{pkg}/lib
%dir %{nodejs_libdir}/%{pkg}/bin
%attr(755,root,root) %{nodejs_libdir}/%{pkg}/bin/node-gyp.js

# waf based tools
%{nodejs_libdir}/%{pkg}/legacy
