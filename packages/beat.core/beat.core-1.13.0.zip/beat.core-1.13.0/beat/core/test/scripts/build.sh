#!/usr/bin/env bash
set -e

mkdir -p build
pushd build
cmake ..
make
popd
rm build -rf
