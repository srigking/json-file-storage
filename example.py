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