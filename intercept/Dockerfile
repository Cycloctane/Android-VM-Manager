FROM alpine:3.19

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apk/repositories;\
    apk add --no-cache --repository https://mirrors.tuna.tsinghua.edu.cn/alpine/edge/testing/ mitmproxy py3-pip;\
    python3 -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --no-cache-dir --break-system-packages sqlalchemy aiomysql redis orjson;\
    apk del py3-pip

WORKDIR /app

COPY ./mitm /app
RUN chmod +x /app/start.sh

# ENV MITM_HOST=
# ENV MITM_PROXY_PORT=
# ENV MITM_WEB_PORT=
# ENV SQLALCHEMY_DATABASE_URL=
# ENV REDIS_URL=
ENTRYPOINT [ "/app/start.sh" ]