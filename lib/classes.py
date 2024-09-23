import pygame, json
from pytmx.util_pygame import load_pygame
from lib.constantes import *
from math import ceil


# ============================= LEVEL =============================
class Level:
    '''Modela tudo correspondente a fase.
    
    Atributos:
        self.screen -> Tela do jogo
    '''
    def __init__(self, display_surface: pygame.Surface):
        '''Método construtor.

        Parâmetros:
            display_surface -> Tela do Jogo
        '''
        self.screen = display_surface
        mapa_idx = 1 # Valor que será passado pelo usuário
        self.carregar_level(mapa_idx)
    
    def carregar_level(self, mapa_idx: int) -> None:
        '''Carrega o mapa que será jogado.
        
        Parâmetros:
            self.mapa_idx -> Valor que indica qual mapa o usuário vai jogar
        '''
        self.scroll = 0
        self.sprite_group_config()
        self.mapa = Mapa(mapa_idx)
        self.add_personagens(mapa_idx)
        self.fim = False
    
    def add_personagens(self, mapa_idx: int) -> None:
        '''Cria os objetos respectivos ao personagem.
        
        Parâmetros:
            self.mapa_idx -> Valor que indica qual mapa o usuário vai jogar
        '''
        with open(os.path.join(DIRETORIO_MAPAS, f'Mapa {mapa_idx}/Data/personagens_pos.json').replace('\\', '/')) as arquivo:
            personagens_data = json.load(arquivo)
        for personagem in personagens_data:
            if personagem['personagem'] == 'capivara':
                self.personagem = CapivaraIsa(personagem['inicio'], personagem['life'], personagem['faceRight'], self.screen, self.sprite_group_inimigos, self.sprite_group_projeteis, self.mapa.sprite_group_superficie)
                self.sprite_group_personagem.add(self.personagem)
            if personagem['personagem'] == 'rato':
                self.sprite_group_inimigos.add(Rato(personagem['inicio'], personagem['life'], personagem['faceRight'], personagem['limites'], self.screen, self.sprite_group_personagem, self.sprite_group_projeteis, self.mapa.sprite_group_superficie))

    def sprite_group_config(self) -> None:
        '''Configura os grupos de sprites.'''
        self.sprite_group_personagem = pygame.sprite.GroupSingle()
        self.sprite_group_inimigos = pygame.sprite.Group()
        self.sprite_group_projeteis = pygame.sprite.Group()

    def update(self) -> None:
        '''Mantém o jogo atualizado constantemente.'''
        self.scroll_antes = self.scroll
        self.mapa.mover_cenario(self.scroll)
        self.sprites_update()
        self.deslocamento_cenario()
        self.corrigir_inimigo_pos()
        if len(self.sprite_group_inimigos) == 0:
            self.fim = True
    
    def sprites_update(self) -> None:
        '''Mantém as sprites atualizadas constantemente.'''
        self.mapa.draw_background(self.screen, self.scroll)
        self.mapa.draw_mapa(self.screen, self.scroll)
        self.sprite_group_personagem.update()
        self.sprite_group_inimigos.update()
        self.sprite_group_projeteis.update()
    
    def corrigir_inimigo_pos(self) -> None:
        '''Corrige a posição do inimigo enquanto o personagem se mexe.'''
        for inimigo in self.sprite_group_inimigos:
            inimigo.x_atual = inimigo.x_origin + self.scroll
            inimigo.x_pos -= self.scroll_antes - self.scroll
    
    def deslocamento_cenario(self) -> None:
        '''Move cenário em relação ao eixo x.'''
        if self.personagem.rect.left + 14 < 225 and not self.personagem.face_right or self.personagem.rect.right - 10 > 675 and self.personagem.face_right:
            self.scroll += -self.personagem.deslocamento_x
        if self.scroll > 0:
            self.scroll = 0
            if self.personagem.deslocamento_x != 0 and self.personagem.rect.left + 14 > 0:
                self.personagem.mover()
        if self.scroll < -self.mapa.width * TILE_SIZE // 2:
            self.scroll = -self.mapa.width * TILE_SIZE // 2
            if self.personagem.deslocamento_x != 0 and self.personagem.rect.right - 10 < LARGURA:
                self.personagem.mover()
    
    def draw(self) -> None:
        '''Desenha todas as sprites na tela.'''
        self.mapa.sprite_group_superficie.draw(self.screen) # Hum...
        self.sprite_group_personagem.draw(self.screen)
        self.sprite_group_inimigos.draw(self.screen)
        self.sprite_group_projeteis.draw(self.screen)
    
    def run(self) -> None:
        '''Carrega todas as funções da classe Level.'''
        self.update()
        self.draw()


# ============================= MAPA =============================
class Mapa:
    '''Configura e apresenta o mapa na tela.'''
    def __init__(self, mapa_idx: int):
        '''Método construtor.
        
        Parâmetros:
            mapa_idx -> Valor que indica qual mapa o usuário vai jogar
        '''
        self.carregar_mapa(mapa_idx)

    def carregar_mapa(self, mapa_idx: int) -> None:
        '''Carrega todas as variavéis do mapa.
        
        Parâmetros:
            mapa_idx -> Valor que indica qual mapa o usuário vai jogar
        '''
        self.mapa = load_pygame(os.path.join(DIRETORIO_MAPAS, f'Mapa {mapa_idx}/Data/tmx/Mapa.tmx').replace('\\', '/'))
        self.width, self.height = self.mapa.width, self.mapa.height
        self.sprite_group_superficie = pygame.sprite.Group()
        self.criar_tiles()
        self.background_config(mapa_idx)
    
    def criar_tiles(self) -> None:
        '''Cria os tiles respectivo ao mapa.'''
        layers = self.mapa.get_layer_by_name('Collision Block')
        for x, y, surface in layers.tiles():
            self.sprite_group_superficie.add(Tile((x * TILE_SIZE, y * TILE_SIZE), surface))
    
    def background_config(self, mapa_idx: int) -> None:
        '''Configura o background respectivo ao mapa escolhido.
        
        Parâmetros:
            mapa_idx -> Valor que indica qual mapa o usuário vai jogar
        '''
        self.background = pygame.image.load(os.path.join(DIRETORIO_MAPAS, f'Mapa {mapa_idx}/Assets/Backgrounds/background.jpg'.replace('\\', '/')))
        self.backgrounds = []
        vezes = self.width * TILE_SIZE // self.background.get_width()
        if vezes < 1:
            vezes = 1
        for n in range(vezes):
            self.backgrounds.append(self.background)

    def draw_mapa(self, screen: pygame.Surface, scroll: int) -> None:
        '''Desenha o mapa na tela.
        
        Parâmetros:
            screen -> Tela do jogo
            scroll -> Tela no eixo x
        '''
        for layer in self.mapa.layers:
            if layer.name != 'Collision Block' and hasattr(layer, 'data'):
                for x, y, surface in layer.tiles():
                    screen.blit(surface, (x * TILE_SIZE + scroll, y * TILE_SIZE))
        for objetos in self.mapa.objects:
            screen.blit(pygame.transform.rotate(objetos.image, -objetos.rotation), (objetos.x + scroll, objetos.y))
    
    def draw_background(self, screen: pygame.Surface, scroll: int) -> None:
        '''Desenha o Background na tela.
        
        Parâmetros:
            screen -> Tela do jogo
            scroll -> Tela no eixo x
        '''
        for idx, background in enumerate(self.backgrounds):
            screen.blit(background, (idx * background.get_width() + scroll // 4, 0))
    
    def mover_cenario(self, scroll: int) -> None:
        '''Move o cenário em relação ao scroll.
        
        Parâmetros:
            scroll -> Tela no eixo x'''
        for tile in self.sprite_group_superficie:
            tile.mover(scroll)


# ============================= TILE =============================
class Tile(pygame.sprite.Sprite):
    '''Representa os Tiles que compõem o mapa.
    
    Atibutos:
        self.image -> As imagens do conjunto de sprites
        self.rect -> Pega o ponto que se encontra o canto superior esquerdo da sprite
        self.rect_colision -> recebe a variável self.rect
        self.x_origin -> posição inicial do tile
    '''
    def __init__(self, pos: tuple, surface: pygame.Surface):
        '''Método construtor.

        Parâmetros:
            pos -> tupla que guarda o eixo x e y do mapa: (eixo_x, eixo_y) respectivamente
            surface -> Tela do jogo
        '''
        pygame.sprite.Sprite.__init__(self)
        self.image = surface
        self.rect = self.image.get_rect(topleft = pos)
        self.rect_colision = self.rect
        self.x_origin = pos[0]
    
    def mover(self, scroll: int) -> None:
        '''Move os tiles da grama de acordo com o scroll.

        Parâmetros:
            scroll -> Tela no eixo x
        '''
        self.rect.x = self.x_origin + scroll


# ============================= PERSONAGEM =============================
class Personagem(pygame.sprite.Sprite):
    '''Modela o personagens do jogo.
    
    Atributo:
        self.life -> Vida do personagem
        self.life_show -> Vida mostrada na tela
        self.max_life -> Vida máxima
        self.x_pos -> Posição no eixo x 
        self.y_pos -> Posição no eixo y
        self.face_right -> Se True deixa a imagem virada para direta. Se false deixa a imagem virada para a esquerda
    '''
    def __init__(self, pos: tuple, life: int, face_right: bool):
        '''Método construtor.

        Parâmetros:
            pos -> tupla que guarda o eixo x e y do mapa: (eixo_x, eixo_y)
            life -> vida do personagem
            face_right -> Se True deixa a imagem virada para direta. Se false deixa a imagem virada para a esquerda
        '''
        pygame.sprite.Sprite.__init__(self)
        self.life = life
        self.life_show = self.life
        self.max_life = self.life
        self.x_pos, self.y_pos = pos
        self.face_right = face_right
    
    def damage(self, dano: int) -> None:
        '''Desconta a vida do personagem principal com base no dano recebido.
        
        Parâmetros:
            dano -> Quantidade de dano
        '''
        if self.life > 0:
            self.life -= dano
    
    def draw_life_bar(self, display_surface: pygame.Surface, width: int) -> None:
        '''Desenha as barras de vida na tela.

        Parâmetros:
            display_surface -> Tela do jogo
            width -> largura da barra de vida
        '''
        if self.life_show > self.life:
            self.life_show -= 2
        pygame.draw.rect(display_surface, (48, 48, 64), (self.x_pos + 18, self.y_pos - 20, width, 16), border_radius=5) # Gambiarra...
        pygame.draw.rect(display_surface, (0, 255, 0), (self.x_pos + 18, self.y_pos - 20, self.life_show / self.max_life * width, 16), border_radius=5) # Gambiarra...
        pygame.draw.rect(display_surface, (48, 48, 64), (self.x_pos + 18, self.y_pos - 20, width, 16), 2, border_radius=5) # Gambiarra...


# ============================= PROJETEIS =============================
class Projeteis(pygame.sprite.Sprite):
    '''Modela os projéteis que serão utilizados nas armas.'''
    def __init__(self, dano: int):
        '''Método construtor.

        Parâmetros:
            dano -> Quantidade de dano que será usada
        '''
        pygame.sprite.Sprite.__init__(self)
        self.dano = dano
    
    def colisao(self, sprite_groups: pygame.sprite.GroupSingle | pygame.sprite.Group) -> bool:
        '''Verifica a colisão entre as sprites.

        Parâmetros:
            sprite_groups -> Grupo de sprites

        Retorna True se houve colisão. False se não houver colisão
        '''
        for sprite_group in sprite_groups:
            for item in pygame.sprite.spritecollide(self, sprite_group, False, pygame.sprite.collide_mask):
                if isinstance(item, Personagem):
                    item.damage(self.dano)
                return True
        return False


# ============================= SPRITE SHEET =============================
class SpriteSheet:
    '''Modela o conjunto de sprites.
    
    Atributos:
        width -> Largura da sprite sheet
        height -> Altura da sprite sheet
        self.sprite -> Conjunto de sprites
        self.sprite_flipped -> Conjunto de sprite virado ao contrário
    '''
    def __init__(self, sprite_sheet: str, size: int):
        '''Método construtor.
        
        Parâmetros:
            sprite_sheet -> Conjunto de sprites
            size -> Tamanho da sprite
        '''
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
        '''Pega o conjunto de sprites de acordo com a orientação.

        Parâmetros:
            flip -> Se False modela o cojunto de sprites virado para direita. Se True modela o conjunto de sprites virado para esquerda
        
        Retorna, se o flip for false, o cojunto de sprites virado para direita. Se o flip for True, o conjunto de sprites será virado para esquerda
        '''
        return self.sprite_flipped if flip else self.sprite


# ============================= CAPIVARA =============================
class CapivaraIsa(Personagem):
    '''Representa o personagem principal herdando os atributos e métodos da classe Personagem.
    
    Atributos:
        sprite_sheet_idle -> Conjunto de sprite parado
        sprite_sheet_run -> Conjunto de sprite correndo
        sprite_sheet_jump -> Conjunto de sprite pulando
        sprite_sheet_death -> Conjunto de sprite morrendo
        self.sprites_sheets -> Dicionário com o conjunto de spites e a sua respectiva velocidade de animação
        self.screen -> Tela do jogo
        self.sprite_group_inimigos -> Grupo de sprite dos inimigos
        self.sprite_group_projeteis -> Grupo de sprite dos projéteis
        self.sprite_group_superficie -> Grupo de sprite da superfície
        self.balas_cadencia -> cadência das balas
        self.image_idx -> Indica qual frame da animação será exibido. Por ser um valor float também dita a velocidade da animação.
        self.estado -> Qual estado o personagem se encontra
        self.speed_animation -> velocidade de transição da sprite
        self.velocidade_y -> velocidade no eixo y
        self.pulando -> Se True roda os conjuntos de sprites pulando
    '''
    def __init__(self, pos: tuple, life: int, face_right: bool, screen: pygame.Surface, sprite_group_inimigos: pygame.sprite.Group, sprite_group_projeteis: pygame.sprite.Group, sprite_group_superficie: pygame.sprite.Group):
        '''Método construtor.

        Parâmetros:
            pos -> tupla que guarda o eixo x e y do mapa: (eixo_x, eixo_y) respectivamente
            life -> vida do personagem principal
            face_right -> Se True deixa a imagem virada para direta. Se false deixa a imagem virada para a esquerda
            screen -> Tela do jogo
            sprite_group_inimigos -> Conjunto de sprites dos inimigos
            sprite_group_projeteis -> Conjunto de sprites dos projéteis
            sprite_group_superficie -> Conjunto de sprites dos Tiles
        '''
        Personagem.__init__(self, pos, life, face_right)
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
        '''Atualiza tudo relacionado a capivara.'''
        estado_antes = self.estado
        self.deslocamento_x = self.deslocamento_y = 0
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
            self.y_pos += self.deslocamento_y
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
        '''Faz a capivara pular.'''
        if (self.keys[pygame.K_w] or self.keys[pygame.K_UP] or self.keys[pygame.K_SPACE]) and not self.pulando and self.colisao()[1]:
            self.estado = 'JUMP'
            self.velocidade_y = -15
            self.pulando = True
    
    def exibicao_config(self) -> None:
        '''Define as configurações de exibição da sprite.'''
        if self.image_idx is not None:
            self.image = self.sprites_atual[int(self.image_idx)]
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect(topleft = (self.x_pos, self.y_pos))
            self.rect_colision = pygame.Rect(self.x_pos + 10, self.y_pos + 25, 75, 50)
    
    def trocar_estado(self) -> None:
        '''Troca o conjunto de sprites da capivara baseado no estado que ela se encontra.'''
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
        '''Seleciona a animação com base no estado do personagem (andando, pulando, parado ou morto).'''
        sprite_sheet = self.sprites_sheets[self.estado][0]
        self.speed_animation = self.sprites_sheets[self.estado][1]
        self.sprites_atual = sprite_sheet.get_sprites(not self.face_right)
    
    def atirar(self) -> None:
        '''Faz a capivara atirar modelando as munições usando a classe Bala.'''
        if self.keys[pygame.K_f] and self.balas_cadencia == 0:
            self.balas_cadencia = 5
            if self.face_right:
                self.sprite_group_projeteis.add(Bala((self.x_pos + 60, self.y_pos + 63), 28, 10, (12, 6),  [self.sprite_group_inimigos, self.sprite_group_superficie]))
            else:
                self.sprite_group_projeteis.add(Bala((self.x_pos + 40, self.y_pos + 63), -28, 10, (12, 6),  [self.sprite_group_inimigos, self.sprite_group_superficie]))
        if self.balas_cadencia > 0:
            self.balas_cadencia -= 1
    
    def gravidade(self) -> None:
        '''Altera a velocidade da capivara com base na gravidade do jogo.'''
        self.velocidade_y += GRAVIDADE
        self.deslocamento_y = self.velocidade_y
    
    def mover(self) -> None:
        '''Move a capivara modificando o valor do eixo x.'''
        self.x_pos += self.deslocamento_x
    
    def animar(self) -> None:
        '''Anima a sprites com base na animação selecionada.'''
        self.image_idx += self.speed_animation
        if self.image_idx >= len(self.sprites_atual) and self.estado != 'JUMP':
            self.image_idx = 0
        elif self.image_idx >= len(self.sprites_atual) and self.estado == 'JUMP':
            self.image_idx = 1
        if self.estado == 'JUMP' and self.velocidade_y > 0 and self.image_idx >= 8:
            self.image_idx = 5
    
    def colisao(self) -> list[bool]:
        '''Verifica se a capivara colide com os tiles do mapa ou com os inimigos.
        
        Retorna uma lista indicicando se a capivara colidiu com o chão ou com os inimigos, respectivamente'''
        colisions = [False, False]
        for group in [self.sprite_group_superficie, self.sprite_group_inimigos]:
            for sprite in group:
                if sprite.rect_colision.colliderect(self.rect_colision.x + self.deslocamento_x, self.rect_colision.y, self.rect_colision.width, self.rect_colision.height):
                    self.deslocamento_x = 0
                    colisions[0] = True
                elif sprite.rect_colision.colliderect(self.rect_colision.x, self.rect_colision.y + ceil(self.velocidade_y), self.rect_colision.width, self.rect_colision.height):
                    if self.velocidade_y > 0:
                        self.deslocamento_y = sprite.rect_colision.top - self.rect_colision.bottom
                        self.pulando = False
                    if self.velocidade_y < 0:
                        self.deslocamento_y = self.rect_colision.top - sprite.rect_colision.bottom
                    self.velocidade_y = 0
                    colisions[1] = True
        return colisions


# ============================= RATO =============================
class Rato(Personagem):
    '''Representa os inimigos herdando os atributos e métodos da classe Personagem.
    
    Atributos:
        sprite_sheet_run -> Conjunto de sprite correndo
        sprite_sheet_attack -> Conjunto de sprite atacando
        sprite_sheet_death -> Conjunto de sprite morrendo
        self.sprites_sheets -> Dicionário com o conjunto de spites e a sua respectiva velocidade de animação
        self.screen -> Tela do jogo
        self.sprite_group_personagem -> Conjunto de sprites do personagem principal
        self.sprite_group_projeteis -> Conjunto de sprites dos projéteis
        self.sprite_group_superficie -> Conjunto de sprites dos superfície
        self.balas_cadencia -> Cadência de balas
        self.image_idx -> Indica qual frame da animação será exibido. Por ser um valor float também dita a velocidade da animação.
        self.estado -> Qual estado o personagem se encontra
        self.x_origin -> Posição x inicial
        self.x_atual -> Posição x que o rato se encontra
        self.distancia -> distancia no eixo x na qual o rato irá se movimentar
        self.velocidade_y -> velocidade no eixo y
        self.deslocamento_x -> O quanto será deslocado no eixo x
    '''
    def __init__(self, pos: tuple, life: int, face_right: bool, limites: tuple, screen: pygame.Surface, sprite_group_personagem: pygame.sprite.GroupSingle, sprite_group_projeteis: pygame.sprite.Group, sprite_group_superficie: pygame.sprite.Group):
        '''Método construtor.

        Parâmetros:
            pos -> tupla que guarda o eixo x e y do mapa: (eixo_x, eixo_y) respectivamente
            life -> vida do inimigo
            face_right -> Se True deixa a imagem virada para direta. Se false deixa a imagem virada para a esquerda
            limites -> são os limites da movimentação do rato. (Baseado em intervalos, Ex: [500, 800])
            screen -> Tela do jogo
            sprite_group_personagem -> Conjunto de sprites do personagem principal
            sprite_group_projeteis -> Conjunto de sprites dos projéteis
            sprite_group_superficie -> Conjunto de sprites dos Tiles
        '''
        Personagem.__init__(self, pos, life, face_right)
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
        '''Atualiza tudo relacionado ao rato.'''
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
            self.colisao()
            self.mover()
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
        '''Muda a direção que o rato anda.'''
        if self.rect.left < self.x_atual:
            self.face_right = True
        elif self.rect.right > self.x_atual + self.distancia:
            self.face_right = False
        if self.face_right:
            self.deslocamento_x = VELOCIDADE // 2
        else:
            self.deslocamento_x = -VELOCIDADE // 2
    
    def exibicao_config(self) -> None:
        '''Define as configurações de exibição da sprite.'''
        if self.image_idx is not None:
            self.image = self.sprites_atual[int(self.image_idx)]
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect(topleft = (self.x_pos, self.y_pos))
            self.rect_colision = pygame.Rect(self.x_pos + 5, self.y_pos + 30, 90, 40)
    
    def select_animation(self) -> None:
        '''Seleciona a animação com base no estado do personagem (andando, atirando ou morto).'''
        sprite_sheet = self.sprites_sheets[self.estado][0]
        self.speed_animation = self.sprites_sheets[self.estado][1]
        self.sprites_atual = sprite_sheet.get_sprites(self.face_right)
    
    def gravidade(self) -> None:
        '''Altera a velocidade do rato com base na gravidade do jogo.'''
        self.velocidade_y += GRAVIDADE
        self.deslocamento_y = self.velocidade_y
    
    def animar(self) -> None:
        '''Anima a sprites com base na animação selecionada.'''
        self.image_idx += self.speed_animation
        if self.image_idx >= len(self.sprites_atual):
            self.image_idx = 0
    
    def mover(self) -> None:
        '''Move o rato modificando o valor do eixo x.'''
        self.x_pos += self.deslocamento_x
        self.y_pos += self.deslocamento_y
    
    def colisao(self) -> None:
        '''Verifica se o rato colide com os tiles do mapa ou com o personagem principal.'''
        for group in [self.sprite_group_superficie, self.sprite_group_personagem]:
            for sprite in group:
                if sprite.rect_colision.colliderect(self.rect_colision.x, self.rect_colision.y + ceil(self.velocidade_y), self.rect_colision.width, self.rect_colision.height):
                    if self.velocidade_y > 0:
                        self.deslocamento_y = sprite.rect_colision.top - self.rect_colision.bottom
                    self.velocidade_y = 0

    def atirar(self) -> None:
        '''Faz o rato atirar modelando as munições usando a classe Bala.'''
        for personagem in self.sprite_group_personagem:
            if personagem.y_pos <= self.rect.centery <= personagem.y_pos + 65 and (-250 < personagem.rect.centerx - self.rect.centerx < 0 and not self.face_right or 250 > personagem.rect.centerx - self.rect.centerx > 0 and self.face_right) and personagem.life > 0:
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
    '''Representa as munições usadas no jogo.
    
    Atributos:
        self.image -> As imagens do conjunto de sprites
        self.mask -> Cria uma máscara que ignora os pixels transparente para verificar se o projétil realmente se chocou com o personagem.
        self.rect -> Pega o ponto que se encontra o canto superior esquerdo da sprite
        self.sprite_group_inimigos -> Grupo de sprite dos inimigos
    '''
    def __init__(self, pos: tuple, velocidade: int, dano: int, size: tuple, sprite_group_inimigos: pygame.sprite.Group) -> None:
        '''Método construtor.
        
        Parâmetros:
            pos -> Tupla que guarda o eixo x e y do mapa: (eixo_x, eixo_y) respectivamente
            velocidade -> Velocidade da munição
            dano -> Quantidade de vida que será removida do alvo caso a bala o atinga
            size -> Tamanho da munição
            sprite_group_inimigos -> Conjunto de sprites dos inimigos
        '''
        Projeteis.__init__(self, dano)
        self.image = pygame.Surface(size)
        self.image.fill((255, 122, 0))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=pos)
        self.velocidade = velocidade
        self.sprite_group_inimigos = sprite_group_inimigos
    
    def update(self) -> None:
        '''Atualiza tudo relacionado a munição.'''
        self.rect.x += self.velocidade
        if self.rect.right < 0 or self.rect.left > LARGURA or self.colisao(self.sprite_group_inimigos):
            self.kill()
