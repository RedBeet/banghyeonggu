from PIL import Image
import requests
import base64
from io import BytesIO

img = Image.open("images/1.jpg")
key = "g1Ti7tDaNAHst1yStjby99hgDOnlUR7HdMJ7Wdcc0RZWwta5kN"


width = img.width/10
height = img.height/10
imgs = []
for i in range(10):
    temp = []
    for j in range(10):
        block = img.crop((width * j, height * i, width * (j + 1), height * (i + 1)))
        temp.append(block)
    imgs.append(temp)

def identify_plant(file_name):
    buffered = BytesIO()
    file_name.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue())
    params = {
        "images": [base64.b64encode(img_str)],
    }
    headers = {
    "Content-Type": "application/json",
    "Api-Key": key,
    }
    response = requests.post("https://api.plant.id/v2/identify",
                             json=params,
                             headers=headers)

    return response.json()
res = {}
for i in range(10):
    for j in range(10):
        data = identify_plant(imgs[i][j])
        if data["is_plant"]:
            flowers = data["suggestions"]
            for item in flowers:
                if item["probability"] >= 0.7:
                    if item["plant_name"] not in res.keys():
                        res[item["plant_name"]] = 1
                    else:
                        res[item["plant_name"]] += 1

total = sum(res.values())
with open("result.txt", "a") as f:
    for i in res:
        if res[i] == max(res.values()):
            f.write(f"density of {i} : {res[i] / total} <<<<< dominant")
        else:
            f.write(f"density of {i} : {res[i] / total}")