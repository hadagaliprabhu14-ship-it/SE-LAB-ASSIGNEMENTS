import re

import pytest
from hypothesis import given, strategies as st

from atm_withdrawal import average_withdrawal, mask_card, notes_needed


def _valid_amount_text(value):
    return re.fullmatch(r"(?:[0-9]+|[0-9]{1,3}(?:,[0-9]{3})+)", value) is not None


def _valid_card_text(value):
    return re.fullmatch(r"[0-9]+(?:\s+[0-9]+){3}", value.strip()) is not None


def _valid_csv_values(value):
    if not isinstance(value, str) or not value.strip():
        return None
    parts = value.split(",")
    if any(not part.strip().isdecimal() for part in parts):
        return None
    return [int(part.strip()) for part in parts]


# Checks valid formatted amounts and expects malformed values or wrong types to raise ValueError.
@given(st.one_of(st.none(), st.text(), st.integers()))
def test_notes_needed_no_crash(s):
    if isinstance(s, str) and _valid_amount_text(s):
        expected = int(s.replace(",", "")) // 100
        assert notes_needed(s) == expected
    else:
        with pytest.raises(ValueError):
            notes_needed(s)


# Checks that exactly four numeric card groups are masked and invalid cards raise ValueError.
@given(st.one_of(st.none(), st.text(), st.lists(st.text(), min_size=0, max_size=6)))
def test_mask_card_no_crash(s):
    if isinstance(s, list):
        card_number = " ".join(s)
    else:
        card_number = s

    if isinstance(card_number, str) and _valid_card_text(card_number):
        fourth_group = card_number.split()[3]
        assert mask_card(card_number) == "XXXX XXXX XXXX " + fourth_group
    else:
        with pytest.raises(ValueError):
            mask_card(card_number)


# Checks averages for nonnegative CSV/list values and expects empty or invalid data to raise ValueError.
@given(
    st.one_of(
        st.none(),
        st.text(),
        st.lists(st.integers(min_value=-100000, max_value=100000), min_size=0, max_size=8),
    )
)
def test_average_withdrawal_no_crash(s):
    if isinstance(s, list):
        amounts_csv = ",".join(str(amount) for amount in s)
    else:
        amounts_csv = s

    values = _valid_csv_values(amounts_csv)
    if values is not None and all(value >= 0 for value in values):
        assert average_withdrawal(amounts_csv) == sum(values) // len(values)
    else:
        with pytest.raises(ValueError):
            average_withdrawal(amounts_csv)