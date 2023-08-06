import socketio
import uuid
import json
import requests

class Rowma:
    """
    Rowma class implements some methods to operate connected robots.

    Attributes:
        base_url (string): ConnectionManager URL
    """

    def __init__(self, base_url = 'https://rowma.moriokalab.com'):
        self.base_url = base_url
        self.sio = socketio.Client()
        self.uuid = str(uuid.uuid4())
        self.namespace = '/rowma'
        self.handlers = {}

    def connect(self):
        """connect to ConnectionManager

        Returns:
            void: No return values

        Examples:
            >>> rowma.connect()

        Note:
            sleep(1) (1 second) exists in this method to wait for connection establishment.
        """

        self.sio.connect(self.base_url, namespaces=[self.namespace])
        # sleep 1 second for connection establishment
        self.sio.sleep(1)
        payload = { 'applicationUuid': self.uuid }
        self.sio.emit('register_application', data=payload, namespace=self.namespace)
        self.sio.on('topic_to_application', handler=self._baseHandler, namespace=self.namespace)

    def run_launch(self, uuid, command):
        """Send `roslaunch` command to the specified robot

        Args:
            uuid (string): Robot UUID
            command (string): An argument of roslaunch command like 'my_pkg test.launch'

        Returns:
            void: No return values

        Examples:
            >>> rowma.connect()
            >>> rowma.run_launch('xxxx-xxxx-xxxx', 'my_pkg test.launch')
            roslaunch my_pkg test.launch will be executed at xxxx-xxxx-xxxx
        """
        destination = { 'type': 'robot', 'uuid': uuid }
        payload = { 'destination': destination, 'command': command }
        self.sio.emit('run_launch', data=payload, namespace=self.namespace)

    def publish(self, uuid, topic, msg):
        """Publish a topic to the specified robot

        Args:
            uuid (string): Robot UUID
            topic (string): Topic name
            msg (any): Topic message based on the topic's type

        Returns:
            void: No return values

        Examples:
            >>> rowma.connect()
            >>> rowma.publish('xxxx-xxxx-xxxx', '/chatter', {'data': 'Hello World!'})

        Note:
            This method can not publish a topic to an Application, only to Robot.
        """
        destination = { 'type': 'robot', 'uuid': uuid }
        topic_message = {
            "op": "publish",
            "topic": topic,
            "msg": msg
        }
        payload = { 'destination': destination, 'msg': topic_message }
        self.sio.emit('topic_transfer', payload, namespace=self.namespace)

    def set_topic_route(self, dest_uuid, topic_dest_type, topic_dest_uuid, topic, alias=None):
        """Create a route of a topic

        Args:
            dest_uuid (string): The destination's UUID of this instruction
            topic_dest_type (string): 'robot' or 'application' for topic destination
            topic_dest_uuid (string): The destination's UUID of the topic
            topic (string): Topic name
            alias? (string): Alias of the topic name, default: None

        Returns:
            void: No return values

        Examples:
            >>> rowma.connect()
            >>> rowma.set_topic_route('xxxx-xxxx-robot', 'application', 'xxxx-xxxx-application, '/chatter'')

        Note:
            This method is a little tricky
        """
        destination = { 'type': 'robot', 'uuid': dest_uuid }
        topic_destination = { 'type': topic_dest_type, 'uuid': topic_dest_uuid }
        msg = {
          'op': 'subscribe',
          'topicDestination': topic_destination,
          'topic': topic
        }
        if alias: msg.update({ 'alias': alias })
        payload = {
                'destination': destination,
                'msg': msg
                }
        self.sio.emit('topic_transfer', payload, namespace=self.namespace)

    def run_rosrun(self, uuid, command, args=''):
        """Send `rosrun` command to the specified robot

        Args:
            uuid (string): Robot UUID
            command (string): The first argument of rosrun command like 'my_pkg my_node'
            args (string, optional): The other arguments for rosrun command like 'setting.yml'

        Returns:
            void: No return values

        Examples:
            >>> rowma.connect()
            >>> rowma.run_rosrun('xxxx-xxxx-xxxx', 'my_pkg my_node', 'setting.yml')
            rosrun my_pkg my_node setting.yml at xxxx-xxxx-xxxx
        """
        destination = { 'type': 'robot', 'uuid': uuid }
        payload = {
                'destination': destination,
                'command': command,
                'args': args
                }
        self.sio.emit('run_rosrun', payload, namespace=self.namespace)

    def kill_nodes(self, uuid, rosnodes):
        """Kill running rosnodes in the specified robot

        Args:
            uuid (string): Robot UUID
            rosnodes (Array<string>): The array of rosnodes' name

        Returns:
            void: No return values

        Examples:
            >>> rowma.connect()
            >>> rowma.kill_nodes('xxxx-xxxx-xxxx', ['/chatter', '/chatter2'])
        """
        destination = { 'type': 'robot', 'uuid': uuid }
        payload = {
                'destination': destination,
                'rosnodes': rosnodes
                }
        self.sio.emit('kill_rosnodes', payload, namespace=self.namespace)

    # TODO: Error handling
    def get_current_connection_list(self):
        """Fetch currently connected robots from ConnectionManager

        Returns:
            Robot List (Array<dict>): An array of robots

        Examples:
            >>> rowma.get_current_connection_list()
            [{'uuid': 'xxxx-xxxx-xxxx', 'rosnodes': [], ......}]
        """
        r = requests.get(self.base_url + '/list_connections')
        return json.loads(r.text)

    # TODO: Error handling
    def get_robot_status(self, uuid):
        """Fetch a robot by uuid from ConnectionManager

        Args:
            uuid (string): Robot UUID

        Returns:
            Robot (dict): An dict of a robot

        Examples:
            >>> rowma.get_robot_status('xxxx-xxxx-xxxx')
            {'uuid': 'xxxx-xxxx-xxxx', 'rosnodes': [], ......}
        """
        params = { 'uuid': uuid }
        r = requests.get(self.base_url + '/robots', params=params)
        return json.loads(r.text)

    def subscribe(self, topic, handler):
        """Add subscriber function to a topic

        Args:
            uuid (string): Robot UUID

        Returns:
            void: No return values

        Examples:
            >>> rowma.connect()
            >>> def callback(msg):
                ... print(msg)
            >>> rowma.subscribe('/chatter', callback)
        """
        self.handlers[topic] = handler

    def set_robot_uuid(self, robot_uuid):
        """Set robot UUID to current Application data stored in ConnectionManager

        Args:
            uuid (string): Robot UUID

        Returns:
            void: No return values

        Examples:
            >>> rowma.connect()
            >>> rowma.set_robot_uuid('xxxx-xxxx-xxxx')

        Note:
            This method is used when subscribing roslaunch_log or rosrun_log
        """
        payload = {
                'uuid': self.uuid,
                'robotUuid': robot_uuid
                }
        self.sio.emit('update_application', payload, namespace=self.namespace)

    def _baseHandler(self, msg):
        if msg['topic'] in self.handlers:
            handler = self.handlers[msg['topic']]
            handler(msg)
