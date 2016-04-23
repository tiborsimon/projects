#!/bin/bash

M_NO_PROJECT='You have %sno projects%s in your project directory!'
M_ONLY_ONE_PROJECT='You only have %sone project%s. Entering that one..'
M_PROJECT_LIST_HEADER='You have %s%d projects%s on your machine.'
M_PROJECT_CHOOSER_PROMPT='Which project do you want to enter?'

BOLD=$(tput bold)
YELLOW=$(tput setaf 3)
GREEN=$(tput setaf 2)
RESET=$(tput sgr0)

PROJECT_COLOR=${YELLOW}
OTHER_COLOR=${GREEN}

create_new_project () {
  echo 'new project'
}

handle_project_root () {
  projects=($(ls))

  case ${#projects[*]} in
    0 )
      printf "\n$M_NO_PROJECT\n" ${BOLD} ${RESET}
      return 1 ;;
    1 )
      printf "\n$M_ONLY_ONE_PROJECT\n" ${BOLD} ${RESET}
      cd ${projects[0]}
      return 0 ;;
    * )
      ;;
  esac

  printf "\n$M_PROJECT_LIST_HEADER\n\n" ${BOLD} ${#projects[*]} ${RESET}
  for index in ${!projects[*]}; do
    printf "  [%s%d%s]:\t%s%s%s\n" "${PROJECT_COLOR}${BOLD}" $[index + 1] ${RESET} ${BOLD} ${projects[$index]} ${RESET}
  done

  printf "\n  [%sn%s]:\tNew project\n" "${OTHER_COLOR}${BOLD}" ${RESET}

  printf "\n\n" && tput cuu1
  while true; do
    echo -en "$M_PROJECT_CHOOSER_PROMPT "
    read input
    if [ $input -le ${#projects[*]} ] 2>/dev/null && [ $input -gt 0 ] 2>/dev/null; then
      cd "$PROJECTS/${projects[$[input - 1]]}"
      break
    elif [ "$input" == "n" ]; then
      create_new_project
      break
    fi
    tput cuu1; tput dch1; tput el
  done
}

handle_in_project_dir () {
  echo 'In project'
}

if [ "$(pwd)" = "$PROJECTS" ]; then
  handle_project_root
elif  echo $(pwd)|grep -q $PROJECTS ; then 
  handle_in_project_dir
else
  cd $PROJECTS
  handle_project_root
fi

