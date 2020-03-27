import requests 

url = "http://klevang.dk:19409/submitcolor"

r = input("Red between 0 - 255\n") 
g = input("Green between 0 - 255\n") 
b = input("Blue between 0 - 255\n") 

color = {
    "board_id": 2,
    "red":int(r),
    "green": int(g),
    "blue": int(b)
}

print("Posting... \n ", color)
requests.post(url, json=color)


