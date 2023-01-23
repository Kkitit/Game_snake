import pygame
import sys
import random
import pygame_menu
pygame.init()

bg_i = pygame.image.load("aw2.jpg")
SIZE_BLOCK = 20
FRAME_COLOR = (255, 20, 147)
WHITE = (255,255,255)
BLUE = (255, 105, 180)
RED = (0, 0, 0)
COUNT_BLOCKS = 20
SNAKE_COLOR = (0, 100, 0)
MARGIN = 1
head_margin = 70
head_color = (255, 105, 180)
size = [SIZE_BLOCK*COUNT_BLOCKS + 2*SIZE_BLOCK + MARGIN*COUNT_BLOCKS,SIZE_BLOCK * COUNT_BLOCKS + 2 * SIZE_BLOCK + MARGIN * COUNT_BLOCKS + head_margin]
print(size)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Змеюшка")
timer = pygame.time.Clock()
courier = pygame.font.SysFont("courier", 37)

class SnakeBlock:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def is_inside(self):
        return 0<self.x<SIZE_BLOCK and 0<=self.y<SIZE_BLOCK


    def __eq__(self, other):
        return  isinstance(other, SnakeBlock) and self.x == other.x and self.y == other.y






def draw_block(color, row, column):
    pygame.draw.rect(screen, color, [SIZE_BLOCK + column * SIZE_BLOCK + MARGIN * (column + 1),
                                     head_margin + SIZE_BLOCK + row * SIZE_BLOCK + MARGIN * (row + 1), SIZE_BLOCK,
                                     SIZE_BLOCK])

def start_the_game():
    def get_randon_empty_block():
        x = random.randint(0, COUNT_BLOCKS - 1)
        y = random.randint(0, COUNT_BLOCKS - 1)
        empty_block = SnakeBlock(x, y)
        while empty_block in snake_blocks:
            empty_block.x = random.randint(0, COUNT_BLOCKS - 1)
            empty_block.y = random.randint(0, COUNT_BLOCKS - 1)
        return empty_block

    snake_blocks = [SnakeBlock(9, 8), SnakeBlock(9, 9), SnakeBlock(9, 10)]
    apple = get_randon_empty_block()
    d_row = buf_row = 0
    d_col = buf_col = 1
    total = 0
    speed = 1

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Пока-Пока")
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and d_col!=0:
                    d_row = -1
                    d_col = 0
                elif event.key == pygame.K_DOWN and d_col!=0:
                    d_row = 1
                    d_col = 0
                elif event.key == pygame.K_LEFT and d_row!=0:
                    d_row = 0
                    d_col = -1
                elif event.key == pygame.K_RIGHT and d_row!=0:
                    d_row = 0
                    d_col = 1

        screen.fill(FRAME_COLOR)
        pygame.draw.rect(screen,head_color, [0,0, size[0], head_margin])

        text_total = courier.render(f"Очки: {total}", 0, WHITE)
        text_speed = courier.render(f"Скорость: {speed}", 0, WHITE)
        screen.blit(text_total, (SIZE_BLOCK,SIZE_BLOCK))
        screen.blit(text_speed, (SIZE_BLOCK+190, SIZE_BLOCK))

        for row in range(COUNT_BLOCKS):
            for column in range(COUNT_BLOCKS):
                if (row + column) % 2==0:
                    color = BLUE
                else:
                    color = WHITE

                draw_block(color, row, column)

        head = snake_blocks[-1]
        if not head.is_inside():
            print("Пока-Пока")
            pygame.quit()
            sys.exit()

        draw_block(RED, apple.x, apple.y)
        for block in snake_blocks:
            draw_block(SNAKE_COLOR, block.x,block.y)
        pygame.display.flip()
        if apple == head:
            total += 1
            speed += total//5 + 1
            snake_blocks.append(apple)
            apple = get_randon_empty_block()


        new_head = SnakeBlock(head.x + d_row, head.y + d_col )
        snake_blocks.append(new_head)
        snake_blocks.pop(0)

        # d_row = buf_row
        # d_col = buf_col

        timer.tick(3+speed)

main_them = pygame_menu.themes.THEME_DARK.copy()
main_them.set_background_color_opacity(0.4)
menu = pygame_menu.Menu('Hey', 400, 300,
                        theme=main_them)

menu.add.text_input('Ваш Ник :', default='Игрок 1')
menu.add.button('Играть', start_the_game)
menu.add.button('Уйти с позором', pygame_menu.events.EXIT)

#menu.mainloop(screen)

while True:

    screen.blit(bg_i, (0, 0))

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            exit()

    if menu.is_enabled():
        menu.update(events)
        menu.draw(screen)

    pygame.display.update()



