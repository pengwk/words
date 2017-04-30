
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

## invalid literal for int() with base 10: '1H32'

没有对时长超过一个小时的支持，需要用正则表达式来提取数据