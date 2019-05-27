#!/usr/bin/env python
# Copyright: see README and LICENSE under the project root directory.
# Author: @Leedehai
#
# File: gn.py
# ---------------------------
# Wrapper script of the GN binary. If binary is not found, it will
# download it.

import os, sys, platform
import subprocess

def get_platform():
    if platform.machine() not in ["AMD64", "x86_64"]:
        return None
    if sys.platform.startswith("linux"):
        return "linux-amd64"
    if sys.platform == "darwin":
        return "mac-amd64"
    raise NotImplementedError("Platform '%s' not supported" % sys.platform)

BIN_DIR = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), "bin", (
        "linux" if get_platform().startswith("linux") else "darwin"))
BIN_PATH = os.path.join(BIN_DIR, "gn")

def main(args):
    if not os.path.isfile(BIN_PATH):
        if 0 != subprocess.call([
            os.path.join(os.path.dirname(os.path.dirname(BIN_DIR)), "get-binary.py") ]):
            return 1
    return subprocess.call([ BIN_PATH ] + args[1:])

if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv))
    except KeyboardInterrupt:
        sys.stderr.write("Interrupted")
        sys.exit(1)