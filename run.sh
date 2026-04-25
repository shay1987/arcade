#!/bin/bash

green='\033[0;32m'
red='\033[0;31m'
reset='\033[0m'

menu=(
    "##############################################################################"
    "# Please choose a game you like to play                                      #"
    "#                               ├── Bastet (1)                               #"
    "#                               ├── Ninvaders (2)                            #"
    "#                               ├── Nsnake (3)                               #"
    "#                               ├── Greed (4)                                #"
    "#                               └── Pacman4console (5)                       #"
    "#                               └── Quit (q)                                 #"
    "#                                                                            #"
    "#                           @@@ Use ctrl+C to exit a game @@@                #"
    "##############################################################################"
)

while true; do
    cols=$(tput cols 2>/dev/null || echo 80)
    rows=$(tput lines 2>/dev/null || echo 24)
    mw=${#menu[0]}
    mh=${#menu[@]}

    cr=$(( (rows - mh) / 2 ))
    cc=$(( (cols - mw) / 2 ))
    [ "$cr" -lt 0 ] && cr=0
    [ "$cc" -lt 0 ] && cc=0

    clear

    for i in "${!menu[@]}"; do
        tput cup $((cr + i)) "$cc"
        printf '%b%s%b' "$red" "${menu[$i]}" "$reset"
    done

    tput cup $((cr + mh + 1)) "$cc"
    printf '%b%s%b ' "$green" "Type the number of the game you wish:" "$reset"

    read -r user_input

    case "$user_input" in
        1) cd /usr/games && ./bastet ;;
        2) cd /usr/games && ./ninvaders ;;
        3) cd /usr/games && ./nsnake ;;
        4) cd /usr/games && ./greed ;;
        5) cd /usr/games && ./pacman4console ;;
        q|Q)
            clear
            printf '%b%s%b\n' "$red" "Goodbye!" "$reset"
            exit 0 ;;
        *)
            tput cup $((cr + mh + 3)) "$cc"
            printf '%b%s%b' "$red" "Invalid choice, please try again." "$reset"
            sleep 1 ;;
    esac

done
