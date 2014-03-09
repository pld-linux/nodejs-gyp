%define		pkg	node-gyp
Summary:	Node.js native addon build tool
Name:		nodejs-gyp
Version:	0.12.2
Release:	1
License:	MIT
Group:		Development/Libraries
URL:		https://github.com/TooTallNate/node-gyp
Source0:	http://registry.npmjs.org/node-gyp/-/node-gyp-%{version}.tgz
# Source0-md5:	a296a511c2a3f4481862ff62966e0972
Patch0:		system-gyp.patch
Patch1:		link-libnode.patch
BuildRequires:	sed >= 4.0
Requires:	gyp
Requires:	make
Requires:	nodejs >= 0.8.0
Requires:	nodejs-devel
Requires:	nodejs-fstream < 1
Requires:	nodejs-glob < 4
Requires:	nodejs-glob >= 3
Requires:	nodejs-graceful-fs < 3
Requires:	nodejs-graceful-fs >= 2
Requires:	nodejs-minimatch < 1
Requires:	nodejs-mkdirp < 1
Requires:	nodejs-nopt < 3
Requires:	nodejs-nopt >= 2
Requires:	nodejs-npmlog < 1
Requires:	nodejs-osenv < 1
Requires:	nodejs-request < 3
Requires:	nodejs-request >= 2
Requires:	nodejs-rimraf < 3
Requires:	nodejs-rimraf >= 2
Requires:	nodejs-semver < 2.3.0
Requires:	nodejs-semver >= 2.2.1
Requires:	nodejs-tar < 1
Requires:	nodejs-which < 2
Requires:	nodejs-which >= 1
Requires:	python >= 2.7
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

# fix shebangs
%{__sed} -i -e '1s,^#!.*node,#!/usr/bin/node,' \
	bin/node-gyp.js

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_bindir},%{nodejs_libdir}/%{pkg}}
cp -pr bin lib package.json $RPM_BUILD_ROOT%{nodejs_libdir}/%{pkg}
cp -pr *.gyp* $RPM_BUILD_ROOT%{nodejs_libdir}/%{pkg}
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
