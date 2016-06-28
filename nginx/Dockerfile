FROM nginx

ADD sites-enabled/ /etc/nginx/sites-enabled

RUN rm /etc/nginx/conf.d/default.conf
ADD conf.d/ /etc/nginx/conf.d
