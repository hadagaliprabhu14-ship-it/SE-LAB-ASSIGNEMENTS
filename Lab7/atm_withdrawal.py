import re


def notes_needed(amount):
    if not isinstance(amount, str):
        raise ValueError("amount must be text")

    normalized = amount.strip()
    if not normalized:
        raise ValueError("amount cannot be empty")

    amount_pattern = r"(?:\d+|\d{1,3}(?:,\d{3})+)"
    if re.fullmatch(amount_pattern, normalized) is None:
        raise ValueError(
            "amount must be a non-negative whole number, optionally comma-grouped"
        )

    return int(normalized.replace(",", "")) // 100


def mask_card(card_number):
    if not isinstance(card_number, str):
        raise ValueError("card number must be text")

    groups = card_number.split()
    if len(groups) != 4 or not all(group.isdecimal() for group in groups):
        raise ValueError("card number must contain exactly four numeric groups")

    return "XXXX XXXX XXXX " + groups[3]


def average_withdrawal(amounts_csv):
    if not isinstance(amounts_csv, str):
        raise ValueError("withdrawals must be text")

    if not amounts_csv.strip():
        raise ValueError("withdrawals cannot be empty")

    parts = [part.strip() for part in amounts_csv.split(",")]
    if any(not part or not part.isdecimal() for part in parts):
        raise ValueError("withdrawals must be non-negative whole numbers separated by commas")

    amounts = [int(part) for part in parts]
    return sum(amounts) // len(amounts)


def main():
    print("==== Running notes_needed ====")
    user_input = input("Enter an amount (e.g. 2,500): ")
    result = notes_needed(user_input)
    print("Number of 100 Notes:", result)

    print("\n==== Running mask_card ====")
    user_input = input("Enter a card number (e.g. 1234 5678 9012 3456): ")
    result = mask_card(user_input)
    print("Masked Card:", result)

    print("\n==== Running average_withdrawal ====")
    user_input = input("Enter withdrawals as CSV (e.g. 500,1000,2000): ")
    result = average_withdrawal(user_input)
    print("Average Withdrawal:", result)


if __name__ == "__main__":
    main()