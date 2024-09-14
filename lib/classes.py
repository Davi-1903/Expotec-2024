import pygame, json
from pytmx.util_pygame import load_pygame
from lib.constantes import *


# ============================= LEVEL =============================
class Level:
    def __init__(self, display_surface: pygame.Surface):
        self.screen = display_surface
        self.scroll = 0
        self.sprite_group_config()
        self.mapa_idx = 1 # Valor que será passado pelo usuário
        self.mapa_config()
        self.add_personagens()
        self.fim = False
    
    def add_personagens(self) -> None:
        with open(os.path.join(DIRETORIO_MAPAS, f'Mapa {self.mapa_idx}/Data/personagens_pos.json').replace('\\', '/')) as arquivo:
            personagens_data = json.load(arquivo)
        for personagem in personagens_data:
            if personagem['personagem'] == 'capivara':
                self.personagem = CapivaraIsa(personagem['inicio'], personagem['life'], personagem['faceRight'], self.screen, self.sprite_group_inimigos, self.sprite_group_projeteis, self.sprite_group_superficie)
                self.sprite_group_personagem.add(self.personagem)
            if personagem['personagem'] == 'rato':
                self.sprite_group_inimigos.add(Rato(personagem['inicio'], personagem['life'], personagem['faceRight'], personagem['limites'], self.screen, self.sprite_group_personagem, self.sprite_group_projeteis, self.sprite_group_superficie))

    def sprite_group_config(self) -> None:
        self.sprite_group_superficie = pygame.sprite.Group()
        self.sprite_group_personagem = pygame.sprite.GroupSingle()
        self.sprite_group_inimigos = pygame.sprite.Group()
        self.sprite_group_projeteis = pygame.sprite.Group()

    def mapa_config(self) -> None:
        self.mapa_data = load_pygame(os.path.join(DIRETORIO_MAPAS, f'Mapa {self.mapa_idx}/Data/tmx/Mapa.tmx').replace('\\', '/'))
        self.background = pygame.image.load(os.path.join(DIRETORIO_MAPAS, f'Mapa {self.mapa_idx}/Assets/Backgrounds/background.jpg').replace('\\', '/'))
        layers = self.mapa_data.get_layer_by_name('Collision Block')
        for x, y, surface in layers.tiles():
            self.sprite_group_superficie.add(Tile((x * TILE_SIZE, y * TILE_SIZE), surface))
        self.backgrounds = []
        vezes = self.mapa_data.width * TILE_SIZE // self.background.get_width()
        if vezes < 1:
            vezes = 1
        for n in range(vezes):
            self.backgrounds.append(self.background)
    
    def draw_mapa(self) -> None:
        for layer in self.mapa_data.layers:
            if layer.name != 'Collision Block' and hasattr(layer, 'data'):
                for x, y, surface in layer.tiles():
                    self.screen.blit(surface, (x * TILE_SIZE + self.scroll, y * TILE_SIZE))
        for objetos in self.mapa_data.objects:
            self.screen.blit(pygame.transform.rotate(objetos.image, -objetos.rotation), (objetos.x + self.scroll, objetos.y))
    
    def draw_background(self) -> None:
        for idx, background in enumerate(self.backgrounds):
            self.screen.blit(background, (idx * background.get_width() + self.scroll // 4, 0))

    def update(self) -> None:
        self.scroll_antes = self.scroll
        self.mover_cenario()
        self.sprites_update()
        self.deslocamento_cenario()
        self.corrigir_inimigo_pos()
        if len(self.sprite_group_inimigos) == 0:
            self.fim = True
    
    def sprites_update(self) -> None:
        self.draw_background()
        self.draw_mapa()
        self.sprite_group_personagem.update()
        self.sprite_group_inimigos.update()
        self.sprite_group_projeteis.update()
    
    def corrigir_inimigo_pos(self) -> None:
        for inimigo in self.sprite_group_inimigos:
            inimigo.x_atual = inimigo.x_origin + self.scroll
            inimigo.x_pos -= self.scroll_antes - self.scroll
    
    def deslocamento_cenario(self) -> None:
        if self.personagem.rect.left + 14 < 225 and not self.personagem.face_right or self.personagem.rect.right - 10 > 675 and self.personagem.face_right:
            self.scroll += -self.personagem.deslocamento_x
        if self.scroll > 0:
            self.scroll = 0
            if self.personagem.deslocamento_x != 0 and self.personagem.rect.left + 14 > 0:
                self.personagem.mover()
        if self.scroll < -self.mapa_data.width * TILE_SIZE // 2:
            self.scroll = -self.mapa_data.width * TILE_SIZE // 2
            if self.personagem.deslocamento_x != 0 and self.personagem.rect.right - 10 < LARGURA:
                self.personagem.mover()
    
    def mover_cenario(self) -> None:
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
    def __init__(self, pos: tuple, surface: pygame.Surface):
        pygame.sprite.Sprite.__init__(self)
        self.image = surface
        self.rect = self.image.get_rect(topleft = pos)
        self.x_origin = pos[0]
    
    def mover(self, scroll: int) -> None:
        self.rect.x = self.x_origin + scroll


# ============================= PERSONAGEM =============================
class Personagem(pygame.sprite.Sprite):
    def __init__(self, pos: tuple, life: int, face_right: bool):
        pygame.sprite.Sprite.__init__(self)
        self.life = life
        self.life_show = self.life
        self.max_life = self.life
        self.x_pos, self.y_pos = pos
        self.face_right = face_right
    
    def damage(self, dano: int) -> None:
        if self.life > 0:
            self.life -= dano
    
    def draw_life_bar(self, display_surface: pygame.Surface, width: int) -> None:
        if self.life_show > self.life:
            self.life_show -= 2
        pygame.draw.rect(display_surface, (48, 48, 64), (self.x_pos + 18, self.y_pos - 20, width, 16), border_radius=5) # Gambiarra...
        pygame.draw.rect(display_surface, (0, 255, 0), (self.x_pos + 18, self.y_pos - 20, self.life_show / self.max_life * width, 16), border_radius=5) # Gambiarra...
        pygame.draw.rect(display_surface, (48, 48, 64), (self.x_pos + 18, self.y_pos - 20, width, 16), 2, border_radius=5) # Gambiarra...


# ============================= PROJETEIS =============================
class Projeteis(pygame.sprite.Sprite):
    def __init__(self, dano: int):
        pygame.sprite.Sprite.__init__(self)
        self.dano = dano
    
    def colisao(self, sprite_groups: pygame.sprite.GroupSingle | pygame.sprite.Group) -> bool:
        for sprite_group in sprite_groups:
            for item in pygame.sprite.spritecollide(self, sprite_group, False, pygame.sprite.collide_mask):
                if isinstance(item, Personagem):
                    item.damage(self.dano)
                return True
        return False


# ============================= SPRITE SHEET =============================
class SpriteSheet:
    def __init__(self, sprite_sheet: str, size: int):
        sprite_sheet = pygame.image.load(sprite_sheet).convert_alpha()
        width = sprite_sheet.get_width()
        height = sprite_sheet.get_height()
        self.sprite = []
        self.sprite_flipped = []
        for l in range(0, height, size):
            for c in range(0, width, size):
                sprite = sprite_sheet.subsurface((c, l, size, size))
                sprite = pygame.transform.scale(sprite, (96, 96)) # Temporário
                self.sprite.append(sprite)
                sprite = pygame.transform.flip(sprite, True, False)
                self.sprite_flipped.append(sprite)
    
    def get_sprites(self, flip: bool = False) -> list:
        return self.sprite_flipped if flip else self.sprite


# ============================= CAPIVARA =============================
class CapivaraIsa(Personagem):
    def __init__(self, pos: tuple, life: int, face_right: bool, screen: pygame.Surface, sprite_group_inimigos: pygame.sprite.Group, sprite_group_projeteis: pygame.sprite.Group, sprite_group_superficie: pygame.sprite.Group):
        Personagem.__init__(self, pos, life, face_right) # Só um teste...
        sprite_sheet_idle = SpriteSheet(os.path.join(DIRETORIO_IMAGENS, 'Capivara Sprites/capivara_tatica_parada.png').replace('\\', '/'), 64)
        sprite_sheet_run = SpriteSheet(os.path.join(DIRETORIO_IMAGENS, 'Capivara Sprites/capivara_tatica_andando.png').replace('\\', '/'), 64)
        sprite_sheet_jump = SpriteSheet(os.path.join(DIRETORIO_IMAGENS, 'Capivara Sprites/capivara_tatica_pulando.png').replace('\\', '/'), 64)
        sprite_sheet_death = SpriteSheet(os.path.join(DIRETORIO_IMAGENS, 'Capivara Sprites/capivara_tatica_morrendo.png').replace('\\', '/'), 64)
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
            self.trocar_estado()
            self.atirar()
            if estado_antes != self.estado:
                self.image_idx = 0
            self.pular()
            self.select_animation()
            self.animar()
            self.exibicao_config()
            self.colisao()
            # PARAR A CAPIVARA ==============================================
            if self.rect.left + 14 >= 225 and not self.face_right or self.rect.right - 10 <= 675 and self.face_right:
                self.mover()
        elif self.image_idx is not None:
            self.estado = 'DEATH'
            if estado_antes != self.estado:
                self.image_idx = 0
            self.select_animation()
            self.image_idx += self.speed_animation
            if self.image_idx >= len(self.sprites_atual):
                self.image_idx = None
            self.exibicao_config()
            self.colisao()
    
    def pular(self) -> None:
        if (self.keys[pygame.K_w] or self.keys[pygame.K_UP] or self.keys[pygame.K_SPACE]) and not self.pulando:
            self.estado = 'JUMP'
            self.velocidade_y = -15
            self.pulando = True
    
    def exibicao_config(self) -> None:
        if self.image_idx is not None:
            self.image = self.sprites_atual[int(self.image_idx)]
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect(topleft = (self.x_pos, self.y_pos))
    
    def trocar_estado(self) -> None:
        self.keys = pygame.key.get_pressed()
        if self.keys[pygame.K_a] or self.keys[pygame.K_LEFT]:
            self.face_right = False
            self.estado = 'RUN'
            self.deslocamento_x = -VELOCIDADE
        elif self.keys[pygame.K_d] or self.keys[pygame.K_RIGHT]:
            self.face_right = True
            self.estado = 'RUN'
            self.deslocamento_x = VELOCIDADE
        else:
            self.estado = 'IDLE'
        if self.pulando:
            self.estado = 'JUMP'

    def select_animation(self) -> None:
        sprite_sheet = self.sprites_sheets[self.estado][0]
        self.speed_animation = self.sprites_sheets[self.estado][1]
        self.sprites_atual = sprite_sheet.get_sprites(not self.face_right)
    
    def atirar(self) -> None:
        if self.keys[pygame.K_f] and self.balas_cadencia == 0:
            self.balas_cadencia = 5
            self.sprite_group_projeteis.add(Bala((self.x_pos + 60, self.y_pos + 63), 28 if self.face_right else -28, 10, (12, 6),  [self.sprite_group_inimigos, self.sprite_group_superficie]))
        if self.balas_cadencia > 0:
            self.balas_cadencia -= 1
    
    def gravidade(self) -> None:
        self.velocidade_y += GRAVIDADE
        self.y_pos += self.velocidade_y
    
    def mover(self) -> None:
        self.x_pos += self.deslocamento_x
    
    def animar(self) -> None:
        self.image_idx += self.speed_animation
        if self.image_idx >= len(self.sprites_atual) and self.estado != 'JUMP':
            self.image_idx = 0
        elif self.image_idx >= len(self.sprites_atual) and self.estado == 'JUMP':
            self.image_idx = 1
        if self.estado == 'JUMP' and self.velocidade_y > 0 and self.image_idx >= 8:
            self.image_idx = 5
    
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
        for inimigo in self.sprite_group_inimigos: # Ajeitar, está meio bugado
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
    def __init__(self, pos: tuple, life: int, face_right: bool, limites: tuple, screen: pygame.Surface, sprite_group_personagem: pygame.sprite.GroupSingle, sprite_group_projeteis: pygame.sprite.Group, sprite_group_superficie: pygame.sprite.Group):
        super().__init__(pos, life, face_right) # Oxi?
        sprite_sheet_run = SpriteSheet(os.path.join(DIRETORIO_IMAGENS, 'Rato Sprites/rato_andando.png').replace('\\', '/'), 64)
        sprite_sheet_attack = SpriteSheet(os.path.join(DIRETORIO_IMAGENS, 'Rato Sprites/rato_atirando.png').replace('\\', '/'), 64)
        sprite_sheet_death = SpriteSheet(os.path.join(DIRETORIO_IMAGENS, 'Rato Sprites/rato_morrendo.png').replace('\\', '/'), 64)
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
        self.exibicao_config()
    
    def update(self) -> None:
        estado_antes = self.estado
        self.gravidade()
        if self.life > 0:
            self.draw_life_bar(self.screen, 72)
            if estado_antes != self.estado:
                self.image_idx = 0
            self.select_animation()
            self.animar()
            self.exibicao_config()
            self.alterar_sentido()
            self.atirar()
            self.mover()
            self.colisao()
        elif self.image_idx is not None:
            self.estado = 'DEATH'
            self.select_animation()
            self.image_idx += self.speed_animation
            if self.image_idx >= len(self.sprites_atual):
                self.image_idx = None
            self.exibicao_config()
            self.colisao()
        else:
            self.kill()
    
    def alterar_sentido(self) -> None:
        if self.rect.left < self.x_atual:
            self.face_right = True
        elif self.rect.right > self.x_atual + self.distancia:
            self.face_right = False
        if self.face_right:
            self.deslocamento_x = VELOCIDADE // 2
        else:
            self.deslocamento_x = -VELOCIDADE // 2
    
    def exibicao_config(self) -> None:
        if self.image_idx is not None:
            self.image = self.sprites_atual[int(self.image_idx)]
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect(topleft = (self.x_pos, self.y_pos))
    
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
        for personagem in self.sprite_group_personagem:
            if personagem.y_pos <= self.rect.centery <= personagem.y_pos + 65 and (-250 < personagem.rect.centerx - self.rect.centerx < 0 and not self.face_right or 250 > personagem.rect.centerx - self.rect.centerx > 0 and self.face_right):
                self.deslocamento_x = 0
                self.estado = 'ATTACK'
            else:
                self.estado = 'RUN'
        if self.estado == 'ATTACK' and self.balas_cadencia == 0:
            self.balas_cadencia = 10
            self.sprite_group_projeteis.add(Bala((self.x_pos + 50, self.y_pos + 25), 28 if self.face_right else -28, 5, (12, 6), [self.sprite_group_personagem, self.sprite_group_superficie]))
        elif self.balas_cadencia > 0:
            self.balas_cadencia -= 1


# ============================= BALA =============================
class Bala(Projeteis):
    def __init__(self, pos: tuple, velocidade: int, dano: int, size: tuple, sprite_group_inimigos: pygame.sprite.Group) -> None:
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
