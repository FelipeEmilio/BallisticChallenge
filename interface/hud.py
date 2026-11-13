import pygame # type: ignore

def draw_hud(screen, font, angle, power, message):
    color = (20, 25, 35)
    lines = [
        f"Angulo: {angle:.2f} graus   Potencia: {power:.2f}%",
        "Setas: ajustar | ESPACO: disparar | ESC: sair",
        message
    ]
    y = 18
    for line in lines:
        surface = font.render(line, True, color)
        screen.blit(surface, (20, y))
        y += 30
