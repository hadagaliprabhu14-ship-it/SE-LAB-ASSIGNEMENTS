import pytest

from atm_withdrawal import note_breakup, pin_check, withdraw


def test_unknown_account_branch():
    with pytest.raises(ValueError, match="unknown account"):
        withdraw(5000, 1000, "business", True)


def test_nonpositive_amount_branch():
    with pytest.raises(ValueError, match="invalid amount"):
        withdraw(5000, 0, "savings", True)


def test_nonmultiple_amount_branch():
    with pytest.raises(ValueError, match="invalid amount"):
        withdraw(5000, 150, "savings", True)


def test_daily_limit_exceeded_branch():
    assert withdraw(30000, 25100, "savings", True) == "limit exceeded"


def test_daily_limit_not_exceeded_branch():
    assert withdraw(25000, 25000, "savings", True) == 0


def test_own_bank_fee_branch():
    assert withdraw(5000, 1000, "savings", True) == 4000


def test_other_bank_fee_without_large_withdrawal_surcharge():
    assert withdraw(12000, 10000, "savings", False) == 1980


def test_other_bank_fee_with_large_withdrawal_surcharge():
    assert withdraw(20000, 10100, "savings", False) == 9870


def test_insufficient_funds_branch():
    assert withdraw(1019, 1000, "savings", False) == "insufficient funds"


def test_sufficient_funds_branch_at_exact_total():
    assert withdraw(1020, 1000, "savings", False) == 0


def test_pin_attempts_at_or_above_three_branch():
    assert pin_check(1234, 1234, 3) == "card blocked"


def test_correct_pin_branch():
    assert pin_check(1234, 1234, 1) == "ok"


def test_wrong_pin_on_attempt_count_two_branch():
    assert pin_check(1111, 1234, 2) == "card blocked"


def test_wrong_pin_on_lower_attempt_count_branch():
    assert pin_check(1111, 1234, 1) == "retry"


def test_invalid_note_amount_branch():
    with pytest.raises(ValueError, match="invalid amount"):
        note_breakup(250)


def test_note_breakup_remainder_below_200_branch():
    assert note_breakup(600) == (1, 0, 1)


def test_note_breakup_remainder_at_least_200_branch():
    assert note_breakup(700) == (1, 1, 0)