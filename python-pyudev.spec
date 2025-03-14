#
# Conditional build:
%bcond_without	doc		# HTML documentation build
%bcond_with	tests		# py.test tests [requires functional udev with device db]
%bcond_without	python2         # Python 2.x module
%bcond_without	python3         # Python 3.x module
#
%define 	module	pyudev
Summary:	Pure Python binding for libudev
Summary(pl.UTF-8):	Czysto pythonowe wiązanie do libudev
Name:		python-%{module}
Version:	0.22.0
Release:	6
License:	LGPL v2.1+
Group:		Development/Languages/Python
#Source0Download: https://pypi.org/simple/pyudev/
Source0:	https://files.pythonhosted.org/packages/source/p/pyudev/%{module}-%{version}.tar.gz
# Source0-md5:	377eda61186c91e9440f01d76dbb4206
Patch0:		%{name}-mock.patch
URL:		http://pyudev.readthedocs.org/
%if %{with python2}
BuildRequires:	python-devel >= 1:2.6
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-docutils >= 0.9
BuildRequires:	python-hypothesis
BuildRequires:	python-mock >= 1.0
BuildRequires:	python-pytest >= 2.8
BuildRequires:	python-six
%endif
%endif
%if %{with python3}
BuildRequires:	python3-devel >= 1:3.2
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-docutils >= 0.9
BuildRequires:	python3-hypothesis
BuildRequires:	python3-pytest >= 2.8
BuildRequires:	python3-six
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
# for tests 1.0b1 is required, but for docs generation 0.8 is sufficient
BuildRequires:	python-mock >= 0.8
BuildRequires:	python-sphinxcontrib-issuetracker >= 0.9
BuildRequires:	python-pytest >= 2.2
BuildRequires:	sphinx-pdg-2 >= 1.0.7
%endif
Requires:	python-modules >= 1:2.6
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
Requires:	python3-modules >= 1:3.2

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

%package apidocs
Summary:	API documentation for Python pyudev module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona pyudev
Group:		Documentation

%description apidocs
API documentation for Python pyudev module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona pyudev.

%prep
%setup -q -n %{module}-%{version}
%patch -P 0 -p1

%build
%if %{with python2}
%py_build

%if %{with tests}
PYTHONPATH=$(pwd):$(pwd)/build-2/lib \
%{__python} -m pytest tests
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTHONPATH=$(pwd):$(pwd)/build-3/lib \
%{__python3} -m pytest tests
%endif
%endif

%if %{with doc}
PYTHONPATH=build-2/lib \
sphinx-build-2 -b html -d doc/_doctrees doc doc/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CHANGES.rst README.rst
%{py_sitescriptdir}/pyudev
%{py_sitescriptdir}/pyudev-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc CHANGES.rst README.rst
%{py3_sitescriptdir}/pyudev
%{py3_sitescriptdir}/pyudev-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc doc/html/{_static,api,tests,*.html,*.js}
%endif
