# GNTest

Taken from Google [GN repo](https://gn.googlesource.com/gn/)'s [tools/gn/example](https://gn.googlesource.com/gn/+/refs/heads/master/tools/gn/example/), and fixed the original's bug of being broken on Mac.

Tested on Mac and Linux, x64.

Execute:
```sh
./run.sh
./run.sh -i # incremental re-build (try modifying some files)
```
If everything runs fine, three `Hello world` will be printed, followed by a tree graph of files.

### Prerequisites
- macOS or Linux
- Python 2.7 or Python 3
- Clang and Clang++ compilers (to use GCC compilers, replace `clang` with `gcc`, and `clang++` with `g++` in all files)

### GN overall build flow
> [GN reference](https://gn.googlesource.com/gn/+/master/docs/reference.md), [GN language](https://gn.googlesource.com/gn/+/master/docs/language.md)

```
1. Look for ".gn" file (see "gn help dotfile") in the current directory and
   walk up the directory tree until one is found. Set this directory to be
   the "source root" and interpret this file to find the name of the build
   config file.

2. Execute the build config file identified by .gn to set up the global
   variables and default toolchain name. Any arguments, variables, defaults,
   etc. set up in this file will be visible to all files in the build.

3. Load the //BUILD.gn (in the source root directory).

4. Recursively evaluate rules and load BUILD.gn in other directories as
   necessary to resolve dependencies. If a BUILD file isn't found in the
   specified location, GN will look in the corresponding location inside
   the secondary_source defined in the dotfile (see "gn help dotfile").

5. When a target's dependencies are resolved, write out the `.ninja` 
   file to disk.

6. When all targets are resolved, write out the root build.ninja file.
```

###### EOF