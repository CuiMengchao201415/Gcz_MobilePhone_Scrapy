class DispatcherBase:
    def __init__(self):
        self.observers = dict()

    def add(self, key, handler):
        if self.observers.__contains__(key):
            self.observers[key].append(handler)
        else:
            self.observers[key] = [handler]

    def remove(self, key, handler):
        if self.observers.__contains__(key):
            lstHandler = self.observers[key]
            lstHandler.remove(handler)
            if (len(lstHandler) == 0):
                self.observers.pop(key)
        else:
            pass

    def dispatch(self, key, value=None):
        if self.observers.__contains__(key):
            lstHandler = self.observers[key]
            if lstHandler != None and len(lstHandler)>0:
                for handler in lstHandler:
                    if handler != None:
                        handler(value)
        else:
            pass


# region 单例
instance = None

def getInstance():
    global instance
    if not instance:
        instance = DispatcherBase()
    return instance
# endregion
