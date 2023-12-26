import random

MAX_LINES: int = 3
MAX_BET: int = 100
MIN_BET: int = 1

ROWS: int = 3
COLS: int = 3

symbol_count: dict = {
    "!": 2,
    "@": 4,
    "#": 6,
    "&": 8
}

symbol_value: dict = {
    "!": 5,
    "@": 4,
    "#": 3,
    "&": 2,
}


def check_winnings(columns, lines, bet, values):
    winnings = 0
    winning_lines = []
    for line in range(lines):
        symbol = columns[0][line]
        for column in columns:
            symbol_to_check = column[line]
            if symbol != symbol_to_check:
                break
        else:
            winnings += values[symbol] * bet
            winning_lines.append(line + 1)

    return winnings, winning_lines


def get_slot_machine_spin(rows, cols, symbols: dict):
    all_symbols = []
    for symbol, symbol_count1 in symbols.items():
        for _ in range(symbol_count1):
            all_symbols.append(symbol)

    columns = []

    for _ in range(cols):
        column = []
        current_symbols = all_symbols[:]
        for _ in range(rows):
            value = random.choice(current_symbols)
            current_symbols.remove(value)
            column.append(value)

        columns.append(column)

    return columns


def print_slot_machine(columns):
    for row in range(len(columns[0])):
        for i, column in enumerate(columns):
            if i != len(columns) - 1:
                print(column[row], end=" | ")
            else:
                print(column[row], end="")

        print()


def deposit():
    while True:
        amount = input("What would you like to deposit? $\n")
        if amount.isdigit():
            amount = int(amount)
            if amount > 0:
                break
            else:
                print("Amount must be greater then 0.\n")
        else:
            print("Please enter a number.\n")

    return amount


def get_number_of_lines():
    while True:
        lines = input(f"Enter the number of lines to bet on (1-{MAX_LINES})? \n")
        if lines.isdigit():
            lines = int(lines)
            if 1 <= lines <= MAX_LINES:
                break
            else:
                print("Enter a valid number of lines.\n")
        else:
            print("Please enter a number.\n")

    return lines


def get_bet():
    while True:
        amount = input("What would you like to bet on each line? $\n")
        if amount.isdigit():
            amount = int(amount)
            if MIN_BET <= amount <= MAX_BET:
                break
            else:
                print(f"Amount must be between ${MIN_BET} - ${MAX_BET}.\n")
        else:
            print("Please enter a number.\n")

    return amount


def spin(balance: int) -> int:
    while True:
        lines = get_number_of_lines()
        bet = get_bet()
        total_bet = bet * lines

        if total_bet > balance:
            print(f"You do not have enough to bet that amount, your current balance is: ${balance}\n")
        else:
            break

    print(f"You are betting ${bet} on {lines} lines. Total bet is equal to: ${total_bet}\n")

    slots = get_slot_machine_spin(ROWS, COLS, symbol_count)
    print_slot_machine(slots)
    winnings, winning_lines = check_winnings(slots, lines, bet, symbol_value)
    print(f"\nYou won {winnings}.")
    print(f"You won on lines:", *winning_lines)
    return winnings - total_bet


def check_balance(balance: int) -> (int, str, str):
    if balance > 0:
        decision = input("Press enter to play (q to quit).\n")
    else:
        print(f"\nYou do not have enough to bet that amount, your current balance is: ${balance}\n")
        while True:
            decision = input("Would you like to deposit? (d to deposit , q to quit)\n")
            if decision == "d":
                balance = balance + deposit()
                break
            elif decision == "q":
                print(f"\nThank you for playing")
                break
    return balance, decision


def main():
    balance = deposit()
    while True:
        balance, decision = check_balance(balance)
        if decision == "q":
            break
        print(f"\nCurrent balance is ${balance}\n")
        balance += spin(balance)

    print(f"You left with ${balance}\n")


main()
