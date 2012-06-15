Summary:	Node.js native addon build tool
Name:		nodejs-gyp
Version:	0.4.1
Release:	1
License:	MIT
Group:		Libraries
URL:		https://github.com/TooTallNate/node-gyp
Source0:	http://registry.npmjs.org/node-gyp/-/node-gyp-%{version}.tgz
# Source0-md5:	70dcb0b846af2be1ce31d568729261e2
# fix package.json dependencies for newer versions in RPMs
Patch1:		node-gyp-fixdeps.patch
BuildRequires:	sed >= 4.0
Requires:	make
Requires:	gcc
Requires:	nodejs
Requires:	nodejs-ansi >= 0.1.0
Requires:	nodejs-fstream
Requires:	nodejs-glob >= 3.1.9
Requires:	nodejs-minimatch
Requires:	nodejs-mkdirp
Requires:	nodejs-nopt
Requires:	nodejs-request
Requires:	nodejs-rimraf
Requires:	nodejs-semver
Requires:	nodejs-tar
Requires:	nodejs-which
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
%patch1 -p0

# fix shebangs
%{__sed} -i -e '1s,^#!.*node,#!/usr/bin/node,' \
	bin/node-gyp.js

# fix #!/usr/bin/env python -> #!/usr/bin/python:
grep -rl 'bin/env python' legacy/tools | xargs %{__sed} -i -e '1s,^#!.*python,#!%{__python},'

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{nodejs_libdir}/node-gyp
cp -pr bin lib legacy package.json $RPM_BUILD_ROOT%{nodejs_libdir}/node-gyp

install -d $RPM_BUILD_ROOT%{_bindir}
ln -sf ../lib/nodejs/node-gyp/bin/node-gyp.js $RPM_BUILD_ROOT%{_bindir}/node-gyp

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md LICENSE
%attr(755,root,root) %{_bindir}/node-gyp
%{nodejs_libdir}/node-gyp
