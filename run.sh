#!/bin/bash

green='\033[0;32m'
red='\033[0;31m'
clear='\033[0m'


echo -e "${red}
##############################################################################
# Please choose a game you like to play                                      #
#                               ├── Bastet (1)                               #
#                               ├── Ninvaders (2)                            #
#                               ├── Nsnake (3)                               #
#                               ├── Greed (4)                                #
#                               └── Pacman4console (5)                       #
#                                                                            #
#                           @@@ Use ctrl+C to exit a game @@@                #
##############################################################################
${clear}"
echo " "

echo -e "${green}Type the number of the game you wish${clear}"
read user_input
if [ $user_input == "1" ];
then
    cd /usr/games
    ./bastet
elif [ $user_input == "2" ];
then
    cd /usr/games
    ./ninvaders
elif [ $user_input == "3" ];
then
    cd /usr/games
    ./nsnake
elif [ $user_input == "4" ];
then
    cd /usr/games
    ./greed
elif [ $user_input == "5" ];
then
    cd /usr/games
    ./pacman4console
else
    echo -e "${red}Wrong! exiting...${clear}"
    exit
fi
