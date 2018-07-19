import json
import requests
import os
import hashlib


def hashsrc(url):
    print("Getting " + url)
    r = requests.get(url)
    sha256 = hashlib.sha256()
    sha256.update(r.content)
    filechecksum = sha256.hexdigest()
    return(filechecksum)

gnome_runtime = "3.28"
fin_args = [
    "--share=ipc",
    "--socket=x11",
    "--device=dri",
    "--share=network",
    "--socket=pulseaudio",
    "--filesystem=~/.cache/thunderbird:create",
    "--filesystem=~/.thunderbird:create",
    "--filesystem=home:ro",
    "--filesystem=xdg-download:rw",
    "--filesystem=xdg-run/dconf",
    "--filesystem=~/.config/dconf:ro",
    "--talk-name=ca.desrt.dconf",
    "--env=DCONF_USER_CONFIG_DIR=.config/dconf",
    "--talk-name=org.a11y.*",
    "--talk-name=org.freedesktop.Notifications"
    ]

clnup = [
    "/include",
    "/lib/pkgconfig",
    "/share/pkgconfig",
    "/share/aclocal",
    "/man",
    "/share/man",
    "*.la",
    "*.a"
]

# Define the structure for the build-options section
build_opts = {}
build_opts["cflags"] = "-O2 -g"
build_opts["cxxflags"] = "-O2 -g"
build_opts["env"] = {"V": "1"}

# Define the modules section
mdles = []

# Autoconf sources
acsrcs = []
acsrc = {}
acsrc["type"] = "archive"
acsrc["url"] = "http://ftp.gnu.org/gnu/autoconf/autoconf-2.13.tar.gz"
acsrc["sha256"] = hashsrc(acsrc["url"])
acsrcs.append(acsrc)

# Autoconf module
ac = {}
ac["name"] = "autoconf-2.13"
ac["cleanup"] = ["*"]
ac["sources"] = acsrcs
ac["post-install"] = ["ln -s /app/bin/autoconf /app/bin/autoconf-2.13"]
mdles.append(ac)

# icu sources
icusrcs = []
icusrc = {}
icusrc["type"] = "archive"
icusrc["url"] = "http://download.icu-project.org/files/icu4c/60.1/icu4c-60_1-src.tgz"
icusrc["sha256"] = hashsrc(icusrc["url"])
icusrcs.append(icusrc)

# icu module
icu = {}
icu["name"] = "icu"
icu["cleanup"] = ["/bin/*", "/sbin/*"]
icu["sources"] = icusrc
icu["subdir"] = {"subdir": "source"}
mdles.append(icu)

# Thunderbird build-options
tbirdbopt = {}
tbirdbopt["clfags"] = "-fno-delete-null-pointer-checks -fno-lifetime-dse -fno-schedule-insns2"
tbirdbopt["cxxflags"] = "-fno-delete-null-pointer-checks -fno-lifetime-dse -fno-schedule-insns2"
tbirdbopt["env"] = {"VERSION": "52.9.1"}

# Thunderbird build-commands
tbirdbc = [
    "make -f client.mk",
    "make -f client.mk install INSTALL_SDK=",
    "for i in 16 22 24 32 48 256;do mkdir -p /app/share/icons/hicolor/${i}x${i}/apps;cp /app/lib/thunderbird-${VERSION}/chrome/icons/default/default${i}.png /app/share/icons/hicolor/${i}x${i}/apps/thunderbird.png;done",
    "mkdir -p /app/share/applications",
    "mkdir -p /app/share/applications",
    "mkdir -p /app/share/appdata",
    "cp org.mozilla.Thunderbird.appdata.xml /app/share/appdata"
]

# Thunderbird sources
tbirdsrc = []

# mozconfig source
mozcfgsrc = {}
mozcfgsrc["type"] = "file"
mozcfgsrc["path"] = "mozconfig"
tbirdsrc.append(mozcfgsrc)

# .desktop source
dsksrc = {}
dsksrc["type"] = "file"
dsksrc["path"] = "org.mozilla.Thunderbird.desktop"
tbirdsrc.append(dsksrc)

# AppData source
appdata = {}
appdata["type"] = "file"
appdata["path"] = "org.mozilla.Thunderbird.appdata.xml"
tbirdsrc.append(appdata)

# Thunderbird source tar
tbtarsrc = {}
tbtarsrc["type"] = "archive"
tbtarsrc["url"] = "https://ftp.mozilla.org/pub/thunderbird/releases/52.9.1/source/thunderbird-52.9.1.source.tar.xz"
tbtarsrc["sha256"] = hashsrc(tbtarsrc["url"])
tbirdsrc.append(tbtarsrc)

# Thunderbird module
tbird = {}
tbird["name"] = "thunderbird"
tbird["buildsystem"] = "simple"
tbird["build-options"] = tbirdbopt
tbird["build-commands"] = tbirdbc
tbird["sources"] = tbirdsrc
#tbird["sources"] = tbirdsrc
mdles.append(tbird)

# Define the basic structure
data = {}
data["app-id"] = "org.mozilla.Thunderbird"
data["runtime"] = gnome_runtime
data["sdk"] = "org.gnome.Sdk"
data["command"] = "thunderbird"
data["rename-icon"] = "thunderbird"
data["finish-args"] = fin_args
data["build-options"] = build_opts
data["cleanup"] = clnup
data["modules"] = mdles
json_data = json.dumps(data)

# Spit out the JSON
print(json_data)