FROM ubuntu:22.04

USER root

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y ttyd bastet ninvaders nsnake greed pacman4console

COPY ./run.sh .
RUN chmod +x ./run.sh

ENV PATH="${PATH}:/usr/games"

EXPOSE 7681

ENTRYPOINT ["ttyd", "--base-path", "/arcade/", "bash", "./run.sh"]
