# Pessoal, este e o lingo do tutotrial do do jogo original:
# https://coderslegacy.com/python/pygame-platformer-game/

import pygame
from pygame.locals import *
import sys
import random
import time
 
pygame.init()
vec = pygame.math.Vector2 #2 for two dimensional
 
HEIGHT = 450
WIDTH = 400
ACC = 0.5
FRIC = -0.12
FPS = 60
 
FramePerSec = pygame.time.Clock()
 
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("LuizDi-Game - AthenasArch Version")

background = pygame.image.load("assets/images/background/background.png")
 
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Carrega a imagem do jogador
        self.surf = pygame.image.load("assets/images/Luiz/luiz.png")
        # Obtém o retângulo da imagem do jogador
        self.rect = self.surf.get_rect()

        # Inicializa a posição, velocidade e aceleração do jogador
        self.pos = vec((10, 360))
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.jumping = False
        self.score = 0

    def move(self):
        self.acc = vec(0, 0.5)

        # Verifica as teclas pressionadas
        pressed_keys = pygame.key.get_pressed()

        # Atualiza a aceleração com base nas teclas pressionadas
        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC
        if pressed_keys[K_RIGHT]:
            self.acc.x = ACC

        # Atualiza a aceleração, velocidade e posição do jogador
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        # Mantém o jogador dentro dos limites da tela
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        # Atualiza a posição do retângulo do jogador
        self.rect.midbottom = self.pos

    def jump(self):
        # Toca o som do pulo
        pygame.mixer.Sound('assets/audio/jump.wav').play()
        # Verifica se o jogador está colidindo com uma plataforma
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = -15

    def cancel_jump(self):
        # Cancela o pulo se o jogador soltar a tecla de espaço
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3

    def update(self):
        # Verifica colisões com as plataformas
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if self.vel.y > 0:
            if hits:
                # Se o jogador estiver acima da plataforma, ajusta a posição e a velocidade
                if self.pos.y < hits[0].rect.bottom:
                    if hits[0].point == True:
                        hits[0].point = False
                        self.score += 1
                    self.pos.y = hits[0].rect.top + 1
                    self.vel.y = 0
                    self.jumping = False


class Coin(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        self.image = pygame.image.load("assets/images/icons/Coin.png")
        self.rect = self.image.get_rect()

        self.rect.topleft = pos

    def update(self):
        if self.rect.colliderect(P1.rect):
            P1.score += 5
            self.kill()
 
 
class platform(pygame.sprite.Sprite):
    def __init__(self, width=0, height=18):
        super().__init__()

        # Define a largura da plataforma e carrega a imagem
        if width == 0:
            width = random.randint(50, 120)

        self.image = pygame.image.load("assets/images/icons/platform.png")
        # Redimensiona a imagem e obtém o retângulo
        self.surf = pygame.transform.scale(self.image, (width, height))
        self.rect = self.surf.get_rect(center=(random.randint(0, WIDTH-10),
                                               random.randint(0, HEIGHT-30)))

        self.point = True
        self.moving = True
        self.speed = random.randint(-1, 1)

        # Verifica se a plataforma está se movendo
        if self.speed == 0:
            self.moving == False

    def move(self):
        # Verifica a colisão entre a plataforma e o jogador
        hits = self.rect.colliderect(P1.rect)
        if self.moving == True:
            # Move a plataforma horizontalmente
            self.rect.move_ip(self.speed, 0)
            # Move o jogador junto com a plataforma
            if hits:
                P1.pos += (self.speed, 0)
            # Loop das plataformas na tela
            if self.speed > 0 and self.rect.left > WIDTH:
                self.rect.right = 0
            if self.speed < 0 and self.rect.right < 0:
                self.rect.left = WIDTH

    def generateCoin(self):
        # Gera uma moeda se a plataforma não estiver se movendo
        if self.speed == 0:
            coins.add(Coin((self.rect.centerx, self.rect.centery - 50)))


# Função para verificar a colisão entre plataformas
def check_collision(platform, groupies):
    if pygame.sprite.spritecollideany(platform, groupies):
        return True
    else:
        for entity in groupies:
            if entity == platform:
                continue
            # Verifica a colisão entre a parte superior e inferior das plataformas
            if (abs(platform.rect.top - entity.rect.bottom) < 40) and (abs(platform.rect.bottom - entity.rect.top) < 40):
                return True
        return False

 
def generate_platforms():
    # Gere plataformas enquanto houver menos de 6 plataformas no jogo
    while len(platforms) < 6:
        # Escolha uma largura aleatória para a plataforma
        width = random.randrange(50, 100)
        p = None
        collision = True

        # Continue gerando plataformas até que não haja colisão com outras plataformas existentes
        while collision:
            p = platform()
            p.rect.center = (random.randrange(0, WIDTH - width),
                             random.randrange(-50, 0))
            collision = check_collision(p, platforms)

        # Gere uma moeda na plataforma e adicione a plataforma aos grupos de sprites
        p.generateCoin()
        platforms.add(p)
        all_sprites.add(p)

def game_loop():
    while True:
        P1.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    P1.jump()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    P1.cancel_jump()

        # Verifica se o jogador caiu
        if P1.rect.top > HEIGHT:
            # Toca o som da morte do jogador
            pygame.mixer.Sound("assets/audio/aiai.wav").play()

            # Aguarda 1 segundo e exibe a tela vermelha
            time.sleep(1)
            displaysurface.fill((255, 0, 0))
            pygame.display.update()

            # Aguarda 1 segundo antes de encerrar o jogo
            time.sleep(1)
            pygame.quit()
            sys.exit()

        # Verifica se o jogador está na parte superior da tela
        if P1.rect.top <= HEIGHT / 3:
            P1.pos.y += abs(P1.vel.y)
            for plat in platforms:
                plat.rect.y += abs(P1.vel.y)
                if plat.rect.top >= HEIGHT:
                    plat.kill()

            for coin in coins:
                coin.rect.y += abs(P1.vel.y)
                if coin.rect.top >= HEIGHT:
                    coin.kill()

        # Gera plataformas
        generate_platforms()

        # Exibe o fundo, o jogador e a pontuação
        displaysurface.blit(background, (0, 0))
        g = pygame.font.SysFont("Verdana", 20).render(str(P1.score), True, (123, 255, 0))
        displaysurface.blit(g, (WIDTH / 2, 10))

        for entity in all_sprites:
            displaysurface.blit(entity.surf, entity.rect)
            entity.move()

        for coin in coins:
            displaysurface.blit(coin.image, coin.rect)
            coin.update()

        pygame.display.update()
        FramePerSec.tick(FPS)

def main():
    global all_sprites, platforms, coins, P1

    # Inicializa os grupos de sprites
    all_sprites = pygame.sprite.Group()
    platforms = pygame.sprite.Group()
    coins = pygame.sprite.Group()

    # Cria a plataforma inicial
    PT1 = platform(450, 80)
    PT1.rect = PT1.surf.get_rect(center=(WIDTH / 2, HEIGHT - 10))
    PT1.moving = False
    PT1.point = False

    # Cria o jogador
    P1 = Player()

    # Adiciona a plataforma inicial e o jogador aos grupos de sprites
    all_sprites.add(PT1)
    all_sprites.add(P1)
    platforms.add(PT1)

    # Gera plataformas adicionais
    for x in range(random.randint(4, 5)):
        collision = True
        pl = platform()
        while collision:
            pl = platform()
            collision = check_collision(pl, platforms)
        pl.generateCoin()
        platforms.add(pl)
        all_sprites.add(pl)

    # Inicia o loop do jogo
    game_loop()


if __name__ == "__main__":
    main()