topic=$1
broker="http://redpanda:9092"
registry="http://redpanda:8081"

rpk topic create $topic -X brokers=$broker 2>&1 | {
  if ! grep -q "TOPIC_ALREADY_EXISTS"; then
      exit 1
  fi
}

rpk registry schema -X brokers=$broker -X registry.hosts=$registry create $topic-value --schema /schemas/$topic-value.avsc
