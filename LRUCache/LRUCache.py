class LRUCache(object):
    class _Node(object):
        def __init__(self, key, value):
            self.key = key
            self.value = value
            self.parent = None
            self.child = None
            
    def __init__(self, capacity):
        self.capacity = capacity if capacity else -1
        self.cache = {}
        self.first = None
        self.last = None
    
    # Promotes a node to the head of the list
    def promote(self, node):
        if self.first == node:
            return
        if self.first is None:
            self.first = self.last = node
            return
        
        if self.last == node:
            self.last = self.last.parent
        
        # if node was in list, connect nodes above and below
        if node.parent: node.parent.child = node.child
        if node.child: node.child.parent = node.parent
        
        # move node to first
        node.parent = None
        node.child = self.first
        self.first.parent = node
        self.first = node
        

    def get(self, key):
        if key not in self.cache or self.capacity < 0: return -1
        
        self.promote(self.cache[key])
        return self.cache[key].value

    def put(self, key, value):
        if self.capacity < 0: return
    
        if key in self.cache:
            self.cache[key].value = value
            self.promote(self.cache[key])
        else:
            # if there is still capacity left, decrease it
            if self.capacity:
                self.capacity -= 1
                
            # else remove last node,
            # taking care to check if it was the only node
            else:
                removed = self.last
                self.last = removed.parent
                if self.last: self.last.child = None
                del self.cache[removed.key]
                
            self.cache[key] = self._Node(key, value)
            self.promote(self.cache[key])