from PIL import Image

img = Image.open("shen.png")
left = 18
top = 18
right = 18 + 84
bottom = 18 + 84
img_res = img.crop((left, top, right, bottom))

img_res.save("shen_square.png")
