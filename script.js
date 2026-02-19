// Dati delle pizze
const pizzas = [
    {
        name: "Margherita",
        category: "classiche",
        ingredients: "Pomodoro DOP, Mozzarella fior di latte, Basilico fresco",
        price: 6.50,
        emoji: "🍅"
    },
    {
        name: "Marinara",
        category: "classiche",
        ingredients: "Pomodoro, Aglio, Origano, Olio EVO",
        price: 5.00,
        emoji: "🌬️"
    },
    {
        name: "Diavola",
        category: "speciali",
        ingredients: "Pomodoro, Mozzarella, Salame piccante, Pepe",
        price: 8.50,
        emoji: "🌶️"
    },
    {
        name: "Quattro Formaggi",
        category: "speciali",
        ingredients: "Mozzarella, Gorgonzola, Parmigiano, Provola",
        price: 9.50,
        emoji: "🧀"
    },
    {
        name: "Capricciosa",
        category: "speciali",
        ingredients: "Pomodoro, Mozzarella, Prosciutto, Funghi, Carciofi, Olive",
        price: 9.00,
        emoji: "🎨"
    },
    {
        name: "Prosciutto e Funghi",
        category: "classiche",
        ingredients: "Pomodoro, Mozzarella, Prosciutto crudo, Funghi porcini",
        price: 9.50,
        emoji: "🍄"
    },
    {
        name: "Bufalina",
        category: "speciali",
        ingredients: "Mozzarella di bufala, Pomodoro fresco, Basilico",
        price: 10.00,
        emoji: "🐃"
    },
    {
        name: "Ortolana",
        category: "speciali",
        ingredients: "Verdure grigliate, Mozzarella, Basilico, Pomodoro",
        price: 8.50,
        emoji: "🥦"
    },
    {
        name: "Tonno e Cipolla",
        category: "speciali",
        ingredients: "Pomodoro, Mozzarella, Tonno, Cipolla rossa",
        price: 8.00,
        emoji: "🐟"
    },
    {
        name: "Frutti di Mare",
        category: "speciali",
        ingredients: "Pomodoro, Mozzarella, Gamberi, Calamari, Cozze",
        price: 11.00,
        emoji: "🦐"
    },
    {
        name: "Napoli",
        category: "classiche",
        ingredients: "Pomodoro, Mozzarella, Acciughe, Capperi",
        price: 7.50,
        emoji: "🌊"
    },
    {
        name: "Siciliana",
        category: "speciali",
        ingredients: "Pomodoro, Ricotta salata, Melanzane, Basilico",
        price: 9.00,
        emoji: "🍆"
    }
];

// Dati delle bevande
const beverages = {
    bibite: [
        { name: "Acqua naturale 0.5L", price: 2.00 },
        { name: "Acqua frizzante 0.5L", price: 2.00 },
        { name: "Coca-Cola 33cl", price: 3.00 },
        { name: "Aranciata 33cl", price: 3.00 }
    ],
    birre: [
        { name: "Birra bionda 33cl", price: 4.00 },
        { name: "Birra artigianale 50cl", price: 5.50 },
        { name: "Birra alla spina 40cl", price: 4.50 }
    ],
    vini: [
        { name: "Vino rosso della casa (bicchiere)", price: 4.00 },
        { name: "Vino bianco della casa (bicchiere)", price: 4.00 },
        { name: "Chianti Classico DOC (bottiglia)", price: 18.00 },
        { name: "Prosecco DOC (bottiglia)", price: 20.00 }
    ]
};

// Elementi DOM
const pizzeGrid = document.getElementById('pizze-grid');
const filterBtns = document.querySelectorAll('.filter-btn');
const navLinks = document.querySelectorAll('.nav-link');
const modal = document.getElementById('modal');
const closeBtn = document.querySelector('.close');

let currentFilter = 'all';

// ===== INIZIALIZZAZIONE =====
document.addEventListener('DOMContentLoaded', () => {
    renderPizzas('all');
    renderBeverages();
    setupEventListeners();
});

// ===== RENDER PIZZAS =====
function renderPizzas(filter) {
    currentFilter = filter;
    
    const filteredPizzas = filter === 'all' 
        ? pizzas 
        : pizzas.filter(p => p.category === filter);
    
    pizzeGrid.innerHTML = filteredPizzas.map((pizza, index) => `
        <div class="menu-item" onclick="openModal('${pizza.name}', '${pizza.emoji}', '${pizza.ingredients}', ${pizza.price})">
            <div class="menu-item-image">${pizza.emoji}</div>
            <div class="menu-item-content">
                <div class="menu-item-category">${pizza.category === 'classiche' ? 'Classica' : 'Speciale'}</div>
                <h3 class="menu-item-name">${pizza.name}</h3>
                <p class="menu-item-ingredients">${pizza.ingredients}</p>
                <div class="menu-item-footer">
                    <span class="menu-item-price">€ ${pizza.price.toFixed(2)}</span>
                    <button class="menu-item-btn" onclick="event.stopPropagation()">Dettagli</button>
                </div>
            </div>
        </div>
    `).join('');
}

// ===== RENDER BEVERAGES =====
function renderBeverages() {
    renderBeverageColumn('bibite', beverages.bibite);
    renderBeverageColumn('birre', beverages.birre);
    renderBeverageColumn('vini', beverages.vini);
}

function renderBeverageColumn(id, items) {
    const container = document.getElementById(`${id}-list`);
    container.innerHTML = items.map(item => `
        <div class="bevanda-item">
            <span class="bevanda-name">${item.name}</span>
            <span class="bevanda-price">€ ${item.price.toFixed(2)}</span>
        </div>
    `).join('');
}

// ===== SETUP EVENT LISTENERS =====
function setupEventListeners() {
    // Filter buttons
    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            filterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            renderPizzas(btn.dataset.filter);
        });
    });

    // Navigation links
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            navLinks.forEach(l => l.classList.remove('active'));
            link.classList.add('active');
        });
    });

    // Modal close
    closeBtn.onclick = closeModal;
    window.onclick = (event) => {
        if (event.target === modal) {
            closeModal();
        }
    };
}

// ===== MODAL FUNCTIONS =====
function openModal(name, emoji, ingredients, price) {
    const modalTitle = document.getElementById('modal-title');
    const modalImage = document.getElementById('modal-image');
    const modalDetails = document.getElementById('modal-details');

    modalTitle.textContent = name;
    modalImage.innerHTML = emoji;
    modalImage.style.fontSize = '120px';
    
    modalDetails.innerHTML = `
        <div>
            <p><strong>Ingredienti:</strong></p>
            <p>${ingredients}</p>
        </div>
        <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 20px; padding-top: 20px; border-top: 2px solid #404040;">
            <span style="font-size: 28px; color: #ff9800; font-weight: bold;">€ ${price.toFixed(2)}</span>
            <button onclick="addToCart('${name}', ${price})" style="background: #ff9800; color: white; border: none; padding: 12px 30px; border-radius: 6px; font-weight: bold; cursor: pointer; font-size: 15px; transition: all 0.3s ease;" onmouseover="this.style.background='#c62828'" onmouseout="this.style.background='#ff9800'">Aggiungi al carrello</button>
        </div>
    `;

    modal.style.display = 'block';
}

function closeModal() {
    modal.style.display = 'none';
}

function addToCart(name, price) {
    // Animazione di feedback
    const notification = document.createElement('div');
    notification.textContent = `✓ ${name} aggiunto al carrello!`;
    notification.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: #4caf50;
        color: white;
        padding: 15px 25px;
        border-radius: 6px;
        font-weight: bold;
        z-index: 2000;
        animation: slideIn 0.3s ease;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    `;
    document.body.appendChild(notification);
    
    closeModal();
    
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// ===== SMOOTH SCROLL =====
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth' });
        }
    });
});

// ===== ANIMAZIONE AL CARICAMENTO =====
window.addEventListener('load', () => {
    const items = document.querySelectorAll('.menu-item');
    items.forEach((item, index) => {
        item.style.opacity = '0';
        item.style.animation = `slideDown 0.5s ease ${index * 0.05}s forwards`;
    });
});
