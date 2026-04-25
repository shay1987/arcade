#!/bin/bash

green='\033[0;32m'
red='\033[0;31m'
reset='\033[0m'

while true; do

    clear
    echo -e "${red}
##############################################################################
# Please choose a game you like to play                                      #
#                               ├── Bastet (1)                               #
#                               ├── Ninvaders (2)                            #
#                               ├── Nsnake (3)                               #
#                               ├── Greed (4)                                #
#                               └── Pacman4console (5)                       #
#                               └── Quit (q)                                 #
#                                                                            #
#                           @@@ Use ctrl+C to exit a game @@@                #
##############################################################################
${reset}"

    echo -e "${green}Type the number of the game you wish${reset}"
    read user_input

    case "$user_input" in
        1) cd /usr/games && ./bastet ;;
        2) cd /usr/games && ./ninvaders ;;
        3) cd /usr/games && ./nsnake ;;
        4) cd /usr/games && ./greed ;;
        5) cd /usr/games && ./pacman4console ;;
        q|Q) echo -e "${red}Goodbye!${reset}"; exit 0 ;;
        *) echo -e "${red}Invalid choice, please try again.${reset}" ;;
    esac

done
