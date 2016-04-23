#!/bin/bash

BOLD=$(tput bold)
RED=$(tput setaf 1)
RESET=$(tput sgr0)

echo ''
if rm -f /usr/bin/p 2>/dev/null; then
  echo "Config files (~/.prc, ~/.p) were not removed. Backup them if you want then delete them manually."
else
  echo "Uninstall ${BOLD}${RED}failed${RESET}. You need administrative privileges to uninstall ${BOLD}p${RESET}."
  echo ''
  exit 1
fi
echo ''
