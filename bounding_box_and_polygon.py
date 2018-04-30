#!/usr/bin/env python3
"""Writes bounding_box_and_polygon.png that illustrates
"""
from PIL import Image, ImageDraw

from pyzbar.pyzbar import decode


image = Image.open('pyzbar/tests/qrcode_rotated.png').convert('RGB')
draw = ImageDraw.Draw(image)
for barcode in decode(image):
    rect = barcode.rect
    draw.rectangle(
        (
            (rect.left, rect.top),
            (rect.left + rect.width, rect.top + rect.height)
        ),
        outline='#0080ff'
    )

    draw.polygon(barcode.polygon, outline='#e945ff')


image.save('bounding_box_and_polygon.png')
