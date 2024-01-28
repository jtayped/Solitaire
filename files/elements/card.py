import pygame
from ..misc.settings import *


class Card:
    def __init__(self, screen, image, pos, type: str, number: int, lookingBack=False) -> None:
        serif = pygame.font.SysFont(None, 40)
        arial = pygame.font.SysFont('arial', 30, True)

        self.screen = screen
        self.image = image

        self.type = type
        self.number = number
        self.isRed = self.isTypeRed(type)
        self.color = 'red' if self.isRed else 'black'

        self.letterSurface = None
        if number > 10 or number == 1:
            if number == 1:
                letter = 'A'
            
            else:
                letter = SPECIAL_TYPES[number-10]
            
            self.letterSurface = arial.render(letter, True, self.color)
            self.upsideDownLetter = pygame.transform.rotate(self.letterSurface, 180)
        
        self.numberSurface = serif.render(str(number), True, self.color)
        self.upsideDownNumber = pygame.transform.rotate(self.numberSurface, 180)

        self.lookingBack = lookingBack
        
        # Movement
        self.rect = pygame.Rect(pos[0], pos[1], CARD_SIZE[0], CARD_SIZE[1])
        self.lastMousePos = None
        self.drag = False
    
    def isTypeRed(self, typeOfCard):
        return typeOfCard == 'hearts' or typeOfCard == 'diamonds'
    
    def drawNumbers(self):
        spacer = CARD_RADIUS//2

        if self.letterSurface == None:
            surface = self.numberSurface
            upsideDown = self.upsideDownNumber
        else:
            surface = self.letterSurface
            upsideDown = self.upsideDownLetter


        left = self.rect.x + spacer
        right = self.rect.right - surface.get_width() - spacer
        
        top = self.rect.y + spacer
        bottom = self.rect.bottom - surface.get_height() - spacer


        self.screen.blit(surface, (left, top))
        self.screen.blit(surface, (right, top))

        self.screen.blit(upsideDown, (left, bottom))
        self.screen.blit(upsideDown, (right, bottom))

    def drawBehindPattern(self):
        behindPatternRect = pygame.Rect(self.rect.x+CARD_RADIUS, self.rect.y+CARD_RADIUS, self.rect.width-CARD_RADIUS*2, self.rect.height-CARD_RADIUS*2)
        pygame.draw.rect(self.screen, 'gray', behindPatternRect, 1, CARD_RADIUS//2)

    def drawCard(self):
        outlineRect = (self.rect.x-CARD_OUTLINE, self.rect.y-CARD_OUTLINE, self.rect.width+CARD_OUTLINE*2, self.rect.height+CARD_OUTLINE*2)
        pygame.draw.rect(self.screen, 'black', outlineRect, border_radius=CARD_RADIUS)

        if not self.lookingBack:
            pygame.draw.rect(self.screen, 'white', self.rect, border_radius=CARD_RADIUS)
            self.drawNumbers()

            imgX, imgY = self.rect.centerx-self.image.get_width()//2, self.rect.centery-self.image.get_height()//2
            self.screen.blit(self.image, (imgX, imgY))
        
        else:
            pygame.draw.rect(self.screen, 'red', self.rect, border_radius=CARD_RADIUS)
            self.drawBehindPattern()

    def update(self):
        self.drawCard()

    
    def __repr__(self) -> str:
        if self.type != None:
            return f'{self.number} of {self.type}'
        
        else:
            return f'{self.special}'