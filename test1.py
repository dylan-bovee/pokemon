import pygame
import random
from game import PokemonGame

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
LARGEUR = 800
HAUTEUR = 600
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Pokémon")

# Charger l'image de la carte
chemin_image = r"C:\Users\kizil\OneDrive\Documents\code\IA B1\Pokemon2\map\map.png"
image_carte = pygame.image.load(chemin_image)
image_carte = pygame.transform.scale(image_carte, (LARGEUR, HAUTEUR))

# Charger le sprite sheet de Red
chemin_sprite_sheet = r"C:\Users\kizil\OneDrive\Documents\code\IA B1\Pokemon2\red\AjFP5.png"
sprite_sheet = pygame.image.load(chemin_sprite_sheet)

# Découper le sprite sheet
NB_COLONNES = 4
NB_LIGNES = 4
LARGEUR_SPRITE = sprite_sheet.get_width() // NB_COLONNES
HAUTEUR_SPRITE = sprite_sheet.get_height() // NB_LIGNES
NOUVELLE_LARGEUR = 50
NOUVELLE_HAUTEUR = 50

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

sprites_red = decouper_et_redimensionner(sprite_sheet, LARGEUR_SPRITE, HAUTEUR_SPRITE, NB_COLONNES, NB_LIGNES, NOUVELLE_LARGEUR, NOUVELLE_HAUTEUR)

# Position initiale
x_red = LARGEUR // 2
y_red = HAUTEUR // 2
vitesse = 5
direction = 0
frame = 0
clock = pygame.time.Clock()

# Police
font = pygame.font.Font(None, 30)

# Définition de la zone de combat spécifique
combat_zone = pygame.Rect(95, 225, 20, 20)  # Rectangular zone for initial combat trigger
rencontre_zone = pygame.Rect(25, 295, 190, 90)  # Zone de rencontre avec un Pokémon
dans_dialogue = False
choix_dialogue = 0  # 0 = Oui, 1 = Non
sorti_zone_combat = True  # Vérifie si le joueur est sorti de la zone

def afficher_dialogue():
    pygame.draw.rect(fenetre, (255, 255, 255), (200, 400, 400, 100))
    texte = font.render("Voulez-vous commencer le combat ?", True, (0, 0, 0))
    fenetre.blit(texte, (220, 420))
    couleur_oui = (255, 0, 0) if choix_dialogue == 0 else (0, 0, 0)
    couleur_non = (255, 0, 0) if choix_dialogue == 1 else (0, 0, 0)
    texte_oui = font.render("Oui", True, couleur_oui)
    texte_non = font.render("Non", True, couleur_non)
    fenetre.blit(texte_oui, (250, 460))
    fenetre.blit(texte_non, (350, 460))

def fondu_noir():
    overlay = pygame.Surface((LARGEUR, HAUTEUR))
    overlay.fill((0, 0, 0))
    for alpha in range(0, 255, 10):
        overlay.set_alpha(alpha)
        fenetre.blit(image_carte, (0, 0))
        fenetre.blit(sprites_red[direction][frame], (x_red, y_red))
        fenetre.blit(overlay, (0, 0))
        pygame.display.flip()
        pygame.time.delay(50)

# Fonction pour vérifier la rencontre avec un Pokémon
def chance_de_rencontre():
    # Une probabilité de 1 sur 10 pour la rencontre avec un Pokémon
    return random.randint(1, 10) == 1

running = True
while running:
    clock.tick(10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if dans_dialogue:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    choix_dialogue = 0
                elif event.key == pygame.K_RIGHT:
                    choix_dialogue = 1
                elif event.key == pygame.K_RETURN:
                    if choix_dialogue == 0:
                        fondu_noir()
                        print("⚔️ Combat contre un Pokémon sauvage !")
                        combat = PokemonGame()
                        combat.run()  # Le combat commence ici
                        print("Retour à l'exploration")
                    dans_dialogue = False
                    sorti_zone_combat = False  # On empêche le dialogue de réapparaître immédiatement
    
    if not dans_dialogue:
        touches = pygame.key.get_pressed()
        moving = False
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

        x_red, y_red = new_x, new_y
        if moving:
            frame = (frame + 1) % 3 + 1
        else:
            frame = 0

        # Vérifie si le joueur est sorti de la zone
        if not combat_zone.collidepoint(x_red, y_red):
            sorti_zone_combat = True  

        # Active le dialogue seulement si le joueur est sorti avant de revenir
        if combat_zone.collidepoint(x_red, y_red) and sorti_zone_combat:
            dans_dialogue = True
            choix_dialogue = 0

        # Vérifier si le joueur est dans la zone de rencontre et s'il y a une chance de rencontre
        if rencontre_zone.collidepoint(x_red, y_red) and chance_de_rencontre():
            print("Un Pokémon sauvage apparaît !")
            fondu_noir()
            print("⚔️ Combat contre un Pokémon sauvage !")
            combat = PokemonGame()
            combat.run()  # Le combat commence ici

    fenetre.blit(image_carte, (0, 0))
    fenetre.blit(sprites_red[direction][frame], (x_red, y_red))

    if dans_dialogue:
        afficher_dialogue()
    
    pygame.display.flip()

pygame.quit()