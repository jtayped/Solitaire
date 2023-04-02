def writeText(screen, font, text, color, pos, align='topleft'):
    textSurface = font.render(text, True, color)
    textRect = textSurface.get_rect(topleft=pos)

    if align == 'center':
        textRect.center = pos[0]

    screen.blit(textSurface, textRect)

def getTextSize(font, text):
    textSurface = font.render(text, True, 'white')
    return textSurface.get_width(), textSurface.get_height()

def debug(screen, font, text, color):
    writeText(screen, font, text, color, (0, 0))