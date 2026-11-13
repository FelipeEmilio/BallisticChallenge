def rk4_step(state, dt, derivative):
    """Executa um passo RK4 para um vetor de estado."""
    k1 = derivative(state)
    s2 = [v + 0.5 * dt * k for v, k in zip(state, k1)]
    k2 = derivative(s2)
    s3 = [v + 0.5 * dt * k for v, k in zip(state, k2)]
    k3 = derivative(s3)
    s4 = [v + dt * k for v, k in zip(state, k3)]
    k4 = derivative(s4)

    return [
        value + (dt / 6.0) * (a + 2*b + 2*c + d)
        for value, a, b, c, d in zip(state, k1, k2, k3, k4)
    ]
