def publish(log, name, *args):
    seq = len(log)
    event = dict(seq=seq, name=name, args=args)
    log.append(event)


class LogList(list):
    """
    A list that notifies all listeners whenever a new item is appended.
    Can be used o implement a simple event system.
    """

    def __init__(self, *args, **kwargs):
        self._listeners = set()
        super(LogList, self).__init__(*args, **kwargs)

    def add_listener(self, listener):
        self._listeners.add(listener)

    def remove_listener(self, listener):
        self._listeners.remove(listener)

    def append(self, event):
        super(LogList, self).append(event)
        for listener in self._listeners:
            listener._on_log_change(event)


class LogListener:

    """
    Can be connected to a list in a object. Every time a new event is appended to the list, a method in this object
    will be called. The method triggered by the item append should follow the naming convention "_on_" + event.name
    """

    def __init__(self):
        self.log = None

    def connect(self, log_ref, context):
        """
        Make this object to listen to a log. It can only listen to one log. Connect it to a log will make it
        automatically disconnect from the previous one.
        :param log_ref: name of an attribute that holds a LogList
        :param context: object that has a LogList attribute
        """
        if self.log is not None:
            self.log.remove_listener(self)
        log = LogList(context[log_ref])
        log.add_listener(self)
        context[log_ref] = log
        self.log = log

    def publish(self, name, *args):
        publish(self.log, name, *args)

    def _on_log_change(self, event):
        handler_name = '_on_' + event['name']
        if hasattr(self, handler_name):
            handle_event = getattr(self, handler_name)
            handle_event(*event['args'])
