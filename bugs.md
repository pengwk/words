
## requests.

exceptions.SSLError: EOF occurred in violation of protocol (_ssl.c:661)

https://docs.python.org/2/library/ssl.html#ssl.SSLEOFError
exceptions.ConnectionError: ('Connection aborted.', BadStatusLine("''",))

## TypeError: 

```
list indices must be integers, not str
Exception in thread Thread-10 (most likely raised during interpreter shutdown):
```

## Unicode Error

#### 'ascii' codec can't decode byte 0xe2 in position 0: ordinal not in range(128)

标点符号前没有加u

####  (_mysql_exceptions.OperationalError) (1366, "Incorrect string value: '\\xF0\\x9F\\x8F\\x88  ...' for column 'title' at row 1")

'Game Picks in 60 Seconds (Week 7) \xe2\x8f\xb1\xf0\x9f\x8f\x88  | NFL NOW

```python
# -*- coding: utf-8 -*-
print s.decode("utf-8")
output = u"Game Picks in 60 Seconds (Week 7) ⏱ 🏈  | NFL"

s = u"\U0001F336"
print s
🌶


```
Unicode: U+1F3C8
ALTER TABLE Tablename CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_bin

collate是字符的比较方法，排序会用到
```python
# 更新数据库URL的charset=utf8mb4
e = create_engine("mysql+pymysql://scott:tiger@localhost/test?charset=utf8mb4”)
```

## 数据库

OperationalError: (2019, "Can't initialize character set utf8mb4 (path: C:\\mysql\\\\share\\charsets\\)")
MySQLdb最高只支持MYSQL5.5，我用的是5.7，使用utf8mb4编码时就不支持，使用pymysql
MySQL-3.23 through 5.5 and Python-2.4 through 2.7 are currently supported. Python-3.0 will be supported in a future release. PyPy is supported.

#### filter

使用`==`和`!=`比较，不能用is 和is not

use `==` and `!=` to compare, don't use `is` and `is not` when compare to `None`

## pool_size=20, max_overflow=100
QueuePool limit of size 5 overflow 10 reached, connection timed out, timeout 30

## hasCaption 错误
 
 `video.has_caption = content_details.get("caption")`
 `caption`key 对应的是字符串的 `"true"` `"false"` ，设置的时候就错了，自动类型转换把所有的都判定为了1
 
 修复``

## invalid literal for int() with base 10: '1H32'



没有对时长超过一个小时的支持，需要用正则表达式来提取数据

## {}.update({})

这个操作的返回值是None，不能直接赋值