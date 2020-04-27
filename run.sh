#!/usr/bin/env bash

if [ ! -f README.txt ]; then
	echo "Current working directory is not $(dirname $0), exit"
	exit 1
fi

if [ $# -eq 1 ] && [ $1 == "-i" ] ; then
	echo "[Info] Incremental: skip gn gen"
else
	echo "[Info] rm -rf out"
	rm -rf out

	printf "\033[32;1m$ utils/buildtools/gn.py gen --check out/darwin --root=. --dotfile=utils/buildtools/configs/.gn\033[0m\n"
	utils/buildtools/gn.py gen --check out/darwin --root=. --dotfile=utils/buildtools/configs/.gn

	if [ $? != 0 ]; then
		exit 1
	fi
fi

printf "\033[32;1m$ utils/buildtools/ninja.py -C out/darwin -v # verbose \033[0m\n"
utils/buildtools/ninja.py -C out/darwin -v

if [ $? != 0 ]; then
	exit 1
fi

if [ -f out/darwin/hello ]; then
	printf "\n"
	printf "\033[33;1m$ cd out/darwin && ./hello && cd ../.. # basic\033[0m\n"
	cd out/darwin && ./hello && cd ../..
	printf "\033[33;1m$ cd out && darwin/hello && cd .. # correctly encode runtime lib path\033[0m\n"
	cd out && darwin/hello && cd ..
	printf "\033[33;1m$ ... # copy exe and runtime to out/darwin/another_path/deeper .. # relocatable\033[0m\n"
	mkdir -p out/darwin/another_path/deeper
	cp out/darwin/hello out/darwin/another_path/deeper && cp -r out/darwin/runtime out/darwin/another_path/deeper
	out/darwin/another_path/deeper/hello
fi

printf "\033[33;1m$ tree -a out/darwin # list directory as tree\033[0m\n"
tree -a out/darwin

printf "\n[Info] To remove generated stuff: rm -rf out\n"
