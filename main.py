from tkinter import *
import pandas
import random


BACKGROUND_COLOR = "#B1DDC6"
rand_word = []


# Button functions

def next_word(n):
    global rand_word, wait
    window.after_cancel(wait)
    rand_word = random.choice(list(data_list))
    if n == 1:
        data_list.remove(rand_word)
        df_data_list = pandas.DataFrame(data_list)
        df_data_list.to_csv("./data/words_to_learn.csv", index=False, mode="w")
    canvas.itemconfig(canvas_image, image=img_card_front)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=f"{rand_word[0]}", fill="black")
    wait = window.after(3000, flip_card)


def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=f"{rand_word[1]}", fill="white")
    canvas.itemconfig(canvas_image, image=img_card_back)


# Read data

try:
    data = pandas.read_csv("./data/words_to_learn.csv")
    data_dict = {row["0"]: row["1"] for (index, row) in data.iterrows()}
    data_list = list(data_dict.items())
except FileNotFoundError:
    data = pandas.read_csv("./data/french_words.csv")
    data_dict = {row.French: row.English for (index, row) in data.iterrows()}
    data_list = list(data_dict.items())


# Screen
window = Tk()
window.title("Flashy")
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)

# Images
img_card_back = PhotoImage(file="./images/card_back.png")
img_card_front = PhotoImage(file="./images/card_front.png")
img_right = PhotoImage(file="./images/right.png")
img_wrong = PhotoImage(file="./images/wrong.png")

# Buttons
button_right = Button(image=img_right, highlightthickness=0, command=lambda: next_word(n=1))
button_wrong = Button(image=img_wrong, highlightthickness=0, command=lambda: next_word(n=0))

# Canvas
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
canvas_image = canvas.create_image(400, 263, image=img_card_front)
card_title = canvas.create_text(400, 150, text="", font=("Arial", 40, "italic"), fill="black")
card_word = canvas.create_text(400, 263, text="", font=("Arial", 60, "bold"), fill="black")

# Grid
canvas.grid(row=0, column=0, columnspan=2)
button_right.grid(row=1, column=1)
button_wrong.grid(row=1, column=0)


wait = window.after(3000, flip_card)
next_word(0)

window.mainloop()
