FROM nginx:latest

COPY ./dist /usr/share/nginx/html
COPY ./compose/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80