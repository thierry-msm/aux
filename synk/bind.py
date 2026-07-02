#q1
import glfw
from OpenGL.GL import *
import math

# Variáveis globais para armazenar a posição e velocidade das naves
# Iniciamos com posições separadas em X para não começarem uma em cima da outra
x1 = -0.5
y1 = 0.0
vel_1 = 0.0
vel_rotate1 = 3.0
aceleraca_1 = 0.0005  # Ajustado para ficar suave igual ao exemplo 2
angulo_1 = 0.0

x2 = 0.5
y2 = 0.0
vel_2 = 0.0
vel_rotate2 = 3.0
aceleraca_2 = 0.0005  # Ajustado para ficar suave igual ao exemplo 2
angulo_2 = 0.0

vel_max = 0.1  # Limite máximo de velocidade suave
 

def init():
    glClearColor(0.0, 0.0, 0.0, 1.0) 

def render(window):
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    
    keys = glfw.get_key

    # --- DESENHAR NAVE 1 (Verde) ---
    glPushMatrix()
    glTranslatef(x1, y1, 0.0)
    glRotatef(angulo_1, 0.0, 0.0, 1.0)

    # Corpo da Nave 1 (Sempre visível)
    glBegin(GL_TRIANGLES)
    glColor3f(0.0, 1.0, 0.0) 
    glVertex2f(0.0, 0.1)     
    glVertex2f(-0.05, -0.05) 
    glVertex2f(0.05, -0.05)  
    glEnd()

    # Fogo da Nave 1 (Apenas quando acelera com UP)
    if keys(window, glfw.KEY_UP) == glfw.PRESS and vel_1 > 0:    
        glBegin(GL_TRIANGLES)
        glColor3f(1.0, 0.5, 0.0) 
        glVertex2f(0.0, -0.05)     
        glVertex2f(-0.03, -0.08) 
        glVertex2f(0.03, -0.08)  
        glEnd()
        
    glPopMatrix()  # Restaura o estado da matriz para não interferir na Nave 2


    # --- DESENHAR NAVE 2 (Azul) ---
    glPushMatrix()
    glTranslatef(x2, y2, 0.0)
    glRotatef(angulo_2, 0.0, 0.0, 1.0)

    # Corpo da Nave 2 (Sempre visível)
    glBegin(GL_TRIANGLES)
    glColor3f(0.0, 0.0, 1.0) 
    glVertex2f(0.0, 0.1)     
    glVertex2f(-0.05, -0.05) 
    glVertex2f(0.05, -0.05)  
    glEnd()

    # Fogo da Nave 2 (Apenas quando acelera com W)
    if keys(window, glfw.KEY_W) == glfw.PRESS and vel_2 > 0:
        glBegin(GL_TRIANGLES)
        glColor3f(1.0, 0.5, 0.0) 
        glVertex2f(0.0, -0.05)     
        glVertex2f(-0.03, -0.08) 
        glVertex2f(0.03, -0.08)  
        glEnd()
        
    glPopMatrix()  # Restaura o estado da matriz

def atualizarPosicaoNave1():         
    global x1, y1
    rad = math.radians(angulo_1 + 90)
    x1 += math.cos(rad) * vel_1
    y1 += math.sin(rad) * vel_1

def atualizarPosicaoNave2():
    global x2, y2
    rad = math.radians(angulo_2 + 90)
    x2 += math.cos(rad) * vel_2
    y2 += math.sin(rad) * vel_2

def moveNave1(window):
    global angulo_1, vel_1
    keys = glfw.get_key
    if keys(window, glfw.KEY_LEFT) == glfw.PRESS:
        angulo_1 += vel_rotate1
    if keys(window, glfw.KEY_RIGHT) == glfw.PRESS:
        angulo_1 -= vel_rotate1
    if keys(window, glfw.KEY_UP) == glfw.PRESS:
        vel_1 = min(vel_1 + aceleraca_1, vel_max)
    if keys(window, glfw.KEY_DOWN) == glfw.PRESS:
        vel_1 = max(vel_1 - aceleraca_1, 0.0)

def moveNave2(window):
    global angulo_2, vel_2
    keys = glfw.get_key
    if keys(window, glfw.KEY_A) == glfw.PRESS:
        angulo_2 += vel_rotate2
    if keys(window, glfw.KEY_D) == glfw.PRESS:
        angulo_2 -= vel_rotate2
    if keys(window, glfw.KEY_W) == glfw.PRESS:
        vel_2 = min(vel_2 + aceleraca_2, vel_max)
    if keys(window, glfw.KEY_S) == glfw.PRESS:
        vel_2 = max(vel_2 - aceleraca_2, 0.0)

def limitar_bordas():
    global x1, y1, x2, y2
    # Nave 1
    if x1 > 1.0: x1 = -1.0
    if x1 < -1.0: x1 = 1.0
    if y1 > 1.0: y1 = -1.0
    if y1 < -1.0: y1 = 1.0

    # Nave 2
    if x2 > 1.0: x2 = -1.0
    if x2 < -1.0: x2 = 1.0
    if y2 > 1.0: y2 = -1.0
    if y2 < -1.0: y2 = 1.0

def main():
    global angulo_1, angulo_2, vel_1, vel_2
    glfw.init()
    window = glfw.create_window(800, 600, "Nave Triangular (OpenGL Legacy) em DOBRO", None, None)
    glfw.make_context_current(window)

    glfw.swap_interval(1)  # Ativa o V-Sync para evitar oscilações na taxa de quadros
    init()
    while not glfw.window_should_close(window):
        glfw.poll_events()        
    
        moveNave1(window)
        moveNave2(window)
        atualizarPosicaoNave1()
        atualizarPosicaoNave2()
        limitar_bordas()  # Agora a função de limites é chamada no loop
        render(window)

        glfw.swap_buffers(window)
        glfw.wait_events_timeout(1.0/120.0)

    glfw.terminate()

if __name__ == "__main__":
    main()