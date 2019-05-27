#!/usr/bin/env python
# Copyright: see README and LICENSE under the project root directory.
# Author: the LLVM authors, @Leedehai
#
# File: get-binary.py
# ---------------------------
# Download latest GN and Ninja binaries.
# You do not need to execute this script directly; gn.py and ninja.py will execute
# it if binaries are needed but not found.

import io
import os
import sys
import zipfile
import platform
import subprocess
import argparse

try: # For Python 3.0 and later, nasty Python
    from urllib.request import urlopen
    from urllib.error import HTTPError
    from urllib.error import URLError
except ImportError: # Fall back to Python 2's urllib2
    from urllib2 import urlopen
    from urllib2 import HTTPError
    from urllib2 import URLError

def get_platform():
    if platform.machine() not in ["AMD64", "x86_64"]:
        return None
    if sys.platform.startswith("linux"):
        return "linux-amd64"
    if sys.platform == "darwin":
        return "mac-amd64"
    raise NotImplementedError("Platform '%s' not supported" % sys.platform)

PLATFORM = get_platform()
BIN_DIR = os.path.join(
    os.path.dirname(__file__), "bin", ("linux" if PLATFORM.startswith("linux") else "darwin"))
GN_BIN = "gn"
GN_URL = "https://chrome-infra-packages.appspot.com/dl/gn/gn/%s/+/latest" % PLATFORM
NINJA_BIN = "ninja"
NINJA_URL = "https://chrome-infra-packages.appspot.com/dl/infra/ninja/%s/+/latest" % PLATFORM

def download_and_unpack(what, url, output_dir, bin_name, only_dowload_if_must):
    """Download an archive from url and extract gn from it into output_dir."""
    file_path = os.path.join(output_dir, bin_name)
    already_exist = os.path.isfile(file_path)
    if only_dowload_if_must and already_exist:
        print("[build tools] %s binary for '%s' already downloaded" % (what, PLATFORM))
        return True
    if already_exist:
        os.remove(file_path)
    print("[build tools] Downloading %s binary for '%s'..." % (what, PLATFORM))
    sys.stdout.flush()
    try:
        zipfile.ZipFile(io.BytesIO(urlopen(url).read())).extract(bin_name, path=output_dir)
    except HTTPError as e:
        print("HTTPError to %s\n%s" % (url, e))
        if int(e.code / 100) == 4:
            print("************** ACTION APPRECIATED **************")
            print("*                                              *")
            print("* If you are *certain* this URL (operated by   *")
            print("* Google Cloud) is not blocked in your region, *")
            print("* please alert the project author the URL was  *")
            print("* likely deprecated, HTTP error %3s            *" % e.code)
            print("*                                              *")
            print("************************************************")
        return False
    except URLError as e:
        print("URLError %s, message: %s" % (url, e))
        print("Are you disconnected from the network? (other reasons may apply)")
        return False
    except Exception as e:
        print(e)
        return False
    return True

def set_executable_bit(path):
    mode = os.stat(path).st_mode
    mode |= (mode & 0o444) >> 2 # Copy R bits to X.
    os.chmod(path, mode)

def print_version_number(path):
    try:
        version_info = subprocess.check_output([path, "--version"]).decode().strip()
    except subprocess.CalledProcessError as e:
        print("[Error] '%s --version' returns an error")
        return False
    print("%14s'%s --version': %s" % (" ", os.path.basename(path), version_info))
    return True

def main():
    parser = argparse.ArgumentParser(description="Download latest GN and Ninja binaries",
                                     epilog="For what GN and Ninja are, and why this project ditched Make,\nsee //zen/why-gn-ninja.md",
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-i", "--only-download-if-must", action="store_true",
                        help="only download if the binary does not exist")
    parser.add_argument("-r", "--remove", action="store_true", # remove bin/darwin or bin/linux, depending on the current OS
                        help="remove downloaded binaries in %s" % BIN_DIR)
    parser.add_argument("-ra", "--remove-all", action="store_true", # remove bin/, bin/darwin, bin/linux
                        help="remove directory %s" % os.path.dirname(BIN_DIR))
    args = parser.parse_args()

    if args.remove:
        subprocess.call("rm -rf ./%s &> /dev/null" % BIN_DIR, shell=True)
        return 0
    elif args.remove_all:
        subprocess.call("rm -rf ./%s &> /dev/null" % os.path.dirname(BIN_DIR), shell=True)
        return 0

    if not PLATFORM:
        print("no prebuilt binary offered for '%s'" % sys.platform)
        return 1

    if not os.path.exists(BIN_DIR):
        os.makedirs(BIN_DIR) # os.makedirs() recursively make the intermediate directories

    has_error = False

    if True == download_and_unpack("GN", GN_URL, BIN_DIR, GN_BIN, args.only_download_if_must):
        set_executable_bit(os.path.join(BIN_DIR, GN_BIN))
        if False == print_version_number(os.path.join(BIN_DIR, GN_BIN)):
            has_error = True
    else:
        has_error = True

    if True == download_and_unpack("Ninja", NINJA_URL, BIN_DIR, NINJA_BIN, args.only_download_if_must):
        set_executable_bit(os.path.join(BIN_DIR, NINJA_BIN))
        if False == print_version_number(os.path.join(BIN_DIR, NINJA_BIN)):
            has_error = True
    else:
        has_error = True

    if has_error:
        print("Error encountered: cannot download binaries.")
        print("To circumvent: see %s/README.md section 'Alternative setup'." % os.path.dirname(__file__))

    return 1 if has_error else 0

if __name__ == "__main__":
    sys.exit(main())
