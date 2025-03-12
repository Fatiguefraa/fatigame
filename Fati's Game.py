import pygame
import random

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
ANCHO = 800
ALTO = 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Picnic en el Bosque Encantado")

# Cargar imágenes y ajustar tamaño
try:
    fondo = pygame.transform.scale(pygame.image.load("./img/bosque.png"), (ANCHO, ALTO))
    personaje = pygame.transform.scale(pygame.image.load("./img/personaje.png"), (50, 70))
    hada_img = pygame.transform.scale(pygame.image.load("./img/hada.png"), (40, 50))
    espejo_img = pygame.transform.scale(pygame.image.load("./img/espejo.png"), (60, 80))

    # Fondos de selección escalados
    lugar1 = pygame.transform.scale(pygame.image.load("./img/prado.png"), (ANCHO, ALTO))
    lugar2 = pygame.transform.scale(pygame.image.load("./img/claro_bosque.png"), (ANCHO, ALTO))
    lugar3 = pygame.transform.scale(pygame.image.load("./img/lago.png"), (ANCHO, ALTO))
except pygame.error as e:
    print(f"Error al cargar las imágenes: {e}")
    pygame.quit()
    exit()

# Cargar sonidos
try:
    sonido_viento = pygame.mixer.Sound("./music/viento.wav")
    sonido_hojas = pygame.mixer.Sound("./music/hojas.wav")
    sonido_agua = pygame.mixer.Sound("./music/agua.wav")

    sonidos = [sonido_viento, sonido_hojas, sonido_agua]

    pygame.mixer.music.load("./music/Forest.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
except pygame.error as e:
    print(f"Error al cargar los sonidos o la música: {e}")
    pygame.quit()
    exit()

# Obtener el nombre del personaje
def pantalla_inicio():
    nombre = ""
    fuente = pygame.font.Font(None, 36)
    reloj = pygame.time.Clock()

    while True:
        pantalla.fill((0, 0, 0))
        texto_intro = fuente.render("Introduce el nombre de tu personaje:", True, (255, 255, 255))
        pantalla.blit(texto_intro, (200, 200))
        texto_nombre = fuente.render(nombre, True, (255, 255, 255))
        pantalla.blit(texto_nombre, (200, 250))

        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_BACKSPACE:
                    nombre = nombre[:-1]
                elif evento.key == pygame.K_RETURN and nombre != "":
                    return nombre
                elif len(nombre) < 15:
                    nombre += evento.unicode

        reloj.tick(30)

# Mostrar introducción
def mostrar_introduccion():
    fuente = pygame.font.Font(None, 36)
    pantalla.fill((0, 0, 0))
    texto1 = fuente.render("Bienvenida a Picnic en el Bosque Encantado.", True, (255, 255, 255))
    texto2 = fuente.render("Buscas el lugar ideal para tu picnic,", True, (255, 255, 255))
    texto3 = fuente.render("y en tu aventura encuentras un espejo mágico.", True, (255, 255, 255))
    texto4 = fuente.render("Un hada aparece y te dice:", True, (255, 255, 255))
    texto5 = fuente.render('"Este espejo te mostrará el lugar perfecto."', True, (255, 255, 255))

    pantalla.blit(texto1, (100, 150))
    pantalla.blit(texto2, (100, 200))
    pantalla.blit(texto3, (100, 250))
    pantalla.blit(texto4, (100, 300))
    pantalla.blit(texto5, (100, 350))

    pygame.display.update()
    pygame.time.delay(5000)

# Nombre del personaje
nombre_personaje = pantalla_inicio()

# Mostrar introducción
mostrar_introduccion()

# Posiciones iniciales
x_personaje = 100
y_personaje = 400
velocidad = 5
modo_seleccion = False
indice_lugar = 0
seleccion_confirmada = False

# Opciones de lugares
lugares = [lugar1, lugar2, lugar3]

# Bucle del juego
ejecutando = True
while ejecutando:
    pygame.time.delay(50)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

    teclas = pygame.key.get_pressed()

    if modo_seleccion:
        pantalla.fill((0, 0, 0))
        pantalla.blit(lugares[indice_lugar], (0, 0))
        fuente = pygame.font.Font(None, 36)
        texto = fuente.render("Usa ← → para elegir, Enter para confirmar", True, (255, 255, 255))
        pantalla.blit(texto, (150, 500))

        if teclas[pygame.K_LEFT] and indice_lugar > 0:
            indice_lugar -= 1
            pygame.time.delay(200)
        if teclas[pygame.K_RIGHT] and indice_lugar < len(lugares) - 1:
            indice_lugar += 1
            pygame.time.delay(200)
        if teclas[pygame.K_RETURN]:
            seleccion_confirmada = True
            modo_seleccion = False
            sonidos[indice_lugar].play()

    elif seleccion_confirmada:
        pygame.mixer.music.stop()
        pantalla.fill((0, 0, 0))
        pantalla.blit(lugares[indice_lugar], (0, 0))
        fuente = pygame.font.Font(None, 36)
        texto = fuente.render(f"¡Este es el lugar perfecto para tu picnic, {nombre_personaje}!", True, (255, 255, 255))
        pantalla.blit(texto, (100, 500))
        pantalla.blit(hada_img, (350, 250))
        pygame.display.update()
        pygame.time.delay(5000)
        pygame.quit()
        exit()

    else:
        # Dibujar el bosque y el personaje
        pantalla.blit(fondo, (0, 0))
        pantalla.blit(personaje, (x_personaje, y_personaje))
        pantalla.blit(hada_img, (500, 220))
        pantalla.blit(espejo_img, (600, 400))

        # Movimiento del personaje
        if teclas[pygame.K_LEFT]:
            x_personaje -= velocidad
        if teclas[pygame.K_RIGHT]:
            x_personaje += velocidad
        if teclas[pygame.K_UP]:
            y_personaje -= velocidad
        if teclas[pygame.K_DOWN]:
            y_personaje += velocidad

        # Restringir movimiento dentro de la pantalla
        x_personaje = max(0, min(ANCHO - 50, x_personaje))
        y_personaje = max(0, min(ALTO - 70, y_personaje))

        # Mostrar mensaje cuando el personaje está cerca del espejo
        if x_personaje > 550:
            fuente = pygame.font.Font(None, 36)
            texto = fuente.render("Presiona 'E' para mirar el espejo", True, (255, 255, 255))
            pantalla.blit(texto, (250, 50))
            if teclas[pygame.K_e]:
                modo_seleccion = True

    pygame.display.update()

pygame.quit()