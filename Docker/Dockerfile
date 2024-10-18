ARG PHP_VERSION=${PHP_VERSION:-php:8.1-fpm-alpine}

###PHP###
FROM ${PHP_VERSION}
ARG PHP_MODULES
ARG USER_ID
RUN addgroup -g ${USER_ID} -S app && adduser -u ${USER_ID} -S app -G app && \
    mkdir -p /usr/share/nginx/html

WORKDIR /usr/share/nginx/html

#Needed packages
RUN apk update && \
    apk add autoconf build-base git nodejs npm \ 
#PHP GD libraries
    libzip-dev \
    libpng-dev \
    libwebp-dev \
    libxpm-dev \
    libjpeg-turbo-dev \
    freetype-dev && \
#PHP GD
    docker-php-ext-configure gd \
    --with-webp \
    --with-jpeg \
    --with-xpm \
    --with-freetype && \
#Else
    docker-php-ext-install ${PHP_MODULES} pdo_mysql pdo mysqli exif gd && \
    pecl install apcu-5.1.21 || true && \
    pecl install memcache || true && \
    docker-php-ext-enable apcu opcache memcache || true

COPY ./conf/php/php.ini /usr/local/etc/php/php.ini
###PHP###
USER app