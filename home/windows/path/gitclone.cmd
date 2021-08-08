@echo off
echo %1
set dist="%userprofile%/home/fs/repos"
echo %dist%
cd /D %dist%
git clone %1
