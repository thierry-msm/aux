#nave spritt
import glfw
from OpenGL.GL import *
from PIL import Image
import time

nave_x = 0.0
nave_y = 0
mov = 0
velocidade = 1
textura_nave = None
textura_fundo = None
delta = 0

def init():
    glClearColor(0, 0, 0, 1)
    # textura
    glEnable(GL_TEXTURE_2D)

def carregar_textura(caminho):

    imagem = Image.open(caminho)
    imagem = imagem.transpose(Image.FLIP_TOP_BOTTOM)

    img_data = imagem.convert("RGBA").tobytes()

    largura = imagem.width
    altura = imagem.height

    tex_id = glGenTextures(1)

    glBindTexture(GL_TEXTURE_2D, tex_id)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    glTexImage2D(
        GL_TEXTURE_2D,
        0,
        GL_RGBA,
        largura,
        altura,
        0,
        GL_RGBA,
        GL_UNSIGNED_BYTE,
        img_data
    )

    return tex_id


def desenhar_nave():
    glBindTexture(GL_TEXTURE_2D, textura_nave)

    glPushMatrix()
    glTranslatef(nave_x, nave_y, 0)
    glBegin(GL_QUADS)

    glTexCoord2f(0, 0)
    glVertex2f(-0.1, -1)

    glTexCoord2f(1, 0)
    glVertex2f(0.1, -1)

    glTexCoord2f(1, 1)
    glVertex2f(0.1, -0.8)

    glTexCoord2f(0, 1)
    glVertex2f(-0.1, -0.8)
    glEnd()
    glPopMatrix()

def desenhar_fundo():

    glBindTexture(GL_TEXTURE_2D, textura_fundo)

    glBegin(GL_QUADS)

    glTexCoord2f(0, 0)
    glVertex2f(-1, -1)

    glTexCoord2f(1, 0)
    glVertex2f(1, -1)

    glTexCoord2f(1, 1)
    glVertex2f(1, 1)

    glTexCoord2f(0, 1)
    glVertex2f(-1, 1)

    glEnd()


def atualizar():
    global nave_x
    nave_x += mov
    # limite da tela
    if nave_x < -0.9:
        nave_x = -0.9

    if nave_x > 0.9:
        nave_x = 0.9

def teclado(window):
    global mov
    keys = glfw.get_key
    if keys(window, glfw.KEY_LEFT) == glfw.PRESS:
        mov = acelerarDelta(-velocidade)
    elif keys(window, glfw.KEY_RIGHT) == glfw.PRESS:
        mov = acelerarDelta(velocidade)
    elif keys(window, glfw.KEY_LEFT) == glfw.RELEASE:              
        mov = 0
    elif keys(window, glfw.KEY_RIGHT) == glfw.RELEASE:
        mov = 0


def acelerarDelta(vel):
    global delta
    return vel*delta

def main():
    global textura_nave, delta, textura_fundo

    glfw.init()

    window = glfw.create_window(800, 600, "Nave com Teclado", None, None)
    glfw.make_context_current(window)

    # transparência
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    textura_nave = carregar_textura("img/nave.png")
    textura_fundo = carregar_textura("img/espaco.jpg")

    init()
    tempo_anterior = glfw.get_time()
    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT)

        tempo_atual = glfw.get_time()
        delta = tempo_atual - tempo_anterior
        tempo_anterior = tempo_atual
        teclado(window)
        atualizar()
        desenhar_fundo()
        desenhar_nave()

        glfw.swap_buffers(window)
        glfw.poll_events()
    glfw.terminate()


main()