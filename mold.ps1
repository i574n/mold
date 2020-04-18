# https://tinyurl.com/mold-init
# Set-ExecutionPolicy RemoteSigned -scope CurrentUser
iwr -useb "https://gist.githubusercontent.com/fc1943s/e02c64f526fe279eb9397592d2bd1c3b/raw/mold.ps1?t=$((get-date -uf '%s').Replace('.',''))" | iex
pause
