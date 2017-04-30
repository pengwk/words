
## requests.

exceptions.SSLError: EOF occurred in violation of protocol (_ssl.c:661)

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

```
Unicode: U+1F3C8
ALTER TABLE Tablename CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_bin

collate是字符的比较方法，排序会用到
```python
# 更新数据库URL的charset=utf8mb4
e = create_engine("mysql+pymysql://scott:tiger@localhost/test?charset=utf8mb4”)
```

## invalid literal for int() with base 10: '1H32'



没有对时长超过一个小时的支持，需要用正则表达式来提取数据

