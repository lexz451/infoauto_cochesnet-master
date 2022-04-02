FROM node:9-alpine as build


RUN apk update && apk add python build-base
RUN apk add git

RUN npm config set unsafe-perm true

RUN npm install -g gulp
RUN npm install -g bower

RUN echo '{ "allow_root": true }' > /root/.bowerrc

WORKDIR /

COPY . .

RUN npm set progress=false
RUN rm -rf package-lock.json
RUN npm install
RUN bower install
RUN npm rebuild node-sass
RUN gulp build

FROM nginx:latest

COPY --from=build /dist /usr/share/nginx/html
COPY --from=build /compose/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80