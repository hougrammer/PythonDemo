class LFUCache(object):
    # Stores key/value nodes along with their usage frequency.
    class _ItemNode(object):
        def __init__(self, key, value):
            self.key = key
            self.value = value
            self.freq = 1
            self.parent = None
            self.child = None
    
    # Stores linked lists of item nodes with equal frequencies.
    class _FreqNode(object):
        def __init__(self, freq):
            self.freq = freq
            self.first = None
            self.last = None
            self.prev = None
            self.next = None

        # Pops an item node out of the frequency node.
        def pop(self):
            item = self.first
            if self.first == self.last:
                self.first = self.last = None
            else:
                self.first = item.child
                item.child = None
                self.first.parent = None
            return item
        
        # Pushes an item node into the frequency node.
        def push(self, item):
            if not self.first:
                self.first = self.last = item
                item.parent = item.child = None
            else:
                item.parent = self.last
                item.child = None
                self.last.child = item
                self.last = item

    # Initialize LFU cache.
    # Capcities < 1 create an empyty cache.
    def __init__(self, capacity):
        self.capacity = capacity if capacity else -1
        self.cache = {} # stores key/value pairs
        self.freq = {0: _FreqNode(0)} # stores frequency nodes
    
    # Adds frequency node to cache.
    def _addFreqNode(self, prevNode, freq):
        newNode = _FreqNode(freq)
        newNode.prev, newNode.next = prevNode, prevNode.next
        if prevNode.next: prevNode.next.prev = newNode
        prevNode.next = newNode
        self.freq[freq] = newNode
        
    # Deletes frequency node from cache.
    def _deleteFreqNode(self, node):
        node.prev.next = node.next
        if node.next: node.next.prev = node.prev
        del self.freq[node.freq]
        
    # Increases the frequency of an item node.
    # Updates the frequency nodes to the new frequency.
    def _increaseFreq(self, item):
        c, f = self.cache, self.freq
        prevNode = f[item.freq]
        
        if prevNode.first == item: prevNode.pop()
        elif prevNode.last == item: prevNode.last = prevNode.last.parent
        
        if item.parent: item.parent.child = item.child
        if item.child: item.child.parent = item.parent

        item.freq += 1
        if item.freq not in f:
            self._addFreqNode(prevNode, item.freq)
        f[item.freq].push(item)
        
        if not prevNode.first:
            self._deleteFreqNode(prevNode)

    # Gets a key value from the cache.
    def get(self, key):
        if self.capacity == -1: return -1
        c, f = self.cache, self.freq
        
        if key not in c: return -1
        
        item = c[key]
        self._increaseFreq(item)
        return item.value

    # Puts a key value into the cache.
    def put(self, key, value):
        if self.capacity == -1: return
        c, f = self.cache, self.freq
        
        if key in c:
            c[key].value = value
            self._increaseFreq(c[key])
        else:
            if self.capacity:
                self.capacity -= 1
            else:
                removed = f[0].next.pop()
                if not f[0].next.first:
                    self._deleteFreqNode(f[0].next)
                del c[removed.key]
                
            item = _ItemNode(key, value)
            c[key] = item
            if 1 not in f:
                self._addFreqNode(f[0], 1)
            f[1].push(item)