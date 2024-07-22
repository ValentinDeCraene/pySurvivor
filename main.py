import pygame
import sys
import math
import random

# Initialisation de PyGame
pygame.init()

# Dimensions de la fenêtre de jeu
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Vampire Survivor Like")

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (100, 100, 100)

# Horloge pour contrôler le taux de rafraîchissement
clock = pygame.time.Clock()
FPS = 60  # Frames per second

# Classe Joueur
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.speed = 10  # Augmenter la vitesse
        self.health = 100
        self.direction = 'right'  # Direction initiale
        self.weapon = Weapon(self)
        self.experience = 0
        self.max_experience = 100
        self.level = 1

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
            self.direction = 'left'
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed
            self.direction = 'right'
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
            self.direction = 'up'
        if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed
            self.direction = 'down'

        self.weapon.update()

        # Collecter les orbes
        hit_orbs = pygame.sprite.spritecollide(self, orbs, True)
        for orb in hit_orbs:
            self.experience += orb.value
            if self.experience >= self.max_experience:
                self.level_up()

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()  # Supprime le joueur s'il n'a plus de points de vie

    def draw_health_bar(self, screen):
        health_bar_length = 100
        health_ratio = self.health / 100
        pygame.draw.rect(screen, RED, (10, 10, health_bar_length, 10))
        pygame.draw.rect(screen, GREEN, (10, 10, health_bar_length * health_ratio, 10))

    def draw_experience_bar(self, screen):
        experience_bar_length = 100
        experience_ratio = self.experience / self.max_experience
        pygame.draw.rect(screen, BLUE, (10, 30, experience_bar_length, 10))
        pygame.draw.rect(screen, GREEN, (10, 30, experience_bar_length * experience_ratio, 10))

    def level_up(self):
        self.experience -= self.max_experience
        self.level += 1
        self.weapon.damage *= 3  # Doubler les dégâts
        self.max_experience = int(self.max_experience * 1.2)  # Augmenter la quantité d'expérience nécessaire pour le prochain niveau

    def draw_level(self, screen):
        font = pygame.font.Font(None, 36)
        level_text = font.render(f"Level: {self.level}", True, WHITE)
        screen.blit(level_text, (10, 50))

# Classe Ennemi
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(0, WIDTH), random.randint(0, HEIGHT))
        self.speed = 4  # Augmenter la vitesse
        self.health = 50

    def update(self):
        # Mouvement vers le joueur
        dx, dy = player.rect.x - self.rect.x, player.rect.y - self.rect.y
        dist = math.hypot(dx, dy)
        dx, dy = dx / dist, dy / dist  # Normalisation
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()  # Supprime l'ennemi s'il n'a plus de points de vie
            global enemies_killed
            enemies_killed += 1  # Augmenter le compteur d'ennemis tués
            create_orb(self.rect.center)  # Créer une orbe à la position de l'ennemi

    def draw_health_bar(self, screen):
        health_bar_length = 50
        health_ratio = self.health / 50
        pygame.draw.rect(screen, RED, (self.rect.x, self.rect.y - 10, health_bar_length, 5))
        pygame.draw.rect(screen, GREEN, (self.rect.x, self.rect.y - 10, health_bar_length * health_ratio, 5))

# Classe Orbe
class Orb(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.value = 10

# Classe Arme
class Weapon(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.player = player
        self.image = pygame.Surface((60, 20))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.damage = 10

    def update(self):
        # Positionner l'épée en fonction de la direction du joueur
        if self.player.direction == 'right':
            self.image = pygame.transform.rotate(pygame.Surface((60, 20)), 0)
            self.image.fill(BLUE)
            self.rect = self.image.get_rect()
            self.rect.midleft = self.player.rect.midright
        elif self.player.direction == 'left':
            self.image = pygame.transform.rotate(pygame.Surface((60, 20)), 180)
            self.image.fill(BLUE)
            self.rect = self.image.get_rect()
            self.rect.midright = self.player.rect.midleft
        elif self.player.direction == 'up':
            self.image = pygame.transform.rotate(pygame.Surface((60, 20)), 90)
            self.image.fill(BLUE)
            self.rect = self.image.get_rect()
            self.rect.midbottom = self.player.rect.midtop
        elif self.player.direction == 'down':
            self.image = pygame.transform.rotate(pygame.Surface((60, 20)), -90)
            self.image.fill(BLUE)
            self.rect = self.image.get_rect()
            self.rect.midtop = self.player.rect.midbottom

        # Vérifier les collisions avec les ennemis
        hit_enemies = pygame.sprite.spritecollide(self, enemies, False)
        for enemy in hit_enemies:
            enemy.take_damage(self.damage)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

def draw_button(screen, text, pos, size):
    font = pygame.font.Font(None, size)
    button_text = font.render(text, True, WHITE)
    button_rect = button_text.get_rect(center=pos)
    pygame.draw.rect(screen, GRAY, button_rect.inflate(20, 20))
    screen.blit(button_text, button_rect)
    return button_rect

def reset_game():
    global all_sprites, enemies, orbs, player, game_over, victory, enemies_killed, enemy_spawn_timer
    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    orbs = pygame.sprite.Group()
    player = Player()
    all_sprites.add(player)

    game_over = False
    victory = False
    enemies_killed = 0
    enemy_spawn_timer = pygame.USEREVENT + 1
    pygame.time.set_timer(enemy_spawn_timer, 2000)  # Apparaître un ennemi toutes les 2 secondes

def create_enemy():
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

def create_orb(pos):
    orb = Orb(pos)
    all_sprites.add(orb)
    orbs.add(orb)

# Initialisation des groupes de sprites et des variables de jeu
reset_game()

# Boucle principale
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        if event.type == enemy_spawn_timer and not game_over:
            create_enemy()

    if not game_over:
        # Mise à jour des sprites
        all_sprites.update()

        # Vérifier les collisions et appliquer les dégâts
        for enemy in enemies:
            if pygame.sprite.collide_rect(player, enemy):
                player.take_damage(1)

        # Vérifier si le joueur est vaincu
        if player.health <= 0:
            game_over = True
            victory = False
            defeat_text = pygame.font.Font(None, 74).render("Defeat!", True, RED)

        # Vérifier si le joueur a vaincu 20 ennemis
        if enemies_killed >= 20:
            game_over = True
            victory = True
            victory_text = pygame.font.Font(None, 74).render("Victory!", True, GREEN)

        # Remplir l'écran avec une couleur
        screen.fill(BLACK)

        # Dessiner tous les sprites
        all_sprites.draw(screen)

        # Dessiner les barres de vie et d'expérience
        player.draw_health_bar(screen)
        player.draw_experience_bar(screen)
        player.draw_level(screen)
        for enemy in enemies:
            enemy.draw_health_bar(screen)

        # Dessiner l'arme
        player.weapon.draw(screen)
    else:
        # Afficher l'écran de victoire ou de défaite
        screen.fill(BLACK)
        if victory:
            screen.blit(victory_text, (WIDTH // 2 - victory_text.get_width() // 2, HEIGHT // 2 - victory_text.get_height() // 2 - 100))
        else:
            screen.blit(defeat_text, (WIDTH // 2 - defeat_text.get_width() // 2, HEIGHT // 2 - defeat_text.get_height() // 2 - 100))

        restart_button = draw_button(screen, "Restart", (WIDTH // 2, HEIGHT // 2 + 50), 50)

        # Vérifier les clics de souris et la touche ESC
        mouse_pressed = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        if mouse_pressed[0] and restart_button.collidepoint(mouse_pos):
            reset_game()
        elif pygame.key.get_pressed()[pygame.K_ESCAPE]:
            running = False

    # Mettre à jour l'écran
    pygame.display.flip()

    # Contrôle du taux de rafraîchissement
    clock.tick(FPS)

pygame.quit()
sys.exit()
