FROM ubuntu:22.04

USER root

# Update package repositories and upgrade installed packages
RUN apt-get update && apt-get upgrade -y
RUN apt-get install ttyd -y
# RUN ttyd bash

# Install required games
RUN apt-get install bastet -y
RUN apt-get install ninvaders -y
RUN apt-get install nsnake -y
RUN apt-get install greed -y
RUN apt-get install pacman4console

# Copy run.sh
COPY ./run.sh .

# chmoding
RUN chmod +x ./run.sh
ENV PATH="${PATH}:/usr/games/ninvaders"

EXPOSE 7681

ENTRYPOINT ["ttyd", "bash", "./run.sh"]
