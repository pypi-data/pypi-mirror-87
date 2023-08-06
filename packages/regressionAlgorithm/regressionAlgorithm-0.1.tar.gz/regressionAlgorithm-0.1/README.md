# POLINOMIAL REGRESSION ALGORITHM

```bash
pip3 install regressionAlgorithm
```
## POLYNOMIAL ORDER 1

!['formula'](https://i.postimg.cc/R3qrYY4P/least-squared.png)

```python
from regressionAlgorithm import PolynomialOrderOne
import matplotlib.pyplot as plt

# value
x = [1,2,3,4,5]
y = [5,4,3,2,1]

# intial
rl = PolynomialOrderOne()
rl.fit(x,y)
rl.start()

# get data
print(rl.plot())
print(rl.line())

# data visualization

plt.figure(figsize=(10,7))
plt.scatter(x,y)
plt.plot(x, rl.line())
plt.savefig("visual.png")

# r squared
print(rl.r_squared()) # result 1.0

# r value
print(rl.r_value()) # result -1.0
```
![graph.png](https://i.postimg.cc/hvd4PJR2/graph.png)

### PREDICT Y VALUE
```python
...
x = 10
# formula (y = a + b * x) = (y = a + b * 10)
print(rl.predict(x)) # result -4.0
```

## POLYNOMIAL ORDER 2

!['formula](https://i.postimg.cc/18vhJShn/kuadratik.png)

```python
from regressionAlgorithm import PolynomialOrderTwo
import matplotlib.pyplot as plt

# value
x = [1,2,3,4,5]
y = [5,4,3,2,1]

# intial
q = PolynomialOrderTwo()
q.fit(x,y)
q.start()

# result
print(q.plot())
print(q.r_square())

# data visualization
plt.figure(figsize=(10,7))
plt.scatter(x,y, color="blue")
plt.plot(x, k.draw_line(), color="red")
plt.savefig("quadratic.png")
```
![quadratic.png](https://i.postimg.cc/G2wVdprj/quadratic.png)

### PREDICT Y VALUE

```python
...
x_pred = 5

# formula y = a + b * x + c * square(x) -> y = a + b * x_red + c * square(x_pred)
print(q.predict(x_pred)) # result 0.9999999999997522
```