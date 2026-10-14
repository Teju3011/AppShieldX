FROM redis:7.2-alpine

# Copy configuration and Lua security scripts
COPY redis.conf /usr/local/etc/redis/redis.conf
COPY scripts/ /data/scripts/

RUN chmod 644 /usr/local/etc/redis/redis.conf && chown -R redis:redis /usr/local/etc/redis /data

USER redis

EXPOSE 6379

CMD ["redis-server", "/usr/local/etc/redis/redis.conf"]
