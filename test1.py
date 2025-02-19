import pygame

# Initialisation de Pygame
pygame.init()

# Définition des dimensions de la fenêtre
LARGEUR = 800
HAUTEUR = 600

# Création de la fenêtre
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Pokémon")

# Charger l'image de la carte
chemin_image = r"C:\Users\noach\OneDrive\Documents\pokemon\map\map.png"
image_carte = pygame.image.load(chemin_image)
image_carte = pygame.transform.scale(image_carte, (LARGEUR, HAUTEUR))

# Charger le sprite sheet de Red
chemin_sprite_sheet = r"C:\Users\noach\OneDrive\Documents\pokemon\red\AjFP5.png"
sprite_sheet = pygame.image.load(chemin_sprite_sheet)

# Dimensions du sprite sheet
NB_COLONNES = 4  # 4 sprites par ligne (immobile + 3 mouvements)
NB_LIGNES = 4    # 4 directions (face, gauche, droite, dos)
LARGEUR_SPRITE = sprite_sheet.get_width() // NB_COLONNES
HAUTEUR_SPRITE = sprite_sheet.get_height() // NB_LIGNES

# Nouvelle taille pour Red (plus petit)
NOUVELLE_LARGEUR = 50
NOUVELLE_HAUTEUR = 50

# Fonction pour découper et redimensionner le sprite sheet
def decouper_et_redimensionner(image, largeur_sprite, hauteur_sprite, nb_colonnes, nb_lignes, nouvelle_largeur, nouvelle_hauteur):
    sprites = []
    for y in range(nb_lignes):
        ligne_sprites = []
        for x in range(nb_colonnes):
            sprite = image.subsurface(pygame.Rect(
                x * largeur_sprite, y * hauteur_sprite, largeur_sprite, hauteur_sprite
            ))
            sprite_redimensionne = pygame.transform.scale(sprite, (nouvelle_largeur, nouvelle_hauteur))
            ligne_sprites.append(sprite_redimensionne)
        sprites.append(ligne_sprites)
    return sprites

# Découper et redimensionner les sprites
sprites_red = decouper_et_redimensionner(sprite_sheet, LARGEUR_SPRITE, HAUTEUR_SPRITE, NB_COLONNES, NB_LIGNES, NOUVELLE_LARGEUR, NOUVELLE_HAUTEUR)

# Position initiale de Red
x_red = LARGEUR // 2
y_red = HAUTEUR // 2
vitesse = 5 # Vitesse de déplacement

# Animation
direction = 0  # 0: Face | 1: Gauche | 2: Droite | 3: Dos
frame = 0  # Frame actuelle
clock = pygame.time.Clock()

# Fonction pour détecter les collisions basées sur l'image
def detecter_collision(x, y):
    # On vérifie la couleur du pixel à la position (x, y)
    pixel = image_carte.get_at((x, y))
    # Si le pixel est noir (par exemple), on considère que c'est un obstacle
    if pixel == (0, 0, 0):  # Tu peux adapter cette couleur en fonction de ton image
        return True
    return False

# Boucle principale
running = True
while running:
    clock.tick(10)  # Limite la vitesse d'animation à 10 FPS

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Gestion des touches
    touches = pygame.key.get_pressed()
    moving = False

    # Calcul des nouvelles positions avec les touches
    new_x, new_y = x_red, y_red

    if touches[pygame.K_LEFT]:
        new_x -= vitesse
        direction = 1
        moving = True
    if touches[pygame.K_RIGHT]:
        new_x += vitesse
        direction = 2
        moving = True
    if touches[pygame.K_UP]:
        new_y -= vitesse
        direction = 3
        moving = True
    if touches[pygame.K_DOWN]:
        new_y += vitesse
        direction = 0
        moving = True

    # Vérification de la collision avant de déplacer Red
    if not detecter_collision(new_x, new_y):
        x_red, y_red = new_x, new_y
        # Gérer l'animation (0 = immobile, 1-3 = marche)
        if moving:
            frame = (frame + 1) % 3 + 1  # Boucle entre 1 et 3
        else:
            frame = 0  # Revenir à la position statique

    # Afficher la carte et le sprite animé
    fenetre.blit(image_carte, (0, 0))
    fenetre.blit(sprites_red[direction][frame], (x_red, y_red))

    # Mettre à jour l'affichage
    pygame.display.flip()

# Quitter Pygame
pygame.quit()
