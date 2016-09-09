%{!?version: %define version 1.0.0}
%{!?release: %define release %(date "+%Y%m%d%H%M%s")}
%{!?_srcdir: %define _srcdir %(readlink -f "%(dirname %0)/")}

%define rpm_root %{buildroot}/../../RPMS 
%define undss_src %{_srcdir}/ia_imaging
%define dss_src  %{undss_src}/linux/dss

%define extra_include  %{_extra_install}/%{_includedir}/libiaaiq/include/ia_imaging
%define extra_lib      %{_extra_install}/%{_prefix}/lib/ 
%define extra_pkg      %{extra_lib}/pkgconfig

%define default_include  %{buildroot}/%{_includedir}/libiaaiq/
%define default_lib      %{buildroot}/%{_prefix}/lib/ 
%define default_pkg      %{default_lib}/pkgconfig

Summary: Lib IA AIQ
Name: libiaaiq
Version: %{version}
Release: %{release}
License: Intel
Group: Development/Tools
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-build

%description
IPU4 firmware binaries.

%build
cd %{_srcdir}
rm -rf %{_srcdir}/rpm/*.rpm
autoreconf -ivf

%if 0%{?_config_flags} && 0%{?_dss}
echo "first configure=========="
%configure \
    --target=x86_64-poky-linux \
    --host=x86_64-poky-linux \
    --build=x86_64-linux \
    --with-libtool-sysroot=%{_libtool_sysroot} \
    --with-project=dss \
    --libdir=/usr/lib
%endif

#%if 0%{?_config_flags} && %{!?_dss:1}
#echo "second configure=========="
#%configure \
#    --target=x86_64-poky-linux \
#    --host=x86_64-poky-linux \
#    --build=x86_64-linux \
#    --with-libtool-sysroot=%{_libtool_sysroot} \
#    --libdir=/usr/lib
#%endif

#%if %{!?_config_flags:1} && 0%{?_dss}
#echo "third configure============"
#%configure \
#    --with-project=dss
#%endif
#
#%if %{!?_config_flags:1} && %{!?_dss:1}
#echo "forth configure============"
#%configure
#%endif


%install
rm -rf %{buildroot}
mkdir -p %{default_pkg} %{default_include}

%if "%{?_dss}" == "enable"
%{__install} -c -m755 %{dss_src}/lib/release/64/* %{default_lib} 
%{__install} -c %{dss_src}/include/*     %{default_include} 
%{__install} -c %{_srcdir}/ia_imaging.pc %{default_pkg}

%if "%{?_extra_install}"
mkdir -p %{extra_lib} %{extra_include} 
%{__install} -c -m755 %{default_lib}/*.* %{extra_lib} 
%{__install} -c %{default_include}/*.*    %{extra_include}
%{__install} -c %{default_pkg}/ia_imaging.pc %{extra_pkg} 
%endif
%else
%{__install} -c -m755 %{undss_src}/linux/lib/release/64/* %{default_lib} 
%{__install} -c %{undss_src}/include/*   %{default_include} 
%{__install} -c %{_srcdir}/ia_imaging.pc %{default_pkg}

%if "%{?_extra_install}"
mkdir -p %{extra_lib} %{extra_include} 
%{__install} -c -m755 %{default_lib}/*.* %{extra_lib} 
%{__install} -c %{default_include}/*.*  %{extra_include} 
%{__install} -c %{default_pkg}/ia_imaging.pc %{extra_pkg} 
%endif
%endif

rm -v %{default_include}/ia_isp_1_*
rm -v %{default_include}/ia_isp_2_*
rm -v %{default_include}/pvl_*
rm -v %{default_lib}/libia_isp_2_*
rm -v %{default_lib}/libia_isp_cif_*

sed -i '1c prefix=\/usr' %{default_pkg}/ia_imaging.pc
sed -i "s/includedir=.*/includedir=\$\{prefix\}\/include\/libiaaiq/" %{default_pkg}/ia_imaging.pc
sed -i "s/Cflags:.*/Cflags: -I\$\{includedir\}/" %{default_pkg}/ia_imaging.pc

%files
/usr/

%clean
cp -v %{rpm_root}/x86_64/*.rpm %{_srcdir}/rpm 
%if "%{?_extra_rpm}"
cp -v %{rpm_root}/x86_64/*.rpm %{_extra_rpm}
%endif
rm -rf %{rpm_root}
rm -rf %{buildroot}
