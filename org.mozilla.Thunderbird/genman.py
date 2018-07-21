import json
import requests
import os
import hashlib
import argparse

# Setup arguments to be parsed
parser = argparse.ArgumentParser(description="Auto generates Thunderbirs' flatpak manifest")
parser.add_argument("-r", "--release", help="Thunderbird release version")
parser.add_argument("-o", "--output", help="File to write to", default="org.mozilla.Thunderbird.updated.json")
args = parser.parse_args()

# File to output the JSON to
output_file = args.output

# Version of the GNOME runtime to use
gnome_runtime = "3.28"

# Take the thunderbird release from the '-r' or --release' argument
release = args.release

# A function which takes a URL, requests the content, and makes a sha256 hash
# of it, and then returns said hash
def hashsrc(url):
    print("Getting " + url)
    r = requests.get(url)
    sha256 = hashlib.sha256()
    sha256.update(r.content)
    filechecksum = sha256.hexdigest()
    return(filechecksum)

# Define the finish-args
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

# Define the files/directories to cleanup
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
tbirdbopt["env"] = {"VERSION": release}

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

# URL formation
burl = "https://ftp.mozilla.org/pub/thunderbird/releases/"
srcdir = "/source/"
srctar = "thunderbird-" + release + ".source.tar.xz"
full_url = burl + release + srcdir + srctar

# Thunderbird source tar
tbtarsrc = {}
tbtarsrc["type"] = "archive"
tbtarsrc["url"] = full_url
tbtarsrc["sha256"] = hashsrc(tbtarsrc["url"])
tbirdsrc.append(tbtarsrc)

# Thunderbird module
tbird = {}
tbird["name"] = "thunderbird"
tbird["buildsystem"] = "simple"
tbird["build-options"] = tbirdbopt
tbird["build-commands"] = tbirdbc
tbird["sources"] = tbirdsrc
mdles.append(tbird)

# Define the basic structure
base = {}
base["app-id"] = "org.mozilla.Thunderbird"
base["runtime"] = gnome_runtime
base["sdk"] = "org.gnome.Sdk"
base["command"] = "thunderbird"
base["rename-icon"] = "thunderbird"
base["finish-args"] = fin_args
base["build-options"] = build_opts
base["cleanup"] = clnup
base["modules"] = mdles
json_data = json.dumps(base)

# Spit out the JSON
with open(output_file, 'w') as f:
        f.write(json_data)
