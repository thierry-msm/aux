import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
import math

WIDTH = 1000
HEIGHT = 800

angulo_orbita = 0.0
angulo_rotacao = 0.0



# NÃO PRECISA MEXER NESSA FUNÇÃO
def carregar_textura(arquivo):
    imagem = Image.open(arquivo)
    imagem = imagem.transpose(Image.FLIP_TOP_BOTTOM)
    dados = imagem.convert("RGB").tobytes()
    textura = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, textura)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D,0,GL_RGB,imagem.width,imagem.height,0,GL_RGB,GL_UNSIGNED_BYTE,dados)

    return textura


# NÃO PRECISA MEXER NESSA FUNÇÃO
def desenha_esfera(textura, raio):

    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, textura)
    esfera = gluNewQuadric()
    gluQuadricTexture(esfera, GL_TRUE)
    gluQuadricNormals(esfera, GLU_SMOOTH)
    gluSphere(esfera, raio, 40, 40)
    gluDeleteQuadric(esfera)

    glDisable(GL_TEXTURE_2D)
 

# NÃO PRECISA MEXER NESSA FUNÇÃO
def inicializa():
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0) 
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK,GL_AMBIENT_AND_DIFFUSE)
    glClearColor(0, 0, 0, 1)
    luz_posicao = [0.0, 0.0, 0.0, 1.0]
    glLightfv(GL_LIGHT0, GL_POSITION, luz_posicao)

    global textura_sol
    global textura_terra

    textura_sol = carregar_textura("sol.jpg")
    textura_terra = carregar_textura("terra.jpg")


# NÃO PRECISA MEXER NESSA FUNÇÃO
def desenha_sol():
    glPushMatrix()
    glDisable(GL_LIGHTING)
    glTranslatef(-0.7, 0, 0)
    desenha_esfera(textura_sol, 0.15)
    glEnable(GL_LIGHTING)
    glPopMatrix()

# A QUESTÃO PODE SER REVOLVIDA TRABALHANDO APENAS NAS DUAS PRÓXIMAS FUNÇÕES
def desenha_terra():
    global angulo_orbita, angulo_rotacao
    glPushMatrix()
    
    # Translada para a posição do Sol (centro da órbita)
    glTranslatef(-0.7, 0, 0)
    
    # Rotaciona ao redor do Sol (órbita) no plano horizontal (eixo Y)
    glRotatef(angulo_orbita, 0, 1, 0)
    
    # Translada para o raio da órbita (a distância inicial era 0.8 - (-0.7) = 1.5)
    glTranslatef(1.5, 0, 0)
    
    # Rotaciona a Terra em torno do próprio eixo para maior realismo
    glRotatef(angulo_rotacao, 0, 1, 0)

    desenha_esfera(textura_terra, 0.08)

    glPopMatrix()

def atualiza():
    global angulo_orbita, angulo_rotacao
    # Atualiza os ângulos de órbita e rotação própria
    angulo_orbita = (angulo_orbita + 0.5) % 360
    angulo_rotacao = (angulo_rotacao + 2.0) % 360



# NÃO PRECISA MEXER NESSA FUNÇÃO - A NÃO SER QUE VOCÊ QUEIRA MEXER NA CÂMERA
def renderiza():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # CÂMERA FIXA OLHANDO PARA O CENTRO DO SISTEMA SOLAR
    gluLookAt(
        0, 2, 1,
        0, 0, 0,
        0, 1, 0
    )

    desenha_sol()
    desenha_terra()


# NÃO PRECISA MEXER NESSA FUNÇÃO
def main():
    glfw.init()
    window = glfw.create_window(WIDTH,HEIGHT,"Sistema Solar",None,None)
    glfw.make_context_current(window)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45,WIDTH / HEIGHT,0.1,100)

    inicializa()

    while not glfw.window_should_close(window):
        glfw.poll_events()

        atualiza()
        renderiza()

        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()