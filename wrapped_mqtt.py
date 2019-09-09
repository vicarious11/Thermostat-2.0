import paho.mqtt.publish as publish_single
import paho.mqtt.client as mqtt
import time
import threading


class MqttCustom():
    def __init__(self,
                 on_connect_func_ref,
                 on_message_func_ref,
                 on_disconnect_func_ref,
                 credentials={}):
        self.clientId = credentials.get("mqttclientid", None)
        self.server = credentials.get("mqttserver", "127.0.0.1")
        self.port = credentials.get("mqttport", 1883)
        self.mqttReconnectDelay = credentials.get("mqttreconnectdelay", 8)
        self.willSetTopic = credentials.get("willsettopic", None)
        self.willSetPayload = credentials.get("willsetpayload", None)
        self.keepalive = credentials.get("mqttkeepalive", 60)
        self.on_connect = on_connect_func_ref
        self.on_message = on_message_func_ref
        self.on_disconnect = on_disconnect_func_ref
        threading.Thread(target=self._mqtt_worker).start()
        time.sleep(1)

    def _retry_connection(self):
        while 1:
            time.sleep(self.mqtt_reconnect_delay)
            try:
                self.client.reconnect()
            except ConnectionRefusedError:
                pass
            else:
                return

    def _mqtt_worker(self):
        self.client = mqtt.Client(client_id=self.clientId)
        self.client.connectionStatus = 0
        if self.willSetTopic and self.willSetPayload:
            self.client.will_set(self.willSetTopic, self.willSetPayload)
        self.client.reconnect_delay_set(min_delay=1,
                                        max_delay=self.mqttReconnectDelay)
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message

        try:
            self.client.connect(self.server, self.port, self.keepalive)
        except ConnectionRefusedError:
            self._retry_connection()

        self.client.connectionStatus = 1
        self.client.loop_forever()

    def subscribe_topics(self, TopicsToSubscribe):
        if isinstance(TopicsToSubscribe, list):
            for topic in TopicsToSubscribe:
                self.client.subscribe(topic)
        elif isinstance(TopicsToSubscribe, str):
            self.client.subscribe(TopicsToSubscribe)

    def publish_topics(self, topic, payload):
        self.client.publish(topic, payload)

    def publish_high_priority(self, topic, payload):
        publish_single.single(topic,
                              payload,
                              hostname=self.server,
                              port=self.port)

    # : TODO --> __del__ method
