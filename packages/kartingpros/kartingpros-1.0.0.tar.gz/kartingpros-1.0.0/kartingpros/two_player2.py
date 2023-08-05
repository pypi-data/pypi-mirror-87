# import pygame module in this program
import pygame
from kartingpros import screen, track2, mainmenu, car, settings, loadimage
from kartingpros.loadimage import _load_image, _load_sound, _load_font
import time
from kartingpros.car import Car
from pygame.locals import *
from pygame import mixer
import sys
import os


def win(display_surface, msg):
    win = mixer.Sound(os.path.join(os.path.abspath(os.path.dirname(__file__)), './sounds/win.wav'))
    mixer.Sound.play(win)
    font = _load_font('./fonts/American Captain.ttf', 32)
    if msg == "p1":
        win_image = _load_image('./images/p1_trophy.png')
    else:
        win_image = _load_image('./images/p2_trophy.png')
    win_image = pygame.transform.scale(win_image, (500, 500))
    car_lap = font.render(msg, True, (255, 255, 255))
    display_surface.blit(win_image, (700, 300))
    #display_surface.blit(car_lap, (1050, 500))
    pygame.display.update()
    pygame.time.delay(5000)
    mixer.music.stop()
    mainmenu.main_menu(display_surface)


def checkpoint1(car, checkpoint, checkpoint_check):
    if (car.hitbox[1] < (checkpoint[1] + 110)) and (car.hitbox[1] > (checkpoint[1] - 110)):
        if (car.hitbox[0] < (checkpoint[0] + 15)) and (car.hitbox[0] > (checkpoint[0] - 15)):
            print("Lap finished")
            checkpoint_check = checkpoint_check + 1
    else:
        checkpoint_check = checkpoint_check

    return checkpoint_check


def checkOutOfBounds(car):
    x, y = 1920, 1080
    if car.position[0] > x or car.position[0] < 0 or car.position[1] > y or car.position[1] < 0:
        return True
    else:
        return False


def collision(car, car2, display_surface):
    if (car.hitbox[1] < (car2.hitbox[1] + 35)) and (car.hitbox[1] > (car2.hitbox[1] - 35)):
        if (car.hitbox[0] < (car2.hitbox[0] + 35)) and (car.hitbox[0] > (car2.hitbox[0] - 35)):
            car2.speed = 0
            car.speed = 0
            # Music for countdown sound
            current_path = os.path.abspath(os.path.dirname(__file__))
            absolute_image_path = os.path.join(
                current_path, './sounds/car_crash.mp3')
            mixer.init()
            mixer.music.load(absolute_image_path)
            mixer.music.set_volume(0.7)
            mixer.music.play()
            crash = _load_image('./images/crash.png')
            display_surface.blit(crash, (600, 250))
            pygame.display.update()
            pygame.time.delay(2500)
            mainmenu.main_menu(display_surface)


def carLap(car, finish_line, lap, msg):
    if (car.hitbox[1] < (finish_line[1] + 100)) and (car.hitbox[1] > (finish_line[1] - 100)):
        if (car.hitbox[0] < (finish_line[0] + 15)) and (car.hitbox[0] > (finish_line[0] - 15)):
            print(msg)
            lap = lap + 1
            return lap
        else:
            return lap
    else:
        return lap


def RaceCars(display_surface):
    track1 = track2.Track2()
    white = (0, 128, 0)
    track = _load_image('./images/track2.png')
    # Official timer
    clock = pygame.time.Clock()
    t0 = time.time()

    # Setup car objects
    start_car1 = (1010, 144)
    car = Car('./images/f1sprite.png', start_car1)
    car_group = pygame.sprite.Group(car)

    start_car2 = (1010, 75)
    car2 = Car('./images/f1sprite2.png', start_car2)
    car_group2 = pygame.sprite.Group(car2)

    # Groups for pads and finish line
    pad_group = track1.getPads()
    finish_line = track1.getFinishLine()

    # Setup lap logic
    checkpoint = (960, 845, 10, 125)
    lap_car1 = 0
    checkpoint_car1 = 0
    lap_car2 = 0
    checkpoint_car2 = 0

    # Collision Check
    collisions = settings.getSetting('collision')
    draw_hitbox = settings.getSetting('draw_hitbox')

    # Countdown timer logic
    countdownTimerStart = time.time()
    countdownFinished = False

    # Music for countdown sound
    current_path = os.path.abspath(os.path.dirname(__file__))
    absolute_image_path = os.path.join(
        current_path, './sounds/race_coundown.mp3')
    mixer.init()
    mixer.music.load(absolute_image_path)
    mixer.music.set_volume(0.7)
    mixer.music.play()
    crowd = mixer.Sound(os.path.join(current_path, './sounds/crowd.wav'))

    # Movement System
    right_press1, left_press1, up_press1, down_press1 = 0, 0, 0, 0
    right_press2, left_press2, up_press2, down_press2 = 0, 0, 0, 0
    while True:
        # Draw the Track
        display_surface.fill(white)
        display_surface.blit(track, (0, 0))
        track2.checkpoint(display_surface)
        delta_t = clock.tick(30)
        font = _load_font('./fonts/American Captain.ttf', 32)
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
            if not hasattr(event, 'key'):
                continue
            # Player 1 Movement
            if event.key == K_RIGHT:
                right_press1 = 1
            elif event.key == K_SPACE:
                car.speed = 0
            elif event.key == K_LEFT:
                left_press1 = 1
            elif event.key == K_UP:
                mixer.music.load(os.path.join(
                    current_path, './sounds/rev.mp3'))
                mixer.music.play(-1)
                up_press1 = 1
            elif event.key == K_DOWN:
                down_press1 = 1
            elif event.key == K_ESCAPE:
                mixer.music.stop()
                mixer.Sound.stop(crowd)
                mainmenu.main_menu(display_surface)

            if event.type == KEYUP:
                if event.key == pygame.K_RIGHT:
                    right_press1 = 0
                elif event.key == pygame.K_LEFT:
                    left_press1 = 0
                elif event.key == pygame.K_UP:
                    mixer.music.stop()
                    up_press1 = 0
                elif event.key == pygame.K_DOWN:
                    down_press1 = 0
            # Player 2 Movement
            if event.key == K_d:
                right_press2 = 1
            elif event.key == K_LSHIFT:
                car.speed = 0
            elif event.key == K_a:
                left_press2 = 1
            elif event.key == K_w:
                mixer.music.load(os.path.join(
                    current_path, './sounds/rev.mp3'))
                mixer.music.play(-1)
                up_press2 = 1
            elif event.key == K_s:
                down_press2 = 1
            elif event.key == K_ESCAPE:
                mixer.Sound.stop(crowd)
                mixer.music.stop()
                mainmenu.main_menu(display_surface)

            if event.type == KEYUP:
                if event.key == pygame.K_d:
                    right_press2 = 0
                elif event.key == pygame.K_a:
                    left_press2 = 0
                elif event.key == pygame.K_w:
                    mixer.music.stop()
                    up_press2 = 0
                elif event.key == pygame.K_s:
                    down_press2 = 0

        car.k_right = right_press1 * -5
        car.k_left = left_press1 * 5
        car.k_up = up_press1 * 2
        car.k_down = down_press1 * -2

        if up_press1 == 0 and down_press1 == 0 and int(car.speed) != 0:
            car.k_down = -.2
            car.k_up = 0

        car2.k_right = right_press2 * -5
        car2.k_left = left_press2 * 5
        car2.k_up = up_press2 * 2
        car2.k_down = down_press2 * -2

        if up_press2 == 0 and down_press2 == 0 and int(car2.speed) != 0:
            car2.k_down = -.2
            car2.k_up = 0

        # Update car and draw track
        carlap1 = font.render("Car 1 Laps completed: " +
                              str(lap_car1) + "/5", True, (255, 255, 255))
        carlap2 = font.render("Car 2 Laps completed: " +
                              str(lap_car2) + "/5", True, (255, 255, 255))
        # Lap count for Cars
        display_surface.blit(carlap1, (0, 0))
        display_surface.blit(carlap2, (0, 30))

        # Update and draw car
        car_group.update(delta_t)
        car_group.draw(display_surface)

        # Update and draw car
        car_group2.update(delta_t)
        car_group2.draw(display_surface)

        if draw_hitbox:
            pygame.draw.rect(display_surface, (255, 0, 0), car.hitbox, 2)
            pygame.draw.rect(display_surface, (255, 0, 0), car2.hitbox, 2)

        # Check if car1 is on track
        on_track = pygame.sprite.groupcollide(
            car_group, pad_group, False, False)

        # Slow down car1 if not on track
        if not on_track:
            car.setOffTrackSpeed()
        else:
            car.setRegularSpeed()

        # Slow down car2 if not on track
        on_track = pygame.sprite.groupcollide(
            car_group2, pad_group, False, False)

        # Slow down car2 if not on track
        if not on_track:
            car2.setOffTrackSpeed()
        else:
            car2.setRegularSpeed()

        pygame.display.flip()
        # Check for collisions only if enabled
        if collisions:
            collision(car, car2, display_surface)

        if checkOutOfBounds(car):
            car.reset(start_car1)
        if checkOutOfBounds(car2):
            car2.reset(start_car2)
        checkpoint_car1 = checkpoint1(car, checkpoint, checkpoint_car1)
        checkpoint_car2 = checkpoint1(car2, checkpoint, checkpoint_car2)
        if checkpoint_car1 >= 1:
            previouslapcar1 = lap_car1
            lap_car1 = carLap(car, finish_line, lap_car1,
                              "Lap finished for car 1!")
            if lap_car1 > previouslapcar1:
                mixer.Sound.play(crowd)
                if lap_car1 == 5:
                    mixer.music.stop()
                    mixer.Sound.stop(crowd)
                    win(display_surface, "p1")
                checkpoint_car1 = 0
        if checkpoint_car2 >= 1:
            previouslapcar2 = lap_car2
            lap_car2 = carLap(car2, finish_line, lap_car2,
                              "Lap finished for car 2!")
            if lap_car2 > previouslapcar2:
                mixer.Sound.play(crowd)
                if lap_car2 == 5:
                    mixer.music.stop()
                    mixer.Sound.stop(crowd)
                    win(display_surface, "p2")
                checkpoint_car2 = 0

        while(time.time()-countdownTimerStart < 4):
            image = _load_image('./images/starting_lights/lights' +
                                str(int(time.time()-countdownTimerStart)+1)+'.png')
            display_surface.blit(image, ((1920/2)-(768/2), 50))
            fontBig = _load_font('./fonts/American Captain.ttf', 64)
            countdown_text = font.render(
                "Time: " + str(4-t0), True, (255, 255, 255))
            t0 = time.time()
            t1 = time.time()
            dt = t1-t0
            countdownFinished = True
            pygame.display.update()
        # pygame.draw.rect(display_surface, (255, 255, 255), (960, 0, 30, 125))
        pygame.display.update()
