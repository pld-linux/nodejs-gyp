#
# Conditional build:
%bcond_with	system_gyp		# build with system gyp package

%define		pkg	node-gyp
Summary:	Node.js native addon build tool
Name:		nodejs-gyp
Version:	11.2.0
Release:	2
License:	MIT
Group:		Development/Libraries
Source0:	http://registry.npmjs.org/node-gyp/-/node-gyp-%{version}.tgz
# Source0-md5:	b458b941ff4e015a1464437532aaffb0
# tar xf node-gyp-%{version}.tgz
# npm -C package install --omit dev --no-audit --no-fund
# tar acf nodejs-gyp-node_modules-%{version}.tar.xz package/node_modules
Source1:	%{name}-node_modules-%{version}.tar.xz
# Source1-md5:	02f806bb4e6b7fc6371c9ca2868ecb9e
Patch0:		system-gyp.patch
Patch1:		link-libnode.patch
URL:		https://github.com/TooTallNate/node-gyp
BuildRequires:	sed >= 4.0
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
%{?with_system_gyp:Requires:	gyp}
Requires:	make
Requires:	nodejs >= 20.5.0
Requires:	nodejs-devel
Requires:	python3
Requires:	python3-modules
Obsoletes:	node-node-gyp
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
node-gyp is a cross-platform command-line tool written in Node.js for
compiling native addon modules for Node.js, which takes away the pain
of dealing with the various differences in build platforms. It is the
replacement to the node-waf program which is removed for node v0.8.

%prep
%setup -qc -a1
mv package/* .
%{?with_system_gyp:%patch -P0 -p1}
%patch -P1 -p1

# fix shebangs
%{__sed} -i -e '1s,^#!.*node,#!/usr/bin/node,' \
	bin/node-gyp.js

grep -r '#!.*env python3' -l gyp | xargs %{__sed} -i -e '1 s,#!.*env python3,#!%{__python3},'
grep -r '#!.*env node' -l node_modules | xargs %{__sed} -i -e '1 s,#!.*env node,#!/usr/bin/node,'

# cleanup backups after patching
find '(' -name '*~' -o -name '*.orig' ')' -print0 | xargs -0 -r -l512 rm -f

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{nodejs_libdir}/%{pkg}}
cp -pr bin lib node_modules package.json $RPM_BUILD_ROOT%{nodejs_libdir}/%{pkg}
cp -pr *.gyp* $RPM_BUILD_ROOT%{nodejs_libdir}/%{pkg}
ln -s %{nodejs_libdir}/%{pkg}/bin/node-gyp.js $RPM_BUILD_ROOT%{_bindir}/node-gyp
%if %{with system_gyp}
install -d $RPM_BUILD_ROOT%{nodejs_libdir}/%{pkg}/gyp
ln -s %{_bindir}/gyp $RPM_BUILD_ROOT%{nodejs_libdir}/%{pkg}/gyp
%else
cp -a gyp $RPM_BUILD_ROOT%{nodejs_libdir}/%{pkg}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md LICENSE
%attr(755,root,root) %{_bindir}/node-gyp
%dir %{nodejs_libdir}/%{pkg}
%{nodejs_libdir}/%{pkg}/package.json
%{nodejs_libdir}/%{pkg}/addon.gypi
%{nodejs_libdir}/%{pkg}/gyp
%{nodejs_libdir}/%{pkg}/lib
%{nodejs_libdir}/%{pkg}/node_modules
%dir %{nodejs_libdir}/%{pkg}/bin
%attr(755,root,root) %{nodejs_libdir}/%{pkg}/bin/node-gyp.js
