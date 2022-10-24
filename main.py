import pygame
import random

pygame.init()

display_width, display_height = 374, 656

display = pygame.display.set_mode((display_width, display_height))

pygame.display.set_caption("flappy bird")

clock = pygame.time.Clock()


def text_to_screen(text, x_displace, y_displace):
    font1 = pygame.font.Font("Font/flappybird/FlappyBirdy.ttf", 50)
    text = font1.render(str(text), True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.center = ((display_width / 2) + x_displace, (display_height / 2) + y_displace)
    display.blit(text, text_rect)


def move_floor(floor_list, floor_moving_speed):
    floor_image = pygame.transform.scale(pygame.image.load("Sprites/floor.png").convert_alpha(), (374, 131))

    for floor_pos in floor_list:
        floor_pos[0] -= floor_moving_speed * delta_time

        display.blit(floor_image, floor_pos)

    return floor_list


def draw_pipes(pipe_pos_list, bird_rect):
    pipe_width = 81
    pipe_height = 450

    lower_pipe_image = pygame.transform.scale(pygame.image.load("Sprites/pipe.png").convert_alpha(),
                                              (pipe_width, pipe_height))

    upper_pipe_image = pygame.transform.flip(
        pygame.transform.scale(pygame.image.load("Sprites/pipe.png").convert_alpha(),
                               (pipe_width, pipe_height)), False, True)

    dist_between_up_and_down_pipe = 125

    for pipe_pos in pipe_pos_list:
        pipe_x = pipe_pos[0] - (pipe_width / 2)
        # draw lower pipe
        display.blit(lower_pipe_image,
                     (pipe_x, pipe_pos[1] + (dist_between_up_and_down_pipe / 2)))
        # draw upper pipe
        display.blit(upper_pipe_image, (pipe_x, pipe_pos[1] - (dist_between_up_and_down_pipe / 2) - pipe_height))

        upper_pipe_rect = (pipe_pos[0] - (pipe_width / 2),
                           pipe_pos[1] - (dist_between_up_and_down_pipe / 2) - pipe_height,
                           pipe_width, pipe_height)

        lower_pipe_rect = (pipe_pos[0] - (pipe_width / 2), pipe_pos[1] + (dist_between_up_and_down_pipe / 2),
                           pipe_width, pipe_height)

        if pygame.Rect(bird_rect).colliderect(upper_pipe_rect) or pygame.Rect(bird_rect).colliderect(lower_pipe_rect):
            return True

    return False


def main():
    global delta_time

    background = pygame.transform.scale(pygame.image.load("Sprites/background.png").convert_alpha(), (374, 656))

    floor_list = [[0, 526], [display_width, 526]]

    pipe_max_height = 400
    pipe_min_height = 150
    pipe_pos_list = [[display_width+75, random.randrange(pipe_min_height, pipe_max_height+1, 50)]]

    pipe_moving_speed = 100
    new_pipe_add_speed = 2000

    bird_states = [pygame.transform.scale(pygame.image.load("Sprites/bird state1.png").convert_alpha(), (51, 36)),
                   pygame.transform.scale(pygame.image.load("Sprites/bird state2.png").convert_alpha(), (51, 36)),
                   pygame.transform.scale(pygame.image.load("Sprites/bird state3.png").convert_alpha(), (51, 36)),
                   pygame.transform.scale(pygame.image.load("Sprites/bird state2.png").convert_alpha(), (51, 36))]

    last_frame_change = pygame.time.get_ticks()
    frame_change_speed = 100  # every 100 ms change frame
    frame_index = 0
    max_frame_index = len(bird_states) - 1

    bird_pos = [75, 275]

    bird_gravity = 0
    bird_g = 8  # bird gravitational pull to the "Earth" (actually floor)

    score = 0

    g_o = False
    g_e = False
    g_s = False  # g_s -- game_start

    while not g_s and not g_e:
        delta_time = clock.tick(100) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                g_e = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                bird_gravity = -3.3
                g_s = True

        current_time = pygame.time.get_ticks()

        if current_time - last_frame_change >= frame_change_speed:
            last_frame_change = pygame.time.get_ticks()
            frame_index += 1

            if frame_index > max_frame_index:
                frame_index = 0

        new_floor_list = []
        for floor_index, floor_pos in enumerate(floor_list):
            if floor_pos[0] > -display_width + 2:
                new_floor_list.append(floor_pos)
            else:
                floor_list.append([display_width, 526])

        floor_list = new_floor_list

        bird_image = bird_states[frame_index]

        display.blit(background, (0, 0))

        floor_list = move_floor(floor_list, floor_moving_speed=pipe_moving_speed)
        display.blit(pygame.transform.rotate(bird_image, 0), bird_pos)

        text_to_screen("Click", 0, -150)

        pygame.display.update()

    last_pipe_add = pygame.time.get_ticks()
    last_score_add = pygame.time.get_ticks() + 1100

    while not g_o and not g_e:
        delta_time = clock.tick(100) / 1000

        if bird_pos[1] < 0:
            bird_pos[1] = 0
            bird_gravity = 0
        elif bird_pos[1] > 490:
            g_o = True

        bird_gravity += (bird_g * delta_time) if bird_gravity < 9 else 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                g_e = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                bird_gravity = -3.3

        current_time = pygame.time.get_ticks()

        if current_time - last_frame_change >= frame_change_speed:
            last_frame_change = pygame.time.get_ticks()
            frame_index += 1

            if frame_index > max_frame_index:
                frame_index = 0

        if current_time - last_score_add >= 2000:
            last_score_add = pygame.time.get_ticks()
            score += 1

        bird_pos[1] += bird_gravity

        bird_image = bird_states[frame_index]

        for pipe_pos in pipe_pos_list:
            pipe_pos[0] -= pipe_moving_speed * delta_time

            if current_time - last_pipe_add > new_pipe_add_speed:
                last_pipe_add = pygame.time.get_ticks()

                pipe_pos_list.append([display_width+75, random.randrange(pipe_min_height, pipe_max_height+1, 50)])

        new_floor_list = []
        for floor_index, floor_pos in enumerate(floor_list):
            if floor_pos[0] > -display_width+2:
                new_floor_list.append(floor_pos)
            else:
                floor_list.append([display_width, 526])

        floor_list = new_floor_list

        bird_ange_turn = bird_gravity * -10

        bird_rect = (bird_pos[0], bird_pos[1], bird_image.get_width(), bird_image.get_height())

        if not g_o:
            display.blit(background, (0, 0))
            g_o = draw_pipes(pipe_pos_list, bird_rect)
            floor_list = move_floor(floor_list, floor_moving_speed=pipe_moving_speed)
            display.blit(pygame.transform.rotate(bird_image, bird_ange_turn), bird_pos)
            text_to_screen(score, 0, -250)

            pygame.display.update()

    if not g_e:
        overlay = pygame.Surface((display_width, display_height))
        overlay_alpha = 255

        floor_image = pygame.transform.scale(pygame.image.load("Sprites/floor.png").convert_alpha(), (374, 131))

        over = False

        while not g_e and not over:
            delta_time = clock.tick(100) / 1000

            bird_gravity += (bird_g * delta_time) if bird_gravity < 9 else 0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    g_e = True

            if overlay_alpha > 0:
                overlay_alpha -= 5

            bird_ange_turn = bird_gravity * -10

            display.blit(background, (0, 0))
            _ = draw_pipes(pipe_pos_list, (0, 0, 0, 0))

            for floor_pos in floor_list:
                display.blit(floor_image, (floor_pos[0], floor_pos[1]))

            if bird_pos[1] < 495:
                bird_pos[1] += bird_gravity
            elif bird_pos[1] > 495 and overlay_alpha == 0:
                bird_ange_turn = -90
                over = True

            display.blit(pygame.transform.rotate(bird_image, bird_ange_turn), bird_pos)

            overlay.fill((255, 255, 255))
            overlay.set_alpha(overlay_alpha)
            display.blit(overlay, (0, 0))

            pygame.display.update()

        over = False

        while not over and not g_e:
            clock.tick(100)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    g_e = True

            if overlay_alpha < 255:
                overlay_alpha += 5
            else:
                over = True

            overlay.fill((0, 0, 0))
            overlay.set_alpha(overlay_alpha)
            display.blit(overlay, (0, 0))

            pygame.display.update()

    return g_e


game_exit = False
while not game_exit:
    game_exit = main()

# password:
# (ill show on example)
# facebook
# koobecaf - reversed
# 1  4 67 -> need to memorize
# kacbbcak
#  76 4  1
# kACbBcaK17644671 -> number part is always the same
