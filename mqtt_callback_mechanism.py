import json


class CallbackMechanism:

    callbackFunctionsTriggers = {}

    @staticmethod
    def wrap_on_connect(on_connect_func):
        """Wraps on_connect function.

        General : Hides details. Clean on the user side.
        Current Utility : saves connection status. Mqtt object should be
            responsible for maintaining connection state. Hence, connection
            status can now be accessed from anywhere using
            mqttObj.client.connectionStatus
        Future Scope : Any general logging/tasks to be done
            whenever client gets connected.
        """

        def wrapped_on_connect(*args):
            client = args[0]
            rc = args[3]
            if rc == 0:
                client.connectionStatus = 1
            on_connect_func(client)

        return wrapped_on_connect

    @staticmethod
    def wrap_on_disconnect(on_disconnect_func):
        """Wraps on_disconnect function.

        General : Hides details. Clean on the user side.
        Current Utility : saves connection status. Mqtt object should be
            responsible for maintaining connection state. Hence, connection
            status can now be accessed from anywhere using
            mqttObj.client.connectionStatus
        Future Scope : Any general logging/tasks to be done
            whenever client gets disconnected.
        """

        def wrapped_on_disconnect(*args):
            client = args[0]
            rc = args[2]
            if rc != 0:
                client.connectionStatus = 0
            on_disconnect_func(client)

        return wrapped_on_disconnect

    @classmethod
    def make_callback(cls, clientId, condition):
        """Easy decorator which adds callback with its trigger in the callback store.

        clientId(str) : for which client this callback is meant for.
        condition(str) : which condition should trigger this callback.
            e.g. `topic.split("/")[0] == "data"`
        Current Utility : Automatically callback gets triggered.
            Makes functions signature more readable on the user side.
            Enforcing callback mechanism avoids complex if/else and an elegant
            method simple to add and register callbacks.
        """

        def decorator(callbackFunc):
            if clientId not in cls.callbackFunctionsTriggers:
                cls.callbackFunctionsTriggers[clientId] = {}
            cls.callbackFunctionsTriggers[clientId][condition] = callbackFunc

            return callbackFunc

        return decorator

    @classmethod
    def register_callback(cls, *, clientId, condition, callbackFunc):
        """Same utility as above.
        Used when need to add a callback in the runtime. See examples on the
        user side.
        """
        if clientId not in cls.callbackFunctionsTriggers:
            cls.callbackFunctionsTriggers[clientId] = {}
        cls.callbackFunctionsTriggers[clientId][condition] = callbackFunc

    @classmethod
    def wrap_on_message(cls, on_message_func):
        """Wraps on_message function.
        General : Abstract way of triggering callbacks - hiding complex
            details. Manages callbacks and triggers. Not being dependent on any
            global callback data structure. One common easy callback interface.
            Also power of original on_connect,on_disconnect,on_message is still
            with users.using this is optional since mqtt library is untouched
            from this callback mechanism.
        Current Utility : automatically triggers callbacks based on different
            conditions.
        Future scope : any type of general logging/task needed to be performed
            every time a message is receieved.
        """
        def wrapped_on_message(*args):
            client = args[0]
            msg = args[2]
            clientId = str(client._client_id)[2:-1]
            topic = msg.topic
            payload = str(msg.payload)[2:-1]
            payload = json.loads(payload.replace("'", '"'))
            on_message_func(topic, payload)
            for condition, callback in cls.callbackFunctionsTriggers[
                    clientId].items():
                if eval(condition):
                    callback(topic, payload)

        return wrapped_on_message
