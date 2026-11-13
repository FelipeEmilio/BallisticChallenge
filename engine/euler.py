def euler_step(state, dt, derivative):
    """Executa um passo do metodo de Euler explicito."""
    rates = derivative(state)
    return [value + dt * rate for value, rate in zip(state, rates)]
