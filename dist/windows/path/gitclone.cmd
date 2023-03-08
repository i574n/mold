@echo off
echo %1
set dist="%SystemDrive%/home/git"
echo %dist%
cd /D %dist%
git clone %1
