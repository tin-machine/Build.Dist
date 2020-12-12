import os

Base = {
    'portage': {
            
        "make.conf": dict(
            CFLAGS="-march=native -O2 -pipe",
            CXXFLAGS="${CFLAGS}",
            FCFLAGS="${CFLAGS}",
            FFLAGS="${CFLAGS}",
            CHOST="aarch64-unknown-linux-gnu",
            USE="bindist -systemd elogind".split(),
            FEATURES="parallel-fetch buildpkg collision-protect binpkg-multi-instance getbinpkg ".split(),
            MAKEOPTS=f"-j{len(os.sched_getaffinity(0))} -l{len(os.sched_getaffinity(0))}",
            VIDEO_CARDS="",
            INPUT_DEVICES="evdev synaptics",
            ACCEPT_LICENSE="* -@EULA",
            LINGUAS="en",
            L10N="en",
        ),
        "patches/": {
            "app-editors/": "patches/app-editors",
            "sys-apps/": "patches/sys-apps"
        }
        
    },
    "etc": {
        "locale.gen": "locale.gen",
        "profile": "profile"
    },
    "TERM": os.environ['TERM'],
    "jobs": len(os.sched_getaffinity(0)),
    "load-average": len(os.sched_getaffinity(0)),
    "distcc": [
        "192.168.1.43/16"
    ],
    "groups": [
        dict(name="cron", gid=16),
    ],
    "users": [
        dict(name="demouser",
             password="password",
             format="SHA512",
             group="users",
             groups="users,wheel,video,audio,adm,disk,lp,cdrom,usb,portage,cron".split(','),
             shell="/bin/bash",
             uid="1000"
             )
    ],
    "locale": "en_US.utf8",
    "overlays": [
        {
            'name': 'gentoo',
            'location': '/var/db/repos/gentoo',
            'sync-type': 'git',
            'sync-depth': '1',
            'sync-uri': 'https://anongit.gentoo.org/git/repo/gentoo.git',
            'auto-sync': 'yes',
        }
    ],
    "enable-services": [
        "cronie",
        "sshd"
    ],
    'sets': [
        "standard"
    ],
    'packages': []
}

GenPi64 = Base | {
    "kernel": [
        "sys-kernel/bcm2711-kernel-bis-bin",
        "sys-boot/rpi3-64bit-firmware"
    ],
    "overlays": Base['overlays'] + [
        {
            'name': 'genpi64',
            'location': '/var/db/repos/genpi64',
            'sync-type': 'git',
            'sync-uri': 'https://github.com/GenPi64/genpi64-overlay.git',
            'priority': '100',
            'auto-sync': 'yes',
            'sync-depth': '1',
        },
        {
            'name': 'genpi-tools',
            'location': '/var/db/repos/sakaki-tools',
            'sync-type': 'git',
            'sync-uri': 'https://github.com/GenPi64/sakaki-tools.git',
            'priority': '50',
            'auto-sync': 'yes',
            'sync-depth': '1',
        }
        
            
    ],
    "portage": Base["portage"] | {
        "make.conf": Base["portage"]["make.conf"] | {
            "CFLAGS": "-mtune=cortex-a72 -march=armv8-a+crc -O2 -pipe",
            "PORTAGE_BINHOST": "https://genpi64.com/",
            "FEATURES": Base["portage"]["make.conf"]["FEATURES"] + "-userpriv -usersandbox -network-sandbox -pid-sandbox".split()
            
        },
        "binrepos.conf": "binrepo_genpi64.conf"
        
    },
    "stage3": "stage3-arm64-20201004T190540Z.tar.xz",
    "profile": "default/linux/arm64/17.0",
    'users': [
        dict(name="demouser",
             password="raspberrypi64",
             format="SHA512",
             group="100",
             groups="users,wheel,video,audio,adm,disk,lp,cdrom,usb,portage,cron,plugdev,gpio,i2c,spi".split(','),
             shell="/bin/bash",
             uid="1000"
        )
    ],

    'groups': [
        dict(name="i2c", gid=371),
        dict(name="gpio", gid=370),
        dict(name="spi", gid=372),
        dict(name="cron", gid=16),
        dict(name="crontab", gid=248),
        dict(name="plugdev", gid=245),
        
    ],

    'image': {
        'name': 'GenPi64.img',
        'size': '8G',
        'format': 'msdos',
        'mount-order': [1,0],
        'partitions': [
            {
                'end': '256MiB',
                'format': 'vfat',
                'mount-point': '/boot',
                'mount-options': 'noatime'
            },
            {
                'end': '100%',
                'format': 'btrfs',
                'mount-point': '/',
                'mount-options': 'compress=zstd:15,ssd,discard'
            }
        ]
    }

}

GenPi64Desktop = GenPi64 | {
    "profile": "default/linux/arm64/17.0/desktop",

}

globals()['nvros-arm'] = GenPi64Desktop