This is an implementation of a least-recently-used (LRU) cache that has <code>O(1)</code> time complexity for both the <code>put</code> and <code>get</code> operations.
The cache stores key/value pairs until it reaches the capacity with which it was initialized.  
Any additional entries into the cache evicts the least recently used entry, where a use is defined as either updating a value (with another call to <code>put</code>) or retrieving a value (with a call to <code>get</code>).
<br><br>
One naive way to implement an LRU cache is to simply store all the key, value pairs in a stack (I'm abusing the fact that I can use Python lists, as stacks with random access capabilities).
Then, we simply do a linear search to find a key in order to update/retrieve it.  Both operations are <code>O(n)</code> and this cache is very slow.  I've implemented it in the <code>SlowCache</code> class.  
<br><br>
A slight improvement would be to at least store all the key/value pairs in a dictionary, improving retrieval to <code>O(1)</code>.  We still have a very slow update, as stacks are not the data structure we should be using.  The implementation of this medium speed cache is in <code>MedCache</code>.  
<br><br>
The fast implementation involves turning the stack into a doubly linked list.  Retrievals are now <code>O(1)</code>.  Hurray!
Honestly this algorithm is not that hard to come up with a basic knowledge of data structures.  The more interesting problem is the LFUCache, located elsewhere on this repository.  In any case, the fast implementation is <code>FastCache</code>.
