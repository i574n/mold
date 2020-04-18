#!/bin/bash


if [[ $UID != 0 ]]; then
    echo "Please run this script with sudo:"
    echo "sudo $0 $*"
    exit 1
fi


SCRIPT=$(readlink -f "$0")
SCRIPTPATH=$(dirname "$SCRIPT")


MOLD_HOME=$(realpath "$SCRIPTPATH/../../../..")

STARTUP_CODE="#!/bin/bash
export MOLD_HOME=$MOLD_HOME
source $MOLD_HOME/fs/linux/portable/mold/startup.sh
"

STARTUP_BASH_PATH="/etc/profile.d/mold_startup.sh"
echo "$STARTUP_CODE" > $STARTUP_BASH_PATH
chmod +x $STARTUP_BASH_PATH

STARTUP_ZSH_PATH="/home/$SUDO_USER/.oh-my-zsh/custom/mold_startup.zsh"
echo "$STARTUP_CODE" > $STARTUP_ZSH_PATH
chmod +x $STARTUP_ZSH_PATH

ln -s -f $MOLD_HOME/fs/linux/portable/exe/exe /usr/bin/exe


echo 'init ok'