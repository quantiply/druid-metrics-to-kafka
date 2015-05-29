Druid metrics collector
===
A simple HTTP server that forwards Druid metrics to a Kafka topic.


Install
---
```
apt-get update
apt-get install -y python-pip
pip install kafka-python cherrypy docopt
```

Run
---

`$ druid-metrics-collector.py <kafka_host> <kafka_port> <kafka_topic> [--log=<dir>]`
