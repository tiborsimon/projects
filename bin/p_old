#!/usr/bin/env bash

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

print_projects () {
  projects=$1
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
}

handle_project_selection () {
  projects=$1
  register=''
  printf "\n\n" && tput cuu1
  while true; do
    printf  "%s %s" "$M_PROJECT_CHOOSER_PROMPT" "$register"
    IFS='' read -s -r -n 1 -d '' input

    if [ ${#register} -eq 0 ] && [ "$input" == "n" ]; then
      create_new_project
      break
    fi

    if [ $input -le ${#projects[*]} ] 2>/dev/null; then
      if [ ${#projects[*]} -lt 10 ] && [ $input -gt 0 ] 2>/dev/null; then
        cd "$PROJECTS/${projects[$[input - 1]]}"
        break
      else

        if [ ${#register} -eq 1 ]; then
          echo -en 'most'
          if [ "$input" == "\n" ]; then
            echo 'enter'
            cd "$PROJECTS/${projects[$[register - 1]]}"
            break
          elif [ "$input" == $'\x7f' ]; then
            echo 'backspace'
            register=''
          else
            register="$register$input"
            if [ $register -gt ${#projects[*]} ]; then
              register=''
            else
              echo -en $input
              cd "$PROJECTS/${projects[$[register - 1]]}"
              break
            fi
          fi
        fi

        if [ ${#register} -eq 0 ] && [ $input -gt 0 ] 2>/dev/null; then
          register=$input
        fi

      fi
    fi
    tput el1
    printf "\r"
  done
  printf "\n"
}

handle_project_root () {
  projects=($(ls))
  print_projects $projects
  handle_project_selection $projects
}

handle_in_project_dir () {
  if [ -f Projectfile ]; then
    source Projectfile
    for c in "${!commands[@]}"; do 
      echo $c
    done
  else
    echo 'No project file..'
  fi
}

if [ "$(pwd)" = "$PROJECTS" ]; then
  handle_project_root
elif  echo $(pwd)|grep -q $PROJECTS ; then 
  handle_in_project_dir
else
  cd $PROJECTS
  handle_project_root
fi

unset -f create_new_project
unset -f handle_project_root
unset -f handle_in_project_dir
unset -f print_projects
unset -f handle_project_selection

