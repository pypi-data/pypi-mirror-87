# mywinpwn

自己用的windows pwntools

env: python3/python2

## install

```bash
pip install q4nwin
```

或者你可以先注释掉build.bat中的后两行, 直接运行build.bat即可构建包在`dist`下

## PWN

simple lib of [winpwn](https://github.com/Byzero512/winpwn)

2020.11.30
    
    增加了一些alias, 比如`sd sla ru`, 删去一些对我而言无用的东西

    `process`添加了`dbg`函数直接去调用`windbgx.attach`, 方便调试

    新增了一个简化版本的 `flat/fit`, 对`(str, bytes, list, tuple)`按照 `context.arch` 进行展开

    新增对`context.endian`大小端的支持


## APIs

### function 

you can find them in `q4nwin/toplevel.py`


## refer

https://github.com/Byzero512/winpwn