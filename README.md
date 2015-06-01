Druid metrics collector
===
A simple HTTP server that forwards Druid metrics to a Kafka topic.


Druid's HTTP emitter sends a batch of metrics to the HTTP endpoint. They typically look like this :

```
[
{"feed": "metrics", "user2": "Code Cache", "service": "middlemanager", "user1": "nonheap", "timestamp": "2015-04-22T19:31:17.685Z", "metric": "jvm/pool/max", "value": 50331648, "host": "middlemanager:8089"},
{"feed": "metrics", "user2": "Code Cache", "service": "middlemanager", "user1": "nonheap", "timestamp": "2015-04-22T19:31:17.685Z", "metric": "jvm/pool/max", "value": 50331648, "host": "middlemanager:8089"}
.....
]
```

Install
---
```
apt-get update
apt-get install -y python-pip
pip install kafka-python cherrypy docopt
```

Run
---
1. `druid-metrics-collector.py <broker_list> <kafka_topic> [--host=<socket_host>] [--port=<socket_port>] [--log=<dir>]`
2. Configure druid to send to the http://<host>:<port>/metrics endpoint.

Test
---
```
curl -XPOST localhost:9999/metrics -H "Content-Type: application/json" -d '[{"feed": "metrics", "user2": "Code Cache", "service": "middlemanager", "user1": "nonheap", "timestamp": "2015-04-22T19:31:17.685Z", "metric": "jvm/pool/max", "value": 50331648, "host": "middlemanager:8089"},{"feed": "metrics", "user2": "Code Cache", "service": "middlemanager", "user1": "nonheap", "timestamp": "2015-04-22T19:31:17.685Z", "metric": "jvm/pool/max", "value": 50331648, "host": "middlemanager:8089"}]'
```
