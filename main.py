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
        self.zerado = False
        self.proximo_estado = self.estado
        self.screen_config()
        self.menu_config()
        self.controls_config()
        self.skins_config()
        self.credits_config()
        self.select_mapa_config()
        self.loop()
    
    def screen_config(self) -> None:
        '''Configura a tela com largura, altura, nome e fps.'''
        self.screen = pygame.display.set_mode((LARGURA, ALTURA))
        pygame.display.set_caption('Operation Capybara: Tactical Strike Beta')
        pygame.display.set_icon(pygame.image.load(os.path.join(DIRETORIO_IMAGENS, 'icon.png')))
        self.clock = pygame.time.Clock()
    
    def menu_config(self) -> None:
        '''Configura o início do jogo.'''
        self.background_menu = pygame.image.load(os.path.join(DIRETORIO_IMAGENS, 'Menu/Capybara.png').replace('\\', '/'))
        self.menu_music = pygame.mixer.Sound(os.path.join(DIRETORIO_MUSICAS,"Ost/Treasury Room.mp3").replace('\\', '/'))
        self.title = pygame.image.load(os.path.join(DIRETORIO_IMAGENS, 'Menu/logo_title.png').replace('\\', '/'))
        self.btn_play = Button((240, ALTURA // 2 + 20), os.path.join(DIRETORIO_IMAGENS, 'Menu/btn_play.png').replace('\\', '/'), (280, 70), self.to_select_mapa)
        self.btn_new_game = Button((240, ALTURA // 2 + 20), os.path.join(DIRETORIO_IMAGENS, 'Menu/btn_new_game.png').replace('\\', '/'), (280, 70), self.new_game)
        self.btn_controls = Button((240, ALTURA // 2 + 100), os.path.join(DIRETORIO_IMAGENS, 'Menu/btn_controls.png').replace('\\', '/'), (280, 70), self.to_controls)
        self.btn_skins = Button((240, ALTURA // 2 + 180), os.path.join(DIRETORIO_IMAGENS, 'Menu/btn_skins.png').replace('\\', '/'), (280, 70), self.to_select_skins)
        self.btn_credits = Button((240, ALTURA // 2 + 260), os.path.join(DIRETORIO_IMAGENS, 'Menu/btn_credits.png').replace('\\', '/'), (280, 70), self.to_credits)

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
    
    def credits_config(self) -> None:
        '''Configurações da tela de créditos.'''
        self.credits_image = pygame.image.load(os.path.join(DIRETORIO_IMAGENS, 'Credits/Credits.png').replace('\\', '/'))
        self.axis_y_credits = ALTURA
        self.btn_menu_credits = Button((35, 35), os.path.join(DIRETORIO_IMAGENS, 'Buttons/btn_menu.png').replace('\\', '/'), (66, 70), self.to_menu)
    
    def select_mapa_config(self) -> None:
        '''Configurações da tela de seleção de mapa.'''
        self.background_select_mapa = pygame.image.load(os.path.join(DIRETORIO_IMAGENS, 'Select Mapa/Capybara.png').replace('\\', '/'))
        self.btn_menu_select_mapa = Button((35, 35), os.path.join(DIRETORIO_IMAGENS, 'Buttons/btn_menu.png').replace('\\', '/'), (66, 70), self.to_menu)
        self.mapa_atual = 1
        self.buttons_list = []
        for idx, diretorio in enumerate(os.listdir(DIRETORIO_MAPAS)):
            self.buttons_list.append(Button((idx * 264 + 216, ALTURA // 2 - 80), os.path.join(DIRETORIO_MAPAS, diretorio, 'Assets/btn_mapa.png').replace('\\', '/'), (96, 96), lambda : None)) # Função vazia 🙃
    
    def menu(self) -> None:
        '''início do jogo.'''
        self.screen.blit(self.background_menu, self.background_menu.get_rect(center=(LARGURA // 2, ALTURA // 2)))
        self.screen.blit(self.title, self.title.get_rect(center=(240, 160)))
        if not self.zerado:
            self.btn_play.draw(self.screen)
        else:
            self.btn_new_game.draw(self.screen)
        self.btn_controls.draw(self.screen)
        self.btn_skins.draw(self.screen)
        self.btn_credits.draw(self.screen)
    
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
    
    def credits(self) -> None:
        '''Tela dos créditos.'''
        self.screen.blit(self.credits_image, (0, self.axis_y_credits))
        self.btn_menu_credits.draw(self.screen)
        if self.axis_y_credits >= -self.credits_image.get_height():
            self.axis_y_credits -= 1
        elif self.proximo_estado == 'CREDITS':
            if self.mapa == len(os.listdir(DIRETORIO_MAPAS)):
                self.zerado = True
            self.proximo_estado = 'MENU'
            Transition.new_close()
    
    def select_mapa(self) -> None:
        '''Tela de seleção de mapa.'''
        self.screen.blit(self.background_select_mapa, self.background_select_mapa.get_rect(center=(LARGURA // 2, ALTURA // 2)))
        self.btn_menu_select_mapa.draw(self.screen)
        for idx, button in enumerate(self.buttons_list):
            if idx in range(self.mapa_atual):
                button.draw(self.screen)
                if button.click and self.proximo_estado == 'SELECT MAPA':
                    self.proximo_mapa = idx + 1
                    self.play()
            else:
                img = pygame.image.load(os.path.join(DIRETORIO_MAPAS, f'Mapa {idx + 1}/Assets/btn_mapa_bloqueado.png').replace('\\', '/'))
                self.screen.blit(img, img.get_rect(center=(idx * 264 + 216, ALTURA // 2 - 80)))

    def estados(self) -> None:
        '''Controla os estados do jogo.'''
        match self.estado:
            case 'MENU':
                self.menu()
            case 'CONTROLES':
                self.controls()
            case 'SKINS':
                self.skins()
            case 'CREDITS':
                self.credits()
            case 'SELECT MAPA':
                self.select_mapa()
            case 'JOGO':
                self.level.run()
                if self.level.fim:
                    if os.path.isdir(os.path.join(DIRETORIO_MAPAS, f'Mapa {self.mapa + 1}').replace('\\', '/')):
                        if self.mapa == self.mapa_atual:
                            self.to_next_level()
                    elif self.proximo_estado == 'JOGO':
                        self.to_credits()
                elif self.level.personagem.image_idx is None: # Gambiarra...
                    self.btn_reset.draw(self.screen)
                else:
                    self.btn_pause.draw(self.screen)
    
    def transicoes(self) -> None:
        '''Transição entre telas.'''
        if Transition.close_circle(self.screen, 1):
            if self.proximo_mapa != self.mapa:
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
        self.btn_menu_extenso = Button((LARGURA // 2, ALTURA // 2 + 240), os.path.join(DIRETORIO_IMAGENS, 'Buttons/btn_menu_extenso.png').replace('\\', '/'), (280, 70), self.to_menu)
        self.btn_pause = Button((40, 40), os.path.join(DIRETORIO_IMAGENS, 'Buttons/btn_pausa.png').replace('\\', '/'), (50, 52), self.to_menu)
        self.btn_reset = Button((LARGURA // 2, ALTURA // 2 + 240), os.path.join(DIRETORIO_IMAGENS, 'Buttons/btn_reset.png').replace('\\', '/'), (280, 70), self.resetar_level)
        self.game_music = pygame.mixer.Sound(os.path.join(DIRETORIO_MUSICAS, 'Ost/Dracula\'s Castle.mp3').replace('\\', '/'))
        self.menu_music.play(-1) # -1 é para tocar em loop

        while True:
            self.screen.fill('black')
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
