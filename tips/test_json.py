import json

# demo1
jsonData = '{"a":1,"b":2,"c":3,"d":4,"e":5}'
text = json.loads(jsonData)
print(text)

# demo2
jsonData = "[[1,2],[3,4]]"
text = json.loads(jsonData)
print(text)

# demo3
array = [['a', 'b'], ['a', 'b']]
text = json.dumps(array)
print(text)

# demo4
jsonData = '[["a", "b"], ["a", "b"]]'
text = json.loads(jsonData)
print(text)
