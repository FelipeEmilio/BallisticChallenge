
import math
import pygame # type: ignore


class Level:

    def __init__(self, width, height):

        self.width = width
        self.height = height

        # Altura do terreno
        self.ground_y = height - 70

        # Posicao do canhao
        self.cannon_x = 95
        self.cannon_screen_y = self.ground_y - 18

        # Coordenadas utilizadas pela engine fisica
        self.cannon_y = height - self.cannon_screen_y

        # Configuracoes do alvo
        self.target_radius = 22
        self.reset_target()

        # Cores do cenario
        self.sky_top = (65, 54, 91)
        self.sky_bottom = (245, 139, 91)

    def reset_target(self):

        self.target_x = self.width - 150
        self.target_y = self.ground_y - 22

    def draw_background(self, screen):
        """Desenha o ceu e o ambiente do por do sol."""

        # Ceu com gradiente
        for y in range(self.height):

            ratio = y / self.height

            r = int(
                self.sky_top[0] * (1 - ratio)
                + self.sky_bottom[0] * ratio
            )

            g = int(
                self.sky_top[1] * (1 - ratio)
                + self.sky_bottom[1] * ratio
            )

            b = int(
                self.sky_top[2] * (1 - ratio)
                + self.sky_bottom[2] * ratio
            )

            pygame.draw.line(
                screen,
                (r, g, b),
                (0, y),
                (self.width, y)
            )

        # Sol
        sun_x = self.width - 260
        sun_y = 210

        pygame.draw.circle(
            screen,
            (255, 190, 120),
            (sun_x, sun_y),
            65
        )

        pygame.draw.circle(
            screen,
            (255, 218, 158),
            (sun_x, sun_y),
            48
        )

        # Montanhas ao fundo
        pygame.draw.polygon(
            screen,
            (91, 73, 94),
            [
                (0, 430),
                (170, 285),
                (310, 410),
                (470, 270),
                (650, 420),
                (820, 300),
                (WIDTH if False else self.width, 420),
                (self.width, self.ground_y),
                (0, self.ground_y)
            ]
        )

        # Montanhas intermediarias
        pygame.draw.polygon(
            screen,
            (75, 66, 78),
            [
                (0, 480),
                (210, 365),
                (390, 455),
                (590, 345),
                (790, 460),
                (960, 350),
                (self.width, 445),
                (self.width, self.ground_y),
                (0, self.ground_y)
            ]
        )

        # Silhuetas de vegetacao distante
        pygame.draw.polygon(
            screen,
            (57, 65, 62),
            [
                (0, 510),
                (130, 450),
                (260, 510),
                (420, 465),
                (600, 520),
                (790, 470),
                (980, 515),
                (self.width, 485),
                (self.width, self.ground_y),
                (0, self.ground_y)
            ]
        )

    def draw_ground(self, screen):
        """Desenha o terreno e seus detalhes."""

        # Base do terreno
        pygame.draw.rect(
            screen,
            (61, 65, 48),
            (
                0,
                self.ground_y,
                self.width,
                self.height - self.ground_y
            )
        )

        # Camada superior da grama
        pygame.draw.line(
            screen,
            (119, 111, 65),
            (0, self.ground_y),
            (self.width, self.ground_y),
            5
        )

        # Detalhes de vegetacao
        for x in range(15, self.width, 35):

            pygame.draw.line(
                screen,
                (91, 113, 65),
                (x, self.ground_y),
                (x - 4, self.ground_y - 7),
                2
            )

            pygame.draw.line(
                screen,
                (91, 113, 65),
                (x, self.ground_y),
                (x + 4, self.ground_y - 5),
                2
            )

    def draw_cannon(self, screen, angle):
        """Desenha um canhao metalico com rodas e tubo giratorio."""

        pivot_x = self.cannon_x
        pivot_y = self.cannon_screen_y

        angle_rad = math.radians(angle)

        barrel_length = 58

        end_x = pivot_x + math.cos(angle_rad) * barrel_length
        end_y = pivot_y - math.sin(angle_rad) * barrel_length

        # Sombra do canhao
        pygame.draw.ellipse(
            screen,
            (42, 43, 38),
            (pivot_x - 42, self.ground_y - 12, 90, 18)
        )

        # Rodas
        for wheel_x in (pivot_x - 17, pivot_x + 19):

            pygame.draw.circle(
                screen,
                (35, 35, 39),
                (wheel_x, pivot_y + 9),
                17
            )

            pygame.draw.circle(
                screen,
                (104, 79, 59),
                (wheel_x, pivot_y + 9),
                12
            )

            pygame.draw.circle(
                screen,
                (48, 48, 49),
                (wheel_x, pivot_y + 9),
                5
            )

        # Estrutura inferior
        pygame.draw.polygon(
            screen,
            (76, 64, 55),
            [
                (pivot_x - 29, pivot_y - 8),
                (pivot_x + 29, pivot_y - 8),
                (pivot_x + 21, pivot_y + 12),
                (pivot_x - 22, pivot_y + 12)
            ]
        )

        # Tubo principal
        pygame.draw.line(
            screen,
            (35, 39, 43),
            (pivot_x, pivot_y),
            (int(end_x), int(end_y)),
            18
        )

        # Reflexo metalico do tubo
        pygame.draw.line(
            screen,
            (105, 112, 112),
            (pivot_x + 2, pivot_y - 5),
            (int(end_x - 3), int(end_y - 5)),
            4
        )

        # Boca do canhao
        pygame.draw.circle(
            screen,
            (27, 29, 33),
            (int(end_x), int(end_y)),
            10
        )

        pygame.draw.circle(
            screen,
            (115, 119, 117),
            (int(end_x), int(end_y)),
            7,
            2
        )

        # Articulacao central
        pygame.draw.circle(
            screen,
            (145, 119, 83),
            (pivot_x, pivot_y),
            13
        )

        pygame.draw.circle(
            screen,
            (45, 47, 49),
            (pivot_x, pivot_y),
            8
        )

    def draw_target(self, screen):
        """Desenha o alvo."""

        # Sombra
        pygame.draw.ellipse(
            screen,
            (42, 43, 38),
            (
                self.target_x - 25,
                self.ground_y - 5,
                50,
                12
            )
        )

        # Corpo do alvo
        pygame.draw.circle(
            screen,
            (111, 43, 37),
            (self.target_x, self.target_y),
            self.target_radius
        )

        pygame.draw.circle(
            screen,
            (218, 194, 151),
            (self.target_x, self.target_y),
            15
        )

        pygame.draw.circle(
            screen,
            (160, 55, 44),
            (self.target_x, self.target_y),
            9
        )

        pygame.draw.circle(
            screen,
            (245, 217, 153),
            (self.target_x, self.target_y),
            3
        )

    def draw(self, screen, angle=22.0):
        """Desenha todos os elementos do cenario."""

        self.draw_background(screen)
        self.draw_ground(screen)
        self.draw_target(screen)
        self.draw_cannon(screen, angle)

    def check_hit(self, x, y_screen):
        """Verifica colisao entre o projetil e o alvo."""

        dx = x - self.target_x
        dy = y_screen - self.target_y

        return (
            dx * dx + dy * dy
            <= self.target_radius ** 2
        )
