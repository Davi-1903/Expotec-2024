import pygame
from lib.constantes import *


# ============================= LEVEL =============================
class Level:
    def __init__(self, display_surface) -> None:
        self.screen = display_surface
        self.scroll = 0

        self.sprite_group_superficie = pygame.sprite.Group()
        self.sprite_group_personagem = pygame.sprite.GroupSingle()
        self.sprite_group_inimigos = pygame.sprite.Group()
        self.sprite_group_projeteis = pygame.sprite.Group()

        self.mapa = [ # Mapa provisório, só para testes
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 3, 3, 3, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]

        for idx_l, linha in enumerate(self.mapa):
            for idx_c, item in enumerate(linha):
                if item != 0:
                    self.sprite_group_superficie.add(Tile((idx_c * TILE_SIZE, idx_l * TILE_SIZE), item))

        self.personagem = CapivaraIsa((50, 500), 200, True, self.screen, self.sprite_group_inimigos, self.sprite_group_projeteis, self.sprite_group_superficie)
        self.sprite_group_personagem.add(self.personagem)
        self.sprite_group_inimigos.add(Rato((500, 300), 100, True, (500, 700), self.screen, self.sprite_group_personagem, self.sprite_group_projeteis, self.sprite_group_superficie))
        self.sprite_group_inimigos.add(Rato((500, 500), 100, True, (500, 850), self.screen, self.sprite_group_personagem, self.sprite_group_projeteis, self.sprite_group_superficie))
        self.sprite_group_inimigos.add(Rato((1100, 200), 100, True, (1100, 1300), self.screen, self.sprite_group_personagem, self.sprite_group_projeteis, self.sprite_group_superficie))
        self.sprite_group_inimigos.add(Rato((1100, 200), 100, True, (1400, 1700), self.screen, self.sprite_group_personagem, self.sprite_group_projeteis, self.sprite_group_superficie))
    
    def update(self) -> None:
        scroll_antes = self.scroll

        self.sprite_group_personagem.update()
        self.sprite_group_inimigos.update()
        self.sprite_group_projeteis.update()

        # MOVER O CENÁRIO ====================================================
        if self.personagem.rect.left + 14 < 225 and not self.personagem.face_right or self.personagem.rect.right - 10 > 675 and self.personagem.face_right:
            self.scroll += -self.personagem.deslocamento_x
        
        # PARAR DE MOVER O CENÁRIO E MOVER A CAPIVARA =========================
        if self.scroll > 0:
            self.scroll = 0
            if self.personagem.deslocamento_x != 0 and self.personagem.rect.left + 14 > 0:
                self.personagem.mover()
        if self.scroll < -len(self.mapa[0]) * TILE_SIZE // 2:
            self.scroll = -len(self.mapa[0]) * TILE_SIZE // 2
            if self.personagem.deslocamento_x != 0 and self.personagem.rect.right - 10 < LARGURA:
                self.personagem.mover()
        
        # CORRIGINDO A POSIÇÃO DO INIMIGO ==========================
        for inimigo in self.sprite_group_inimigos:
            inimigo.x_atual = inimigo.x_origin + self.scroll
            inimigo.x_pos -= scroll_antes - self.scroll

        # MOVENDO O CENÁRIO ===========================
        for tile in self.sprite_group_superficie:
            tile.mover(self.scroll)
    
    def draw(self) -> None:
        self.sprite_group_superficie.draw(self.screen)
        self.sprite_group_personagem.draw(self.screen)
        self.sprite_group_inimigos.draw(self.screen)
        self.sprite_group_projeteis.draw(self.screen)
    
    def run(self) -> None:
        self.update()
        self.draw()


# ============================= TILE =============================
class Tile(pygame.sprite.Sprite):
    def __init__(self, pos: tuple, item: int) -> None:
        pygame.sprite.Sprite.__init__(self)
        sprite_sheet = SpriteSheet(os.path.join(DIRETORIO_IMAGENS, 'Grass/Grass Tile.png'), [
            (0, 0, 64, 64),
            (64, 0, 64, 64),
            (128, 0, 64, 64)
        ])
        self.image = pygame.transform.scale(sprite_sheet.get_sprites()[item - 1], (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect(topleft = pos)
        self.x_origin = pos[0]
    
    def mover(self, scroll: int) -> None:
        self.rect.x = self.x_origin + scroll


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
    
    def draw_life_bar(self, display_surface, width: int) -> None:
        if self.life_show > self.life:
            self.life_show -= 2
        
        pygame.draw.rect(display_surface, (48, 48, 64), (self.x_pos + 18, self.y_pos - 20, width, 16), border_radius=5) # Gambiarra...
        pygame.draw.rect(display_surface, (0, 255, 0), (self.x_pos + 18, self.y_pos - 20, self.life_show / self.max_life * width, 16), border_radius=5) # Gambiarra...
        pygame.draw.rect(display_surface, (48, 48, 64), (self.x_pos + 18, self.y_pos - 20, width, 16), 2, border_radius=5) # Gambiarra...


# ============================= PROJETEIS =============================
class Projeteis(pygame.sprite.Sprite):
    def __init__(self, dano: int) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.dano = dano
    
    def colisao(self, sprite_groups) -> bool:
        for sprite_group in sprite_groups:
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
            sprite = pygame.transform.scale(sprite, (96, 96)) # Temporário
            self.sprite.append(sprite)
            sprite = pygame.transform.flip(sprite, True, False)
            self.sprite_flipped.append(sprite)
    
    def get_sprites(self, flip: bool = False) -> list:
        if flip:
            return self.sprite_flipped
        return self.sprite


# ============================= CAPIVARA =============================
class CapivaraIsa(Personagem):
    def __init__(self, pos: tuple, life: int, face_right, screen, sprite_group_inimigos, sprite_group_projeteis, sprite_group_superficie) -> None:
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

        self.screen = screen
        self.sprite_group_inimigos = sprite_group_inimigos
        self.sprite_group_projeteis = sprite_group_projeteis
        self.sprite_group_superficie = sprite_group_superficie
        self.balas_cadencia = 0
        self.image_idx = 0
        self.estado = 'IDLE'
        self.speed_animation = self.sprites_sheets[self.estado][1]
        self.velocidade_y = 0
        self.pulando = False
    
    def update(self) -> None:
        estado_antes = self.estado
        self.deslocamento_x = 0

        self.gravidade()

        if self.life > 0: # Talvez usar o `life_show`
            self.draw_life_bar(self.screen, 72)

            # TROCAR ESTADO =============================================
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                self.face_right = False
                self.estado = 'RUN'
                self.deslocamento_x = -VELOCIDADE
            elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                self.face_right = True
                self.estado = 'RUN'
                self.deslocamento_x = VELOCIDADE
            else:
                self.estado = 'IDLE'
            if self.pulando:
                self.estado = 'JUMP'
            
            # ATIRAR ======================================================
            if keys[pygame.K_f] and self.balas_cadencia == 0:
                self.balas_cadencia = 5
                self.atirar()
            if self.balas_cadencia > 0:
                self.balas_cadencia -= 1
            
            # PULAR =======================================================
            if (keys[pygame.K_w] or keys[pygame.K_UP] or keys[pygame.K_SPACE]) and not self.pulando:
                self.estado = 'JUMP'
                self.velocidade_y = -15
                self.pulando = True

            if estado_antes != self.estado:
                self.image_idx = 0

            self.select_animation()

            self.animar()

            self.image = self.sprites_atual[int(self.image_idx)]
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect(topleft = (self.x_pos, self.y_pos))

            self.colisao()

            # PARAR A CAPIVARA ==============================================
            if self.rect.left + 14 >= 225 and not self.face_right or self.rect.right - 10 <= 675 and self.face_right:
                self.mover()
        elif self.image_idx is not None:
            # RODAR ANIMAÇÃO DE MORTE ====================================
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

            self.rect = pygame.Rect(self.x_pos + 10.5, self.y_pos + 1.75, 10, 19)

            self.colisao()

    def select_animation(self) -> None:
        sprite_sheet = self.sprites_sheets[self.estado][0]
        self.speed_animation = self.sprites_sheets[self.estado][1]
        self.sprites_atual = sprite_sheet.get_sprites(not self.face_right)
    
    def atirar(self) -> None:
        if self.face_right:
            self.sprite_group_projeteis.add(Bala((self.x_pos + 60, self.y_pos + 63), 28, 10, (12, 6),  [self.sprite_group_inimigos, self.sprite_group_superficie]))
        else:
            self.sprite_group_projeteis.add(Bala((self.x_pos + 32, self.y_pos + 63), -28, 10, (12, 6), [self.sprite_group_inimigos, self.sprite_group_superficie]))
    
    def gravidade(self) -> None:
        self.velocidade_y += GRAVIDADE
        self.y_pos += self.velocidade_y
    
    def mover(self) -> None:
        self.x_pos += self.deslocamento_x
    
    def animar(self) -> None:
        self.image_idx += self.speed_animation
        if self.image_idx >= len(self.sprites_atual):
            self.image_idx = 0
        if self.estado == 'JUMP' and self.velocidade_y > 0 and self.image_idx >= 7:
            self.image_idx = 4
    
    def colisao(self) -> None:
        # COLISÃO COM BLOCOS ===================================================
        for tile in self.sprite_group_superficie:
            if tile.rect.colliderect(self.x_pos + 10.5 + self.deslocamento_x, self.y_pos + 21.25 + self.velocidade_y, 76.5, 54.5):
                self.deslocamento_x = 0
            if tile.rect.colliderect(self.x_pos + 10.5, self.y_pos + 21.75 + self.velocidade_y, 76.5, 64.5):
                if self.velocidade_y > 0:
                    self.y_pos = tile.rect.top - 76.5
                    self.pulando = False
                self.velocidade_y = 0
        
        # COLISÃO COM INIMIGOS =================================================
        for inimigo in self.sprite_group_inimigos:
            if inimigo.rect.colliderect(self.x_pos + 10.5, self.y_pos + 21.25 + self.velocidade_y, 76.5, 54.5):
                self.y_pos = self.rect.top - 1
                self.pulando = False
                self.velocidade_y = 0
            if inimigo.rect.colliderect(self.rect):
                if self.rect.centerx - inimigo.rect.centerx < 0 and self.face_right:
                    self.deslocamento_x = 0
                elif self.rect.centerx - inimigo.rect.centerx < 0 and not self.face_right:
                    self.deslocamento_x = inimigo.rect.left - 96.5 - self.x_pos
                elif self.rect.centerx - inimigo.rect.centerx > 0 and not self.face_right:
                    self.deslocamento_x = 0


# ============================= RATO =============================
class Rato(Personagem):
    def __init__(self, pos: tuple, life: int, face_right: bool, limites: tuple, screen, sprite_group_personagem, sprite_group_projeteis, sprite_group_superficie) -> None:
        super().__init__(pos, life, face_right) # Oxi?
        sprite_sheet_run = SpriteSheet(
            os.path.join(DIRETORIO_IMAGENS, 'Rato Sprites/rato_andando.png'),
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
        sprite_sheet_attack = SpriteSheet(
            os.path.join(DIRETORIO_IMAGENS, 'Rato Sprites/rato_atirando.png'),
            [
                (0, 0, 64, 64),
                (64, 0, 64, 64)
            ]
        )
        sprite_sheet_death = SpriteSheet(
            os.path.join(DIRETORIO_IMAGENS, 'Rato Sprites/rato_morrendo.png'),
            [
                (0, 0, 64, 64),
                (64, 0, 64, 64),
                (128, 0, 64, 64),
                (192, 0, 64, 64),
                (256, 0, 64, 64),
                (320, 0, 64, 64),
                (384, 0, 64, 64)
            ]
        )

        self.sprites_sheets = {
            'RUN': (sprite_sheet_run, 0.25),
            'DEATH': (sprite_sheet_death, 0.15),
            'ATTACK': (sprite_sheet_attack, 0.25)
        }

        self.screen = screen
        self.sprite_group_personagem = sprite_group_personagem
        self.sprite_group_projeteis = sprite_group_projeteis
        self.sprite_group_superficie = sprite_group_superficie

        self.balas_cadencia = 0
        self.image_idx = 0
        self.estado = 'RUN'
        self.x_origin = limites[0]
        self.x_atual = self.x_origin
        self.distancia = limites[1] - self.x_atual
        self.velocidade_y = 0
        self.deslocamento_x = 0

        self.select_animation()
        self.image = self.sprites_atual[int(self.image_idx)]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft = (self.x_pos, self.y_pos))
        self.speed_animation = self.sprites_sheets[self.estado][1]
    
    def update(self) -> None:
        estado_antes = self.estado

        self.gravidade()

        if self.life > 0:
            self.draw_life_bar(self.screen, 72)

            if estado_antes != self.estado:
                self.image_idx = 0
            
            self.select_animation()

            self.animar()

            self.image = self.sprites_atual[int(self.image_idx)]
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect(topleft = (self.x_pos, self.y_pos))

            # ALTERAR O SENTIDO DO RATO ==================================
            if self.rect.left < self.x_atual:
                self.face_right = True
            elif self.rect.right > self.x_atual + self.distancia:
                self.face_right = False
            
            if self.face_right:
                self.deslocamento_x = VELOCIDADE // 2
            else:
                self.deslocamento_x = -VELOCIDADE // 2

            # VERIFICAR SE É POSSÍVEL ATIRAR =============================================
            for personagem in self.sprite_group_personagem:
                if personagem.y_pos <= self.rect.centery <= personagem.y_pos + 65 and (-250 < personagem.rect.centerx - self.rect.centerx < 0 and not self.face_right or 250 > personagem.rect.centerx - self.rect.centerx > 0 and self.face_right):
                    self.deslocamento_x = 0
                    self.estado = 'ATTACK'
                else:
                    self.estado = 'RUN'
            
            # ATIRAR =====================================================
            if self.estado == 'ATTACK' and self.balas_cadencia == 0:
                self.balas_cadencia = 10
                self.atirar()
            elif self.balas_cadencia > 0:
                self.balas_cadencia -= 1

            self.mover()

            self.colisao()
        elif self.image_idx is not None:
            # RODAR ANIMAÇÃO DE MORTE ================================================
            self.estado = 'DEATH'

            self.select_animation()

            self.image_idx += self.speed_animation
            if self.image_idx >= len(self.sprites_atual):
                self.image_idx = None
            elif self.image_idx is not None:
                self.image = self.sprites_atual[int(self.image_idx)]
                self.mask = pygame.mask.from_surface(self.image)
    
            self.rect = self.image.get_rect(topleft = (self.x_pos, self.y_pos))
            
            self.colisao()
        else:
            self.kill()
    
    def select_animation(self) -> None:
        sprite_sheet = self.sprites_sheets[self.estado][0]
        self.speed_animation = self.sprites_sheets[self.estado][1]
        self.sprites_atual = sprite_sheet.get_sprites(self.face_right)
    
    def gravidade(self) -> None:
        self.velocidade_y += GRAVIDADE
        self.y_pos += self.velocidade_y
    
    def animar(self) -> None:
        self.image_idx += self.speed_animation
        if self.image_idx >= len(self.sprites_atual):
            self.image_idx = 0
    
    def mover(self) -> None:
        self.x_pos += self.deslocamento_x
    
    def colisao(self) -> None: # Agora aqui tem gambiarra...
        for tile in self.sprite_group_superficie:
            if tile.rect.colliderect(self.x_pos + 10.5, self.y_pos + 21.25, 76.5, 10):
                self.deslocamento_x = 0
            if tile.rect.colliderect(self.x_pos + 10.5, self.y_pos + 21.75, 76.5, 64.5):
                if self.velocidade_y > 0:
                    self.y_pos = tile.rect.top - 76.5
                    self.pulando = False
                self.velocidade_y = 0

    def atirar(self) -> None:
        if self.face_right:
            self.sprite_group_projeteis.add(Bala((self.x_pos + 50, self.y_pos + 25), 28, 5, (12, 6), [self.sprite_group_personagem, self.sprite_group_superficie]))
        else:
            self.sprite_group_projeteis.add(Bala((self.x_pos + 50, self.y_pos + 25), -28, 5, (12, 6), [self.sprite_group_personagem, self.sprite_group_superficie]))


# ============================= BALA =============================
class Bala(Projeteis):
    def __init__(self, pos: tuple, velocidade: int, dano: int, size: tuple, sprite_group_inimigos) -> None:
        Projeteis.__init__(self, dano)
        self.image = pygame.Surface(size) # Tamanho temporário
        self.image.fill((255, 122, 0))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=pos)
        self.velocidade = velocidade
        self.sprite_group_inimigos = sprite_group_inimigos
    
    def update(self) -> None:
        self.rect.x += self.velocidade
        if self.rect.right < 0 or self.rect.left > LARGURA or self.colisao(self.sprite_group_inimigos):
            self.kill()
