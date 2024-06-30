FROM alpine:3.20.1
WORKDIR /app

RUN apk add --no-cache curl unzip

# Download and unzip rpk
RUN curl -LO https://github.com/redpanda-data/redpanda/releases/download/v23.3.11/rpk-linux-amd64.zip
RUN unzip rpk-linux-amd64.zip -d /usr/local/bin
RUN chmod +x /usr/local/bin/rpk

COPY create_topic.sh /app/create_topic.sh
RUN mv /app/create_topic.sh /usr/local/bin/create_topic
RUN chmod +x /usr/local/bin/create_topic

ENTRYPOINT ["sh", "-c"]
CMD ["create_topic"]