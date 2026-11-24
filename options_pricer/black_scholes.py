"""Milestone 1: Black-Scholes prices for European calls and puts.

Inputs used everywhere in this project:
    S      spot price of the stock today
    K      strike price
    T      time to expiry in years (e.g. 0.5 = six months)
    r      continuously compounded risk-free rate (0.05 = 5%)
    sigma  volatility of the stock's log returns, per year (0.2 = 20%)
"""

from math import erf, exp, log, sqrt


def norm_cdf(x: float) -> float:
    """Standard normal CDF N(x): the probability a N(0,1) variable is <= x.

    Uses the identity N(x) = (1 + erf(x / sqrt(2))) / 2, so no SciPy needed.
    """
    return 0.5 * (1.0 + erf(x / sqrt(2.0)))


def d1_d2(S: float, K: float, T: float, r: float, sigma: float) -> tuple[float, float]:
    """The two numbers that appear inside every Black-Scholes formula."""
    if S <= 0 or K <= 0 or T <= 0 or sigma <= 0:
        raise ValueError("S, K, T and sigma must all be positive")
    d1 = (log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * sqrt(T))
    d2 = d1 - sigma * sqrt(T)
    return d1, d2


def call_price(S: float, K: float, T: float, r: float, sigma: float) -> float:
    """European call: C = S N(d1) - K e^{-rT} N(d2)."""
    d1, d2 = d1_d2(S, K, T, r, sigma)
    return S * norm_cdf(d1) - K * exp(-r * T) * norm_cdf(d2)


def put_price(S: float, K: float, T: float, r: float, sigma: float) -> float:
    """European put: P = K e^{-rT} N(-d2) - S N(-d1)."""
    d1, d2 = d1_d2(S, K, T, r, sigma)
    return K * exp(-r * T) * norm_cdf(-d2) - S * norm_cdf(-d1)


def put_call_parity_gap(S: float, K: float, T: float, r: float, sigma: float) -> float:
    """C - P - (S - K e^{-rT}). Should be ~0: parity holds for any model with no arbitrage."""
    return call_price(S, K, T, r, sigma) - put_price(S, K, T, r, sigma) - (S - K * exp(-r * T))
