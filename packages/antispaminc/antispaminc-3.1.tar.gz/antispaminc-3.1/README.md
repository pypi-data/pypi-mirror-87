# AntispamInc

An Python Wrapper For AntispamInc Api.

# Support

* Channel : @AntispamInc
* Group : @AntispamIncSupport
* Bot : @AntispamIncBot
* Website : antispaminc.tk

# Usage Example

```python
from antispaminc.connect import Connect
mytoken = 'your_token_from_@antispamincbot'
sed = Connect(mytoken)
sed2 = sed.is_banned('12974624')
print(sed2.reason) 
```

# Installing
```sh
pip install antispaminc
```
or 
```shell script
pip3 install antispaminc
