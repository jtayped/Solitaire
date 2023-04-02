FPS = 60
WIDTH, HEIGHT = 1000, 750

# Card
SPACER = 5
N_COLUMNS = 7

cardWidth = WIDTH//N_COLUMNS-SPACER
cardHeight = cardWidth*1.5

CARD_SIZE = (cardWidth, cardHeight)
DEALING_SPACE = CARD_SIZE[1] + SPACER*4
CARD_RADIUS = 10
CARD_OUTLINE = 1
Y_SPACE_CARDS = 30
N_CARD_HOLDERS = 4


CARD_TYPES = ['clubs', 'diamonds', 'hearts', 'spades']
SPECIAL_TYPES = ['A', 'J', 'Q', 'K']

CARDS = {}
for cardType in CARD_TYPES:
    CARDS[cardType] = list(range(1, 14))

BUFFER_POS = (SPACER+CARD_SIZE[0]+SPACER*1.5, SPACER)