thisdict =	{
    "cars":{
      "brand": "Ford",
      "model": "Mustang",
      "year": 1964
      }
}
thisdict[thisdict.setdefault("owner", {})] = "John Smith"
print(thisdict)
