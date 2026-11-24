"""Run: python example.py"""
from options_pricer.black_scholes import call_price, put_call_parity_gap, put_price

S, K, T, r, sigma = 100.0, 100.0, 1.0, 0.05, 0.20
print(f"Call: {call_price(S, K, T, r, sigma):.4f}")
print(f"Put:  {put_price(S, K, T, r, sigma):.4f}")
print(f"Put-call parity gap: {put_call_parity_gap(S, K, T, r, sigma):.2e}")
