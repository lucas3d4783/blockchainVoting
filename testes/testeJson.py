import json as json

# some JSON:
x =  '{ "name":"John", "age":30, "city":"New York"}'

# parse x:
y = json.loads(x)

# the result is a Python dictionary:
print(y["age"]) 

# a Python object (dict):
a = {
  "name": "John",
  "age": 30,
  "city": "New York"
}

# convert into JSON:
b = json.dumps(a)

# the result is a JSON string:
print(b) 

print(json.dumps({"name": "John", "age": 30})) # vira um objeto em javascript
print(json.dumps(["apple", "bananas"])) # vira um array em javascript
print(json.dumps(("apple", "bananas")))  # vira um array em javascript
print(json.dumps("hello")) # # vira uma String em javascript
print(json.dumps(42)) # vira um Number em javascript
print(json.dumps(31.76)) # vira um Number em javascrip
print(json.dumps(True)) # quando é convertido para jason, vira true
print(json.dumps(False)) # quando é convertido para jason, vira false
print(json.dumps(None)) # quando é convertido para jason, vira null


d = {
  "name": "John",
  "age": 30,
  "married": True,
  "divorced": False,
  "children": ("Ann","Billy"),
  "pets": None,
  "cars": [
    {"model": "BMW 230", "mpg": 27.5},
    {"model": "Ford Edge", "mpg": 24.1}
  ]
}

print(json.dumps(d))

eleicao_pk=1
eleitor_pk=2
candidato_pk=3
dados_string = json.dumps({"eleicao_pk": eleicao_pk, "eleitor_pk": eleitor_pk, "candidato_pk": candidato_pk})
dados = json.loads(dados_string)
print(type(dados))
print(dados)