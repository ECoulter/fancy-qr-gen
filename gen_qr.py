#!/usr/bin/env python3

import argparse
import xml.etree.ElementTree as ET

import qrcode
from qrcode.image.svg import SvgPathImage
from qrcode.image.styles.moduledrawers.svg import SvgPathCircleDrawer
from qrcode.image.styles.colormasks import SolidFillColorMask

SVG_NS = "http://www.w3.org/2000/svg"

ET.register_namespace("", SVG_NS)

#class ColoredSvgPathImage(SvgPathImage):
#        QR_PATH_STYLE = {
#            "fill": "#FE8658",
#            "fill-opacity": "1.0",
#            "fill-rule": "nonzero",
#            "stroke": "none",
#        }


def parse_viewbox(root):
    """
    Returns:
        min_x, min_y, width, height
    """
    viewbox = root.get("viewBox")
    if viewbox:
        return tuple(map(float, viewbox.split()))

    width = float(root.get("width"))
    height = float(root.get("height"))
    return (0.0, 0.0, width, height)


def create_qr_svg(data):
    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        border=4,
        box_size=20,
    )

    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(
        image_factory=SvgPathImage,
        module_drawer=SvgPathCircleDrawer(),
    )

    return img.to_string(encoding="unicode")

def add_outer_border(
    qr_root,
    qr_w,
    qr_h,
    color,
    backg_color,
    border_width_frac=0.02,
    radius_frac=0.08,
):
    border_width = qr_w * border_width_frac
    radius = qr_w * radius_frac

    inset = border_width / 4

    border = ET.Element(
        f"{{{SVG_NS}}}rect",
        {
            "x": str(inset),
            "y": str(inset),
            "width": str(qr_w - border_width),
            "height": str(qr_h - border_width),
            "rx": str(radius),
            "ry": str(radius),
            "fill": backg_color,
            "stroke": color,
            "stroke-width": str(border_width),
        },
    )

    #
    # Insert as first child so it renders behind
    # the logo badge.
    #
    qr_root.insert(0, border)


def embed_logo(qr_svg_text, logo_path, border_color, backg_color, logo_backg_color, logo_fraction=0.20):
    qr_root = ET.fromstring(qr_svg_text)
    logo_root = ET.parse(logo_path).getroot()

    qr_min_x, qr_min_y, qr_w, qr_h = parse_viewbox(qr_root)

    add_outer_border(qr_root,qr_w,qr_h,border_color,backg_color)

    logo_min_x, logo_min_y, logo_w, logo_h = parse_viewbox(logo_root)

    #
    # Logo should occupy this fraction of QR width.
    #
    target_width = qr_w * logo_fraction

    #
    # Preserve logo aspect ratio.
    #
    scale = target_width / logo_w

    scaled_logo_w = logo_w * scale
    scaled_logo_h = logo_h * scale

    #
    # Center logo.
    #
    x = (qr_w - scaled_logo_w) / 2.0
    y = (qr_h - scaled_logo_h) / 2.0

    #
    # Backg_color backing plate
    #
    padding = target_width * 0.20
    radius = target_width * 0.30
    border_width = target_width * 0.08
    
    ET.SubElement(
        qr_root,
        f"{{{SVG_NS}}}rect",
        {
            "x": str(x - padding),
            "y": str(y - padding),
            "width": str(scaled_logo_w + 2 * padding),
            "height": str(scaled_logo_h + 2 * padding),
            "rx": str(radius),
            "ry": str(radius),
            "fill": logo_backg_color,
            "stroke": border_color,
            "stroke-width": str(border_width),
        },
    )
    #
    # Create placement group.
    #
    logo_group = ET.SubElement(
        qr_root,
        f"{{{SVG_NS}}}g",
        {
            "transform": (
                f"translate({x},{y}) "
                f"scale({scale}) "
                f"translate({-logo_min_x},{-logo_min_y})"
            )
        },
    )

    #
    # Copy contents of logo SVG into group.
    #
    for child in list(logo_root):
        logo_group.append(child)

    return ET.tostring(
        qr_root,
        encoding="unicode",
    )

def recolor_qr(svg_root, color):
    """
    Recolor QR code geometry while leaving
    logo and border elements untouched.
    """

    qr_root = ET.fromstring(svg_root)

    for elem in qr_root.iter():
        if elem.tag.endswith("path"):
            elem.set("fill", color)

    return ET.tostring(
        qr_root,
        encoding="unicode",
    )

def main():
    parser = argparse.ArgumentParser(
        description="Generate SVG QR code with embedded SVG logo."
    )

    parser.add_argument(
        "url",
        help="URL or text to encode"
    )

    parser.add_argument(
        "logo_svg",
        help="Path to SVG logo"
    )

    parser.add_argument(
        "-o",
        "--output",
        default="qr.svg",
        help="Output SVG filename"
    )

    parser.add_argument(
        "--logo-size",
        type=float,
        default=0.20,
        help="Fraction of QR width occupied by logo (default: 0.20)"
    )

    parser.add_argument(
        "--qr-color",
        default="#000000",
        help="SVG QR code fill color"
    )

    parser.add_argument(
        "--logo-backg-color",
        default="#FFFFFF",
        help="SVG QR code Logo background color"
    )

    parser.add_argument(
        "--backg-color",
        default="#FFFFFF",
        help="SVG QR code background color"
    )

    parser.add_argument(
        "--border-color",
        default="#000000",
        help="SVG QR code border color"
    )

    args = parser.parse_args()

    qr_svg = create_qr_svg(args.url)

    qr_svg = recolor_qr(qr_svg, args.qr_color)

    final_svg = embed_logo(
        qr_svg,
        args.logo_svg,
        args.border_color,
        args.backg_color,
        args.logo_backg_color,
        logo_fraction=args.logo_size,
    )
 
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(final_svg)

    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()

