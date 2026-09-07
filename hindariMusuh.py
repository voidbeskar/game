import pygame
import sys
import random
import math

# Inisialisasi Pygame
pygame.init()

# Ukuran Layar
WIDTH, HEIGHT = 650, 550
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Visual Effects & Enemy Variety Demo")

# Warna
BACKGROUND = (15, 15, 25)
PLAYER_COLOR = (0, 255, 200)
TEXT_COLOR = (255, 255, 255)

# Tipe Musuh (Warna, Ukuran, Kecepatan, Skor)
ENEMY_TYPES = {
    "BIASA": {"color": (255, 60, 60), "size": 35, "speed": 5, "score": 1},
    "CEPAT": {"color": (255, 220, 0), "size": 22, "speed": 8, "score": 2},
    "RAKSASA": {"color": (170, 50, 255), "size": 65, "speed": 3, "score": 3}
}

FPS = 60
clock = pygame.time.Clock()

FONT_LARGE = pygame.font.SysFont("Arial", 44, bold=True)
FONT_MEDIUM = pygame.font.SysFont("Arial", 24, bold=True)


class Particle:
    """Sistem Partikel untuk Ledakan Visual"""
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        angle = random.uniform(0, math.pi * 2)
        speed = random.uniform(2, 7)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.size = random.randint(4, 8)
        self.lifetime = 30  # Frame hidup

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 1
        self.size = max(0, self.size - 0.2)

    def draw(self, surface, offset_x=0, offset_y=0):
        if self.lifetime > 0 and self.size > 0:
            pygame.draw.circle(
                surface, 
                self.color, 
                (int(self.x + offset_x), int(self.y + offset_y)), 
                int(self.size)
            )


class Enemy:
    """Kelas untuk Mengelola Musuh Bervariasi"""
    def __init__(self):
        self.reset()

    def reset(self):
        # Memilih tipe musuh secara acak berdasarkan bobot peluang
        types = ["BIASA", "CEPAT", "RAKSASA"]
        weights = [0.6, 0.25, 0.15]  # 60% biasa, 25% cepat, 15% raksasa
        self.type_name = random.choices(types, weights=weights)[0]
        
        spec = ENEMY_TYPES[self.type_name]
        self.color = spec["color"]
        self.size = spec["size"]
        self.speed = spec["speed"]
        self.score_value = spec["score"]

        self.rect = pygame.Rect(
            random.randint(0, WIDTH - self.size),
            -random.randint(50, 200),
            self.size,
            self.size
        )

    def update(self):
        self.rect.y += self.speed

    def draw(self, surface, offset_x=0, offset_y=0):
        draw_rect = self.rect.move(offset_x, offset_y)
        pygame.draw.rect(surface, self.color, draw_rect, border_radius=6)


def main():
    player_size = 35
    player = pygame.Rect(WIDTH // 2 - player_size // 2, HEIGHT - 70, player_size, player_size)
    player_speed = 6
    
    # Simpan posisi terdahulu untuk efek bayangan/trail
    trail_positions = []

    # Buat daftar musuh
    enemies = [Enemy() for _ in range(4)]

    particles = []
    score = 0
    shake_time = 0  # Durasi efek guncangan layar
    game_over = False

    while True:
        clock.tick(FPS)

        # Efek Screen Shake (Guncangan Layar)
        offset_x = 0
        offset_y = 0
        if shake_time > 0:
            shake_time -= 1
            offset_x = random.randint(-8, 8)
            offset_y = random.randint(-8, 8)

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if game_over and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main()  # Restart Game

        if not game_over:
            # Controls
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                player.x -= player_speed
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                player.x += player_speed
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                player.y -= player_speed
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                player.y += player_speed

            player.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

            # Rekam jejak pemain untuk efek Motion Trail
            trail_positions.append(player.copy())
            if len(trail_positions) > 8:  # Panjang jejak
                trail_positions.pop(0)

            # Pergerakan & Logika Musuh
            for enemy in enemies:
                enemy.update()

                # Jika musuh lewat bawah layar
                if enemy.rect.y > HEIGHT:
                    score += enemy.score_value
                    enemy.reset()

                # Deteksi Tabrakan
                if player.colliderect(enemy.rect):
                    shake_time = 20  # Pemicu Screen Shake
                    # Ledakan partikel sesuai warna musuh
                    for _ in range(40):
                        particles.append(Particle(player.centerx, player.centery, enemy.color))
                    game_over = True

        # --- DRAWING / RENDER ---
        screen.fill(BACKGROUND)

        # 1. Gambar Motion Trail Pemain
        for i, pos in enumerate(trail_positions):
            alpha = int((i + 1) * (255 / len(trail_positions)) * 0.3)
            trail_surface = pygame.Surface((player_size, player_size), pygame.SRCALPHA)
            trail_color = (*PLAYER_COLOR, alpha)
            pygame.draw.rect(trail_surface, trail_color, (0, 0, player_size, player_size), border_radius=6)
            screen.blit(trail_surface, (pos.x + offset_x, pos.y + offset_y))

        # 2. Gambar Pemain
        if not game_over:
            draw_player = player.move(offset_x, offset_y)
            pygame.draw.rect(screen, PLAYER_COLOR, draw_player, border_radius=6)

        # 3. Gambar Musuh
        for enemy in enemies:
            enemy.draw(screen, offset_x, offset_y)

        # 4. Gambar & Update Partikel
        for p in particles[:]:
            p.update()
            p.draw(screen, offset_x, offset_y)
            if p.lifetime <= 0:
                particles.remove(p)

        # 5. UI & Game Over
        if not game_over:
            score_txt = FONT_MEDIUM.render(f"Skor: {score}", True, TEXT_COLOR)
            screen.blit(score_txt, (15, 15))
        else:
            over_txt = FONT_LARGE.render("GAME OVER", True, (255, 60, 60))
            score_txt = FONT_MEDIUM.render(f"Skor Akhir: {score}", True, TEXT_COLOR)
            restart_txt = FONT_MEDIUM.render("Tekan [R] untuk Restart", True, PLAYER_COLOR)

            screen.blit(over_txt, (WIDTH // 2 - over_txt.get_width() // 2, HEIGHT // 2 - 60))
            screen.blit(score_txt, (WIDTH // 2 - score_txt.get_width() // 2, HEIGHT // 2))
            screen.blit(restart_txt, (WIDTH // 2 - restart_txt.get_width() // 2, HEIGHT // 2 + 50))

        pygame.display.flip()


if __name__ == "__main__":
    main()