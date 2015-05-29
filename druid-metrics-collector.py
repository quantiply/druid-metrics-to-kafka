"""
 Copyright 2014-2015 Quantiply Corporation. All rights reserved.
 
  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at
 
      http://www.apache.org/licenses/LICENSE-2.0
 
  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.

Usage:
  druid-metrics-collector.py <kafka_host> <kafka_port> <kafka_topic> [--log=<dir>]
"""
from docopt import docopt

import cherrypy
import json

from kafka.client import KafkaClient
from kafka.producer import SimpleProducer
import logging


class KafkaMetrics(object):
    
    def __init__(self, kafka_host, kafka_port, kafka_topic, log_file):
        logging.basicConfig(level=logging.INFO, filename=log_file)
        self.log = logging.getLogger('druid-kafka-metrics')
        self.log.info("Kafka (host=%s, port=%s, topic=%s), log=%s" %(kafka_host, kafka_port, kafka_topic, log_file))
        kafka = '%s:%s' % (kafka_host, kafka_port)
        client = KafkaClient(kafka)
        self.producer = SimpleProducer(client, batch_send=True,  batch_send_every_n=20, batch_send_every_t=60)
        self.msg_count = 0
        self.kafka_topic = kafka_topic
        
    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def metrics(self):
        messages = cherrypy.request.json

        for message in messages:
            self.msg_count += 1

            self.log.debug("%s - %s" % (self.msg_count, str(message)))
            self.producer.send_messages(self.kafka_topic, simplejson.dumps(message))

            if self.msg_count % 100 == 0 :
                self.log.info("%s messages processed." % (self.msg_count, ))

        return "{'code':200}"
    

if __name__ == '__main__':    
    arguments = docopt(__doc__, version='0.1.1rc')
    KAFKA_HOST = arguments['<kafka_host>']
    KAFKA_PORT = arguments['<kafka_port>'] #9092
    TOPIC = arguments['<kafka_topic>'] # "druid-metrics"
    LOG_FILE = "./druid_metrics.log"
    if arguments['--log']:
        LOG_FILE = arguments['--log']
    cherrypy.config.update({'server.socket_port': 9999})
    cherrypy.config.update({'server.socket_host': '0.0.0.0'})
    cherrypy.quickstart(KafkaMetrics(KAFKA_HOST, KAFKA_PORT, TOPIC, LOG_FILE))
