# RHash

## License

All code except `setup.py` is licensed under the 'BSD Zero Clause License'. `setup.py` is licensed under the 'ISC License'.

## Example

```python
import rhash
ctx = rhash.RHash(rhash.CRC32 | rhash.MD5)
ctx.update('Hello, ').update('world!').finish()
assert 'EBE6C6E6' == ctx.HEX(rhash.CRC32)
assert '6cd3556deb0da54bca060b4c39479839' == ctx.hex(rhash.MD5)
```
