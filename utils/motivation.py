import random

MOTIVATION_MESSAGES = {
    'Happy': [
        "Keep spreading that joy! Your happiness is contagious! 🌟",
        "What a wonderful emotion! Keep shining bright! ✨",
        "Your positive energy is amazing! Keep it up! 😊",
        "Happiness looks good on you! Stay blessed! 🌈",
        "You're radiating positivity! Keep that smile! 🎉"
    ],
    'Sad': [
        "It's okay to feel sad. Remember, tough times don't last, tough people do! 💪",
        "Every storm runs out of rain. Better days are coming! 🌤️",
        "You're stronger than you think. This too shall pass! 🌺",
        "Take your time to heal. You've got this! 🌟",
        "Remember, after rain comes the rainbow! Stay strong! 🌈"
    ],
    'Angry': [
        "Take a deep breath. You're in control! 🧘",
        "Channel that energy into something positive! You've got this! 💪",
        "Anger is temporary. Your peace is permanent. Find your calm! 🕊️",
        "Step back and breathe. Better solutions come with a calm mind! 🌊",
        "You're stronger when you're calm. Take a moment for yourself! 🌿"
    ],
    'Fear': [
        "Courage is not the absence of fear, but action in spite of it! 🦁",
        "You're braver than you believe! Face your fears! 💫",
        "Fear is just False Evidence Appearing Real. You can do this! 🌟",
        "Every great achievement begins with facing a fear! You're amazing! 🚀",
        "Believe in yourself! You're capable of overcoming anything! 💪"
    ],
    'Surprise': [
        "Life is full of wonderful surprises! Embrace them! 🎊",
        "Stay curious and open to new experiences! 🌟",
        "Surprises make life interesting! Keep that sense of wonder! ✨",
        "Your reaction shows you're fully present! Keep living in the moment! 🎭",
        "Life keeps things interesting! Enjoy the unexpected! 🎪"
    ],
    'Neutral': [
        "Stay balanced and centered! You're doing great! ⚖️",
        "Peace and stability are valuable! Keep that equilibrium! 🧘",
        "Your calm demeanor is admirable! Stay focused! 🎯",
        "Sometimes neutral is exactly where we need to be! 🌸",
        "Balance is key! You're right where you need to be! 🌿"
    ],
    'Disgust': [
        "It's okay to have boundaries! Trust your instincts! 🛡️",
        "Your feelings are valid! Take care of yourself! 💚",
        "Sometimes we need to step away from what doesn't serve us! 🌱",
        "Listen to your gut feelings! They're there to protect you! 🦋",
        "It's healthy to recognize what you don't resonate with! 🌟"
    ]
}

def get_motivation_message(emotion):
    '''
    Get a random motivational message based on emotion
    '''
    if emotion in MOTIVATION_MESSAGES:
        return random.choice(MOTIVATION_MESSAGES[emotion])
    else:
        return "You're amazing just the way you are! Keep being you! 💫"
