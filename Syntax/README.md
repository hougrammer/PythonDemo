I won't even include a separate .py script as this is just a silly showcase of the some Python syntax.  The following function finds all unique combinations of `k` single-digit numbers that add up to `n`.  For example, with `k=3` and `n=9`, it returns `[[1,2,6], [1,3,5], [2,3,4]]`.  Admittedly, I wrote this just as practice to solve an algorithm problem, but I thought that it showed some nice things about Python syntax like `+` for list extension, list comprehensions, an intuitive tertiary statement structure, and indexing by boolean.  Of course, the one liner is horribly unreadable, but I'm just having a bit of fun.

```python
def combinationSum(k, n, start=1):
	return [[i]+c for i in xrange(start,10)	for c in self.combinationSum(k-1,n-i,i+1)] if k > 1 else [[], [[n]]][start<=n<=9]
```
