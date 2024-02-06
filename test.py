cards = [
    {"cat": "gato"},
    {"dog": "perro"},
    {"hello": "hola"},
    {"table": "mesa"},
    {"juice": "jugo"},
    {"water": "agua"},
    {"lamp": "lampara"},
    {"butter": "mantequilla"}]

eve = []

for dict in cards:
    key = list(dict.keys())[0]
    val = list(dict.values())[0]
    eve.append(key)
    eve.append(val)

print(eve)