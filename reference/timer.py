import time

start = time.time()

a = 0

for i in range(1000000):
    a += i

print("time :", time.time() - start)
print(a)