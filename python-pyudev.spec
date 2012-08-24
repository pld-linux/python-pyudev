#
# Conditional build:
%bcond_without	tests	# do not perform "make test"

%define 	module	pyudev
Summary:	Pure Python binding for libudev
Summary(pl.UTF-8):	Czysto pythonowe wiązanie do libudev
Name:		python-%{module}
Version:	0.16.1
Release:	1
License:	LGPL v2.1+
Group:		Development/Languages/Python
Source0:	http://pypi.python.org/packages/source/p/pyudev/%{module}-%{version}.tar.gz
# Source0-md5:	4034de584b6d9efcbfc590a047c63285
URL:		http://pyudev.readthedocs.org/
BuildRequires:	python-distribute
BuildRequires:	rpm-pythonprov
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

%prep
%setup -q -n %{module}-%{version}

%build
%{__python} setup.py build

%{?with_tests:%{__python} setup.py test}

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install \
	--skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%py_comp $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_ocomp $RPM_BUILD_ROOT%{py_sitescriptdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.rst README.rst doc/
%{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/pyudev-%{version}-py*.egg-info
