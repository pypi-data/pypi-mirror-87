# PhysicsNum
 Physics Numerical methods applied and used during the bachlelor degree in Physics at Lund University. Most notbly is the numerical approximation methods and similar.
 The code regression works upon least square methods, and weighted least square methods and have been verified. If an issue occurs when using this package, contact via GitHub for a fast solution.

# Code
```python
xlist1 = np.array([1,2,3,4,5,6,7,8,9,10])
ylist1 = np.array([4,6,9,10,12,14,16,18,20,21])
Model = ForceLinearreg(xlist1, ylist1)
print(Model)
plt.plot(xlist1, ylist1, '.', label = "DATA")
plt.plot(xlist1, xlist1 * Model[0], '-', label = "Regression")
plt.legend()
plt.show()
```

# Contribute
 Feel free to contribute to this code, it is found on Github under the authors name.
