FROM ubuntu:22.04

USER root

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y ttyd bastet ninvaders nsnake greed pacman4console \
    nethack-console moon-buggy nudoku git

RUN git clone --depth=1 https://github.com/shakedc1599/Tennis-paper-game-bash.git /tmp/tennis && \
    cp /tmp/tennis/tennis.sh /usr/local/bin/tennis && \
    chmod +x /usr/local/bin/tennis && \
    rm -rf /tmp/tennis

COPY ./run.sh .
RUN chmod +x ./run.sh

ENV PATH="${PATH}:/usr/games"

EXPOSE 7681

ENTRYPOINT ["ttyd", "--base-path", "/arcade/", "-t", "fontSize=18", "bash", "./run.sh"]
