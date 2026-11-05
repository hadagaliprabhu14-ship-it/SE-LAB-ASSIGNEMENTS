import pytest

from atm_withdrawal import note_breakup, pin_check, withdraw


def test_unknown_account_is_rejected():
    with pytest.raises(ValueError, match="unknown account"):
        withdraw(5000, 1000, "business", True)


@pytest.mark.parametrize("amount", [0, -100, 50])
def test_invalid_withdrawal_amount_is_rejected(amount):
    with pytest.raises(ValueError, match="invalid amount"):
        withdraw(5000, amount, "savings", True)


@pytest.mark.parametrize(
    ("account_type", "amount"),
    [("savings", 25100), ("current", 50100)],
)
def test_daily_limit_is_enforced(account_type, amount):
    assert withdraw(100000, amount, account_type, True) == "limit exceeded"


def test_withdrawal_at_savings_limit_succeeds():
    assert withdraw(25000, 25000, "savings", True) == 0


def test_own_bank_withdrawal_has_no_fee():
    assert withdraw(5000, 1000, "savings", True) == 4000


def test_other_bank_withdrawal_up_to_10000_adds_20_fee():
    assert withdraw(5000, 1000, "savings", False) == 3980


def test_other_bank_withdrawal_over_10000_adds_30_fee():
    assert withdraw(20000, 10100, "savings", False) == 9870


def test_withdrawal_fee_can_make_balance_insufficient():
    assert withdraw(1019, 1000, "savings", False) == "insufficient funds"


def test_balance_equal_to_withdrawal_and_fee_is_accepted():
    assert withdraw(1020, 1000, "savings", False) == 0


def test_pin_is_blocked_after_three_attempts_even_if_correct():
    assert pin_check(1234, 1234, 3) == "card blocked"


def test_correct_pin_before_blocking_attempts_is_accepted():
    assert pin_check(1234, 1234, 0) == "ok"


def test_wrong_pin_on_final_attempt_blocks_card():
    assert pin_check(1111, 1234, 2) == "card blocked"


def test_wrong_pin_before_final_attempt_allows_retry():
    assert pin_check(1111, 1234, 1) == "retry"


def test_note_breakup_rejects_amount_not_divisible_by_100():
    with pytest.raises(ValueError, match="invalid amount"):
        note_breakup(150)


def test_note_breakup_without_200_notes():
    assert note_breakup(600) == (1, 0, 1)


def test_note_breakup_with_200_notes():
    assert note_breakup(700) == (1, 1, 0)