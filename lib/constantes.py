import os


LARGURA, ALTURA = 960, 640
FPS = 60
GRAVIDADE = 0.7

# Usando o método `replace` para funcionar no Linux
DIRETORIO_PRINCIPAL = os.path.dirname(__file__).replace('\\', '/')
DIRETORIO_IMAGENS = os.path.join(DIRETORIO_PRINCIPAL, 'Images').replace('\\', '/')
DIRETORIO_MAPAS = os.path.join(DIRETORIO_PRINCIPAL, 'Mapas').replace('\\', '/')
DIRETORIO_MUSICAS = os.path.join(DIRETORIO_PRINCIPAL, 'Musics').replace('\\', '/')

VELOCIDADE = 4
TILE_SIZE = 64
