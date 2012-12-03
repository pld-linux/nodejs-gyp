Summary:	Node.js native addon build tool
Name:		nodejs-gyp
Version:	0.7.3
Release:	1
License:	MIT
Group:		Development/Libraries
URL:		https://github.com/TooTallNate/node-gyp
Source0:	http://registry.npmjs.org/node-gyp/-/node-gyp-%{version}.tgz
# Source0-md5:	6ed1cda95544587a78287975cdb0ce5d
BuildRequires:	sed >= 4.0
Requires:	make
Requires:	gcc
Requires:	nodejs
Requires:	nodejs-ansi >= 0.1.0
Requires:	nodejs-fstream >= 0.1.13, nodejs-fstream < 0.2.0
Requires:	nodejs-glob >= 3.0.0, nodejs-glob < 4.0.0
Requires:	nodejs-graceful-fs >= 1.0.0, nodejs-graceful-fs < 2.0.0
Requires:	nodejs-minimatch >= 0.2.0, nodejs-minimatch < 0.3.0
Requires:	nodejs-mkdirp >= 0.3.0, nodejs-mkdirp < 0.4.0
Requires:	nodejs-nopt >= 2.0.0, nodejs-nopt < 3.0.0
Requires:	nodejs-request >= 2.9.0, nodejs-request < 2.10.0
Requires:	nodejs-rimraf >= 2.0.0, nodejs-rimraf < 3.0.0
Requires:	nodejs-semver >= 1.0.0, nodejs-semver < 2.0.0
Requires:	nodejs-tar >= 0.1.12, nodejs-tar < 0.2.0
Requires:	nodejs-which >= 1.0.0, nodejs-which < 2.0.0
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
