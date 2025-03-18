import random
import time

CARD_VALUE = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
    '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14, 'L Joker': 15, 'B Joker': 16
}

PLAYERS = []  # Stores player data


def get_num_players():
    while True:
        try:
            num = int(input("Enter number of players (2-4): "))
            if 2 <= num <= 4:
                return num
            print("Invalid number of players. Please enter between 2 and 4.")
        except ValueError:
            print("Invalid input. Please enter an integer between 2 and 4.")


def make_players(num_players):
    global PLAYERS
    PLAYERS.clear()

    print("\n🔹 Player 1, you control when each round starts! 🔹\n")

    for i in range(1, num_players + 1):
        while True:
            name = input(f"Player {i}, enter your name: ").strip()
            if 2 <= len(name) <= 15 and name.isalpha():
                break
            print("Invalid name! Name must be 2-15 characters long and only contain letters.")

        PLAYERS.append({
            "name": name,
            "hand": [],
            "pile": []
        })


def make_deck():
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    deck = [(value, suit) for suit in suits for value in values]

    if len(PLAYERS) <= 3:
        deck.extend([('B Joker', 'Big'), ('L Joker', 'Little')])

    return deck


def shuffle_cards(deck):
    random.shuffle(deck)


def deal_deck(deck):
    current_player = 0
    while deck:
        PLAYERS[current_player]["hand"].append(deck.pop(0))
        current_player = (current_player + 1) % len(PLAYERS)


def refill_hand(player):
    """Shuffles and moves pile to hand at the end of each round."""
    if player["pile"]:
        # print(f"\n♻️ {player['name']} refills their hand with their pile.\n")
        random.shuffle(player["pile"])
        player["hand"].extend(player["pile"])
        player["pile"].clear()


def find_highest_card_players():
    highest_value = -1
    highest_players = []
    war_pile = []  # This should only store cards, not player names

    print("\n🔹 Time for the battle! Each player reveals their card... 🔹\n")

    for player in PLAYERS:
        if not player["hand"]:
            continue

        top_card = player["hand"].pop(0)
        card_value = CARD_VALUE[top_card[0]]

        war_pile.append(top_card)  # Store only the card

        print(f"{player['name']} plays: {top_card} (Value: {card_value})")
        time.sleep(0.5)

        if card_value > highest_value:
            highest_value = card_value
            highest_players = [player]
        elif card_value == highest_value:
            highest_players.append(player)

    while len(highest_players) > 1:
        print("\n⚔️ WAR! Players put down 3 cards and reveal the 4th! ⚔️\n")
        time.sleep(1.5)

        new_war_pile = []
        highest_value = -1
        new_highest_players = []

        for player in highest_players:
            if len(player["hand"]) >= 4:
                new_war_pile.extend(player["hand"][:3])
                player["hand"] = player["hand"][3:]
                top_card = player["hand"].pop(0)
                card_value = CARD_VALUE[top_card[0]]

                print(f"{player['name']}'s WAR card: {top_card} (Value: {card_value})")
                time.sleep(1.0)

                new_war_pile.append(top_card)

                if card_value > highest_value:
                    highest_value = card_value
                    new_highest_players = [player]
                elif card_value == highest_value:
                    new_highest_players.append(player)

            else:
                print(f"{player['name']} does not have enough cards for WAR and is eliminated.")
                PLAYERS.remove(player)

        war_pile.extend(new_war_pile)  # Only cards are stored
        highest_players = new_highest_players

    winner = highest_players[0] if highest_players else None
    if winner:
        print(f"\n🎉 {winner['name']} wins the round and takes all played cards! 🎉\n")
        winner["pile"].extend(war_pile)  # Ensure only cards are added

    return winner


def start_round():
    player1 = PLAYERS[0]["name"]
    input(f"\n🔹 {player1}, press Enter to start the round... 🔹\n")


# Game Setup
NUM_PLAYERS = get_num_players()
make_players(NUM_PLAYERS)
DECK = make_deck()
shuffle_cards(DECK)
deal_deck(DECK)

# Game Loop
while len([p for p in PLAYERS if p["hand"]]) > 1:
    start_round()
    find_highest_card_players()

    # Refill each player's hand from their pile at the end of every round
    for player in PLAYERS:
        refill_hand(player)

# Determine Overall Winner
winner = max(PLAYERS, key=lambda p: len(p["pile"]))
print(f"\n🏆 {winner['name']} is the ultimate champion of WAR! 🏆")






"""
pseudo
suits = ♥♠♣♦
jokers= big🃏 small🂿
~Name user player
~Choose amount of players
~Deal out cards to equally to amount of players
~Play cards from each player from top of their respective hand
~Check which player has highest card value from played
    ~If cards are equal play additional 3 cards with the last one determine respectively chose the winner 
        ~If the last card of the additional 3 are the same repeat until till process is broken and one is bigger
            ~If player does not enough cards to play additional 3 cards they will shuffle their pile and play the remaining cards
                ~If player does not have enough cards in pile they use the last card able
                ~If the last card is the same still the player without the cards to keep going loses and removed from play
~Whoever wins the hand(cards played in the round) gets cards of the hand
~Add the the cards won to a a respective pile for player
~Once a player has played all cards in their deck, they shuffle their a pile and turns into the new deck to use
    ~If player has no cards in their hand they lose and are removed from play
Once a player have all 54(52) cards game is over and WON the war
"""

