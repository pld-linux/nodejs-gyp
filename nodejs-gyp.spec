Summary:	Node.js native addon build tool
Name:		nodejs-gyp
Version:	0.9.3
Release:	1
License:	MIT
Group:		Development/Libraries
URL:		https://github.com/TooTallNate/node-gyp
Source0:	http://registry.npmjs.org/node-gyp/-/node-gyp-%{version}.tgz
# Source0-md5:	7b7c87c7ede0614e34acce0b7fab7ea6
BuildRequires:	sed >= 4.0
Requires:	gcc
Requires:	make
Requires:	nodejs
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

# fix shebangs
%{__sed} -i -e '1s,^#!.*node,#!/usr/bin/node,' \
	bin/node-gyp.js

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{nodejs_libdir}/node-gyp
cp -pr bin lib legacy package.json $RPM_BUILD_ROOT%{nodejs_libdir}/node-gyp

install -d $RPM_BUILD_ROOT%{_bindir}
ln -s %{nodejs_libdir}/node-gyp/bin/node-gyp.js $RPM_BUILD_ROOT%{_bindir}/node-gyp

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md LICENSE
%attr(755,root,root) %{_bindir}/node-gyp
%dir %{nodejs_libdir}/node-gyp
%{nodejs_libdir}/node-gyp/package.json
%{nodejs_libdir}/node-gyp/lib
%dir %{nodejs_libdir}/node-gyp/bin
%attr(755,root,root) %{nodejs_libdir}/node-gyp/bin/node-gyp.js

# waf based tools
%{nodejs_libdir}/node-gyp/legacy
