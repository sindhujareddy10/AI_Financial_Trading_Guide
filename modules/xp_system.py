def calculate_level(xp):

    if xp < 100:
        return "Beginner Investor"

    elif xp < 300:
        return "Smart Saver"

    elif xp < 700:
        return "Market Explorer"

    elif xp < 1500:
        return "Strategic Trader"

    else:
        return "Stock Market Master"