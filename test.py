def addDicts(original, addition): #, remove):
    if 'subsets' in addition:
        addition.pop('subsets', None)
    for key in addition:
        if key in original:
            if isinstance(original[key], dict) and isinstance(addition[key], dict):
                original[key] = addDicts(original[key], addition[key])
            # elif isinstance(original[key], int) and isinstance(addition[key], int): #or array
            else:
                original[key] += addition[key]
        else:
            original[key] = addition[key]
    return original

addDicts({'ad': 23, 'subsets': [1,2,3], 'hi': 213})
# import re
# a = "[[1,2,3,4,5,6,7], [1,2,3]]"
# # fib = re.sub(r'\], \[', '|', a)
# # fib = re.sub(r'\]|\[', '', fib)
# fib = re.sub(r'\], \[', '|', a)
# re.sub(r'\], \[', '@', a)
# fib = re.sub(r'\]|\[', '', fib)
# fib = fib.split('|')
# # for num in range(len(a)):
# #   a[num] = 0
# print fib
# print a
#
# a = [0,1,2,3,4,5]
# print a[2:4]
#
#
# words = ['AS-dc SFBKK', 'a', 'saj']
# word = 'b'
# # print words.lower()
# if not word in words:
#     print 'hi'
#
# for char in 'abcdefg':
#     print char
#
# c = {
#     'high': 34,
#     'donuts': 23
# }
#
# print isinstance({'hi': 0, 'a': 1}, dict)
#
# for i in range(4):
#     a += [[]]
#     print len(a)
#
#
# print '\n\n\n'
# if 'hi' in {'12': 23, 'hisa': 'hi'}:
#     print 'hi'

# in == in .keys()

# print 'hilo' if True

# x = {'hs': 23, if True: 'a': 12}
