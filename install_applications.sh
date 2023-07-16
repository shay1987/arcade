#!/bin/bash

red='\033[0;31m'
clear='\033[0m'
green='\033[0;32m'


if [ "$EUID" -ne 0 ]; then 
    echo -e "${red}Please run as root${clear}"
    echo -e "${green}Exiting${clear}"
    exit 0
fi


function is_command_installed() {
    command -v "$1" >/dev/null 2>&1
}


function install_docker () {
    
    if is_command_installed docker; then
        echo "Docker is already installed"
        return
    fi

    echo "Removing older version of Docker"
    echo "................."
    apt-get remove docker docker-engine docker.io containerd runc
    echo "Installing Docker"
    echo "................."
    apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin
    echo "Manage Docker as a non-root user"
    groupadd docker
    usermod -aG docker $SUDO_USER
    gpasswd -a $SUDO_USER docker
    echo "Finished Docker installtion "
}


function install_k8s () {
    if is_command_installed kubectl; then
        echo "Kubernetes (kubectl) is already installed"
        return
    fi

    echo "Installing K8s"
    echo ".............."
    apt-get install -y ca-certificates curl
    echo "Finished Kubernetes installtion"
}


function install_minikube() {
    if minikube version >/dev/null 2>&1; then
        echo "Minikube is already installed"
        return
    fi

    echo "Installing Minikube"
    echo ".............."
    curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64.deb
    dpkg -i minikube-linux-amd64.deb
    apt-get install -f -y
    rm minikube-linux-amd64.deb
    echo "Finished Minikube installation"
}


function timer () {
    sec=10
    while [ $sec -ge 0 ]; do
            echo -ne "          $sec\033[0K\r"
            let "sec=sec-1"
            sleep 1
    done
}


echo -e "${green}The script will run the installtion now${clear}"
echo -e "${red}FYI there will be a reboot after so please save your work${clear}"
read -p "Do you wish to continue? (y/n)" user_input
if [ $user_input == "y" ] || [ $user_input == "Y" ]; then

    install_docker
    install_k8s
    install_minikube
    apt update -y && apt upgrade -y && apt autoremove -y

    echo "Finished installtion rebootting in 10 sec"
    timer

    reboot
else echo "Aborting..."
    exit 0
fi