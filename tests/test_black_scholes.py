from math import exp

import pytest

from options_pricer.black_scholes import call_price, norm_cdf, put_call_parity_gap, put_price

# Textbook example (e.g. Hull): S=100, K=100, T=1, r=5%, sigma=20%
S, K, T, R, SIGMA = 100.0, 100.0, 1.0, 0.05, 0.20


def test_norm_cdf_known_values():
    assert norm_cdf(0.0) == pytest.approx(0.5)
    assert norm_cdf(1.96) == pytest.approx(0.975, abs=1e-4)


def test_known_prices():
    assert call_price(S, K, T, R, SIGMA) == pytest.approx(10.4506, abs=1e-4)
    assert put_price(S, K, T, R, SIGMA) == pytest.approx(5.5735, abs=1e-4)


@pytest.mark.parametrize("strike", [60.0, 90.0, 100.0, 110.0, 150.0])
def test_put_call_parity(strike):
    assert put_call_parity_gap(S, strike, T, R, SIGMA) == pytest.approx(0.0, abs=1e-10)


def test_price_bounds():
    # A call is worth at least its discounted intrinsic value and at most the stock.
    c = call_price(S, K, T, R, SIGMA)
    assert max(S - K * exp(-R * T), 0.0) <= c <= S


def test_deep_in_the_money_call_approaches_forward_value():
    assert call_price(S, 10.0, T, R, SIGMA) == pytest.approx(S - 10.0 * exp(-R * T), abs=1e-8)


def test_bad_inputs_raise():
    with pytest.raises(ValueError):
        call_price(S, K, 0.0, R, SIGMA)
