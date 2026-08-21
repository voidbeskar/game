import pygame
import sys
import random

# Inisialisasi pygame
pygame.init()

# Ukuran layar
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Pygame - Hindari Musuh")

# Warna
PUTIH = (255, 255, 255)
BIRU = (0, 0, 255)
MERAH = (255, 0, 0)
HITAM = (0, 0, 0)

# Kecepatan
PLAYER_SPEED = 5
ENEMY_SPEED = 4

# Pemain
player_size = 40
player_x = WIDTH // 2 - player_size // 2
player_y = HEIGHT - player_size - 10

# Musuh
enemy_size = 40
enemy_x = random.randint(0, WIDTH - enemy_size)
enemy_y = -enemy_size

# Skor
score = 0
font = pygame.font.SysFont("Arial", 24)

# Clock
clock = pygame.time.Clock()

# Fungsi untuk menggambar teks
def draw_text(text, size, color, x, y):
    font_obj = pygame.font.SysFont("Arial", size)
    label = font_obj.render(text, True, color)
    screen.blit(label, (x, y))

# Fungsi deteksi tabrakan
def is_collision(px, py, ex, ey):
    return (px < ex + enemy_size and
            px + player_size > ex and
            py < ey + enemy_size and
            py + player_size > ey)

# Loop utama
running = True
while running:
    clock.tick(60)  # 60 FPS

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Kontrol pemain
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= PLAYER_SPEED
    if keys[pygame.K_RIGHT]:
        player_x += PLAYER_SPEED
    if keys[pygame.K_UP]:
        player_y -= PLAYER_SPEED
    if keys[pygame.K_DOWN]:
        player_y += PLAYER_SPEED

    # Batas layar
    player_x = max(0, min(WIDTH - player_size, player_x))
    player_y = max(0, min(HEIGHT - player_size, player_y))

    # Gerak musuh
    enemy_y += ENEMY_SPEED
    if enemy_y > HEIGHT:
        enemy_y = -enemy_size
        enemy_x = random.randint(0, WIDTH - enemy_size)
        score += 1  # Tambah skor setiap berhasil menghindar

    # Cek tabrakan
    if is_collision(player_x, player_y, enemy_x, enemy_y):
        screen.fill(HITAM)
        draw_text("GAME OVER", 48, PUTIH, WIDTH // 2 - 120, HEIGHT // 2 - 30)
        draw_text(f"Skor: {score}", 36, PUTIH, WIDTH // 2 - 50, HEIGHT // 2 + 20)
        pygame.display.flip()
        pygame.time.delay(2000)
        pygame.quit()
        sys.exit()

    # Gambar background
    screen.fill(PUTIH)

    # Gambar pemain
    pygame.draw.rect(screen, BIRU, (player_x, player_y, player_size, player_size))

    # Gambar musuh
    pygame.draw.rect(screen, MERAH, (enemy_x, enemy_y, enemy_size, enemy_size))

    # Gambar skor
    draw_text(f"Skor: {score}", 24, HITAM, 10, 10)

    # Update layar
    pygame.display.flip()

