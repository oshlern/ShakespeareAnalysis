import re
a = "[[1,2,3,4,5,6,7], [1,2,3]]"
# fib = re.sub(r'\], \[', '|', a)
# fib = re.sub(r'\]|\[', '', fib)
fib = re.sub(r'\], \[', '|', a)
re.sub(r'\], \[', '@', a)
fib = re.sub(r'\]|\[', '', fib)
fib = fib.split('|')
# for num in range(len(a)):
#   a[num] = 0
print fib
print a
