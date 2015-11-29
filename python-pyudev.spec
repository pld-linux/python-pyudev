#
# Conditional build:
%bcond_without	doc		# HTML documentation build
%bcond_without	tests		# do not perform "make test"
%bcond_without	python2         # Python 2.x module
%bcond_without	python3         # Python 3.x module
#
%define 	module	pyudev
Summary:	Pure Python binding for libudev
Summary(pl.UTF-8):	Czysto pythonowe wiązanie do libudev
Name:		python-%{module}
Version:	0.17
Release:	2
License:	LGPL v2.1+
Group:		Development/Languages/Python
Source0:	http://pypi.python.org/packages/source/p/pyudev/%{module}-%{version}.tar.gz
# Source0-md5:	0450afde50383538a987d16450853fb1
#Source1:	http://docs.python.org/2/objects.inv#/python-objects.inv
Source1:	python-objects.inv
# Source1-md5:	ad9c579afde0743e007b472cff7f1364
#Source2:	http://pytest.org/latest/objects.inv#/pytest-objects.inv
Source2:	pytest-objects.inv
# Source2-md5:	0704c1b84755f3dd4d0cb782826791c6
#Source3:	https://deptinfo-ensip.univ-poitiers.fr/ENS/pyside-docs/objects.inv#/pyside-objects.inv
Source3:	pyside-objects.inv
# Source3-md5:	8cc5c1ff0bb5ef9f4e9968c9b4a01984
Patch0:		%{name}-offline.patch
URL:		http://pyudev.readthedocs.org/
BuildRequires:	rpmbuild(macros) >= 1.710
%if %{with python2}
BuildRequires:	python-devel >= 1:2.6
BuildRequires:	python-setuptools
%endif
%if %{with python3}
BuildRequires:	python3-devel >= 1:3.2
BuildRequires:	python3-setuptools
%endif
BuildRequires:	rpm-pythonprov
%if %{with doc}
# for tests 1.0b1 is required, but for docs generation 0.8 is sufficient
#BuildRequires:	python-mock >= 1.0-0.b1
BuildRequires:	python-mock >= 0.8
BuildRequires:	python-sphinxcontrib-issuetracker >= 0.9
BuildRequires:	python-pytest >= 2.2
BuildRequires:	sphinx-pdg >= 1.0.7
%endif
Requires:	python-modules
Requires:	udev-libs >= 1:151
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
pyudev is a LGPL licensed, pure Python binding for libudev, the device
and hardware management and information library for Linux. It supports
almost all libudev functionality, you can enumerate devices, query
device properties and attributes or monitor devices, including
asynchronous monitoring with threads, or within the event loops of Qt,
GLib or wxPython.

%description -l pl.UTF-8
pyudev to wydane na licencji LGPL czysto pythonowe wiązanie do libudev
- biblioteki zarządzania urządzeniami i sprzętem dla Linuksa.
Obsługuje prawie całą funkcjonalność libudev, potrafi wyliczać
urządzenia, odpytywać o właściwości i atrybuty urządzeń oraz
monitorować urządzenia, włącznie z asynchronicznym monitorowaniem z
użyciem wątków albo wewnątrz pętli zdarzeń Qt, GLiba czy wxPythona.

%package -n python3-%{module}
Summary:	Pure Python binding for libudev
Summary(pl.UTF-8):	Czysto pythonowe wiązanie do libudev
Group:		Development/Languages/Python
Requires:	python3-modules

%description -n python3-%{module}
pyudev is a LGPL licensed, pure Python binding for libudev, the device
and hardware management and information library for Linux. It supports
almost all libudev functionality, you can enumerate devices, query
device properties and attributes or monitor devices, including
asynchronous monitoring with threads, or within the event loops of Qt,
GLib or wxPython.

%description -n python3-%{module} -l pl.UTF-8
pyudev to wydane na licencji LGPL czysto pythonowe wiązanie do libudev
- biblioteki zarządzania urządzeniami i sprzętem dla Linuksa.
Obsługuje prawie całą funkcjonalność libudev, potrafi wyliczać
urządzenia, odpytywać o właściwości i atrybuty urządzeń oraz
monitorować urządzenia, włącznie z asynchronicznym monitorowaniem z
użyciem wątków albo wewnątrz pętli zdarzeń Qt, GLiba czy wxPythona.

%prep
%setup -q -n %{module}-%{version}
%patch0 -p1

cp -p %{SOURCE1} %{SOURCE2} %{SOURCE3} doc

%build
%if %{with python2}
%py_build %{?with_tests:test}
%endif

%if %{with python3}
%py3_build %{?with_tests:test}
%endif

%if %{with doc}
sphinx-build -b html -d doc/_doctrees doc doc/html
%endif

%install
rm -rf $RPM_BUILD_ROOT
%if %{with python2}
%py_install

%{__rm} -r $RPM_BUILD_ROOT%{py_sitescriptdir}/tests
%endif
%if %{with python3}
%py3_install

%{__rm} -r $RPM_BUILD_ROOT%{py3_sitescriptdir}/tests
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CHANGES.rst README.rst %{?with_doc:doc/html}
%{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/pyudev-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc CHANGES.rst README.rst %{?with_doc:doc/html}
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/pyudev-%{version}-py*.egg-info
%endif
