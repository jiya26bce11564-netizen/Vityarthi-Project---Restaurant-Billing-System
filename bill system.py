"""
=======================================================
        SMART RESTAURANT BILLING SYSTEM 
=======================================================

What it can do:
    1. Show the menu
    2. Take an order (item + quantity)
    3. Calculate subtotal, tax, discount and total
    4. Print a receipt
    5. Save the receipt to a text file

Author: (you!)
=========================================================
"""

import datetime

# --------------------------------------------------------------
# SECTION 1: BASIC SETTINGS
# --------------------------------------------------------------
# Keeping all the "settings" together at the top makes it easy
# to change the restaurant's details, tax rate, etc. later,
# without having to search through the whole file.
#
# These are called "constants". By convention, Python
# programmers write constant names in ALL_CAPS so that anyone
# reading the code immediately knows these values are not
# meant to change while the program is running.

# The name shown at the top of the menu and every receipt.
RESTAURANT_NAME = "The Python Kitchen"

# The symbol used before every price (e.g. "Rs.120").
# Change this if your currency is different, e.g. "$" or "€".
CURRENCY_SYMBOL = "Rs."

# TAX_RATE of 0.05 means 5%. To turn a percentage into a
# decimal you divide by 100, so 5% becomes 0.05.
TAX_RATE = 0.05

# DISCOUNT_RATE of 0.10 means 10% off, but only if the order
# is large enough (see DISCOUNT_MIN_AMOUNT below).
DISCOUNT_RATE = 0.10

# The customer only gets a discount if their subtotal (before
# tax) is at least this amount.
DISCOUNT_MIN_AMOUNT = 1000

# Extra discount rates based on who the customer is.
# This is a dictionary of { customer_type: discount_rate }.
# For example, 0.05 means a 5% discount.
CUSTOMER_DISCOUNTS = {
    "regular": 0.00,    # no special discount
    "student": 0.05,    # 5% off for students
    "premium": 0.15,    # 15% off for premium/loyalty customers
    "couple": 0.10,     # 10% off for a couple's meal
}

# The name of the file where each receipt gets saved.
# Every new bill will overwrite this same file, which keeps
# the example simple for beginners.
RECEIPT_FILE_NAME = "receipt.txt"


# --------------------------------------------------------------
# SECTION 2: THE MENU
# --------------------------------------------------------------
# The menu is stored as a "dictionary". A dictionary stores
# information in key-value pairs, similar to a real dictionary
# where a word (the key) has a meaning (the value).
#
# Here, each key is the item's name, and each value is its
# price:
#       { item_name: price }

menu = {
    "Spring Roll": 120,
    "Paneer Tikka": 180,
    "Chicken Wings": 220,
    "Veg Biryani": 200,
    "Chicken Biryani": 260,
    "Butter Naan": 40,
    "Dal Makhani": 150,
    "Cold Coffee": 90,
    "Fresh Lime Soda": 60,
    "Masala Chai": 40,
    "Gulab Jamun": 70,
    "Ice Cream Scoop": 60,
}


# --------------------------------------------------------------
# SECTION 3: SMALL HELPER FUNCTIONS
# --------------------------------------------------------------

def print_line():
    """
    Prints a simple dashed line, like: ----------------------
    This is just used to visually separate sections of text
    so the console output is easier to read.
    """
    print("-" * 40)


def get_number(prompt, minimum=1):
    """
    Asks the user to type a whole number and keeps asking again
    if the input is not valid.

    """
    while True:
        text = input(prompt)
        if text.isdigit() and int(text) >= minimum:
            return int(text)
        print(f"Please enter a whole number that is at least {minimum}.")


def get_yes_no(prompt):
    """
    Asks a yes/no question and keeps asking until the user
    replies with exactly "y" or "n".
    Returns True for yes, and False for no.
    """
    while True:
        answer = input(prompt + " (y/n): ").lower()
        if answer == "y":
            return True
        if answer == "n":
            return False
        print("Please type y or n.")


# --------------------------------------------------------------
# SECTION 4: SHOWING THE MENU
# --------------------------------------------------------------

def show_menu():
    """
    Prints every item in the menu with a number next to it,
    so the customer/cashier can choose items by typing a number.
    """
    print_line()
    print(RESTAURANT_NAME.center(40))
    print("MENU".center(40))
    print_line()

    # enumerate() gives us both the position (1, 2, 3...) and
    # the item name at the same time.
    for position, item_name in enumerate(menu.keys(), start=1):
        price = menu[item_name]
        print(f"{position}. {item_name} - {CURRENCY_SYMBOL}{price}")

    print_line()


def get_item_name_by_number(number):
    """
    Given a menu number (like 3), returns the matching item name.
    Returns None if the number does not exist on the menu.

    """
    item_names = list(menu.keys())
    if 1 <= number <= len(item_names):
        return item_names[number - 1]
    return None


# --------------------------------------------------------------
# SECTION 5: TAKING THE ORDER
# --------------------------------------------------------------

def take_order():
    """
    Lets the customer pick items one at a time.
    Returns the order as a list of small dictionaries, like:
        [
            {"name": "Spring Roll", "price": 120, "qty": 2},
            {"name": "Cold Coffee", "price": 90, "qty": 1},
        ]
    Using a list of dictionaries (instead of a nested dictionary)
    keeps the data very easy to read and loop through.
    """
    order = []

    show_menu()
    print("Type the item number to add it to the order.")
    print("Type 0 when you are done.\n")

    while True:
        choice = get_number("Item number (0 to finish): ", minimum=0)

        if choice == 0:
            break

        item_name = get_item_name_by_number(choice)

        if item_name is None:
            print("That number is not on the menu. Try again.")
            continue

        quantity = get_number(f"How many '{item_name}'? ")
        price = menu[item_name]

        order.append({"name": item_name, "price": price, "qty": quantity})
        print(f"Added {quantity} x {item_name}\n")

    return order


# --------------------------------------------------------------
# SECTION 5B: CHOOSING THE CUSTOMER TYPE
# --------------------------------------------------------------
# This dictionary connects a menu number to a customer type.
# Each customer type is a tuple: (key, label)
#   - "key" matches a key in CUSTOMER_DISCOUNTS (used for maths)
#   - "label" is the friendly name shown to the user

CUSTOMER_TYPE_OPTIONS = {
    1: ("regular", "Regular Customer"),
    2: ("student", "Student"),
    3: ("premium", "Premium Customer"),
    4: ("couple", "Couple"),
}


def choose_customer_type():
    """
    Asks the cashier/customer to pick a customer type from a
    short list, and returns that type as (key, label).

    The discount percentage is shown next to each option so
    the user can see exactly what they are choosing.
    """
    print("\nSelect Customer Type:")
    for number, (key, label) in CUSTOMER_TYPE_OPTIONS.items():
        percent = int(CUSTOMER_DISCOUNTS[key] * 100)
        print(f"{number}. {label} ({percent}% discount)")

    while True:
        choice = get_number("Choose an option (1-4): ")
        if choice in CUSTOMER_TYPE_OPTIONS:
            return CUSTOMER_TYPE_OPTIONS[choice]
        print("Please choose a number between 1 and 4.")



# Each calculation is its own small function. This makes the
# math easy to follow and easy to test one piece at a time.

def get_subtotal(order):
    """
    Adds up price * quantity for every item in the order.

    Example: if the order has 2 Spring Rolls at Rs.120 each
    and 1 Cold Coffee at Rs.90, the subtotal is:
        (2 * 120) + (1 * 90) = 240 + 90 = 330
    """
    subtotal = 0
    for entry in order:
        subtotal = subtotal + (entry["price"] * entry["qty"])
    return subtotal


def get_discount(subtotal, customer_key):
    """
    Returns the discount amount to apply.

    There are two ways to earn a discount:
        1. A "bulk order" discount, if the subtotal is large
           enough (DISCOUNT_MIN_AMOUNT or more).
        2. A "customer type" discount, based on who the
           customer is (student, premium, couple, etc.) -
           see CUSTOMER_DISCOUNTS near the top of the file.

    The customer gets whichever discount is BIGGER, not both
    added together - this keeps the math simple and avoids
    accidentally giving away too much.
    """
    bulk_order_rate = DISCOUNT_RATE if subtotal >= DISCOUNT_MIN_AMOUNT else 0
    customer_type_rate = CUSTOMER_DISCOUNTS.get(customer_key, 0)

    best_rate = max(bulk_order_rate, customer_type_rate)
    return subtotal * best_rate


def get_tax(amount):
    """
    Returns the tax amount for the given amount.
    Tax is calculated on the amount AFTER the discount has
    already been taken off, which is the usual real-world rule.
    """
    return amount * TAX_RATE


def calculate_bill(order, customer_key, customer_label):
    """
    Runs all the bill calculations in the correct order and
    returns everything as one dictionary, so it is easy to pass
    around and print later.

    The order of operations matters here:
        1. Work out the subtotal (before anything else)
        2. Work out the discount, based on the subtotal AND
           the customer type
        3. Subtract the discount to get the discounted amount
        4. Work out tax on the discounted amount
        5. Add tax to the discounted amount to get the total
    """
    subtotal = get_subtotal(order)
    discount = get_discount(subtotal, customer_key)
    amount_after_discount = subtotal - discount
    tax = get_tax(amount_after_discount)
    total = amount_after_discount + tax

    # Returning a dictionary (instead of several separate
    # values) means the caller gets one neat bundle of results,
    # and we can add new fields later without changing every
    # function signature that uses this bill.
    return {
        "subtotal": subtotal,
        "discount": discount,
        "tax": tax,
        "total": total,
        "customer_label": customer_label,
    }


# --------------------------------------------------------------
# SECTION 7: PRINTING AND SAVING THE RECEIPT
# --------------------------------------------------------------

def build_receipt_text(order, bill):
    """
    Builds the receipt as one big piece of text.

    Doing it this way (building a list of lines, then joining
    them into one string at the end) means we can print the
    receipt AND save it to a file using the exact same text,
    instead of writing the formatting logic twice.
    """
    lines = []

    lines.append("=" * 40)
    lines.append(RESTAURANT_NAME.center(40))
    lines.append("=" * 40)

    now = datetime.datetime.now()
    lines.append("Date: " + now.strftime("%d-%m-%Y %H:%M:%S"))
    lines.append("-" * 40)

    # Column headings
    lines.append(f"{'Item':<18}{'Qty':>5}{'Amount':>15}")
    lines.append("-" * 40)

    # One line per ordered item
    for entry in order:
        name = entry["name"]
        qty = entry["qty"]
        amount = entry["price"] * qty
        amount_text = f"{CURRENCY_SYMBOL}{amount}"
        lines.append(f"{name:<18}{qty:>5}{amount_text:>15}")

    lines.append("-" * 40)
    lines.append(f"{'Subtotal':<25}{CURRENCY_SYMBOL}{bill['subtotal']:.2f}")
    lines.append(f"Customer Type: {bill['customer_label']}")
    lines.append(f"{'Discount':<25}-{CURRENCY_SYMBOL}{bill['discount']:.2f}")
    lines.append(f"{'Tax':<25}{CURRENCY_SYMBOL}{bill['tax']:.2f}")
    lines.append("=" * 40)
    lines.append(f"{'TOTAL':<25}{CURRENCY_SYMBOL}{bill['total']:.2f}")
    lines.append("=" * 40)
    lines.append("Thank you! Visit again.".center(40))

    # Join all the lines into one string, separated by newlines
    return "\n".join(lines)


def save_receipt(receipt_text):
    """
    Saves the receipt text to a simple text file.

    The "with open(...) as file:" pattern automatically closes
    the file for us once we're done writing to it, even if an
    error happens - so we don't have to remember to close it
    ourselves.
    """
    with open(RECEIPT_FILE_NAME, "w") as file:
        file.write(receipt_text)
    print(f"\nReceipt saved to '{RECEIPT_FILE_NAME}'")


def print_and_save_receipt(order, bill):
    """Builds the receipt, prints it, and saves it to a file."""
    receipt_text = build_receipt_text(order, bill)
    print("\n" + receipt_text)
    save_receipt(receipt_text)


# --------------------------------------------------------------
# SECTION 8: SHOWING THE ORDER BEFORE BILLING
# --------------------------------------------------------------

def show_order_summary(order):
    """Prints a quick summary of what has been ordered so far."""
    if not order:
        print("\nNo items have been ordered yet.")
        return

    print("\nYour order so far:")
    print_line()
    for entry in order:
        print(f"{entry['name']} x {entry['qty']}")
    print_line()


# --------------------------------------------------------------
# SECTION 9: THE MAIN MENU (what the user sees first)
# --------------------------------------------------------------

def print_main_menu():
    """Prints the top-level list of options."""
    print("\n" + "=" * 40)
    print("MAIN MENU".center(40))
    print("=" * 40)
    print("1. Place a New Order")
    print("2. View Restaurant Menu")
    print("3. Exit")
    print("=" * 40)


def handle_new_order():
    """
    Runs the full flow for one customer, step by step:
        1. Take the order (item numbers + quantities)
        2. Show a quick summary of what was ordered
        3. Ask for confirmation
        4. Calculate and print/save the final bill

    Keeping this as one function that simply calls the other
    functions in order makes the overall flow of the program
    very easy to follow, even for someone reading the code for
    the first time.
    """
    order = take_order()
    show_order_summary(order)

    if not order:
        print("No bill generated since the order was empty.")
        return

    if get_yes_no("Generate the final bill now?"):
        customer_key, customer_label = choose_customer_type()
        bill = calculate_bill(order, customer_key, customer_label)
        print_and_save_receipt(order, bill)
    else:
        print("Bill was not generated.")


# --------------------------------------------------------------
# SECTION 10: PROGRAM ENTRY POINT
# --------------------------------------------------------------

def main():
    """
    The main loop of the program.

    Keeps showing the main menu until the user chooses to exit.
    This kind of "loop that keeps running until the user picks
    exit" is often called an event loop, and it's the standard
    way to structure a simple console program like this one.
    """
    print("Welcome to the Smart Restaurant Billing System!")

    while True:
        print_main_menu()
        choice = get_number("Choose an option (1-3): ")

        if choice == 1:
            handle_new_order()
        elif choice == 2:
            show_menu()
        elif choice == 3:
            print("\nThank you for using the billing system. Goodbye!")
            break
        else:
            print("Please choose 1, 2 or 3.")


# --------------------------------------------------------------
# WHY THIS LAST PART LOOKS THE WAY IT DOES
# --------------------------------------------------------------
# In Python, every file has a special variable called __name__.
#   - When you RUN this file directly (python billing.py),
#     __name__ is automatically set to "__main__".
#   - When this file is IMPORTED into another program instead
#     (import billing), __name__ is set to "billing" instead.
#
# So the check below means: "only start the program if this
# file was run directly - don't start it automatically just
# because someone imported it." This is a very common pattern
# in Python programs, and it's good practice to always include
# it at the bottom of a script like this one.

if __name__ == "__main__":
    main()