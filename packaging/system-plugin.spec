#%define _unpackaged_files_terminate_build 0
#%define debug_package %{nil}

Name:      system-plugin
Summary:   Target specific system configuration files
Version:   0.1
Release:   1
Group:     Base/Startup
License:   Apache-2.0
Source0:   %{name}-%{version}.tar.bz2
Source1:   %{name}.manifest
Source2:   liblazymount.manifest

Requires(post): /usr/bin/systemctl
Requires(post): /usr/bin/udevadm
BuildRequires: pkgconfig(vconf)
BuildRequires: pkgconfig(libsystemd)

%description
This package provides target specific system configuration files.

%package device-spreadtrum
Summary:  Spreadtrum specific system configuration files
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description device-spreadtrum
This package provides Spreadtrum specific system configuration files.

%package device-n4
Summary:  Note4 specific system configuration files
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description device-n4
This package provides Note4 specific system configuration files.

%package device-circle
Summary:  Circle specific system configuration files
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description device-circle
This package provides Circle specific system configuration files.

%package device-u3
Summary:  U3/XU3 specific system configuration files
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description device-u3
This package provides U3/XU3 specific system configuration files.

%package device-rpi3
Summary: RPI3
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description device-rpi3
This package provides system configuration files for the RPI3 device.

%package feature-init_wrapper
Summary: Support init.wrapper booting.
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description feature-init_wrapper
This package provides init.wrapper and init symlink file for init wrapper booting.

%package feature-init_wrapper_overlayfs
Summary: Support init.wrapper and overlayfs booting.
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description feature-init_wrapper_overlayfs
This package provides init.wrapper and init symlink file for init wrapper booting.
In addition, overlayfs is mounted upon the rootfs.

%package feature-lazymount
Summary: Library for lazy mount feature
Requires(post): /usr/bin/vconftool
Requires: vconf

%description feature-lazymount
Library for lazy mount feature. It supports some interface functions.

%package feature-lazymount-devel
Summary: Development library for lazy mount feature
Requires: vconf
Requires: %{name}-feature-lazymount = %{version}

%description feature-lazymount-devel
Development library for lazy mount feature. It supports some interface functions.

%package feature-image-reduction
Summary:  System configuration files for reducing image size
Requires: %{name} = %{version}-%{release}
Requires: dbus
BuildArch: noarch

%description feature-image-reduction
This package provides system configuration files for reducing image size.

%package config-env-headless
Summary:  System configuration files for headless images
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description config-env-headless
This package provides system configuration files for headless images.

%package config-udev-sdbd
Summary: System configuration files to trigger sdb with udev rule
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description config-udev-sdbd
This package provides configuration files to trigger sdb with udev rule.

%package config-2parts
Summary: System configuration files for storage partitions
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description config-2parts
This package provides configuration files for /etc/fstab(remount) and resize2fs@.service.

%package config-3parts
Summary: System configuration files for storage partitions
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description config-3parts
This package provides configuration files for /etc/fstab(remount) and resize2fs@.service.

%package config-3parts-lzuser
Summary: System configuration files for storage partitions
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description config-3parts-lzuser
This package provides configuration files for /etc/fstab(remount) and resize2fs@.service.

%prep
%setup -q

%build
cp %{SOURCE1} .
cp %{SOURCE2} .

./autogen.sh
%reconfigure \
		--disable-static \
		--prefix=%{_prefix} \
		--disable-debug-mode \
		--disable-eng-mode

%__make %{?jobs:-j%jobs} \
	CFLAGS+=-DLIBDIR=\\\"%{_libdir}\\\"

%install
rm -rf %{buildroot}
%make_install

mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_userunitdir}
mkdir -p %{buildroot}/csa
mkdir -p %{buildroot}/initrd
install -m 644 units/resize2fs@.service %{buildroot}%{_unitdir}
install -m 644 units/tizen-system-env.service %{buildroot}%{_unitdir}

# csa mount
install -m 644 units/csa.mount %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_unitdir}/local-fs.target.wants
ln -s ../csa.mount %{buildroot}%{_unitdir}/local-fs.target.wants/csa.mount

# Resize partition for 3-parted target
mkdir -p %{buildroot}%{_unitdir}/basic.target.wants
ln -s ../resize2fs@.service %{buildroot}%{_unitdir}/basic.target.wants/resize2fs@dev-disk-by\\x2dlabel-system\\x2ddata.service
ln -s ../resize2fs@.service %{buildroot}%{_unitdir}/basic.target.wants/resize2fs@dev-disk-by\\x2dlabel-user.service
ln -s ../resize2fs@.service %{buildroot}%{_unitdir}/basic.target.wants/resize2fs@dev-disk-by\\x2dlabel-rootfs.service

ln -s ../tizen-system-env.service %{buildroot}%{_unitdir}/basic.target.wants/tizen-system-env.service

mkdir -p %{buildroot}%{_prefix}/lib/udev/rules.d/
install -m 644 rules/51-system-plugin-exynos.rules %{buildroot}%{_prefix}/lib/udev/rules.d/
install -m 644 rules/51-system-plugin-spreadtrum.rules %{buildroot}%{_prefix}/lib/udev/rules.d/

mkdir -p %{buildroot}%{_prefix}/lib/udev/hwdb.d/
install -m 644 rules/60-evdev.hwdb %{buildroot}%{_prefix}/lib/udev/hwdb.d/

# /etc/fstab
mkdir -p %{buildroot}%{_sysconfdir}
install -m 644 etc/fstab_3parts %{buildroot}%{_sysconfdir}
install -m 644 etc/fstab_2parts %{buildroot}%{_sysconfdir}

# fstrim
mkdir -p %{buildroot}%{_unitdir}/graphical.target.wants
install -m 644 units/tizen-fstrim-user.timer %{buildroot}%{_unitdir}
ln -s ../tizen-fstrim-user.timer %{buildroot}%{_unitdir}/graphical.target.wants/tizen-fstrim-user.timer
install -m 644 units/tizen-fstrim-user.service %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_bindir}
install -m 755 scripts/tizen-fstrim-on-charge.sh %{buildroot}%{_bindir}

# fixed-multi-user
install -m 775 -D scripts/fixed-multi-user.sh %{buildroot}%{_datadir}/fixed_multiuser/fixed-multi-user.sh

# init_wrapper
mkdir -p %{buildroot}%{_sbindir}
install -m 755 scripts/init.wrapper %{buildroot}%{_sbindir}
install -m 755 scripts/init.wrapper.overlayfs %{buildroot}%{_sbindir}

# headless
mkdir -p %{buildroot}%{_sbindir}
install -m 755 scripts/sdb-mode.sh %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_sysconfdir}/profile.d
install -m 755 scripts/headless_env.sh %{buildroot}%{_sysconfdir}/profile.d

# config-udev-sdbd
mkdir -p %{buildroot}%{_prefix}/lib/udev/rules.d/
install -m 644 rules/99-sdb-extcon.rules %{buildroot}%{_prefix}/lib/udev/rules.d/

# /opt/usr lazy mount
mkdir -p %{buildroot}%{_unitdir}/local-fs.target.wants
mkdir -p %{buildroot}%{_unitdir}/wait-mount@opt-usr.service.d
mkdir -p %{buildroot}%{_userunitdir}/basic.target.wants
mkdir -p %{buildroot}%{_userunitdir}/wait-mount@opt-usr.service.d
install -m 644 units/opt-usr.mount %{buildroot}%{_unitdir}
install -m 644 units/opt-usr-fsck.service %{buildroot}%{_unitdir}
install -m 644 units/wait-mount@.service %{buildroot}%{_unitdir}
install -m 644 units/wait-mount-session@.service %{buildroot}%{_userunitdir}/wait-mount@.service
install -m 644 units/no-wait.conf %{buildroot}%{_unitdir}/wait-mount@opt-usr.service.d
install -m 644 units/no-wait.conf %{buildroot}%{_userunitdir}/wait-mount@opt-usr.service.d
ln -s ../opt-usr.mount %{buildroot}%{_unitdir}/local-fs.target.wants/opt-usr.mount
ln -s ../wait-mount@.service %{buildroot}%{_unitdir}/local-fs.target.wants/wait-mount@opt-usr.service
ln -s ../wait-mount@.service %{buildroot}%{_userunitdir}/basic.target.wants/wait-mount@opt-usr.service

%clean
rm -rf %{buildroot}

%post
systemctl daemon-reload

%files
%manifest %{name}.manifest
%license LICENSE.Apache-2.0
%{_unitdir}/resize2fs@.service
%{_unitdir}/tizen-system-env.service
%{_unitdir}/basic.target.wants/tizen-system-env.service

%files device-spreadtrum
%manifest %{name}.manifest
%license LICENSE.Apache-2.0
/initrd
/csa
%{_prefix}/lib/udev/rules.d/51-system-plugin-spreadtrum.rules
%{_unitdir}/tizen-system-env.service
%{_unitdir}/basic.target.wants/tizen-system-env.service
%{_unitdir}/csa.mount
%{_unitdir}/local-fs.target.wants/csa.mount
%{_unitdir}/graphical.target.wants/tizen-fstrim-user.timer
%{_unitdir}/tizen-fstrim-user.timer
%{_unitdir}/tizen-fstrim-user.service
%{_bindir}/tizen-fstrim-on-charge.sh
%{_datadir}/fixed_multiuser/fixed-multi-user.sh

%files device-n4
%manifest %{name}.manifest
%license LICENSE.Apache-2.0
%{_unitdir}/graphical.target.wants/tizen-fstrim-user.timer
%{_unitdir}/tizen-fstrim-user.timer
%{_unitdir}/tizen-fstrim-user.service
%{_bindir}/tizen-fstrim-on-charge.sh

%files device-circle
%manifest %{name}.manifest
%license LICENSE.Apache-2.0
/initrd
/csa
%{_unitdir}/csa.mount
%{_unitdir}/local-fs.target.wants/csa.mount

%files device-u3
%manifest %{name}.manifest
%license LICENSE.Apache-2.0
%{_prefix}/lib/udev/hwdb.d/60-evdev.hwdb
%{_prefix}/lib/udev/rules.d/51-system-plugin-exynos.rules

%post device-u3
%{_prefix}/bin/udevadm hwdb --update

%files device-rpi3
%manifest %{name}.manifest
%license LICENSE.Apache-2.0
%{_prefix}/lib/udev/hwdb.d/60-evdev.hwdb

%post device-rpi3
%{_prefix}/bin/udevadm hwdb --update

%files feature-init_wrapper
%license LICENSE.Apache-2.0
%{_sbindir}/init.wrapper

%posttrans feature-init_wrapper
rm -f /sbin/init
ln -s /sbin/init.wrapper /sbin/init

%files feature-init_wrapper_overlayfs
%license LICENSE.Apache-2.0
%{_sbindir}/init.wrapper.overlayfs

%posttrans feature-init_wrapper_overlayfs
rm -f /sbin/init
ln -s /sbin/init.wrapper.overlayfs /sbin/init
mkdir -p /.overlayfs_merged
mkdir -p /.rootfs_old

%files feature-lazymount
%defattr(-,root,root,-)
%manifest liblazymount.manifest
%license LICENSE.Apache-2.0
%{_libdir}/liblazymount.so.*
%{_unitdir}/basic.target.wants/lazy_mount.path
%{_unitdir}/lazy_mount.path
%{_unitdir}/lazy_mount.service
%{_bindir}/mount-user.sh

%post feature-lazymount
/sbin/ldconfig
systemctl daemon-reload

%postun feature-lazymount -p /sbin/ldconfig

%files feature-lazymount-devel
%defattr(-,root,root,-)
%manifest liblazymount.manifest
%license LICENSE.Apache-2.0
%{_libdir}/liblazymount.so
%{_includedir}/lazymount/lazy_mount.h
%{_libdir}/pkgconfig/liblazymount.pc

%posttrans feature-image-reduction
# platform/upstream/dbus
rm -f %{_bindir}/dbus-cleanup-sockets
rm -f %{_bindir}/dbus-run-session
rm -f %{_bindir}/dbus-test-tool
rm -f %{_bindir}/dbus-update-activation-environment
rm -f %{_bindir}/dbus-uuidgen
# platform/upstream/e2fsprogs
rm -f %{_sbindir}/e4crypt

%files config-env-headless
%manifest %{name}.manifest
%license LICENSE.Apache-2.0
%{_sysconfdir}/profile.d/headless_env.sh

%files config-udev-sdbd
%manifest %{name}.manifest
%license LICENSE.Apache-2.0
%{_bindir}/sdb-mode.sh
%{_prefix}/lib/udev/rules.d/99-sdb-extcon.rules

%files config-2parts
%manifest %{name}.manifest
%license LICENSE.Apache-2.0
%{_unitdir}/basic.target.wants/resize2fs@dev-disk-by\x2dlabel-rootfs.service
%{_unitdir}/basic.target.wants/resize2fs@dev-disk-by\x2dlabel-system\x2ddata.service
%{_sysconfdir}/fstab_2parts
%{_unitdir}/wait-mount@.service
%{_unitdir}/wait-mount@opt-usr.service.d/no-wait.conf
%{_unitdir}/local-fs.target.wants/wait-mount@opt-usr.service
%{_userunitdir}/wait-mount@.service
%{_userunitdir}/wait-mount@opt-usr.service.d/no-wait.conf
%{_userunitdir}/basic.target.wants/wait-mount@opt-usr.service

%post config-2parts
mv %{_sysconfdir}/fstab_2parts %{_sysconfdir}/fstab

%files config-3parts
%manifest %{name}.manifest
%license LICENSE.Apache-2.0
%{_unitdir}/basic.target.wants/resize2fs@dev-disk-by\x2dlabel-rootfs.service
%{_unitdir}/basic.target.wants/resize2fs@dev-disk-by\x2dlabel-system\x2ddata.service
%{_unitdir}/basic.target.wants/resize2fs@dev-disk-by\x2dlabel-user.service
%{_sysconfdir}/fstab_3parts
%{_unitdir}/wait-mount@.service
%{_unitdir}/local-fs.target.wants/wait-mount@opt-usr.service
%{_userunitdir}/wait-mount@.service
%{_userunitdir}/basic.target.wants/wait-mount@opt-usr.service

%post config-3parts
mv %{_sysconfdir}/fstab_3parts %{_sysconfdir}/fstab

%files config-3parts-lzuser
%manifest %{name}.manifest
%license LICENSE.Apache-2.0
%{_unitdir}/basic.target.wants/resize2fs@dev-disk-by\x2dlabel-rootfs.service
%{_unitdir}/basic.target.wants/resize2fs@dev-disk-by\x2dlabel-system\x2ddata.service
%{_unitdir}/basic.target.wants/resize2fs@dev-disk-by\x2dlabel-user.service
%{_sysconfdir}/fstab_2parts
%{_unitdir}/opt-usr.mount
%{_unitdir}/opt-usr-fsck.service
%{_unitdir}/wait-mount@.service
%{_unitdir}/local-fs.target.wants/opt-usr.mount
%{_userunitdir}/wait-mount@.service
%{_userunitdir}/basic.target.wants/wait-mount@opt-usr.service

%post config-3parts-lzuser
mv %{_sysconfdir}/fstab_2parts %{_sysconfdir}/fstab
