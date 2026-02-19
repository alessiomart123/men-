#!/usr/bin/env python3
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import mm
from textwrap import wrap
from PIL import Image, ImageDraw, ImageFont


IMG_W = 60 * mm
IMG_H = 45 * mm


def ensure_images(image_dir, pizzas):
    os.makedirs(image_dir, exist_ok=True)
    for p in pizzas:
        path = os.path.join(image_dir, p['image'])
        if not os.path.exists(path):
            # Create a simple placeholder image with the pizza name
            img_w, img_h = int(IMG_W), int(IMG_H)
            img = Image.new('RGB', (img_w, img_h), color=(244, 143, 177))
            draw = ImageDraw.Draw(img)
            try:
                font = ImageFont.truetype("DejaVuSans-Bold.ttf", 20)
            except Exception:
                font = ImageFont.load_default()
            lines = wrap(p['name'], 18)
            text_h = 0
            for line in lines:
                bbox = draw.textbbox((0, 0), line, font=font)
                h = bbox[3] - bbox[1]
                text_h += h
            y = (img_h - text_h) // 2
            for line in lines:
                bbox = draw.textbbox((0, 0), line, font=font)
                w = bbox[2] - bbox[0]
                h = bbox[3] - bbox[1]
                draw.text(((img_w - w) / 2, y), line, fill=(33, 33, 33), font=font)
                y += h
            img.save(path)


def draw_menu(output_path="menu_pizzeria.pdf"):
    width, height = A4
    c = canvas.Canvas(output_path, pagesize=A4)
    margin = 16 * mm

    # Header background
    c.setFillColor(colors.HexColor("#b71c1c"))
    c.rect(0, height - 110, width, 110, fill=1, stroke=0)

    # Title and slogan
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 34)
    c.drawCentredString(width / 2, height - 62, "Pizzeria La Repubblica")
    c.setFont("Helvetica-Oblique", 12)
    c.drawCentredString(width / 2, height - 80, "Dove la tradizione incontra il forno a legna")
    c.setFont("Helvetica", 11)
    slogan = 'Vieni per la pizza, resta per il sorriso — Ogni morso, un ricordo.'
    c.drawCentredString(width / 2, height - 95, slogan)

    # Decorative stripe
    c.setFillColor(colors.HexColor("#fff3e0"))
    c.rect(margin - 8 * mm, margin, 8 * mm, height - 2 * margin - 110, fill=1, stroke=0)

    # Data
    pizzas = [
        {"name": "Margherita", "desc": "Pomodoro DOP, mozzarella fior di latte, basilico", "price": 6.50, "image": "margherita.png"},
        {"name": "Marinara", "desc": "Pomodoro, aglio, origano, olio EVO", "price": 5.00, "image": "marinara.png"},
        {"name": "Diavola", "desc": "Salame piccante, mozzarella, pepe", "price": 8.50, "image": "diavola.png"},
        {"name": "Quattro Formaggi", "desc": "Mozzarella, gorgonzola, parmigiano, provola", "price": 9.50, "image": "4formaggi.png"},
        {"name": "Capricciosa", "desc": "Prosciutto, funghi, carciofi, olive", "price": 9.00, "image": "capricciosa.png"},
        {"name": "Prosciutto e Funghi", "desc": "Prosciutto crudo, funghi porcini", "price": 9.50, "image": "prosciutto_funghi.png"},
        {"name": "Bufalina", "desc": "Mozzarella di bufala, pomodoro fresco", "price": 10.00, "image": "bufalina.png"},
        {"name": "Ortolana", "desc": "Verdure grigliate, mozzarella, basilico", "price": 8.50, "image": "ortolana.png"},
        {"name": "Tonno e Cipolla", "desc": "Tonno di qualità, cipolla rossa", "price": 8.00, "image": "tonno_cipolla.png"},
        {"name": "Frutti di Mare", "desc": "Gamberi, calamari, cozze, pomodoro", "price": 11.00, "image": "frutti_mare.png"},
        {"name": "Napoli", "desc": "Acciughe, capperi, pomodoro", "price": 7.50, "image": "napoli.png"},
        {"name": "Siciliana", "desc": "Melanzane, ricotta salata, pomodoro", "price": 9.00, "image": "siciliana.png"},
    ]

    beverages = [
        {"name": "Acqua naturale 0.5L", "price": 2.00},
        {"name": "Acqua frizzante 0.5L", "price": 2.00},
        {"name": "Coca-Cola 33cl", "price": 3.00},
        {"name": "Aranciata 33cl", "price": 3.00},
        {"name": "Birra bionda 33cl", "price": 4.00},
        {"name": "Birra artigianale 50cl", "price": 5.50},
        {"name": "Vino rosso della casa (bicchiere)", "price": 4.00},
        {"name": "Vino bianco della casa (bicchiere)", "price": 4.00},
        {"name": "Chianti DOC (bottiglia)", "price": 18.00},
        {"name": "Prosecco DOC (bottiglia)", "price": 20.00},
        {"name": "Birra alla spina 40cl", "price": 4.50},
    ]

    # Ensure images exist
    image_dir = os.path.join(os.path.dirname(__file__), 'images')
    ensure_images(image_dir, pizzas)

    # Layout pizzas with images in two columns
    col_x = [margin, width / 2 + 6 * mm]
    y_start = height - 130
    box_h = IMG_H + 18 * mm
    per_col = 6

    for col in range(2):
        x = col_x[col]
        y = y_start
        c.setFont("Helvetica-Bold", 18)
        if col == 0:
            c.setFillColor(colors.HexColor("#212121"))
            c.drawString(x, y, "Pizze")
        y -= 14
        c.setFont("Helvetica", 10)
        for i in range(per_col):
            idx = col * per_col + i
            if idx >= len(pizzas):
                break
            p = pizzas[idx]
            # Box
            box_y = y - IMG_H
            box_w = (width / 2) - margin - 8 * mm
            c.setStrokeColor(colors.HexColor("#bdbdbd"))
            c.rect(x - 2 * mm, box_y - 6 * mm, box_w, box_h - 6 * mm, stroke=1, fill=0)

            # Image
            img_path = os.path.join(image_dir, p['image'])
            img_x = x + 6 * mm
            img_y = box_y + 6 * mm
            c.drawImage(img_path, img_x, img_y, width=IMG_W, height=IMG_H, preserveAspectRatio=True, mask='auto')

            # Text
            text_x = img_x + IMG_W + 6 * mm
            text_y = box_y + IMG_H
            c.setFont("Helvetica-Bold", 12)
            c.setFillColor(colors.HexColor("#212121"))
            c.drawString(text_x, text_y, f"{p['name']}  —  €{p['price']:.2f}")
            text_y -= 12
            c.setFont("Helvetica", 9)
            for line in wrap(p['desc'], 40):
                c.drawString(text_x, text_y, line)
                text_y -= 10

            y = box_y - 12 * mm

    # Beverages section on a new page for clarity
    c.showPage()
    c.setFont("Helvetica-Bold", 20)
    c.setFillColor(colors.HexColor("#b71c1c"))
    c.drawCentredString(width / 2, height - 60, "Bevande e Vini")
    c.setFont("Helvetica", 11)
    x_left = margin
    y = height - 100
    for b in beverages:
        if y < margin + 40:
            c.showPage()
            y = height - margin
        c.setFillColor(colors.HexColor("#212121"))
        c.drawString(x_left, y, f"{b['name']}  —  €{b['price']:.2f}")
        y -= 14

    # Footer with larger contact details
    footer_y = margin + 8 * mm
    c.setFillColor(colors.HexColor("#424242"))
    c.setFont("Helvetica-Bold", 12)
    contact = "Via della Repubblica 15"
    c.drawCentredString(width / 2, footer_y + 18, contact)
    c.setFont("Helvetica", 11)
    c.drawCentredString(width / 2, footer_y + 4, "Tel. +39 012 345 6789 — iltuo.ristorante@gmail.com")

    # Small decorative circle on footer
    c.setFillColor(colors.HexColor("#b71c1c"))
    c.circle(width - margin - 14 * mm, footer_y + 12, 6 * mm, fill=1)

    c.save()


if __name__ == '__main__':
    draw_menu()
