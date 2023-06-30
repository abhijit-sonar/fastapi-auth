from flask import Flask, request, send_file
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

app = Flask(__name__)

font = ImageFont.truetype("font.ttf", 500)

def get_name_initials(name: str) -> str:
    return "".join(map(lambda word: word[0], name.split()[:2])).upper()

@app.get("/")
def avatar():
    name = request.args["name"]
    initials = get_name_initials(name)

    image = Image.new(mode="RGB", size=(1000, 1000))
    draw = ImageDraw.ImageDraw(image)
    draw.text((200, 200), initials, font=font)

    image_buffer = BytesIO()
    image_buffer.name = "avatar.png"

    image.save(fp=image_buffer, format="png")
    image_buffer.seek(0)

    return send_file(image_buffer, download_name="avatar.png")


if __name__ == "__main__":
    app.run("0.0.0.0", 8080, debug=True)
