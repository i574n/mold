#!/bin/bash

echo 'start'

cd ~
mkdir -p "home" && cd "$_"
mkdir -p "fs" && cd "$_"
mkdir -p "tmp" && cd "$_"

curl -LO matmoul.github.io/archfi

sh archfi

# english
# br-abnt2
# vim
# auto partitions gpt
