1. The performance of quick-sort relies greatly on the selection of partition key, therefore quick-sort algorithm suggests a shuffling before the sorting. Here we propse a method to improve the selection of partition key - to make it closer to the middle point. The method is, instead of randomly pick one value, we randomly pick K values (K could be 3, 5, or higher, but according to our investigation, 5 is enough, we won't gain that much by going beyond 5), then find the middle one (median), then swap this one with the first value, then start the splitting （对接二分，两个盾构机相向而行，直到相遇）.

2. Here is the simulation code:
```python
N = 10000
M = 10000
vec = np.arange(N)

K = np.arange(start=1, stop=16, step=2)
ratio = np.full((len(K),), None, dtype=float)
theoretical_variance = (N*N-1)/12
for i, k in enumerate(K):
    sample = np.array([np.median(np.random.choice(vec, size=k, replace=False, p=None)) for i in np.arange(M)])
    print(np.mean(sample))
    print(np.var(sample))
    ratio[i] = np.var(sample)/theoretical_variance
print(ratio)
```
Here is thee result:
```python
5012.5153
8343458.23817
4947.8171
5051942.11225
4973.8719
3573911.48329
4980.3896
2773978.86661
4992.9284
2275894.59247
4972.6089
1933864.46754
4981.4073
1691273.55501
5016.4774
1463399.34069
[ 1.001215    0.60623306  0.42886938  0.33287747  0.27310735  0.23206374
  0.20295283  0.17560792]
```
We can see by using K = 3, 5, 7, 9, 11, we get unchanged expection, and the variance decreases to 58.33%, 44.05%, 32.14%, 27.38%, and 22.62%. We see that the decreasing after K=5 is not that significant, therefore we suggest use K=5 (or K=3).
