# -*- coding: utf-8 -*-
# TODO:: hashlib待了解、学习，尤其是常见的hash函数：md5等
import hashlib

test_str = 'zhushuli'
test_str1 = test_str
m = hashlib.md5()

b = test_str.encode(encoding='utf-8')
m.update(b)
str_md5 = m.hexdigest()
print(str_md5)

# test_str1 = 'zhushuli'
b1 = test_str1.encode(encoding='utf-8')
m.update(b1)
str_md51 = m.hexdigest()
print(str_md51)

test = hashlib.md5(b'zhushuli').hexdigest()
print(test)
