
import math

from engine.euler import euler_step
from engine.runge_kutta import rk4_step


# Gravidade na escala de pixels do jogo
GRAVITY = 300.0


def derivatives(state):
    """
    Calcula as derivadas do estado:
    [x, y, vx, vy]
    """

    x, y, vx, vy = state

    return [
        vx,
        vy,
        0.0,
        -GRAVITY
    ]


def simulate(
    x0,
    y0,
    angle_degrees,
    speed,
    method="rk4",
    dt=0.02,
    max_time=20.0,
    ground_level=0.0
):
    """
    Simula a trajetoria do projetil utilizando Euler ou RK4.

    Estado:
    [x, y, vx, vy]

    A simulacao termina quando o projetil toca o solo
    ou quando atinge o tempo maximo.
    """

    angle = math.radians(angle_degrees)

    state = [
        float(x0),
        float(y0),
        speed * math.cos(angle),
        speed * math.sin(angle)
    ]

    points = [state[:]]

    steps = int(max_time / dt)

    method = method.lower()

    if method == "rk4":
        stepper = rk4_step

    elif method == "euler":
        stepper = euler_step

    else:
        raise ValueError(
            "Metodo invalido. Utilize 'rk4' ou 'euler'."
        )

    for _ in range(steps):

        state = stepper(state, dt, derivatives)

        points.append(state[:])

        # Verifica se o projetil tocou o solo
        if state[1] <= ground_level:
            break

    return points
