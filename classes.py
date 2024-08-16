from typing import Any
import pygame
from constantes import *


# ============================= LEVEL =============================
class Level:
    def __init__(self, display_surface) -> None:
        self.screen = display_surface

        self.sprite_group_personagem = pygame.sprite.GroupSingle()
        self.sprite_group_projeteis = pygame.sprite.Group()

        self.sprite_group_personagem.add(CapivaraIsa((225, 500), 200, True, self.sprite_group_personagem, self.sprite_group_projeteis))
    
    def update(self) -> None:
        self.sprite_group_personagem.update()
        self.sprite_group_projeteis.update()
    
    def draw(self) -> None:
        self.sprite_group_personagem.draw(self.screen)
        self.sprite_group_projeteis.draw(self.screen)
    
    def run(self) -> None:
        self.update()
        self.draw()


# ============================= PERSONAGEM =============================
class Personagem(pygame.sprite.Sprite):
    def __init__(self, pos: tuple, life: int, face_right: bool) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.life = life
        self.life_show = self.life
        self.max_life = self.life
        self.x_pos, self.y_pos = pos
        self.face_right = face_right
    
    def damage(self, dano: int) -> None:
        if self.life > 0:
            self.life -= dano
    
    # def draw_life_bar(self) -> None:
    #     if self.life_show > self.life:
    #         self.life_show -= 1
        
    #     pygame.draw.rect()
    #     pygame.draw.rect()
    #     pygame.draw.rect()


# ============================= PROJETEIS =============================
class Projeteis(pygame.sprite.Sprite):
    def __init__(self, dano: int) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.dano = dano
    
    def colisao(self, sprite_group) -> bool:
        for item in pygame.sprite.spritecollide(self, sprite_group, False, pygame.sprite.collide_mask):
            if isinstance(item, Personagem):
                item.damage(self.dano)
                return True
        return False


# ============================= SPRITE SHEET =============================
class SpriteSheet:
    def __init__(self, sprite_sheet: str, sprite_position: list) -> None:
        sprite_sheet = pygame.image.load(sprite_sheet).convert_alpha()
        self.sprite = []
        self.sprite_flipped = []
        for pos in sprite_position:
            sprite = sprite_sheet.subsurface(pygame.Rect(pos))
            sprite = pygame.transform.scale(sprite, (128, 128)) # Temporário
            self.sprite.append(sprite)
            sprite = pygame.transform.flip(sprite, True, False)
            self.sprite_flipped.append(sprite)
    
    def get_sprites(self, flip: bool = False) -> list:
        if flip:
            return self.sprite_flipped
        return self.sprite


# ============================= CAPIVARA =============================
class CapivaraIsa(Personagem):
    def __init__(self, pos: tuple, life: int, face_right, sprite_group_personagens, sprite_group_projeteis) -> None:
        Personagem.__init__(self, pos, life, face_right) # Só um teste...
        sprite_sheet_idle = SpriteSheet(
            os.path.join(DIRETORIO_IMAGENS, 'Capivara Sprites/capivara_tatica_parada.png'),
            [
                (0, 0, 64, 64),
                (64, 0, 64, 64),
                (128, 0, 64, 64),
                (192, 0, 64, 64),
                (256, 0, 64, 64),
                (320, 0, 64, 64),
                (384, 0, 64, 64),
                (448, 0, 64, 64)
            ]
        )
        sprite_sheet_run = SpriteSheet(
            os.path.join(DIRETORIO_IMAGENS, 'Capivara Sprites/capivara_tatica_andando.png'),
            [
                (0, 0, 64, 64),
                (64, 0, 64, 64),
                (128, 0, 64, 64),
                (192, 0, 64, 64),
                (256, 0, 64, 64),
                (320, 0, 64, 64),
                (384, 0, 64, 64),
                (448, 0, 64, 64)
            ]
        )
        sprite_sheet_jump = SpriteSheet(
            os.path.join(DIRETORIO_IMAGENS, 'Capivara Sprites/capivara_tatica_pulando.png'),
            [
                (0, 0, 64, 64),
                (64, 0, 64, 64),
                (128, 0, 64, 64),
                (192, 0, 64, 64),
                (256, 0, 64, 64),
                (320, 0, 64, 64),
                (384, 0, 64, 64),
                (448, 0, 64, 64)
            ]
        )
        sprite_sheet_death = SpriteSheet(
            os.path.join(DIRETORIO_IMAGENS, 'Capivara Sprites/capivara_tatica_morrendo.png'),
            [
                (0, 0, 64, 64),
                (64, 0, 64, 64),
                (128, 0, 64, 64),
                (192, 0, 64, 64),
                (256, 0, 64, 64),
                (320, 0, 64, 64),
                (384, 0, 64, 64),
                (448, 0, 64, 64),
                (512, 0, 64, 64),
                (576, 0, 64, 64),
                (640, 0, 64, 64),
                (704, 0, 64, 64),
                (768, 0, 64, 64),
                (832, 0, 64, 64),
                (896, 0, 64, 64),
                (960, 0, 64, 64),
                (1024, 0, 64, 64),
                (1088, 0, 64, 64),
                (1152, 0, 64, 64),
                (1216, 0, 64, 64),
                (1280, 0, 64, 64),
                (1344, 0, 64, 64),
                (1408, 0, 64, 64),
                (1472, 0, 64, 64),
                (1536, 0, 64, 64)
            ]
        )

        self.sprites_sheets = {
            'IDLE': (sprite_sheet_idle, 0.15),
            'RUN': (sprite_sheet_run, 0.25),
            'JUMP': (sprite_sheet_jump, 0.25),
            'DEATH': (sprite_sheet_death, 0.25)
        }

        self.sprite_group_personagens = sprite_group_personagens
        self.sprite_group_projeteis = sprite_group_projeteis
        self.balas_cadencia = 0
        self.image_idx = 0
        self.estado = 'IDLE'
        self.speed_animation = self.sprites_sheets[self.estado][1]
        self.velocidade = 0
        self.pulando = False
    
    def update(self) -> None:
        estado_antes = self.estado
        self.x_dir = 0

        self.gravidade()

        if self.life > 0: # Talvez usar o `life_show`
            # self.draw_life_bar()    

            # TROCAR ESTADO =============================================
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                self.face_right = False
                self.estado = 'RUN'
                self.x_dir = -1
            elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                self.face_right = True
                self.estado = 'RUN'
                self.x_dir = 1
            else:
                self.estado = 'IDLE'
            if self.pulando:
                self.estado = 'JUMP'
            
            # ATIRAR ======================================================
            if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and self.balas_cadencia == 0:
                self.balas_cadencia = 5
                self.atirar()
            if self.balas_cadencia > 0:
                self.balas_cadencia -= 1
            
            # PULAR =======================================================
            if (keys[pygame.K_w] or keys[pygame.K_UP]) and not self.pulando:
                self.estado = 'JUMP'
                self.velocidade = -15
                self.pulando = True

            if estado_antes != self.estado:
                self.image_idx = 0

            self.select_animation()

            self.animar()

            self.image = self.sprites_atual[int(self.image_idx)]
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = pygame.Rect(self.x_pos - 18, self.y_pos - 14, 96, 106)

            # Cenário começa a se mover
            # if self.rect.left + 14 < 0 and not self.face_right or self.rect.centerx >= LARGURA // 4 and self.face_right:
            #     self.x_dir = 0

            self.move_horizontal()

        elif self.image_idx is not None:
            self.estado = 'DEATH'

            if estado_antes != self.estado:
                self.image_idx = 0

            self.select_animation()

            self.image_idx += self.speed_animation
            if self.image_idx >= len(self.sprites_atual):
                self.image_idx = None
            elif self.image_idx is not None:
                self.image = self.sprites_atual[int(self.image_idx)]
                self.mask = pygame.mask.from_surface(self.image)

            self.rect = pygame.Rect(self.x_pos - 18, self.y_pos - 14, 10, 19)

    def select_animation(self) -> None:
        sprite_sheet = self.sprites_sheets[self.estado][0]
        self.speed_animation = self.sprites_sheets[self.estado][1]
        self.sprites_atual = sprite_sheet.get_sprites(not self.face_right)
    
    def atirar(self) -> None:
        if self.face_right:
            self.sprite_group_projeteis.add(Bala((self.x_pos + 70, self.y_pos + 71), 28, 10, self.sprite_group_personagens))
        else:
            self.sprite_group_projeteis.add(Bala((self.x_pos + 20, self.y_pos + 71), -28, 10, self.sprite_group_personagens))
        self.x_pos += -2 if self.face_right else 2
    
    def gravidade(self) -> None:
        self.velocidade += GRAVIDADE
        self.y_pos += self.velocidade
        if self.y_pos + 98 >= ALTURA:
            self.pulando = False
            self.y_pos = ALTURA - 98
            self.velocidade = 0
    
    def move_horizontal(self) -> None:
        self.x_pos += self.x_dir * VELOCIDADE
    
    def animar(self) -> None:
        self.image_idx += self.speed_animation
        if self.image_idx >= len(self.sprites_atual):
            self.image_idx = 0
        if self.velocidade > 0 and self.image_idx >= 7:
                self.image_idx = 4


# ============================= CAPIVARA =============================
class Bala(Projeteis):
    def __init__(self, pos: tuple, velocidade: int, dano: int, sprite_group_personagens) -> None:
        Projeteis.__init__(self, dano)
        self.image = pygame.Surface((12, 6)) # Tamanho temporário
        self.image.fill((255, 122, 0))
        self.rect = self.image.get_rect(center=pos)
        self.velocidade = velocidade
        self.sprite_group_personagens = sprite_group_personagens
    
    def update(self) -> None:
        self.rect.x += self.velocidade

        if self.rect.right < 0 or self.rect.left > LARGURA or self.colisao(self.sprite_group_personagens):
            self.kill()
