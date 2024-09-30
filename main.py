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
        self.screen_config()
        self.menu_config()
        self.controls_config()
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
        self.btn_play = Button((240, ALTURA // 2 + 80), os.path.join(DIRETORIO_IMAGENS, 'Menu/btn_play_normal.png').replace('\\', '/'), os.path.join(DIRETORIO_IMAGENS, 'Menu/btn_play_hover.png').replace('\\', '/'), self.play)
        self.btn_controls = Button((240, ALTURA // 2 + 160), os.path.join(DIRETORIO_IMAGENS, 'Menu/btn_controls_normal.png').replace('\\', '/'), os.path.join(DIRETORIO_IMAGENS, 'Menu/btn_controls_hover.png').replace('\\', '/'), self.to_controls)

    def controls_config(self) -> None:
        '''Configura a tela de controles.'''
        self.background_controls = pygame.image.load(os.path.join(DIRETORIO_IMAGENS, 'Controls/Capybara.png').replace('\\', '/'))
        self.teclado_contros_img = pygame.image.load(os.path.join(DIRETORIO_IMAGENS, 'Controls/teclado.png').replace('\\', '/'))
        self.btn_menu_controls = Button((35, 35), os.path.join(DIRETORIO_IMAGENS, 'Buttons/btn_menu_normal.png').replace('\\', '/'), os.path.join(DIRETORIO_IMAGENS, 'Buttons/btn_menu_hover.png').replace('\\', '/'), self.to_menu)
    
    def menu(self) -> None:
        '''início do jogo.'''
        self.screen.blit(self.background_menu, self.background_menu.get_rect(center=(LARGURA // 2, ALTURA // 2)))
        self.screen.blit(self.title, self.title.get_rect(center=(240, 160)))
        self.btn_play.draw(self.screen)
        self.btn_controls.draw(self.screen)
    
    def controls(self) -> None:
        '''Tela de controles.'''
        self.screen.blit(self.background_controls, self.background_controls.get_rect(center=(LARGURA // 2, ALTURA // 2)))
        self.screen.blit(self.teclado_contros_img, self.teclado_contros_img.get_rect(center=(LARGURA // 2, ALTURA // 2)))
        self.btn_menu_controls.draw(self.screen)
    
    def estados(self) -> None:
        '''Controla os estados do jogo.'''
        match self.estado:
            case 'MENU':
                self.menu()
            case 'CONTROLES':
                self.controls()
            case 'JOGO':
                self.level.run()
                if self.level.fim:
                    if os.path.isdir(os.path.join(DIRETORIO_MAPAS, f'Mapa {self.mapa + 1}').replace('\\', '/')):
                        self.btn_next_level.draw(self.screen)
                    else:
                        self.btn_menu_extenso.draw(self.screen)
    
    def loop(self) -> None:
        '''Deixa o jogo rodando continuamente e o atualiza constantemente.'''
        self.mapa = 1
        self.level = Level(self.screen, self.mapa)
        self.btn_next_level = Button((LARGURA // 2, ALTURA // 2 + 240), os.path.join(DIRETORIO_IMAGENS, 'Buttons/btn_next_level_normal.png').replace('\\', '/'), os.path.join(DIRETORIO_IMAGENS, 'Buttons/btn_next_level_hover.png').replace('\\', '/'), self.to_next_level)
        self.btn_menu_extenso = Button((LARGURA // 2, ALTURA // 2 + 240), os.path.join(DIRETORIO_IMAGENS, 'Buttons/btn_menu_extenso_normal.png').replace('\\', '/'), os.path.join(DIRETORIO_IMAGENS, 'Buttons/btn_menu_extenso_hover.png').replace('\\', '/'), self.to_menu)
        self.game_music = pygame.mixer.Sound(os.path.join(DIRETORIO_MUSICAS,"Ost/Dracula's Castle.mp3").replace('\\', '/'))
        self.menu_music.play(-1) # -1 é para tocar em loop

        while True:
            self.screen.fill((235, 235, 235))
            self.clock.tick(FPS)
            self.eventos()
            self.estados()
            pygame.display.flip()

    def eventos(self) -> None:
        '''Analisa se o usário fechou o jogo ou não.'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()


if __name__ == '__main__':
    Game()
