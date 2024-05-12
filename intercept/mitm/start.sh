#! /bin/ash
mitmweb --listen-host $MITM_HOST --listen-port $MITM_PROXY_PORT --no-web-open-browser --web-host $MITM_HOST --web-port $MITM_WEB_PORT --set confdir=./config --scripts ./scripts/main.py --no-http2 --no-rawtcp --set stream_large_bodies=10m
