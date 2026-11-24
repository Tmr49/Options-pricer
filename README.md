# Options Pricer

A small, readable options pricer in Python, built in four milestones. The goal is to understand every formula, not to cover everything.

| Milestone | What | Status |
|---|---|---|
| M1 | Black-Scholes call and put prices, put-call parity check | Done |
| M2 | Greeks (delta, gamma, vega, theta, rho), checked by finite differences | Planned |
| M3 | Binomial tree (European and American), convergence to Black-Scholes | Planned |
| M4 | Implied volatility (Newton's method with bisection fallback) | Planned |
| Optional | Volatility smile/surface from real option prices; Monte Carlo pricer | Maybe later |

Each milestone has a step-by-step learning walkthrough in [`docs/learn/`](docs/learn/) (theory, code line by line, exercises).

## Quick start

```bash
pip install -r requirements.txt
python example.py      # prints a call and put price
python -m pytest -q    # runs the tests
```

## M1: Black-Scholes

### The setup

A European call gives the right to buy a stock at strike $K$ on date $T$; it pays $\max(S_T - K, 0)$. A put pays $\max(K - S_T, 0)$.

Black-Scholes assumes the stock follows geometric Brownian motion,

$$dS_t = \mu S_t\,dt + \sigma S_t\,dW_t,$$

that you can trade continuously with no costs, and that there is a constant risk-free rate $r$. The key idea: you can hedge the option perfectly with the stock, so its price cannot depend on $\mu$ (the stock's expected return). We may therefore price as if every asset earns $r$ (the *risk-neutral* world) and discount the expected payoff:

$$C = e^{-rT}\,\mathbb{E}^{\mathbb{Q}}\left[\max(S_T - K, 0)\right].$$

Under that measure $\ln S_T$ is normal with mean $\ln S + (r - \tfrac12\sigma^2)T$ and variance $\sigma^2 T$. Working out the expectation gives the formulas below.

### The formulas

$$d_1 = \frac{\ln(S/K) + (r + \tfrac12\sigma^2)T}{\sigma\sqrt{T}}, \qquad d_2 = d_1 - \sigma\sqrt{T}$$

$$C = S\,N(d_1) - K e^{-rT} N(d_2)$$

$$P = K e^{-rT} N(-d_2) - S\,N(-d_1)$$

$N(\cdot)$ is the standard normal CDF. How to read them:

- $N(d_2)$ is the risk-neutral probability that the call finishes in the money.
- $K e^{-rT} N(d_2)$ is the present value of paying the strike, weighted by that probability.
- $S\,N(d_1)$ is the present value of receiving the stock when the option is exercised. $N(d_1)$ is also the call's delta (M2).

### Put-call parity

Owning a call and selling a put with the same $K$ and $T$ pays $S_T - K$ in every case, which is exactly a forward contract. So with no arbitrage,

$$C - P = S - K e^{-rT}.$$

This holds for *any* model, so it is a good check on the code. `put_call_parity_gap` computes $C - P - (S - Ke^{-rT})$, and the tests check it is zero to 10 decimal places.

### The code

`options_pricer/black_scholes.py`:

- `norm_cdf(x)` computes $N(x) = \tfrac12\left(1 + \operatorname{erf}(x/\sqrt2)\right)$ with the standard library, so there is no SciPy dependency.
- `d1_d2(...)` computes $d_1, d_2$ and rejects non-positive inputs.
- `call_price`, `put_price` are the two formulas above, line for line.
- `put_call_parity_gap` is the parity check.

### Tests

`tests/test_black_scholes.py` checks:

1. Known values: with $S=K=100$, $T=1$, $r=5\%$, $\sigma=20\%$, the call is 10.4506 and the put 5.5735 (the standard textbook example).
2. Put-call parity across strikes from 60 to 150.
3. No-arbitrage bounds: $\max(S - Ke^{-rT}, 0) \le C \le S$.
4. A deep in-the-money call is worth $S - Ke^{-rT}$ (it will almost surely be exercised).
5. Bad inputs raise an error.

### Questions to be able to answer

- Why doesn't the stock's expected return $\mu$ appear in the formula?
- What happens to $C$ as $\sigma \to 0$? As $T \to \infty$?
- Why does put-call parity hold without any model assumptions?
