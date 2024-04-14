FROM busybox:1.35

ARG IP=$IP

RUN adduser -D stud
USER stud
WORKDIR /home/stud

COPY src/ .

RUN sed -i "s/ipAddress/$IP/g" index.html && \
    sed -i "s/ipAddress/$IP/g" game.js

ENTRYPOINT ["busybox"]
CMD ["httpd", "-f", "-v", "-p", "3000"]