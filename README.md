Druid metrics ollector
===
A HTTP Server that sends Druid metrics to a Kafka topic.


Install
---
```
apt-get update
apt-get install -y python-pip
apt-get install -y python-twisted
pip install kafka-python cherrypy docopt simplejson
```

Run
---

`$ druid-metrics-collector.py <kafka_host> <kafka_port> <kafka_topic> [--log=<dir>]`
