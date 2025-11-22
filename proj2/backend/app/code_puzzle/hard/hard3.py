def fib(n):
	a,b = 1,1
	for _ in range(n-2):
		a,b = b,a+b
	return b

print(fib(10))
