// Breathing Exercise
let breathingInterval;

function startBreathing() {
    document.getElementById('breathing-area').style.display = 'block';
    document.getElementById('breathing-area').scrollIntoView({ behavior: 'smooth' });

    const phases = ['Breathe In...', 'Hold...', 'Breathe Out...', 'Hold...'];
    let currentPhase = 0;

    updateBreathingText();

    breathingInterval = setInterval(() => {
        currentPhase = (currentPhase + 1) % phases.length;
        updateBreathingText();
    }, 4000);

    function updateBreathingText() {
        document.getElementById('breathing-text').textContent = phases[currentPhase];
    }
}

function stopBreathing() {
    clearInterval(breathingInterval);
    document.getElementById('breathing-area').style.display = 'none';
}

// Positive Quotes
const quotes = [
    "Believe you can and you're halfway there. - Theodore Roosevelt",
    "The only way to do great work is to love what you do. - Steve Jobs",
    "Success is not final, failure is not fatal: It is the courage to continue that counts. - Winston Churchill",
    "You are never too old to set another goal or to dream a new dream. - C.S. Lewis",
    "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
    "It does not matter how slowly you go as long as you do not stop. - Confucius",
    "Everything you've ever wanted is on the other side of fear. - George Addair",
    "Believe in yourself. You are braver than you think, more talented than you know, and capable of more than you imagine. - Roy T. Bennett",
    "I learned that courage was not the absence of fear, but the triumph over it. - Nelson Mandela",
    "Your limitation—it's only your imagination.",
    "Great things never come from comfort zones.",
    "Dream it. Wish it. Do it.",
    "Success doesn't just find you. You have to go out and get it.",
    "The harder you work for something, the greater you'll feel when you achieve it.",
    "Don't stop when you're tired. Stop when you're done."
];

function showQuote() {
    const quoteArea = document.getElementById('quote-area');
    const quoteText = document.getElementById('quote-text');

    const randomQuote = quotes[Math.floor(Math.random() * quotes.length)];
    quoteText.textContent = `"${randomQuote}"`;

    quoteArea.style.display = 'block';
    quoteArea.scrollIntoView({ behavior: 'smooth' });
}

function closeQuote() {
    document.getElementById('quote-area').style.display = 'none';
}

// Memory Game
let memoryCards = [];
let flippedCards = [];
let moves = 0;
let matches = 0;

function startMemoryGame() {
    document.getElementById('memory-area').style.display = 'block';
    document.getElementById('memory-area').scrollIntoView({ behavior: 'smooth' });

    moves = 0;
    matches = 0;
    flippedCards = [];

    document.getElementById('moves').textContent = moves;
    document.getElementById('matches').textContent = matches;

    // Create card pairs
    const emojis = ['😊', '😎', '🥳', '😍', '🤗', '🌟', '🎉', '🎈'];
    memoryCards = [...emojis, ...emojis].sort(() => Math.random() - 0.5);

    const board = document.getElementById('memory-game-board');
    board.innerHTML = '';

    memoryCards.forEach((emoji, index) => {
        const card = document.createElement('div');
        card.className = 'memory-card';
        card.dataset.emoji = emoji;
        card.dataset.index = index;
        card.textContent = '?';
        card.addEventListener('click', flipCard);
        board.appendChild(card);
    });
}

function flipCard() {
    if (flippedCards.length >= 2 || this.classList.contains('flipped')) {
        return;
    }

    this.classList.add('flipped');
    this.textContent = this.dataset.emoji;
    flippedCards.push(this);

    if (flippedCards.length === 2) {
        moves++;
        document.getElementById('moves').textContent = moves;

        setTimeout(checkMatch, 800);
    }
}

function checkMatch() {
    const [card1, card2] = flippedCards;

    if (card1.dataset.emoji === card2.dataset.emoji) {
        matches++;
        document.getElementById('matches').textContent = matches;

        if (matches === 8) {
            setTimeout(() => {
                alert(`Congratulations! You won in ${moves} moves!`);
            }, 500);
        }
    } else {
        card1.classList.remove('flipped');
        card2.classList.remove('flipped');
        card1.textContent = '?';
        card2.textContent = '?';
    }

    flippedCards = [];
}

function closeMemoryGame() {
    document.getElementById('memory-area').style.display = 'none';
}
