FROM node:9-alpine


RUN apk update && apk add python build-base
RUN apk add git

RUN npm config set unsafe-perm true

RUN npm install -g gulp
RUN npm install -g bower

RUN echo '{ "allow_root": true }' > /root/.bowerrc

COPY ./compose/entrypoint.sh /entrypoint
RUN sed -i 's/\r//' /entrypoint
RUN chmod +x /entrypoint

COPY ./compose/start.sh /start
RUN sed -i 's/\r//' /start
RUN chmod +x /start

WORKDIR /code
ENTRYPOINT ["/entrypoint"]
