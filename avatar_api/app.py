from flask import Flask, request, send_file
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from typing import Tuple

app = Flask(__name__)

font = ImageFont.truetype("font.ttf", 500)


def hex_color(hex: str) -> Tuple[int, int, int]:
    value = int(hex, 16)
    return (
        (value & 0xff0000) >> 16,
        (value & 0x00ff00) >> 8,
        (value & 0x0000ff) >> 0
    )


background_colors = (
    hex_color("9B5DE5"),
    hex_color("F15BB5"),
    hex_color("FEE440"),
    hex_color("00BBF9"),
    hex_color("00F5D4"),
)


def get_name_initials(name: str) -> str:
    return "".join(map(lambda word: word[0], name.split()[:2])).upper()


def get_background_color_for_key(key: int) -> Tuple[int, int, int]:
    return background_colors[key % len(background_colors)]


@app.get("/")
def avatar():
    name = request.args["name"]
    initials = get_name_initials(name)

    key = int(request.args.get("key", hash(name)))
    background_color = get_background_color_for_key(key)

    image = Image.new(mode="RGB", size=(1000, 1000))
    draw = ImageDraw.ImageDraw(image)
    draw.rectangle((0, 0, 1000, 1000), fill=background_color)
    draw.text((200, 200), initials, font=font)

    image_buffer = BytesIO()
    image_buffer.name = "avatar.png"

    image.save(fp=image_buffer, format="png")
    image_buffer.seek(0)

    return send_file(image_buffer, download_name="avatar.png")


if __name__ == "__main__":
    app.run("0.0.0.0", 8080, debug=True)
