import json_file_handler
import random
import string
import time
import concurrent.futures


def randomString(stringLength):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


jfh = json_file_handler.JsonFileHandler(debug=False)

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

# Generate Dummy data
writelist = []
jsonlist = []

for _ in range(25):
    key = randomString(25)
    writelist.append(key)
    jsonlist.append(json_string)

start = time.perf_counter()
# Testing
with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(jfh.create, writelist, jsonlist)
    executor.map(jfh.read, writelist)
    executor.map(jfh.delete, writelist)
    
end = time.perf_counter()

print(f'Finished in {round(end-start, 2)} sec (s)')