FROM python:3.9-alpine

RUN apk add which git cmake make g++ && \
    pip install -U flask

RUN touch /README.md && \
    mkdir -p /bin && \
    echo '#!/bin/sh' > /bin/print_hello && \
    echo 'echo "Hello world"' >> /bin/print_hello && \
    chmod +x /bin/print_hello

COPY . .

RUN mkdir -p build && cd build && cmake .. && make && \
    chmod +x /bin/C

RUN adduser -D devops2024user
USER devops2024user
EXPOSE 8898

CMD ["python3", "app.py", "--host", "0.0.0.0", "--port", "8898"]
