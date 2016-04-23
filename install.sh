#!/bin/bash

BOLD=$(tput bold)
RED=$(tput setaf 1)
GREEN=$(tput setaf 2)
RESET=$(tput sgr0)

echo ''
echo "Installing ${BOLD}p${RESET}.."

if cp p /usr/bin/p 2>/dev/null; then
  
  if [ -f ~/.prc ]; then
    touch ~/.prc
    echo "Config file (~/.prc) created."
  else
    echo "Config file (~/.prc) already exist."
  fi

  if [ -d ~/.p ]; then
    mkdir ~/.p
    echo "Template directory (~/.p) created."
  else
    echo "Template directory (~/.p) already exist."
  fi

  echo "${BOLD}${GREEN}Success!${RESET}"

else
  echo "Uninstall ${BOLD}${RED}failed${RESET}. You need administrative privileges.."
  echo ''
  exit 1
fi
echo ''
