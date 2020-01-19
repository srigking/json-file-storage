# Freshworks - File Storage

## Requirements

- Python 3.6
- Windows / Linux (Tested on Windows 10)

## Demo

### Sample File `example.py`

``` 

import json_file_handler

jfh = json_file_handler.JsonFileHandler()

json_string = """
{
    "name": "Bob",
    "age": 30
}
"""

print(jfh.create('userbob', json_string, 1))
print(jfh.read('userbob'))
print(jfh.delete('userbob'))

```

### Multithreaded Sample File `example_threaded.py`

```
...

with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(jfh.create, writelist, jsonlist)
    executor.map(jfh.read, writelist)
    executor.map(jfh.delete, writelist)

...
```

### Unit test `test_json_file_handler.py`

```
python -m unittest test_json_file_handler.py
```
