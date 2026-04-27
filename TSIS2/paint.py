import pygame
import sys
import datetime
import tools

pygame.init()

WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint App")

canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill((255, 255, 255))

clock = pygame.time.Clock()

tool = "pencil"
color = (0, 0, 0)
brush_size = 2

drawing = False
start_pos = None
last_pos = None


text_mode = False
text_input = ""
text_pos = (0, 0)
font = pygame.font.SysFont(None, 28)

running = True
while running:
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_p:
                tool = "pencil"
            elif event.key == pygame.K_l:
                tool = "line"
            elif event.key == pygame.K_r:
                tool = "rect"
            elif event.key == pygame.K_c:
                tool = "circle"
            elif event.key == pygame.K_f:
                tool = "fill"
            elif event.key == pygame.K_t:
                tool = "text"

            elif event.key == pygame.K_1:
                brush_size = 2
            elif event.key == pygame.K_2:
                brush_size = 5
            elif event.key == pygame.K_3:
                brush_size = 10

            elif event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                filename = datetime.datetime.now().strftime("drawing_%Y%m%d_%H%M%S.png")
                pygame.image.save(canvas, filename)
                print("Saved:", filename)

            
            if text_mode:
                if event.key == pygame.K_RETURN:
                    text_surface = font.render(text_input, True, color)
                    canvas.blit(text_surface, text_pos)
                    text_mode = False

                elif event.key == pygame.K_ESCAPE:
                    text_mode = False

                elif event.key == pygame.K_BACKSPACE:
                    text_input = text_input[:-1]

                else:
                    text_input += event.unicode

        
        if event.type == pygame.MOUSEBUTTONDOWN:

            if tool == "fill":
                tools.flood_fill(canvas, *event.pos, color)

            elif tool == "text":
                text_mode = True
                text_pos = event.pos
                text_input = ""

            else:
                drawing = True
                start_pos = event.pos
                last_pos = event.pos

        elif event.type == pygame.MOUSEBUTTONUP:
            if drawing:

                if tool == "line":
                    tools.draw_line(canvas, color, start_pos, event.pos, brush_size)

                elif tool == "rect":
                    tools.draw_rect(canvas, color, start_pos, event.pos, brush_size)

                elif tool == "circle":
                    tools.draw_circle(canvas, color, start_pos, event.pos, brush_size)

            drawing = False

        elif event.type == pygame.MOUSEMOTION:
            if drawing and tool == "pencil":
                tools.draw_pencil(canvas, color, last_pos, event.pos, brush_size)
                last_pos = event.pos

    
    if tool in ["line", "rect", "circle"] and drawing:
        temp = canvas.copy()

        if tool == "line":
            tools.draw_line(temp, color, start_pos, mouse_pos, brush_size)

        elif tool == "rect":
            tools.draw_rect(temp, color, start_pos, mouse_pos, brush_size)

        elif tool == "circle":
            tools.draw_circle(temp, color, start_pos, mouse_pos, brush_size)

        screen.blit(temp, (0, 0))
    else:
        screen.blit(canvas, (0, 0))

    
    if text_mode:
        temp = canvas.copy()
        text_surface = font.render(text_input, True, color)
        temp.blit(text_surface, text_pos)
        screen.blit(temp, (0, 0))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()