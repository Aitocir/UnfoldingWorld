import pygame

class TextView():
    def __init__(self, text, font, rect, color=(0,0,0)):
        self.text = text
        self.font = font
        self.rect = rect
        self.color = color
    def render(self):
        return self.font.render(self.text, True, self.color)
    def pos(self, xoff=0, yoff=0):
        return (self.rect.x+xoff, self.rect.y+yoff)

def init_inputbox(x, y, w, h):
    inputfont = pygame.font.Font(None, 24)
    inputbox = pygame.Rect(x, y, w, h)
    return TextView('', inputfont, inputbox)

def init_outputbox(x, y, w, h):
    outputfont = pygame.font.Font(None, 24)
    outputbox = pygame.Rect(x, y, w, h)
    return TextView('', outputfont, outputbox)

def init_statbox(x, y, w, h):
    statfont = pygame.font.Font(None, 32)
    statbox = pygame.Rect(x, y, w, h)
    return TextView('', statfont, statbox)

def get_input(current_text):
    signals = {'Quit': False, 'Enter': False, 'Scroll': 0, 'Newtext': ''}
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            signals['Quit'] = True
            break
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_RETURN:
                signals['Enter'] = True
            elif e.key == pygame.K_BACKSPACE:
                if signals['Enter']:
                    signals['Newtext'] = signals['Newtext'][:-1]
                else:
                    current_text = current_text[:-1]
            elif e.key == pygame.K_UP:
                signals['Scroll'] += 1
            elif e.key == pygame.K_DOWN:
                signals['Scroll'] -= 1
            elif signals['Enter']:
                signals['Newtext'] += e.unicode
            else:
                current_text += e.unicode
    return signals, current_text

def start(input_q, output_q, view_name='Game :D'):
    pygame.init()
    #  init values
    scroll_offset = 0
    game_messages = ['' for _ in range(100)]
    clock = pygame.time.Clock()
    #  init views
    input_view = init_inputbox(10, 560, 780, 30)
    output_views_box = pygame.Rect(10, 304, 780, 250)
    output_views = []
    for i in range(10):
        output_views.append(init_outputbox(10, 520-(24*i), 780, 24))
    """
    stat_views_box = pygame.Rect(500, 10, 290, 290)
    stat_views = []
    for i in range(len(stats_callback())):
        stat_views.append(init_statbox(500, 10+(35*i), 290, 32))
    """
    #  TODO: other views
    #
    # Game loop
    #
    #  init window
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption(view_name)
    screen.fill((220,220,220))
    running = True
    input_dirty = True
    output_dirty = True
    while running:
        #
        # Update
        #
        old_text = input_view.text
        signals, input_view.text = get_input(input_view.text)
        input_dirty = old_text != input_view.text
        scroll_offset = max(0, min(100-10, scroll_offset + signals['Scroll']))
        output_dirty = output_dirty or signals['Scroll'] != 0
        #
        #  update output with new items
        try:
            game_messages.append(output_q.get_nowait())
            game_messages = game_messages[-100:]
            output_dirty = True
        except:
            pass
        if signals['Enter']:
            #
            #  report input to client for processing
            input_q.put(input_view.text)            
            scroll_offset = 0
            input_view.text = signals['Newtext']
            output_dirty = True
            input_dirty = True
        if signals['Quit']:
            running = False
        #
        # Draw
        #
        if input_dirty or output_dirty:
            screen.fill((220,220,220))
            itext = input_view.render()
            pygame.draw.rect(screen, (0,0,0), input_view.rect, 2)
            screen.blit(itext, input_view.pos(5, 5))
            pygame.draw.rect(screen, (0,0,0), output_views_box, 2)
            for i in range(10):
                output_views[i].text = game_messages[-1-i-scroll_offset]
                output_views[i].color = (25,25,25) #  (100,100,100) if game_messages[-1-i-scroll_offset][0] == 'INFO' else (25,25,25)
                otext = output_views[i].render()
                screen.blit(otext, output_views[i].pos(5, 5))
            """
            stats = stats_callback()
            pygame.draw.rect(screen, (0,0,0), stat_views_box, 2)
            for i in range(len(stats)):
                stat_views[i].text = '{0}: {1}'.format(*stats[i])
                stext = stat_views[i].render()
                screen.blit(stext, stat_views[i].pos(5, 5))
            """
        pygame.display.flip()
        clock.tick(30)
        input_dirty = False
        output_dirty = False
        