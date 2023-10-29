import pygame
import a

def updateFish(image,i):
    gracz = image[i]
    gracz = pygame.transform.scale(gracz, (210, 210))
    return gracz

def updateShark(imageS,i):
    shark = imageS[i]
    #gracz = pygame.transform.scale(gracz, (210, 210))
    return shark