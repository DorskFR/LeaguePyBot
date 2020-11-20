# Convert the annotations.json file that Super Annotate produces to the format .txt that is wanted by the cascade classifier


import json

path = "positive/"

with open('annotations.json', 'r') as f:
    data = f.read()

    obj = json.loads(data)

    for img, attrs in obj.items():
        annotations = []
        for attr in attrs:
            try:
                x1 = attr["points"]["x1"]
                x2 = attr["points"]["x2"]
                y1 = attr["points"]["y1"]
                y2 = attr["points"]["y2"]
                annotation = f" {int(x1)} {int(y1)} {int(x2-x1)} {int(y2-y1)}"
                annotations.append(annotation)
            except:
                 pass
        if len(annotations) > 0:
            line = f"{path}{img} {len(annotations)}"
            for annotation in annotations:
                line += annotation
            print(line, file=open('pos.txt', 'a'))