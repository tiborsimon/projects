#!/bin/bash

BOLD=$(tput bold)
RED=$(tput setaf 1)
GREEN=$(tput setaf 2)
RESET=$(tput sgr0)

USER_HOME=$(eval echo ~${SUDO_USER})

echo ''
echo "Installing ${BOLD}p${RESET}.."

if cp p /usr/bin/p 2>/dev/null; then
  
  if [ -f ${USER_HOME}/.prc ]; then
    echo "Config file (~/.prc) already exist."
  else
    touch ${USER_HOME}/.prc
    echo "Config file (~/.prc) created."
  fi

  if [ -d ${USER_HOME}/.p ]; then
    echo "Template directory (~/.p) already exist."
  else
    mkdir ${USER_HOME}/.p
    echo "Template directory (~/.p) created."
  fi

  echo "${BOLD}${GREEN}Success!${RESET}"

else
  echo "Uninstall ${BOLD}${RED}failed${RESET}. You need administrative privileges.."
  echo ''
  exit 1
fi
echo ''
