# Build tools: GN + Ninja

[Ninja](https://ninja-build.org) is the build tool of this project, and [GN](https://gn.googlesource.com/gn/) is the meta-build utility that generates Ninja files. You do not need to install them manually, because there are scripts that automate the process.

- `gn.py`: wrapper script for the GN binary.
- `ninja.py`: wrapper script for the Ninja binary.
- `get-binary.py` downloads the GN and Ninja binaries from the repository maintained by the Google Chrome project. You do not need to execute this script directly; `gn.py` and `ninja.py` will execute it if binaries are needed but not found. Use option `-r` to remove the binaries.

Of course, you can execute `get-binary.py` on your own. Use option `-h` for help.

Re-executing the `get-binary.py` script will re-download all binaries. If you wish to only install the ones that are missing, pass option `-i`.

### Alternative setup
> How to not execute `get-binary.py`.

If you do not want to download the binaries over the network, or the downloading script threw an error, you need to have built/installed GN and Ninja binaries on your machine. In this case, you should manually create two symbolic links so that `gn.py` and `ninja.py` can find them:
```sh
# 1. create directory
# assume your current directory is this directory.
mkdir -p bin/linux  # for macOS: mkdir -p bin/darwin

# 2. create symbolic links
# assume your GN and Ninja binaries are at /usr/local/bin
cd bin/linux  # for macOS: cd bin/darwin
ln -s /usr/local/bin/gn gn
ln -s /usr/local/bin/ninja ninja
cd ../..

# 3. verify
./gn.py --version
./ninja.py --version
```

It is your responsibility to ensure your GN and Ninja binaries are up-to-date with the releases used by the Chromium projects.

> You may ask... why can't `gen.py` and `ninja.py` just use `gn` and `ninja` on my `PATH`? Answer: many users do not have GN and Ninja installed by default, and they do not want to install something into their `PATH` just for one project.

###### EOF
