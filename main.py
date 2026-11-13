
import math
import pygame # type: ignore

from engine.physics import simulate
from game.levels import Level
from interface.hud import draw_hud


# ==========================================
# CONFIGURACOES
# ==========================================

WIDTH = 1100
HEIGHT = 700
FPS = 60

PROJECTILE_ANIMATION_SPEED = 200
MAX_SIMULATION_TIME = 20.0

ANGLE_ADJUST_SPEED = 12.0
POWER_ADJUST_SPEED = 8.0

MIN_ANGLE = 5.0
MAX_ANGLE = 85.0

MIN_POWER = 10.0
MAX_POWER = 100.0

POWER_MULTIPLIER = 11.0


# ==========================================
# PAINEL DE CONFIGURACAO
# ==========================================

PANEL_X = WIDTH - 285
PANEL_Y = 20
PANEL_WIDTH = 265
PANEL_HEIGHT = 135

INPUT_RECTS = {
    "angle": pygame.Rect(PANEL_X + 14, PANEL_Y + 63, 108, 34),
    "power": pygame.Rect(PANEL_X + 143, PANEL_Y + 63, 108, 34)
}


def draw_input_panel(screen, fonts, angle, power, active_field, input_buffers):

    panel = pygame.Rect(
        PANEL_X,
        PANEL_Y,
        PANEL_WIDTH,
        PANEL_HEIGHT
    )

    pygame.draw.rect(
        screen,
        (25, 29, 38),
        panel,
        border_radius=10
    )

    pygame.draw.rect(
        screen,
        (75, 85, 100),
        panel,
        width=1,
        border_radius=10
    )

    # Titulo
    title = fonts["panel_title"].render(
        "CONFIGURACAO DO DISPARO",
        True,
        (235, 240, 245)
    )

    screen.blit(title, (PANEL_X + 14, PANEL_Y + 12))

    # Rotulos
    angle_label = fonts["small"].render(
        "ANGULO",
        True,
        (170, 180, 195)
    )

    power_label = fonts["small"].render(
        "POTENCIA",
        True,
        (170, 180, 195)
    )

    screen.blit(angle_label, (PANEL_X + 14, PANEL_Y + 43))
    screen.blit(power_label, (PANEL_X + 143, PANEL_Y + 43))

    # Valores
    values = {
        "angle": (
            input_buffers["angle"]
            if active_field == "angle"
            else f"{angle:.2f}"
        ),

        "power": (
            input_buffers["power"]
            if active_field == "power"
            else f"{power:.2f}"
        )
    }

    for field, rect in INPUT_RECTS.items():

        selected = active_field == field

        background = (45, 55, 70) if selected else (36, 41, 52)
        border_color = (90, 180, 255) if selected else (85, 95, 110)

        pygame.draw.rect(
            screen,
            background,
            rect,
            border_radius=6
        )

        pygame.draw.rect(
            screen,
            border_color,
            rect,
            width=2 if selected else 1,
            border_radius=6
        )

        value_text = fonts["value"].render(
            values[field],
            True,
            (255, 255, 255)
        )

        screen.blit(
            value_text,
            (rect.x + 10, rect.y + 5)
        )

    # Unidades
    degree = fonts["small"].render(
        "graus",
        True,
        (155, 165, 180)
    )

    percent = fonts["small"].render(
        "%",
        True,
        (155, 165, 180)
    )

    screen.blit(degree, (PANEL_X + 92, PANEL_Y + 102))
    screen.blit(percent, (PANEL_X + 225, PANEL_Y + 102))

    # Instrucao
    hint = fonts["hint"].render(
        "Clique para editar | ENTER confirmar",
        True,
        (145, 155, 170)
    )

    screen.blit(hint, (PANEL_X + 14, PANEL_Y + 119))


# ==========================================
# CONFIRMACAO DOS VALORES
# ==========================================

def commit_input(field, input_buffers, angle, power):

    try:

        text = input_buffers[field].strip().replace(",", ".")

        value = float(text)

        if field == "angle":

            angle = max(
                MIN_ANGLE,
                min(MAX_ANGLE, value)
            )

        elif field == "power":

            power = max(
                MIN_POWER,
                min(MAX_POWER, value)
            )

    except ValueError:
        pass

    input_buffers["angle"] = f"{angle:.2f}"
    input_buffers["power"] = f"{power:.2f}"

    return angle, power


# ==========================================
# DESENHO DA SETA
# ==========================================

def draw_arrowhead(screen, points, color=(30, 50, 70), size=12):

    if len(points) < 2:
        return

    end = points[-1]
    previous = points[-2]

    dx = end[0] - previous[0]
    dy = end[1] - previous[1]

    length = math.hypot(dx, dy)

    if length == 0:
        return

    dx /= length
    dy /= length

    perpendicular_x = -dy
    perpendicular_y = dx

    base_x = end[0] - dx * size
    base_y = end[1] - dy * size

    left = (
        base_x + perpendicular_x * size * 0.5,
        base_y + perpendicular_y * size * 0.5
    )

    right = (
        base_x - perpendicular_x * size * 0.5,
        base_y - perpendicular_y * size * 0.5
    )

    pygame.draw.polygon(
        screen,
        color,
        [end, left, right]
    )


# ==========================================
# LIMITAR TRAJETORIA PROXIMA AO ALVO
# ==========================================

def trim_trajectory_before_target(
    points,
    target_x,
    target_y,
    margin=35
):

    minimum_distance = margin + 22

    for i, point in enumerate(points):

        distance = math.hypot(
            point[0] - target_x,
            point[1] - target_y
        )

        if distance <= minimum_distance and i >= 2:
            return points[:i + 1]

    return points


# ==========================================
# INICIALIZACAO
# ==========================================

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ballistic Challenge")

clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 22)

fonts = {
    "panel_title": pygame.font.SysFont("Arial", 15, bold=True),
    "small": pygame.font.SysFont("Arial", 12),
    "value": pygame.font.SysFont("Arial", 19, bold=True),
    "hint": pygame.font.SysFont("Arial", 10)
}

level = Level(WIDTH, HEIGHT)

angle = 45.0
power = 50.0

input_buffers = {
    "angle": f"{angle:.2f}",
    "power": f"{power:.2f}"
}

active_field = None

projectile = None

message = "Ajuste o angulo e a potencia para acertar o alvo!"

running = True

ground_level = HEIGHT - level.ground_y


# ==========================================
# LOOP PRINCIPAL
# ==========================================

while running:

    dt = clock.tick(FPS) / 1000.0

    # --------------------------------------
    # EVENTOS
    # --------------------------------------

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # Clique nos campos
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            if projectile is None:

                clicked_field = None

                for field, rect in INPUT_RECTS.items():

                    if rect.collidepoint(event.pos):
                        clicked_field = field
                        break

                if clicked_field is not None:

                    active_field = clicked_field

                    # Limpa o campo para receber novo valor
                    input_buffers[active_field] = ""

                elif active_field is not None:

                    if input_buffers[active_field].strip():

                        angle, power = commit_input(
                            active_field,
                            input_buffers,
                            angle,
                            power
                        )

                    else:

                        input_buffers[active_field] = (
                            f"{angle:.2f}" if active_field == "angle"
                            else f"{power:.2f}"
                        )

                    active_field = None

        # ----------------------------------
        # EVENTOS DO TECLADO
        # ----------------------------------

        if event.type == pygame.KEYDOWN:

            # Se estiver editando um campo
            if active_field is not None:

                if event.key == pygame.K_RETURN:

                    if input_buffers[active_field].strip():

                        angle, power = commit_input(
                            active_field,
                            input_buffers,
                            angle,
                            power
                        )

                        active_field = None

                elif event.key == pygame.K_TAB:

                    if input_buffers[active_field].strip():

                        angle, power = commit_input(
                            active_field,
                            input_buffers,
                            angle,
                            power
                        )

                    else:

                        input_buffers[active_field] = (
                            f"{angle:.2f}" if active_field == "angle"
                            else f"{power:.2f}"
                        )

                    active_field = (
                        "power" if active_field == "angle"
                        else "angle"
                    )

                    input_buffers[active_field] = ""

                elif event.key == pygame.K_BACKSPACE:

                    input_buffers[active_field] = (
                        input_buffers[active_field][:-1]
                    )

                elif event.key == pygame.K_ESCAPE:

                    input_buffers["angle"] = f"{angle:.2f}"
                    input_buffers["power"] = f"{power:.2f}"

                    active_field = None

                else:

                    character = event.unicode

                    if character.isdigit():

                        input_buffers[active_field] += character

                    elif character in (".", ","):

                        current_text = input_buffers[active_field]

                        if "." not in current_text and "," not in current_text:
                            input_buffers[active_field] += character

                continue

            # Controles normais
            if event.key == pygame.K_ESCAPE:
                running = False

            # Disparo
            if event.key == pygame.K_SPACE and projectile is None:

                trajectory = simulate(
                    level.cannon_x,
                    level.cannon_y,
                    angle,
                    power * POWER_MULTIPLIER,
                    method="rk4",
                    dt=0.02,
                    max_time=MAX_SIMULATION_TIME,
                    ground_level=ground_level
                )

                projectile = {
                    "points": trajectory,
                    "index": 0
                }

                message = "Projetil disparado!"

    # --------------------------------------
    # CONTROLES PELAS SETAS
    # --------------------------------------

    keys = pygame.key.get_pressed()

    if projectile is None and active_field is None:

        if keys[pygame.K_UP]:
            angle += ANGLE_ADJUST_SPEED * dt

        if keys[pygame.K_DOWN]:
            angle -= ANGLE_ADJUST_SPEED * dt

        if keys[pygame.K_RIGHT]:
            power += POWER_ADJUST_SPEED * dt

        if keys[pygame.K_LEFT]:
            power -= POWER_ADJUST_SPEED * dt

        angle = max(MIN_ANGLE, min(MAX_ANGLE, angle))
        power = max(MIN_POWER, min(MAX_POWER, power))

    # --------------------------------------
    # ATUALIZAR CAMPOS
    # --------------------------------------

    if active_field is None:

        input_buffers["angle"] = f"{angle:.2f}"
        input_buffers["power"] = f"{power:.2f}"

    # --------------------------------------
    # ATUALIZAR PROJETIL
    # --------------------------------------

    if projectile is not None:

        projectile["index"] += max(
            1,
            int(dt * PROJECTILE_ANIMATION_SPEED)
        )

        if projectile["index"] >= len(projectile["points"]):

            final_point = projectile["points"][-1]

            projectile = None

            if level.check_hit(
                final_point[0],
                HEIGHT - final_point[1]
            ):

                message = "Alvo atingido!"

            else:

                message = "Tente novamente!"

    # --------------------------------------
    # DESENHO DO CENARIO
    # --------------------------------------

    screen.fill((135, 190, 230))

    level.draw(screen)

    # --------------------------------------
    # PREVISAO DA TRAJETORIA
    # --------------------------------------

    if projectile is None:

        preview = simulate(
            level.cannon_x,
            level.cannon_y,
            angle,
            power * POWER_MULTIPLIER,
            method="rk4",
            dt=0.04,
            max_time=MAX_SIMULATION_TIME,
            ground_level=ground_level
        )

        if len(preview) > 1:

            points = [
                (int(x), int(HEIGHT - y))
                for x, y, *_ in preview
            ]

            points = trim_trajectory_before_target(
                points,
                level.target_x,
                level.target_y,
                margin=35
            )

            if len(points) > 1:

                pygame.draw.lines(
                    screen,
                    (30, 50, 70),
                    False,
                    points,
                    2
                )

                draw_arrowhead(
                    screen,
                    points,
                    color=(30, 50, 70),
                    size=12
                )

    # --------------------------------------
    # DESENHAR PROJETIL
    # --------------------------------------

    if projectile is not None:

        index = min(
            projectile["index"],
            len(projectile["points"]) - 1
        )

        x, y, *_ = projectile["points"][index]

        pygame.draw.circle(
            screen,
            (35, 35, 35),
            (int(x), int(HEIGHT - y)),
            7
        )

    # --------------------------------------
    # HUD
    # --------------------------------------

    draw_hud(
        screen,
        font,
        angle,
        power,
        message
    )

    # --------------------------------------
    # PAINEL SUPERIOR DIREITO
    # --------------------------------------

    draw_input_panel(
        screen,
        fonts,
        angle,
        power,
        active_field,
        input_buffers
    )

    # --------------------------------------
    # ATUALIZAR TELA
    # --------------------------------------

    pygame.display.flip()


# ==========================================
# FINALIZACAO
# ==========================================

pygame.quit()
