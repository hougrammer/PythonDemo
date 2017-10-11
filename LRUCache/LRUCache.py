class SlowCache(object):
    def __init__(self, capacity):
        if capacity < 1: raise ValueError('Invalid capacity')
        self.capacity = capacity
        self.stack = []
    
    # Promotes a key to the top of the stack
    # Returns true if the key was in the stack
    def _promote(self, key):
        for i, (k,v) in enumerate(self.stack):
            if k == key:
                self.stack.append(self.stack.pop(i))
                return True
        return False
        
    def get(self, key):
        if self._promote(key):
            return self.stack[-1][1]
        raise KeyError(1)

    def put(self, key, value):
        if self._promote(key):
            self.stack[-1][1] = value
        else:
            if self.capacity:   self.capacity -= 1
            else:               self.stack.pop(0)
            
            self.stack.append([key, value])

class MedCache(object):
    def __init__(self, capacity):
        if capacity < 1: raise ValueError('Invalid capacity')
        self.capacity = capacity
        self.stack = []
        self.cache = {}
    
    # Promotes a key to the top of the stack
    # Returns true if the key was in the stack
    def _promote(self, key):
        if key not in self.cache: return False
        s = self.stack
        s.append(s.pop(s.index(key)))
        return True
        
    def get(self, key):
        return self.cache[key]

    def put(self, key, value):
        if self._promote(key):
            self.cache[key] = value
        else:
            if self.capacity:   self.capacity -= 1
            else:               del self.cache[self.stack.pop(0)]
            
            self.stack.append(key)
            self.cache[key] = value

class FastCache(object):
    class _Node(object):
        def __init__(self, key, value):
            self.key = key
            self.value = value
            self.parent = None
            self.child = None
            
    def __init__(self, capacity):
        if capacity < 1: raise ValueError('Invalid capacity')
        self.capacity = capacity
        self.cache = {}
        self.first = None
        self.last = None
    
    # Promotes a node to the head of the list
    def _promote(self, node):
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
        if key not in self.cache or self.capacity < 0: 
            return None
        
        self._promote(self.cache[key])
        return self.cache[key].value

    def put(self, key, value):
        if self.capacity < 0: return
    
        if key in self.cache:
            self.cache[key].value = value
            self._promote(self.cache[key])
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
            self._promote(self.cache[key])