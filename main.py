import requests
from tkinter import *
import pyperclip

# Get the data from coingecko, save it as a JSON
gecko = requests.get(url="https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=ethereum")
geckoj = gecko.json()

# Save the value of ethereum as a USD value, and the price change over 24 hour period (why not?)
eth_usd = geckoj[0]['current_price']
price_change = round(geckoj[0]['price_change_24h'], 2)

# If ether price has increased in last 24 hours, text is green, if decreased it's red
if price_change >= 0:
    price_change = f"+ ${price_change}"
    change_colour = "green"
else:
    price_change = f"- ${price_change}"
    change_colour = "red"

# Gets the USD tp AUD conversion rate
currency = requests.get(url='https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies/usd/aud.json')
currency_converter = currency.json()
us_to_au = currency_converter['aud']

def calculate():
    # Get the vlues that user has entered, as well as the correct answer
    ether = float(amount_entry.get())
    user_guess = float(guess_entry.get())
    correct = round(eth_usd * ether, 2)

    # Copy the correct answer to the clipboard
    pyperclip.copy(correct)

    # Display the correct answer
    correct_answer = Label(text=f"Correct Answer Is ${correct}", font=('Arial', 14))
    correct_answer.grid(row=5, column=0, columnspan=3, pady=5)

    # Display the difference between the users guess and the correct answer
    wrong_by = Label(text=f"You Were Off By {round(correct - user_guess, 2)}", font=('Arial', 14))
    wrong_by.grid(row=6, column=0, columnspan=3, pady=10)

    # Get the answer in AUD as well
    aud = Label(text=f"In Australian Dollars ${round(correct * us_to_au, 2)}", font=('Arial', 14))
    aud.grid(row=7, column=0, columnspan=3, pady=5)

# Build the window
window = Tk()
window.config(padx=20, pady=20)
window.geometry("500x500")
window.title("Guess the Conversion")

# Heading with current ether prices and its price change
current_price = Label(text=f"1 Ether = ${eth_usd} USD", font=('Arial', 26, 'bold'))
current_price.grid(row=0, column=0, columnspan=2)
day_change = Label(text=f"24 Hour Change {price_change}", font=('Arial', 20, 'bold'), fg=change_colour)
day_change.grid(row=1, column=0, columnspan=2, padx=80)

# Enter in the amount of ether that we are trying to oonvert
amount_lbl = Label(text="Ether Amount", pady=40, font=('Arial', 12))
amount_lbl.grid(row=2, column=0, columnspan=1)
amount_entry = Entry(width=20)
amount_entry.focus_force()
amount_entry.grid(row=2, column=1)

# Enter in your best guess as to the correct conversion number
guess_lbl = Label(text="Guess How Much USD", font=('Arial', 12), pady=8)
guess_lbl.grid(row=3, column=0)
guess_entry = Entry(width=15)
guess_entry.grid(row=3, column=1)

# Click to run
the_button = Button(text="Tell Me How Wrong I Am", command=calculate)
the_button.grid(row=4, column=0, columnspan=3, pady=30)

window.mainloop()
