import pygame, sys, random, os
from ..misc.settings import *
from ..elements.card import Card


class Level:
    def __init__(self, screen, clock) -> None:
        # Init
        self.screen, self.clock = screen, clock

        # Game Loop Vars
        self.gameOver = False
        self.click = False

        self.background = pygame.image.load('files/assets/background.jpg')
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))

        self.icons = self.loadIcons()
        
        self.cardDummy = Card(self.screen, self.icons['clubs'], (SPACER, SPACER), 'clubs', 1, lookingBack=True)

        self.cardPositions = {}
        self.initCardPositions()

        self.selectedCard = None
        self.lastMousePos = None

    
    def events(self):
        self.click = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.click = True
    
    def loadIcons(self):
        iconsDir = 'files/assets/icons/'
        icons = {}

        for icon in os.listdir(iconsDir):
            iconName = icon.split('.')[0] # get icon name without ".png"

            image = pygame.image.load(iconsDir+icon)
            icons[iconName] = pygame.transform.scale_by(image, 0.01)
        
        return icons

    def drawCard(self, x, y):
        number = random.randint(2, 10)
        hiddenBuffer = self.cardPositions['buffer']['hidden']

        type = random.choice(list(hiddenBuffer.keys()))
        number = random.choice(hiddenBuffer[type])

        hiddenBuffer[type].remove(number)
        if len(hiddenBuffer[type]) == 0:
            del hiddenBuffer[type]
        
        image = self.icons[type]

        card = Card(self.screen, image, (x, y), type, number, lookingBack=False)
        return card

    def initBuffer(self):
        return {'hidden': CARDS, 'visible': []}

    def initPlayingArea(self):
        playingArea = []
        hiddenCards = self.cardPositions['buffer']['hidden']

        for i in range(N_COLUMNS):
            cx = i*cardWidth + (i+1)*SPACER
            col = []
            
            for j in range(i+1):
                cy = DEALING_SPACE+j*Y_SPACE_CARDS
                number = random.randint(2, 10)

                type = random.choice(list(hiddenCards.keys()))
                number = random.choice(hiddenCards[type])

                hiddenCards[type].remove(number)
                if len(hiddenCards[type]) == 0:
                    del hiddenCards[type]
                
                image = self.icons[type]

                card = Card(self.screen, image, (cx, cy), type, number, lookingBack=(j < i))
                col.append(card)

            playingArea.append(col)

        return playingArea
    
    def initHolders(self):
        holders = []
        for i in range(N_CARD_HOLDERS):
            holders.append([])
        
        return holders

    def initCardPositions(self):
        self.cardPositions['buffer'] = self.initBuffer()
        self.cardPositions['holders'] = self.initHolders()
        self.cardPositions['playingArea'] = self.initPlayingArea()

    def selectCard(self, mx, my):
        playingArea = self.cardPositions['playingArea']

        for columnIndex,column in enumerate(playingArea):
            for cardIndex,card in enumerate(column):

                if not card.lookingBack and card.rect.collidepoint(mx, my):
                    self.selectedCard = {
                        'origin': 'playingArea',
                        'originPos': card.rect.topleft,
                        'index': [columnIndex, cardIndex],
                        'cards': playingArea[columnIndex][cardIndex:],
                    }
        

        buffer = self.cardPositions['buffer']

        if len(buffer['visible']) > 0:
            bufferCard = buffer['visible']

            if not bufferCard.lookingBack and bufferCard.rect.collidepoint(mx, my):
                self.selectedCard = {
                    'origin': 'buffer',
                    'originPos': (SPACER*2.5+CARD_SIZE, SPACER),
                    'index': [-1],
                    'cards': [bufferCard],
                }

    def dragCard(self, mx, my):
        selectedCard = self.selectedCard['cards'][0]

        if selectedCard.drag or selectedCard.rect.collidepoint(mx, my):
            selectedCard.drag = True

            if self.lastMousePos != None:
                for card in self.selectedCard['cards']:
                    card.rect.x += mx-self.lastMousePos[0]
                    card.rect.y += my-self.lastMousePos[1] 

            self.lastMousePos = (mx, my)

        else:
            selectedCard.drag = False

    def inGameCardMoveValid(self, tailCard, movingCard):
        return tailCard.number-1 == movingCard.number and tailCard.isRed != movingCard.isRed

    def inHolderCardMoveValid(self, lastHolderCard, movingCard):
        return lastHolderCard.type == movingCard.type and lastHolderCard.number+1 == movingCard.number 

    def pointOnScreen(self, x, y):
        return (x > 0 and x <= WIDTH) and (y > 0 and y <= HEIGHT)

    def cardMovement(self):
        if pygame.mouse.get_pressed()[0]:
            mx, my = pygame.mouse.get_pos()

            if self.selectedCard == None:
                self.selectCard(mx, my)
            
            else:
                self.dragCard(mx, my)
        
        else:
            if self.selectedCard != None:
                # Move Card
                mx, my = pygame.mouse.get_pos()

                if self.pointOnScreen(mx, my):
                    # Playing area
                    if my > SPACER*2 + CARD_SIZE[1]:
                        col = mx//CARD_SIZE[0]
                        area = 'playingArea'
                    
                    # Dealing and holder area
                    else:
                        if mx > WIDTH - (N_CARD_HOLDERS*CARD_SIZE[0]+N_CARD_HOLDERS*SPACER):
                            col = (WIDTH-mx)//CARD_SIZE[0] - 1
                            area = 'holders'
                        
                    for movedCard in self.selectedCard['cards']:
                        self.cardPositions[area][col].append(movedCard)

                        if area == 'buffer':
                            self.cardPositions[area][-1].pop()
                        
                        else:
                            prevAreaIndex, prevColIndex = self.selectedCard['origin'], self.selectedCard['index'][0]
                            self.cardPositions[prevAreaIndex][prevColIndex].remove(movedCard)

                # Reset Values
                self.selectedCard = None
                self.lastMousePos = None

    def drawPlaceHolders(self):
        for i in range(len(self.cardPositions['holders'])):
            x = WIDTH-(N_CARD_HOLDERS*CARD_SIZE[0]+N_CARD_HOLDERS*SPACER) + i*CARD_SIZE[0]+i*SPACER
            pygame.draw.rect(self.screen, 'grey', (x, SPACER, CARD_SIZE[0], CARD_SIZE[1]), 5, CARD_RADIUS)

    def drawCardToBuffer(self):
        buffer = self.cardPositions['buffer']

        if not len(buffer) == 0: 
            buffer['visible'].append(self.drawCard(BUFFER_POS[0], BUFFER_POS[1]))

    def updateCards(self):
        for value in list(self.cardPositions.values()):

            if type(value) != list:
                for card in value['visible']:
                    card.update()
            
            else:
                for column in value:
                    for card in column:
                        card.update()
        
        if self.selectedCard != None:
            for card in self.selectedCard['cards']:
                card.update()

    def reShuffleBuffer(self):
        buffer = self.cardPositions['buffer']

        for card in buffer['visible']:
            if card.type in self.cardPositions['buffer']['hidden']:
                buffer['hidden'][card.type].append(card.number)
            
            else:
                buffer['hidden'][card.type] = [card.number]   

        buffer['visible'].clear() 

    def update(self):
        self.events()

        #### Game Events ####

        self.screen.blit(self.background, (0, 0))
        self.drawPlaceHolders()

        if not len(self.cardPositions['buffer']['hidden']) == 0:
            self.cardDummy.drawCard()
        else:
            pygame.draw.rect(self.screen, 'lightgray', self.cardDummy.rect, 2, CARD_RADIUS)
            pygame.draw.circle(self.screen, 'lightgray', self.cardDummy.rect.center, CARD_SIZE[0]//3, 8)

        if self.click:
            mx, my = pygame.mouse.get_pos()

            if self.cardDummy.rect.collidepoint(mx, my):
                if len(self.cardPositions['buffer']['hidden']) == 0:
                    self.reShuffleBuffer()
                else:
                    self.drawCardToBuffer()

        self.cardMovement()
        self.updateCards()

        #####################

        pygame.display.flip()
        self.clock.tick(FPS)

    def run(self):
        while not self.gameOver:
            self.update()