# Ballistic Challenge

Jogo 2D de mira com trajetória calculada por uma engine numérica própria em Python.

## Requisitos
- Python 3.10 ou superior
- pip

## Instalação
No terminal, dentro da pasta do projeto:

```bash
python -m venv .venv
```

Windows:
```bash
.venv\Scripts\activate
```

Linux/macOS:
```bash
source .venv/bin/activate
```

Instale as dependências:
```bash
pip install -r requirements.txt
```

## Executar
```bash
python main.py
```

## Controles
- Seta para cima/baixo: aumenta/diminui o ângulo.
- Seta para direita/esquerda: aumenta/diminui a potência.
- Espaço: dispara.
- Esc: sair.

## Engine numérica
A pasta `engine/` contém implementações próprias dos métodos de Euler e Runge-Kutta de 4ª ordem (RK4). Não são utilizados solvers prontos do SciPy ou NumPy.

## Modelo físico atual
O protótipo considera gravidade constante e resistência do ar desprezada:
- dx/dt = vx
- dy/dt = vy
- dvx/dt = 0
- dvy/dt = -g

As coordenadas matemáticas usam origem no canto inferior esquerdo; a interface converte para o sistema de coordenadas do Pygame.

## Estrutura
- `engine/`: métodos numéricos e modelo físico.
- `game/`: cenário, canhão e alvos.
- `interface/`: elementos visuais e HUD.
- `assets/`: espaço reservado para imagens e sons.

Este é um protótipo inicial para evolução acadêmica. A detecção de colisão é circular e simplificada.
