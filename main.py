import pygame
from lib.constantes import *
from lib.classes import *


class Game(Funcionalidades):
    '''Modela o jogo inteiro.'''
    def __init__(self):
        '''Método construtor.'''
        pygame.init()
        pygame.mixer.init()
        self.estado = 'MENU'
        self.proximo_estado = self.estado
        self.screen_config()
        self.menu_config()
        self.controls_config()
        self.skins_config()
        self.loop()
    
    def screen_config(self) -> None:
        '''Configura a tela com largura, altura, nome e fps.'''
        self.screen = pygame.display.set_mode((LARGURA, ALTURA))
        pygame.display.set_caption('ADGP V1.0')
        self.clock = pygame.time.Clock()
    
    def menu_config(self) -> None:
        '''Configura o início do jogo.'''
        self.background_menu = pygame.image.load(os.path.join(DIRETORIO_IMAGENS, 'Menu/Capybara.png').replace('\\', '/'))
        self.menu_music = pygame.mixer.Sound(os.path.join(DIRETORIO_MUSICAS,"Ost/Treasury Room.mp3").replace('\\', '/'))
        self.title = pygame.image.load(os.path.join(DIRETORIO_IMAGENS, 'Menu/logo_title.png').replace('\\', '/'))
        self.btn_play = Button((240, ALTURA // 2 + 80), os.path.join(DIRETORIO_IMAGENS, 'Menu/btn_play.png').replace('\\', '/'), (280, 70), self.play)
        self.btn_controls = Button((240, ALTURA // 2 + 160), os.path.join(DIRETORIO_IMAGENS, 'Menu/btn_controls.png').replace('\\', '/'), (280, 70), self.to_controls)
        self.btn_skins = Button((240, ALTURA // 2 + 240), os.path.join(DIRETORIO_IMAGENS, 'Menu/btn_skins.png').replace('\\', '/'), (280, 70), self.to_select_skins)

    def controls_config(self) -> None:
        '''Configura a tela de controles.'''
        self.background_controls = pygame.image.load(os.path.join(DIRETORIO_IMAGENS, 'Controls/Capybara.png').replace('\\', '/'))
        self.teclado_contros_img = pygame.image.load(os.path.join(DIRETORIO_IMAGENS, 'Controls/teclado.png').replace('\\', '/'))
        self.btn_menu_controls = Button((35, 35), os.path.join(DIRETORIO_IMAGENS, 'Buttons/btn_menu.png').replace('\\', '/'), (66, 70), self.to_menu)
    
    def skins_config(self) -> None:
        '''Configurações da tela de selecionar skins.'''
        self.skins_list = ['normal', 'gold', 'astronauta', 'pirata', 'palhaço', 'ciro']
        self.skins_idx = 0
        self.skins_exibicao_idx = 0
        self.skin_selecionada = self.skins_list[self.skins_idx]
        self.skins_exibicao = SpriteSheet(os.path.join(DIRETORIO_IMAGENS, f'Skins/skins', f'{self.skins_list[self.skins_idx]}.png').replace('\\', '/'), (64, 64))
        self.skins_exibicao = self.skins_exibicao.get_sprites()
        self.background_skins = pygame.image.load(os.path.join(DIRETORIO_IMAGENS, 'Skins/Capybara.png').replace('\\', '/'))
        self.btn_menu_skins = Button((35, 35), os.path.join(DIRETORIO_IMAGENS, 'Buttons/btn_menu.png').replace('\\', '/'), (66, 70), self.to_menu)
        self.btn_anterior = Button((LARGURA // 2 - 180, ALTURA // 2), os.path.join(DIRETORIO_IMAGENS, 'Skins/btn_anterior.png').replace('\\', '/'), (66, 70), self.skin_anterior)
        self.btn_proximo = Button((LARGURA // 2 + 180, ALTURA // 2), os.path.join(DIRETORIO_IMAGENS, 'Skins/btn_proximo.png').replace('\\', '/'), (66, 70), self.proxima_skin)
        self.btn_select_skin = Button((LARGURA // 2, ALTURA // 2 + 160), os.path.join(DIRETORIO_IMAGENS, 'Skins/btn_select.png').replace('\\', '/'), (280, 70), self.selecionar_skins)
        self.img_selected = pygame.image.load(os.path.join(DIRETORIO_IMAGENS, 'Skins/img_selected.png').replace('\\', '/'))
    
    def menu(self) -> None:
        '''início do jogo.'''
        self.screen.blit(self.background_menu, self.background_menu.get_rect(center=(LARGURA // 2, ALTURA // 2)))
        self.screen.blit(self.title, self.title.get_rect(center=(240, 160)))
        self.btn_play.draw(self.screen)
        self.btn_controls.draw(self.screen)
        self.btn_skins.draw(self.screen)
    
    def controls(self) -> None:
        '''Tela de controles.'''
        self.screen.blit(self.background_controls, self.background_controls.get_rect(center=(LARGURA // 2, ALTURA // 2)))
        self.screen.blit(self.teclado_contros_img, self.teclado_contros_img.get_rect(center=(LARGURA // 2, ALTURA // 2)))
        self.btn_menu_controls.draw(self.screen)
    
    def skins(self) -> None:
        '''Tela de selecionar skins.'''
        self.screen.blit(self.background_skins, self.background_skins.get_rect(center=(LARGURA // 2, ALTURA // 2)))
        self.skins_exibicao_idx += 0.15
        if self.skins_exibicao_idx >= len(self.skins_exibicao):
            self.skins_exibicao_idx = 0
        img = pygame.transform.scale(self.skins_exibicao[int(self.skins_exibicao_idx)], (192, 192))
        self.screen.blit(img, img.get_rect(center=(LARGURA // 2, ALTURA // 2)))
        self.btn_menu_skins.draw(self.screen)
        self.btn_anterior.draw(self.screen)
        self.btn_proximo.draw(self.screen)
        if self.skin_selecionada != self.skins_list[self.skins_idx]:
            self.btn_select_skin.draw(self.screen)
        else:
            self.screen.blit(self.img_selected, self.img_selected.get_rect(center=(LARGURA // 2, ALTURA // 2 + 160)))
    
    def estados(self) -> None:
        '''Controla os estados do jogo.'''
        match self.estado:
            case 'MENU':
                self.menu()
            case 'CONTROLES':
                self.controls()
            case 'SKINS':
                self.skins()
            case 'JOGO':
                self.level.run()
                if self.level.fim:
                    if os.path.isdir(os.path.join(DIRETORIO_MAPAS, f'Mapa {self.mapa + 1}').replace('\\', '/')):
                        self.btn_next_level.draw(self.screen)
                    else:
                        self.btn_menu_extenso.draw(self.screen)
                elif self.level.personagem.image_idx is None: # Gambiarra...
                    self.btn_reset.draw(self.screen)
                else:
                    self.btn_pause.draw(self.screen)
    
    def transicoes(self) -> None:
        '''Transição entre telas.'''
        if Transition.close_circle(self.screen, 1):
            if self.proximo_estado != self.estado:
                self.estado = self.proximo_estado
            elif self.proximo_mapa != self.mapa:
                self.mapa = self.proximo_mapa
                self.level.carregar_level(self.mapa)
                self.level.personagem.set_skin(self.skin_selecionada)
            elif self.level.personagem.image_idx is None:
                self.level.carregar_level(self.mapa)
                self.level.personagem.set_skin(self.skin_selecionada)
            self.estado = self.proximo_estado
            Transition.new_open()
        Transition.open_circle(self.screen, 1)
    
    def loop(self) -> None:
        '''Deixa o jogo rodando continuamente e o atualiza constantemente.'''
        self.proximo_mapa = self.mapa = 1
        self.level = Level(self.screen, self.mapa)
        self.btn_next_level = Button((LARGURA // 2, ALTURA // 2 + 240), os.path.join(DIRETORIO_IMAGENS, 'Buttons/btn_next_level.png').replace('\\', '/'), (350, 70), self.to_next_level)
        self.btn_menu_extenso = Button((LARGURA // 2, ALTURA // 2 + 240), os.path.join(DIRETORIO_IMAGENS, 'Buttons/btn_menu_extenso.png').replace('\\', '/'), (280, 70), self.to_menu)
        self.btn_pause = Button((40, 40), os.path.join(DIRETORIO_IMAGENS, 'Buttons/btn_pausa.png').replace('\\', '/'), (50, 52), self.to_menu)
        self.btn_reset = Button((LARGURA // 2, ALTURA // 2 + 240), os.path.join(DIRETORIO_IMAGENS, 'Buttons/btn_reset.png').replace('\\', '/'), (280, 70), self.resetar_level)
        self.game_music = pygame.mixer.Sound(os.path.join(DIRETORIO_MUSICAS,"Ost/Dracula's Castle.mp3").replace('\\', '/'))
        self.menu_music.play(-1) # -1 é para tocar em loop

        while True:
            self.screen.fill((235, 235, 235))
            self.clock.tick(FPS)
            self.eventos()
            self.estados()
            self.transicoes()
            pygame.display.flip()

    def eventos(self) -> None:
        '''Analisa se o usário fechou o jogo ou não.'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()


if __name__ == '__main__':
    Game()
