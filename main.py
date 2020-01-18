import json_file_handler
import json

jfh = json_file_handler.JsonFileHandler()

json_string = """
{
    "researcher": {
        "name": "Ford Prefect",
        "species": "Betelgeusian",
        "relatives": [
            {
                "name": "Zaphod Beeblebrox",
                "species": "Betelgeusian"
            }
        ]
    }
}
"""


jfh.create('test', json_string, 1)
print(jfh.read('test'))
jfh.delete('test')