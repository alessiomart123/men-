#!/usr/bin/env python3
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import mm
from textwrap import wrap
from PIL import Image, ImageDraw, ImageFont

IMG_W = 70 * mm
IMG_H = 52 * mm

def create_pizza_image(path, pizza_name):
    """Create a nice looking pizza placeholder image"""
    px_w, px_h = 560, 416  # 4x scaling of mm
    
    # Create image with gradient-like background
    img = Image.new('RGB', (px_w, px_h), color=(245, 200, 150))
    draw = ImageDraw.Draw(img)
    
    # Add decorative border and background
    draw.rectangle([(0, 0), (px_w-1, px_h-1)], outline=(180, 100, 50), width=8)
    
    # Decorative circle in center
    cx, cy = px_w // 2, px_h // 2
    radius = 120
    draw.ellipse([(cx-radius, cy-radius), (cx+radius, cy+radius)], 
                 fill=(255, 230, 200), outline=(200, 120, 60), width=6)
    
    # Draw pizza name
    try:
        font_big = ImageFont.truetype("DejaVuSans-Bold.ttf", 64)
        font_small = ImageFont.truetype("DejaVuSans.ttf", 36)
    except:
        font_big = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Pizza name centered
    lines = wrap(pizza_name, 12)
    total_h = len(lines) * 70
    start_y = cy - total_h // 2
    
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font_big)
        w = bbox[2] - bbox[0]
        draw.text(((px_w - w) // 2, start_y), line, fill=(100, 50, 0), font=font_big)
        start_y += 70
    
    # Add "Pizza House" subtitle
    bbox = draw.textbbox((0, 0), "Pizza House", font=font_small)
    w = bbox[2] - bbox[0]
    draw.text(((px_w - w) // 2, cy + 80), "Pizza House", fill=(150, 80, 30), font=font_small)
    
    img.save(path)

def ensure_images(image_dir, pizzas):
    os.makedirs(image_dir, exist_ok=True)
    for p in pizzas:
        path = os.path.join(image_dir, p['image'])
        if not os.path.exists(path):
            create_pizza_image(path, p['name'])

def draw_menu():
    width, height = A4
    c = canvas.Canvas("menu_pizzeria.pdf", pagesize=A4)
    margin = 14 * mm
    
    # Page 1: Pizze
    # ===============
    
    # Background
    c.setFillColor(colors.HexColor("#fef5f0"))
    c.rect(0, 0, width, height, fill=1, stroke=0)
    
    # Header
    c.setFillColor(colors.HexColor("#c62828"))
    c.rect(0, height - 95, width, 95, fill=1, stroke=0)
    
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 36)
    c.drawCentredString(width/2, height - 50, "PIZZERIA LA REPUBBLICA")
    
    c.setFont("Helvetica-Oblique", 12)
    c.drawCentredString(width/2, height - 72, "Autentica pizza al forno a legna")
    
    # Decoration line
    c.setStrokeColor(colors.HexColor("#ff9800"))
    c.setLineWidth(2)
    c.line(margin, height - 85, width - margin, height - 85)
    
    # Data
    pizzas = [
        {"name": "Margherita", "desc": "Pomodoro DOP, Mozzarella fior di latte, Basilico fresco", "price": 6.50, "image": "margherita.png"},
        {"name": "Marinara", "desc": "Pomodoro, Aglio, Origano, Olio EVO", "price": 5.00, "image": "marinara.png"},
        {"name": "Diavola", "desc": "Pomodoro, Mozzarella, Salame piccante, Pepe", "price": 8.50, "image": "diavola.png"},
        {"name": "Quattro Formaggi", "desc": "Mozzarella, Gorgonzola, Parmigiano, Provola", "price": 9.50, "image": "4formaggi.png"},
        {"name": "Capricciosa", "desc": "Pomodoro, Mozzarella, Prosciutto, Funghi, Carciofi, Olive", "price": 9.00, "image": "capricciosa.png"},
        {"name": "Prosciutto e Funghi", "desc": "Pomodoro, Mozzarella, Prosciutto crudo, Funghi porcini", "price": 9.50, "image": "prosciutto_funghi.png"},
        {"name": "Bufalina", "desc": "Mozzarella di bufala, Pomodoro fresco, Basilico", "price": 10.00, "image": "bufalina.png"},
        {"name": "Ortolana", "desc": "Verdure grigliate, Mozzarella, Basilico, Pomodoro", "price": 8.50, "image": "ortolana.png"},
        {"name": "Tonno e Cipolla", "desc": "Pomodoro, Mozzarella, Tonno, Cipolla rossa", "price": 8.00, "image": "tonno_cipolla.png"},
        {"name": "Frutti di Mare", "desc": "Pomodoro, Mozzarella, Gamberi, Calamari, Cozze", "price": 11.00, "image": "frutti_mare.png"},
        {"name": "Napoli", "desc": "Pomodoro, Mozzarella, Acciughe, Capperi", "price": 7.50, "image": "napoli.png"},
        {"name": "Siciliana", "desc": "Pomodoro, Ricotta salata, Melanzane, Basilico", "price": 9.00, "image": "siciliana.png"},
    ]
    
    image_dir = os.path.join(os.path.dirname(__file__), 'images')
    ensure_images(image_dir, pizzas)
    
    # Draw pizzas: 2 pizzas per row
    y = height - 115
    pizzas_per_row = 2
    
    for idx, p in enumerate(pizzas):
        col = idx % pizzas_per_row
        
        if col == 0 and idx > 0:
            y -= IMG_H + 50
            if y < margin + 40:
                c.showPage()
                c.setFillColor(colors.HexColor("#fef5f0"))
                c.rect(0, 0, width, height, fill=1, stroke=0)
                y = height - margin
        
        x = margin + col * (width/2 - margin - 4*mm)
        
        # Pizza box with rounded corners
        box_h = IMG_H + 60
        c.setFillColor(colors.white)
        c.setStrokeColor(colors.HexColor("#ddd"))
        c.roundRect(x, y - box_h, width/2 - margin - 6*mm, box_h, 6, stroke=1, fill=1)
        
        # Image
        img_path = os.path.join(image_dir, p['image'])
        img_x = x + 8*mm
        img_y = y - IMG_H - 6*mm
        c.drawImage(img_path, img_x, img_y, width=IMG_W, height=IMG_H, 
                   preserveAspectRatio=True, mask='auto')
        
        # Name - big and bold
        name_x = img_x + IMG_W + 6*mm
        name_y = y - 14*mm
        c.setFont("Helvetica-Bold", 16)
        c.setFillColor(colors.HexColor("#c62828"))
        c.drawString(name_x, name_y, p['name'])
        
        # Price - very large and prominent
        price_y = name_y - 18
        c.setFont("Helvetica-Bold", 20)
        c.setFillColor(colors.HexColor("#ff9800"))
        c.drawString(name_x, price_y, f"€ {p['price']:.2f}")
        
        # Ingredients - clear label and content
        ing_y = price_y - 14
        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(colors.HexColor("#555"))
        c.drawString(name_x, ing_y, "Ingredienti:")
        
        ing_y -= 11
        c.setFont("Helvetica", 9)
        c.setFillColor(colors.HexColor("#333"))
        for line in wrap(p['desc'], 50):
            c.drawString(name_x, ing_y, line)
            ing_y -= 10
    
    # Page 2: Bevande e Vini
    # ====================
    c.showPage()
    
    # Background
    c.setFillColor(colors.HexColor("#fef5f0"))
    c.rect(0, 0, width, height, fill=1, stroke=0)
    
    # Header
    c.setFillColor(colors.HexColor("#c62828"))
    c.rect(0, height - 80, width, 80, fill=1, stroke=0)
    
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 32)
    c.drawCentredString(width/2, height - 40, "BEVANDE & VINI")
    
    # Decoration
    c.setStrokeColor(colors.HexColor("#ff9800"))
    c.setLineWidth(2)
    c.line(margin, height - 70, width - margin, height - 70)
    
    beverages = [
        {"name": "Acqua naturale 0.5L", "price": 2.00},
        {"name": "Acqua frizzante 0.5L", "price": 2.00},
        {"name": "Coca-Cola 33cl", "price": 3.00},
        {"name": "Aranciata 33cl", "price": 3.00},
        {"name": "Birra bionda 33cl", "price": 4.00},
        {"name": "Birra artigianale 50cl", "price": 5.50},
        {"name": "Vino rosso della casa (bicchiere)", "price": 4.00},
        {"name": "Vino bianco della casa (bicchiere)", "price": 4.00},
        {"name": "Chianti Classico DOC (bottiglia)", "price": 18.00},
        {"name": "Prosecco DOC (bottiglia)", "price": 20.00},
        {"name": "Birra alla spina 40cl", "price": 4.50},
    ]
    
    # Three sections: Soft drinks, Birre, Vini
    col_width = (width - 2*margin) / 3
    
    # Left column: Soft drinks
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(colors.HexColor("#c62828"))
    c.drawString(margin, height - 100, "BIBITE")
    
    y = height - 125
    c.setFont("Helvetica", 11)
    c.setFillColor(colors.HexColor("#333"))
    for b in beverages[:4]:
        c.drawString(margin, y, b['name'])
        c.setFont("Helvetica-Bold", 11)
        c.setFillColor(colors.HexColor("#ff9800"))
        c.drawRightString(margin + col_width - 8*mm, y, f"€ {b['price']:.2f}")
        c.setFont("Helvetica", 11)
        c.setFillColor(colors.HexColor("#333"))
        y -= 16
    
    # Middle column: Birre
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(colors.HexColor("#c62828"))
    col2_x = margin + col_width
    c.drawString(col2_x, height - 100, "BIRRE")
    
    y = height - 125
    c.setFont("Helvetica", 11)
    c.setFillColor(colors.HexColor("#333"))
    for b in beverages[4:8]:
        c.drawString(col2_x, y, b['name'])
        c.setFont("Helvetica-Bold", 11)
        c.setFillColor(colors.HexColor("#ff9800"))
        c.drawRightString(col2_x + col_width - 8*mm, y, f"€ {b['price']:.2f}")
        c.setFont("Helvetica", 11)
        c.setFillColor(colors.HexColor("#333"))
        y -= 16
    
    # Right column: Vini
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(colors.HexColor("#c62828"))
    col3_x = margin + 2 * col_width
    c.drawString(col3_x, height - 100, "VINI")
    
    y = height - 125
    c.setFont("Helvetica", 11)
    c.setFillColor(colors.HexColor("#333"))
    for b in beverages[8:]:
        c.drawString(col3_x, y, b['name'])
        c.setFont("Helvetica-Bold", 11)
        c.setFillColor(colors.HexColor("#ff9800"))
        c.drawRightString(col3_x + col_width - 8*mm, y, f"€ {b['price']:.2f}")
        c.setFont("Helvetica", 11)
        c.setFillColor(colors.HexColor("#333"))
        y -= 16
    
    # Footer on page 2
    footer_y = margin + 10*mm
    c.setFillColor(colors.white)
    c.setStrokeColor(colors.HexColor("#ddd"))
    c.roundRect(margin, footer_y - 8*mm, width - 2*margin, 20*mm, 4, stroke=1, fill=1)
    
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(colors.HexColor("#333"))
    c.drawCentredString(width/2, footer_y + 8*mm, "Via della Repubblica 15")
    
    c.setFont("Helvetica", 11)
    c.drawCentredString(width/2, footer_y - 2*mm, "Tel. +39 012 345 6789  •  iltuo.ristorante@gmail.com")
    
    c.save()
    print("✓ PDF generato: menu_pizzeria.pdf")

if __name__ == '__main__':
    draw_menu()
