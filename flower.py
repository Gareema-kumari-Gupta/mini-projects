import numpy as np
import pygame, math

# ── Constants ──────────────────────────────────────────────────────────────────
WIDTH, HEIGHT = 500, 600
STEM_X = WIDTH // 2
STEM_BASE_Y = HEIGHT - 40

PINK = np.array([255, 182, 193])
GREY = np.array([160, 160, 160])
GREEN = (60, 160, 60)

# ── Pygame setup ───────────────────────────────────────────────────────────────
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("life of a flower")
clock = pygame.time.Clock()

# ── State ──────────────────────────────────────────────────────────────────────
life = 0.0   # 0 = seed, 1 = gone
t    = 0.0   # elapsed time in seconds

# ── Helper math ────────────────────────────────────────────────────────────────
def ease(x):
    """Smoothstep: eases 0->1 with smooth acceleration/deceleration."""
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)

def smooth(life, start, width=0.15):
    """Return how far past `start` life has progressed, clamped to [0,1]."""
    return max(0.0, min(1.0, (life - start) / width))

def mix(a, b, t):
    """Linear interpolate between two numpy colour arrays."""
    return (a * (1 - t) + b * t).astype(int)

# ── Drawing helpers ────────────────────────────────────────────────────────────
def draw_stem(surface, life, t):
    """Wavy green stem that grows upward as life goes from 0 -> 0.4."""
    h = ease(life / 0.4) * 470
    if h < 2:
        return None
    y_vals = np.linspace(0, h, 900)
    x_offsets = 14 * np.sin(y_vals / 80 + t)

    points = [
        (int(STEM_X + x_offsets[i]), int(STEM_BASE_Y - y_vals[i]))
        for i in range(len(y_vals))
    ]
    if len(points) > 1:
        pygame.draw.lines(surface, GREEN, False, points, 3)

    tip_x = int(STEM_X + x_offsets[-1])
    tip_y = int(STEM_BASE_Y - h)
    return tip_x, tip_y

def draw_petals(surface, cx, cy, n, radius, colour):
    """Draw `n` evenly-spaced petals around (cx, cy)."""
    if radius < 1:
        return
    r = tuple(int(c) for c in colour)
    for i in range(n):
        angle = 2 * math.pi * i / n
        px = cx + int(radius * math.cos(angle))
        py = cy + int(radius * 0.6 * math.sin(angle))
        petal_r = max(1, int(radius * 0.45))
        pygame.draw.circle(surface, r, (px, py), petal_r)

def draw_bloom(surface, cx, cy, life):
    """Four rings of petals that open progressively."""
    for ring in range(4):
        open_amt = smooth(life, 0.42 + ring * 0.04)
        n_petals = ring * 6 + 5
        radius   = open_amt * 1.3 * (18 + ring * 12)
        t_mix    = ring / 3
        colour   = mix(PINK, np.array([255, 220, 230]), t_mix)
        draw_petals(surface, cx, cy, n_petals, radius, colour)
    # Centre
    open_amt = smooth(life, 0.42)
    if open_amt > 0:
        pygame.draw.circle(surface, (255, 220, 50), (cx, cy), max(1, int(open_amt * 10)))

def draw_wilt(surface, cx, cy, life):
    """Petals droop and fade to grey after life > 0.75."""
    droop = smooth(life, 0.75)
    if droop == 0:
        return
    colour = mix(PINK, GREY, droop)
    for ring in range(4):
        open_amt = smooth(life, 0.42 + ring * 0.04)
        n_petals = ring * 6 + 5
        base_radius = open_amt * 1.3 * (18 + ring * 12)
        fall_y  = cy + int(droop * 60)
        radius  = base_radius * (1 - droop * 0.5)
        draw_petals(surface, cx, fall_y, n_petals, radius, colour)

def draw(surface, life, tip, t):
    """Master draw call."""
    if tip is None:
        return
    cx, cy = tip
    if life < 0.75:
        draw_bloom(surface, cx, cy, life)
    else:
        draw_wilt(surface, cx, cy, life)

# ── Main loop ──────────────────────────────────────────────────────────────────
running = True
while running:
    dt = clock.tick(60) / 1000.0   # seconds since last frame

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    life += dt / 29
    t    += dt

    screen.fill((0, 0, 0))

    tip = draw_stem(screen, life, t)
    draw(screen, life, tip, t)

    pygame.display.flip()

    if life >= 1.0:
        running = False

pygame.quit()