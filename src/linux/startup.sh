#!/bin/bash

if [ -z "${MOLD_HOME// }" ]; then
	echo "\$$MOLD_HOME is empty." >&2
	exit 1
fi

if [ ${MOLD_HOME:0:1} != "/" ]; then
	echo "\$MOLD_HOME is invalid ($MOLD_HOME)." >&2
	exit 1
fi

alias yt-mp3='youtube-dl -x --audio-format=mp3'

export DENO_INSTALL="/home/l1/.deno"
export PATH="$DENO_INSTALL/bin:$PATH"
export PATH="/mnt/c/home/fs/git-repos/elixir/bin:$PATH"





# eval "$(starship init bash)" # zsh
