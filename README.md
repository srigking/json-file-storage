# For Freshworks - File Storage

## Requirements

- Python 3.6
- Windows / Linux (Tested on Windows 10)

## Sample File

### File `main.py`

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

