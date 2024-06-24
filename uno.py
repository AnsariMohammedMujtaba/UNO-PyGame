import tkinter as tk
from tkinter import messagebox
import random

def buildDeck():
    deck = []
    colours = ["Red", "Green", "Yellow", "Blue"]
    values = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, "Draw Two", "Skip", "Reverse"]
    wilds = ["Wild", "Wild Draw Four"]
    for colour in colours:
        for value in values:
            cardVal = f"{colour} {value}"
            deck.append(cardVal)
            if value != 0:
                deck.append(cardVal)
    for _ in range(4):
        deck.append(wilds[0])
        deck.append(wilds[1])
    return deck

def shuffleDeck(deck):
    random.shuffle(deck)
    return deck

def drawCards(numCards):
    cardsDrawn = []
    for _ in range(numCards):
        if unoDeck:
            cardsDrawn.append(unoDeck.pop(0))
        else:
            messagebox.showinfo("Deck Empty", "No more cards in the deck.")
    return cardsDrawn

def showHand(player, playerHand):
    hand_frame = player_frames[player]
    for widget in hand_frame.winfo_children():
        widget.destroy()
    tk.Label(hand_frame, text=f"Player {player + 1}'s Hand", font=('Helvetica', 14)).pack()
    for idx, card in enumerate(playerHand):
        cardColor = "black"  # Default color
        if "Red" in card:
            cardColor = "red"
        elif "Green" in card:
            cardColor = "green"
        elif "Yellow" in card:
            cardColor = "gold"
        elif "Blue" in card:
            cardColor = "blue"
        elif "Wild" in card:
            cardColor = "black"

        btn = tk.Button(hand_frame, text=card, fg=cardColor, command=lambda idx=idx: playCard(player, idx))
        btn.pack(side=tk.LEFT)

def playCard(player, cardIndex):
    global playerTurn, currentColour, cardVal, playDirection
    
    if player != playerTurn:
        messagebox.showerror("Invalid Move", "It's not your turn.")
        return
    
    card = players[player][cardIndex]
    splitCard = card.split(" ", 1)

    if canPlay(currentColour, cardVal, [card]):
        discards.append(players[player].pop(cardIndex))

        if len(players[player]) == 0:
            messagebox.showinfo("Game Over", f"Player {player + 1} wins!")
            root.destroy()
            return

        currentColour = splitCard[0]
        cardVal = splitCard[1] if len(splitCard) > 1 else "Any"

        if currentColour == "Wild":
            chooseColour()

        if cardVal == "Reverse":
            playDirection *= -1
        elif cardVal == "Skip":
            playerTurn = (playerTurn + playDirection) % numPlayers

        elif cardVal == "Draw Two":
            drawPlayer = (playerTurn + playDirection) % numPlayers
            players[drawPlayer].extend(drawCards(2))
            showHand(drawPlayer, players[drawPlayer])

        elif cardVal == "Draw Four":
            drawPlayer = (playerTurn + playDirection) % numPlayers
            players[drawPlayer].extend(drawCards(4))
            showHand(drawPlayer, players[drawPlayer])

        playerTurn = (playerTurn + playDirection) % numPlayers
        updateGUI()

    else:
        messagebox.showerror("Invalid Move", "You cannot play that card.")

def drawCard():
    global playerTurn
    players[playerTurn].extend(drawCards(1))
    playerTurn = (playerTurn + playDirection) % numPlayers
    updateGUI()

def canPlay(colour, value, playerHand):
    for card in playerHand:
        if "Wild" in card or colour in card or value in card:
            return True
    return False

def chooseColour():
    global colours  # Ensure the colours list is accessible in this function
    def setColour(newColour):
        global currentColour
        currentColour = newColour
        colorWindow.destroy()
        updateGUI()

    colorWindow = tk.Toplevel(root)
    colorWindow.title("Choose Colour")
    tk.Label(colorWindow, text="Choose a new colour", font=('Helvetica', 14)).pack()
    colours = ["Red", "Green", "Yellow", "Blue"]
    for idx, color in enumerate(colours):
        btn = tk.Button(colorWindow, text=color, command=lambda color=color: setColour(color))
        btn.pack(side=tk.LEFT)

def updateGUI():
    discard_label.config(text=f"Top of Discard Pile: {discards[-1]}")
    turn_label.config(text=f"Player {playerTurn + 1}'s Turn")
    for i in range(numPlayers):
        showHand(i, players[i])

def startGame():
    global numPlayers, unoDeck, players, playerTurn, playDirection, discards, currentColour, cardVal

    try:
        numPlayers = int(num_players_entry.get())
        if numPlayers < 2 or numPlayers > 4:
            raise ValueError
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a number between 2 and 4.")
        return

    unoDeck = shuffleDeck(buildDeck())
    discards = []
    players = []
    for player in range(numPlayers):
        players.append(drawCards(5))

    playerTurn = 0
    playDirection = 1
    discards.append(unoDeck.pop(0))
    splitCard = discards[0].split(" ", 1)
    currentColour = splitCard[0]
    cardVal = splitCard[1] if currentColour != "Wild" else "Any"

    start_frame.pack_forget()
    game_frame.pack()
    updateGUI()

# Setup GUI
root = tk.Tk()
root.title("UNO Game")

start_frame = tk.Frame(root)
start_frame.pack()

tk.Label(start_frame, text="Enter number of players (2-4):", font=('Helvetica', 14)).pack()
num_players_entry = tk.Entry(start_frame, font=('Helvetica', 14))
num_players_entry.pack()
tk.Button(start_frame, text="Start Game", command=startGame, font=('Helvetica', 14)).pack()

game_frame = tk.Frame(root)

turn_label = tk.Label(game_frame, text="", font=('Helvetica', 16))
turn_label.pack()

discard_frame = tk.Frame(game_frame)
discard_frame.pack()
discard_label = tk.Label(discard_frame, text="", font=('Helvetica', 14))
discard_label.pack()

player_frames = []
for i in range(4):  # Max number of players is 4
    frame = tk.Frame(game_frame)
    frame.pack()
    player_frames.append(frame)

draw_button = tk.Button(game_frame, text="Draw Card", command=drawCard)
draw_button.pack()

root.mainloop()
