# Print Object in Python3.x

- Print your variable/object in beautiful way
- It's easier way to print variable name & it's value
- pobj print any type of value. Like int, str, bool, list, dict, django request, dataframe, ... few more

---
## Install with pip
```
pip install pobj
```

---
## Upgrade with pip
```
pip install pobj --upgrade
```

---
## How to implement
1) install package by `pip install pobj`
2) import pobj by `from pobj import pobj` in class.py
3) use pobj in your code as bellow standards...
```
pobj(your_variable)
```

---
## Demo / Example

### Source Code/File:
```
class Fruits:

    def get_apple_detail(self, price: float = 0.0):
        result = {
            'fruit': 'Apple',
            'price': price or 120,
            'quantity': 2,
            'available': True
        }
        pobj(result)
        return result

```

### OutPut:
```
---result---type:dict---size:0.24-KB---
{
  "available": true,
  "fruit": "Apple",
  "price": 120,
  "quantity": 2
}

```


---
# ChangeLog Version

---
## v1.2.2 | 2020-11-30
### Show size in KB | Added | Done
- display size in KB instead of bytes
- basically we convert size of object/variable bytes into KB unit 
- Note: 1000 bytes = 1 KB

---
## v1.2.1 | 2020-11-30
### Also show type & size of object | Added | Done
- additionally we also print type & size of object/variable
- type it's print the which type of variable it's. Like int/str/list/...
- size it's shows the how much memory is occupy by this variable 

---
## v1.1.1 | 2020-11-29
### Print Object | Added | Done
- print your object/variable
- by using simply `pobj` keyword
- like: pobj(your_obj)

---