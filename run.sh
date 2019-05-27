#!/usr/bin/env bash

if [ ! -f README.txt ]; then
	echo "Current working directory is not $(dirname $0), exit"
	exit 1
fi

echo "[Info] rm -rf out"
rm -rf out

printf "\033[32;1;m$ utils/buildtools/gn.py gen out/Default\033[0;m\n"
utils/buildtools/gn.py gen out/Default

if [ $? != 0 ]; then
	exit 1
fi

printf "\033[32;1;m$ utils/buildtools/ninja.py -C out/Default -v # verbose \033[0;m\n"
utils/buildtools/ninja.py -C out/Default -v

if [ $? != 0 ]; then
	exit 1
fi

if [ -f out/Default/hello ]; then
	printf "\n"
	printf "\033[33;1;m$ cd out/Default && ./hello && cd ../.. # basic\033[0;m\n"
	cd out/Default && ./hello && cd ../..
	printf "\033[33;1;m$ cd out && Default/hello && cd .. # correctly encode runtime lib path\033[0;m\n"
	cd out && Default/hello && cd ..
	printf "\033[33;1;m$ ... # copy exe and runtime to out/Default/another_path/deeper .. # relocatable\033[0;m\n"
	mkdir -p out/Default/another_path/deeper
	cp out/Default/hello out/Default/another_path/deeper && cp -r out/Default/runtime out/Default/another_path/deeper
	out/Default/another_path/deeper/hello
fi

printf "\033[33;1;m$ tree out/Default # list directory as tree \033[0;m\n"
tree out/Default

printf "\n[Info] To remove generated stuff: rm -rf out\n"
