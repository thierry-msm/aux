import glfw
from OpenGL.GL import *

VELOCIDADE = 0.02

def inicializa_objetos():

    vermelho = {"x": -0.8,"y": -0.8,"tam": 0.15, "cor": (1.0, 0.0, 0.0)}

    azuis = [
        {"x": -0.2, "y": -0.2, "tam": 0.15, "cor": (0.0, 0.0, 1.0)},
        {"x": 0.3, "y": 0.4, "tam": 0.15, "cor": (0.0, 0.0, 1.0)}
    ]

    amarelos = [
        {"x": -0.7, "y": 0.6, "tam": 0.15, "cor": (1.0, 1.0, 0.0)},
        {"x": 0.6, "y": -0.35, "tam": 0.15, "cor": (1.0, 1.0, 0.0)}
    ]

    return vermelho, azuis, amarelos

def desenha_quadrado(x, y, tamanho, cor):
    glColor3f(*cor)

    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x + tamanho, y)
    glVertex2f(x + tamanho, y + tamanho)
    glVertex2f(x, y + tamanho)
    glEnd()

def renderiza(vermelho, azuis, amarelos):
    glClearColor(1, 1, 1, 1)
    glClear(GL_COLOR_BUFFER_BIT)

    glLoadIdentity()

    desenha_quadrado(vermelho["x"], vermelho["y"], vermelho["tam"], vermelho["cor"])
    desenha_quadrado(azuis[0]["x"], azuis[0]["y"], azuis[0]["tam"], azuis[0]["cor"])
    desenha_quadrado(azuis[1]["x"], azuis[1]["y"], azuis[1]["tam"], azuis[1]["cor"])
    desenha_quadrado(amarelos[0]["x"], amarelos[0]["y"], amarelos[0]["tam"], amarelos[0]["cor"])
    desenha_quadrado(amarelos[1]["x"], amarelos[1]["y"], amarelos[1]["tam"], amarelos[1]["cor"])

def verifica_colisao(obj_a, obj_b):
    return (obj_a["x"] < obj_b["x"] + obj_b["tam"] and
            obj_a["x"] + obj_a["tam"] > obj_b["x"] and
            obj_a["y"] < obj_b["y"] + obj_b["tam"] and
            obj_a["y"] + obj_a["tam"] > obj_b["y"])

def movimenta_vermelho(window, vermelho, azuis, amarelos):
    dx = 0
    dy = 0

    if glfw.get_key(window, glfw.KEY_LEFT) == glfw.PRESS:
        dx = -VELOCIDADE

    if glfw.get_key(window, glfw.KEY_RIGHT) == glfw.PRESS:
        dx = VELOCIDADE

    if glfw.get_key(window, glfw.KEY_UP) == glfw.PRESS:
        dy = VELOCIDADE

    if glfw.get_key(window, glfw.KEY_DOWN) == glfw.PRESS:
        dy = -VELOCIDADE

    # --- MOVIMENTO E COLISÃO HORIZONTAL (EIXO X) ---
    if dx != 0:
        proximo_x = vermelho["x"] + dx
        
        # Limite da tela para o vermelho
        if proximo_x < -1.0:
            proximo_x = -1.0
        elif proximo_x + vermelho["tam"] > 1.0:
            proximo_x = 1.0 - vermelho["tam"]
            
        vermelho_temp = {"x": proximo_x, "y": vermelho["y"], "tam": vermelho["tam"]}
        
        # Colisão com Amarelo (Obstáculo)
        for yellow in amarelos:
            if verifica_colisao(vermelho_temp, yellow):
                yellow["cor"] = (0.0, 1.0, 0.0) # Muda para Verde
                if dx > 0:
                    proximo_x = yellow["x"] - vermelho["tam"]
                else:
                    proximo_x = yellow["x"] + yellow["tam"]
                vermelho_temp["x"] = proximo_x
                
        # Colisão com Azul (Empurrar)
        for azul in azuis:
            if verifica_colisao(vermelho_temp, azul):
                if dx > 0:
                    proximo_azul_x = proximo_x + vermelho["tam"]
                    # Limite da tela para o azul
                    if proximo_azul_x + azul["tam"] > 1.0:
                        proximo_azul_x = 1.0 - azul["tam"]
                        proximo_x = proximo_azul_x - vermelho["tam"]
                    azul["x"] = proximo_azul_x
                else:
                    proximo_azul_x = proximo_x - azul["tam"]
                    # Limite da tela para o azul
                    if proximo_azul_x < -1.0:
                        proximo_azul_x = -1.0
                        proximo_x = proximo_azul_x + azul["tam"]
                    azul["x"] = proximo_azul_x
                    
        vermelho["x"] = proximo_x

    # --- MOVIMENTO E COLISÃO VERTICAL (EIXO Y) ---
    if dy != 0:
        proximo_y = vermelho["y"] + dy
        
        # Limite da tela para o vermelho
        if proximo_y < -1.0:
            proximo_y = -1.0
        elif proximo_y + vermelho["tam"] > 1.0:
            proximo_y = 1.0 - vermelho["tam"]
            
        vermelho_temp = {"x": vermelho["x"], "y": proximo_y, "tam": vermelho["tam"]}
        
        # Colisão com Amarelo (Obstáculo)
        for yellow in amarelos:
            if verifica_colisao(vermelho_temp, yellow):
                yellow["cor"] = (0.0, 1.0, 0.0) # Muda para Verde
                if dy > 0:
                    proximo_y = yellow["y"] - vermelho["tam"]
                else:
                    proximo_y = yellow["y"] + yellow["tam"]
                vermelho_temp["y"] = proximo_y
                
        # Colisão com Azul (Empurrar)
        for azul in azuis:
            if verifica_colisao(vermelho_temp, azul):
                if dy > 0:
                    proximo_azul_y = proximo_y + vermelho["tam"]
                    # Limite da tela para o azul
                    if proximo_azul_y + azul["tam"] > 1.0:
                        proximo_azul_y = 1.0 - azul["tam"]
                        proximo_y = proximo_azul_y - vermelho["tam"]
                    azul["y"] = proximo_azul_y
                else:
                    proximo_azul_y = proximo_y - azul["tam"]
                    # Limite da tela para o azul
                    if proximo_azul_y < -1.0:
                        proximo_azul_y = -1.0
                        proximo_y = proximo_azul_y + azul["tam"]
                    azul["y"] = proximo_azul_y
                    
        vermelho["y"] = proximo_y

    
def main():

    glfw.init()

    window = glfw.create_window(800, 800,"Questao 1", None, None)
    glfw.make_context_current(window)

    vermelho, azuis, amarelos = inicializa_objetos()

    while not glfw.window_should_close(window):
        glfw.poll_events()

        movimenta_vermelho(window, vermelho, azuis, amarelos)
        renderiza(vermelho, azuis, amarelos)

        glfw.swap_buffers(window)

    glfw.terminate()


if __name__ == "__main__":
    main()