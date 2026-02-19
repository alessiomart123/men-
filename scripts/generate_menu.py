#!/usr/bin/env python3
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import mm
from textwrap import wrap


def draw_menu(output_path="menu_pizzeria.pdf"):
    width, height = A4
    c = canvas.Canvas(output_path, pagesize=A4)
    margin = 18 * mm

    # Header background
    c.setFillColor(colors.HexColor("#d84315"))
    c.rect(0, height - 90, width, 90, fill=1, stroke=0)

    # Title
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 30)
    c.drawCentredString(width / 2, height - 50, "Pizzeria La Repubblica")
    c.setFont("Helvetica", 11)
    c.drawCentredString(width / 2, height - 68, "Autentica pizza italiana - Ricette tradizionali")

    # Decorative left stripe
    c.setFillColor(colors.HexColor("#fbe9e7"))
    c.rect(margin - 6 * mm, margin, 6 * mm, height - 2 * margin - 90, fill=1, stroke=0)

    # Sample data
    pizzas = [
        {"name": "Margherita", "desc": "Pomodoro, mozzarella fior di latte, basilico fresco", "price": 6.50},
        {"name": "Marinara", "desc": "Pomodoro, aglio, origano, olio extra vergine d'oliva", "price": 5.50},
        {"name": "Diavola", "desc": "Pomodoro, mozzarella, salame piccante", "price": 8.00},
        {"name": "Quattro Formaggi", "desc": "Mozzarella, gorgonzola, parmigiano, provola", "price": 9.00},
        {"name": "Capricciosa", "desc": "Pomodoro, mozzarella, prosciutto cotto, funghi, carciofi, olive", "price": 9.50},
        {"name": "Prosciutto e Funghi", "desc": "Pomodoro, mozzarella, prosciutto crudo, funghi", "price": 9.00},
    ]

    beverages = [
        {"name": "Acqua naturale 0.5L", "price": 2.00},
        {"name": "Acqua frizzante 0.5L", "price": 2.00},
        {"name": "Coca-Cola 33cl", "price": 3.00},
        {"name": "Birra alla spina 40cl", "price": 4.50},
        {"name": "Vino della casa (bicchiere)", "price": 3.50},
        {"name": "Aranciata 33cl", "price": 3.00},
    ]

    # Left column - Pizze
    x_left = margin
    y = height - 120
    c.setFillColor(colors.HexColor("#212121"))
    c.setFont("Helvetica-Bold", 18)
    c.drawString(x_left, y, "Pizze")
    y -= 18
    c.setFont("Helvetica", 11)

    for p in pizzas:
        if y < margin + 80:
            c.showPage()
            y = height - margin
        c.setFont("Helvetica-Bold", 12)
        name_price = f"{p['name']}  —  €{p['price']:.2f}"
        c.drawString(x_left, y, name_price)
        y -= 14
        c.setFont("Helvetica", 10)
        for line in wrap(p['desc'], 60):
            c.drawString(x_left + 6 * mm, y, line)
            y -= 12
        y -= 8

    # Right column - Bevande
    x_right = width / 2 + 6 * mm
    y = height - 120
    c.setFont("Helvetica-Bold", 18)
    c.drawString(x_right, y, "Bevande")
    y -= 18
    c.setFont("Helvetica", 11)

    for b in beverages:
        if y < margin + 60:
            c.showPage()
            y = height - margin
        c.setFont("Helvetica", 11)
        c.drawString(x_right, y, f"{b['name']}  —  €{b['price']:.2f}")
        y -= 16

    # Footer - contact
    footer_y = margin
    c.setFillColor(colors.HexColor("#424242"))
    c.setFont("Helvetica", 9)
    contact = "Via della Repubblica 15 — Tel. +39 012 345 6789 — iltuo.ristorante@gmail.com"
    c.drawCentredString(width / 2, footer_y + 8, contact)

    # Small flourish
    c.setFillColor(colors.HexColor("#d84315"))
    c.circle(width - margin - 10 * mm, footer_y + 14, 6 * mm, fill=1)

    c.save()


if __name__ == '__main__':
    draw_menu()
