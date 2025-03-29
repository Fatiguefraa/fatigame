
'''El contexto de mi juego se basa en que el jugador toma el papel de una joven que ha preparado un picnic
 y ha decidido ir a un bosque encantado en busca del lugar ideal para disfrutarlo. Mientras recoge flores en el bosque,
ecuentra un espejo mágico. Este espejo no es un objeto cualquiera, 
   pues tiene el poder de mostrarle el sitio perfecto para su picnic.

Justo en ese momento, aparece una pequeña hada con alas blancas,
el hada le explica que el espejo puede ayudarla a encontrar el mejor lugar.
 Así comienza su aventura, guiada por el hada, en busca de ese lugar especial donde podrá disfrutar de su picnic. '''
import pygame

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
    personaje = pygame.transform.scale(pygame.image.load("./img/personaje.png"), (130, 100))  # Imagen de personaje mejorada
    hada_img = pygame.transform.scale(pygame.image.load("./img/hada.png"), (40, 50))
    espejo_img = pygame.transform.scale(pygame.image.load("./img/espejo.png"), (60, 80))
    flor_img = pygame.transform.scale(pygame.image.load("./img/flor.png"), (40, 40))  # Imagen de la flor

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
    sonido_agua = pygame.mixer.Sound("./music/agua.wav")  # Sonido fijo de agua

    # Cargar la música de fondo de "hojas"
    pygame.mixer.music.load("./music/sound.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)  # Reproduce de forma indefinida
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
        texto_intro = fuente.render("Introduce el nombre de tu personaje:", True, (211, 211, 211))  # Gris claro
        pantalla.blit(texto_intro, (200, 200))
        texto_nombre = fuente.render(nombre, True, (211, 211, 211))  # Gris claro
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
    
    # Mantener el fondo en cada ciclo
    pantalla.blit(fondo, (0, 0))

    # Mostrar el texto encima del fondo con color gris claro
    texto1 = fuente.render("Bienvenida a Picnic en el Bosque Encantado.", True, (211, 211, 211))  # Gris claro
    texto2 = fuente.render("Buscas el lugar ideal para tu picnic,", True, (211, 211, 211))  # Gris claro
    texto3 = fuente.render("y en tu aventura encuentras un espejo mágico.", True, (211, 211, 211))  # Gris claro
    texto4 = fuente.render("Un hada aparece y te dice:", True, (211, 211, 211))  # Gris claro
    texto5 = fuente.render('"Este espejo te mostrará el lugar perfecto."', True, (211, 211, 211))  # Gris claro

    # Blit de los textos
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

# Crear una lista de flores con posiciones fijas
flores_posiciones = [
    pygame.Rect(250, 430, 40, 40),  # Flor en la posición (250, 430)
    pygame.Rect(120, 500, 40, 40),  # Flor en la posición (120, 500)
    pygame.Rect(380, 520, 40, 40),  # Flor en la posición (380, 520)
    pygame.Rect(620, 479, 40, 40),  # Flor en la posición (620, 479)
]

# Inventario de flores recogidas
flores_recogidas = 0

# Bucle del juego
ejecutando = True
while ejecutando:
    pygame.time.delay(50)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

    teclas = pygame.key.get_pressed()

    if modo_seleccion:
        # Fase de selección de lugar
        pantalla.fill((0, 0, 0))
        pantalla.blit(lugares[indice_lugar], (0, 0))
        fuente = pygame.font.Font(None, 36)
        texto = fuente.render("Usa ← → para elegir, Enter para confirmar", True, (211, 211, 211))  # Gris claro
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
            sonido_agua.play()  # Mantener siempre el sonido de agua

    elif seleccion_confirmada:
        # El lugar ha sido seleccionado, mostrar la confirmación
        pygame.mixer.music.stop()
        pantalla.fill((0, 0, 0))
        pantalla.blit(lugares[indice_lugar], (0, 0))
        fuente = pygame.font.Font(None, 36)
        texto = fuente.render(f"¡Este es el lugar perfecto para tu picnic, {nombre_personaje}!", True, (211, 211, 211))  # Gris claro
        pantalla.blit(texto, (100, 500))
        pantalla.blit(hada_img, (350, 250))
        pygame.display.update()

        # Restablecer la posición del personaje en el nuevo lugar
        x_personaje = 100
        y_personaje = 400

        # Fin del juego después de la selección del lugar
        pygame.time.delay(4000)  # Pausa antes de finalizar
        break  # Finaliza el juego

    else:
        # Fase de recolección de flores
        pantalla.blit(fondo, (0, 0))
        pantalla.blit(personaje, (x_personaje, y_personaje))
        pantalla.blit(hada_img, (500, 220))

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
        x_personaje = max(0, min(ANCHO - 100, x_personaje))  # Ajustado para el tamaño del personaje
        y_personaje = max(0, min(ALTO - 140, y_personaje))  # Ajustado para el tamaño del personaje

        # Crear el rectángulo del personaje para colisión
        rect_personaje = pygame.Rect(x_personaje, y_personaje, 130, 100)  # Tamaño del personaje

        # Dibujar las flores en el mapa
        for flor in flores_posiciones[:]:
            pantalla.blit(flor_img, (flor.x, flor.y))

            # Verificar si el personaje recoge la flor
            if rect_personaje.colliderect(flor):  # Verifica si el rectángulo del personaje toca la flor
                flores_recogidas += 1
                flores_posiciones.remove(flor)  # Eliminar la flor del mapa
                print(f"Flores recogidas: {flores_recogidas}")

        # Mostrar mensaje de flores recogidas
        fuente = pygame.font.Font(None, 36)
        texto = fuente.render(f"Flores recogidas: {flores_recogidas}", True, (211, 211, 211))  # Gris claro
        pantalla.blit(texto, (10, 50))

        # Mostrar el espejo cuando todas las flores han sido recogidas
        if flores_recogidas == 4:  # Solo si todas las flores están recogidas
            pantalla.blit(espejo_img, (600, 400))  # Solo aparece cuando todas las flores están recogidas

            # Mostrar mensaje para interactuar con el espejo
            if x_personaje > 550:  # Verificar si está cerca del espejo
                fuente = pygame.font.Font(None, 36)
                texto = fuente.render("Presiona 'E' para mirar el espejo", True, (211, 211, 211))  # Gris claro
                pantalla.blit(texto, (400, 350))
                if teclas[pygame.K_e]:
                    modo_seleccion = True

    pygame.display.update()

pygame.quit()
