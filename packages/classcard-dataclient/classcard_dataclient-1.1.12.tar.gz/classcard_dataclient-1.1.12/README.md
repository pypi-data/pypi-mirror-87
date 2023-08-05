## DataClient

### Introduction
this is a tool which save data to class card server

### Usage

##### 1. install
```bash
pip install classcard-dataclient
```

##### 2. init client
```python
# init instance
client = DataClient()
# set the config
client.set_config_module("config")
```

##### 3. call method
```python
data = Model(**{
    "xxx": "xxx"
})
code, msg = client.create_section(data)
```

**Notice:**
* when data is model instance , code is integer, msg is string, 
* when data is instance list, the code is list, msg is also list.




