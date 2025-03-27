# import required libraries
from time import sleep
import pygame
import sqlite3
import bcrypt

# import individual classes and functions
from button_class import Button
from note_class import Note, hardNote, tutorialNote, holdNote, tutorialHoldNote
from note_generator import generate_notes
from sql import create_account, add_score, check_user, check_password, top_five, top_five_from_level, top_five_from_user, get_level
from notes import levels_dict

# import beatmaps

# define screens

def start(screen):
    global current_pos
    global current_screen

    bg = pygame.image.load("images/startmenu.png")
    screen.blit(bg, (0, 0))

    # initialise buttons

    start_button = Button('startbutton.png', 'startbuttonselected.png', (0, 0), 0, 'menu1')
    quit_button = Button('quitbutton.png', 'quitbuttonselected.png', (0, 0), 1, 'quit')
    info = font.render("Enter to select", True, (255, 138, 138))
    info2 = font.render("WASD to navigate", True, (255, 138, 138))
    screen.blit(info, (105, 430))
    screen.blit(info2, (95, 460))

    buttons = [start_button, quit_button]

    # load buttons

    start_button.check_selection(screen, current_pos)
    quit_button.check_selection(screen, current_pos)

    # change current selected button

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_UP or event.key == pygame.K_w) and current_pos > 0:
                current_pos -= 1
            elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and current_pos < 1:
                current_pos +=1
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                current_screen = buttons[current_pos].action()

def menu1(screen):
    global current_pos
    global current_screen
    global start_flag

    # initialise notes - allows user to restart level again

    start_flag = True
    
    bg = pygame.image.load("images/menuscreen.png")
    screen.blit(bg, (0, 0))
    scrollbar = pygame.image.load("images/scrollbar.png")
    screen.blit(scrollbar, (0,0))

    # initialise buttons

    levels_button = Button('levelsbutton.png', 'levelsbuttonselected.png', (0, 0), 0, 'levels')
    tutorial_button = Button('tutorialbutton.png', 'tutorialbuttonselected.png', (0, 0), 1, 'tutorial')
    account_button = Button('accountbutton.png', 'accountbuttonselected.png', (0, 0), 2, 'accounts')
    rankings_button = Button('rankingsbutton.png', 'rankingsbuttonselected.png', (0, 0), 3, 'rankings')

    buttons = [levels_button, tutorial_button, account_button, rankings_button]

    # load buttons

    for x in range(0, 4):
        buttons[x].check_selection(screen, current_pos)

    # change current selected button

    for event in pygame.event.get():

        # increment position on screen

        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_UP or event.key == pygame.K_w) and current_pos > 0:
                current_pos -= 1
            elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and current_pos < 4:
                current_pos +=1

        # if the current position is off the screen, load the next menu page

        if current_pos == 4:
            current_pos = 0
            current_screen = 'menu2'

        # if the user clicks enter, carry out the function of the button

        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            hold = buttons[current_pos].action()
            current_pos = 0
            current_screen = hold

def menu2(screen):
    global current_pos
    global current_screen

    
    bg = pygame.image.load("images/menuscreen.png")
    screen.blit(bg, (0, 0))
    scrollbar = pygame.image.load("images/scrollbar2.png")
    screen.blit(scrollbar, (0,0))

    # initialise buttons

    options_button = Button('optionsbutton.png', 'optionsbuttonselected.png', (0, 0), 0, 'options')
    back_button = Button('backbutton.png', 'backbuttonselected.png', (0, 0), 1, 'start')

    buttons = [options_button, back_button]

    # load buttons

    for x in range(0, 2):
        buttons[x].check_selection(screen, current_pos)

    # change current selected button

    for event in pygame.event.get():

        # increment position on screen

        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_UP or event.key == pygame.K_w) and current_pos > -1:
                current_pos -= 1
            elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and current_pos < 1:
                current_pos +=1

        # if the current position is off the screen, load the previous menu page

        if current_pos == -1:
            current_pos = 3
            current_screen = 'menu1'

        # if the user clicks enter, carry out the function of the button

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                current_screen = buttons[current_pos].action()

def options(screen):
    global current_pos
    global current_screen
    global keybind
    global current_vol
    
    transparent_screen = pygame.Surface((500, 500), pygame.SRCALPHA)
    transparent_screen.fill((0, 0, 0, 100)) 
    
    bg = pygame.image.load("images/menuscreen.png")
    screen.blit(bg, (0, 0))

    # initialise buttons

    change_volume = Button('volumebutton.png', 'volumebuttonselected.png', (0, 0), 0, None)
    change_key = Button('keybindbutton.png', 'keybindbuttonselected.png', (0, 0), 1, None)
    back_button = Button('backbutton2.png', 'backbutton2selected.png', (0, 0), 2, 'menu1')

    buttons = [change_volume, change_key, back_button]

    # load buttons

    for x in range(0, 3):
        buttons[x].check_selection(screen, current_pos)

    # change currently selected button

    for event in pygame.event.get():

        # increment position on screen

        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_UP or event.key == pygame.K_w) and current_pos > -1:
                current_pos -= 1

            elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and current_pos < 2:
                current_pos +=1

            # changing volume

            elif event.key == pygame.K_RETURN and current_pos == 0:

                # initialise information text

                changing = True
                screen.blit(transparent_screen, (0,0))
                optionsinfo = pygame.image.load('images/optionsinfo.png')
                screen.blit(optionsinfo, (0,0))
                pygame.display.flip()

                # check for changes or exit
                
                while changing == True:
                    
                    current_vol_temp = pygame.mixer.music.get_volume()

                    # initialise background

                    screen.blit(bg, (0, 0))
                    screen.blit(transparent_screen, (0,0))
                    screen.blit(optionsinfo, (0,0))
                    
                    # changing image of volume bar

                    if current_vol_temp > 0:

                        vol_image = pygame.image.load('images/volume' + str(current_vol_temp) + '.png')
                        screen.blit(vol_image, (0,0))

                    pygame.display.flip()

                    # change volume

                    for event in pygame.event.get():

                        if event.type == pygame.KEYDOWN:
                            if (event.key == pygame.K_UP or event.key == pygame.K_w) and current_vol_temp <= 1:
                                current_vol_temp += 0.25
                                print(current_vol)
                            elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and current_vol_temp >= 0:
                                current_vol_temp -= 0.25
                                print(current_vol)
                            elif (event.key == pygame.K_SPACE):
                                changing = False
                        
                        current_vol = current_vol_temp
                        pygame.mixer.music.set_volume(current_vol)

            # change keybind

            elif event.key == pygame.K_RETURN and current_pos == 1:
                
                key_pressed = False
                new_key = keybind

                # check for key pressed or exit

                while key_pressed != True:

                    # print information text

                    screen.blit(bg, (0, 0))
                    screen.blit(transparent_screen, (0,0))
                    keybindinfo = pygame.image.load('images/keybindinfo.png')
                    screen.blit(keybindinfo, (0,0))
                    pygame.display.flip()


                    for event in pygame.event.get():

                        if event.type == pygame.KEYDOWN:

                            if event.key == 13:

                                # load invalid text

                                invalidkeybind = pygame.image.load('images/keybindinvalid.png')
                                screen.blit(bg, (0, 0))
                                screen.blit(transparent_screen, (0,0))
                                screen.blit(invalidkeybind, (0,0))
                                pygame.display.flip()
                                sleep(3)

                            elif event.key == 27:
                                key_pressed = True

                            else:

                                # load success text

                                successkeybind = pygame.image.load('images/keybindsuccess.png')
                                screen.blit(bg, (0, 0))
                                screen.blit(transparent_screen, (0,0))
                                screen.blit(successkeybind, (0,0))
                                new_key = event.key
                                key_pressed = True
                                pygame.display.flip()
                                sleep(3)
                        
                # change keybind

                keybind = new_key
                print(keybind)
                

            elif event.key == pygame.K_RETURN and current_pos == 2:
                current_screen = back_button.action()

def levelselect1(screen):
    global current_pos
    global current_screen
    global start_flag
    global notes_score
    global discrepancy_sum

    # re-initialise scores

    discrepancy_sum = 0
    notes_score = [0, 0, 0, 0]
    start_flag = True

    bg = pygame.image.load("images/menuscreen.png")
    screen.blit(bg, (0, 0))
    scrollbar = pygame.image.load("images/scrollbar.png")
    screen.blit(scrollbar, (0,0))

    level1_button = Button('level1button.png', 'level1buttonselected.png', (0, 0), 0, '1')
    level2_button = Button('level2button.png', 'level2buttonselected.png', (0, 0), 1, '2')
    level3_button = Button('level3button.png', 'level3buttonselected.png', (0, 0), 2, '3')
    level4_button = Button('level4button.png', 'level4buttonselected.png', (0, 0), 3, '4')

    buttons = [level1_button, level2_button, level3_button, level4_button]

    # load buttons

    for x in range(0, 4):
        buttons[x].check_selection(screen, current_pos)

    # change current selected button

    for event in pygame.event.get():

        # increment position on screen

        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_UP or event.key == pygame.K_w) and current_pos > 0:
                current_pos -= 1
            elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and current_pos < 4:
                current_pos +=1
                # if the current position is off the screen, load the next menu page
                if current_pos == 4:
                    current_pos = 0
                    current_screen = 'levelselect2'
            elif event.key == pygame.K_RETURN:
                levels(screen, start_time, buttons[current_pos].action())

def levelselect2(screen):
    global current_pos
    global current_screen
    global start_flag
    global notes_score
    global discrepancy_sum
    
    # re-initialise scores

    discrepancy_sum = 0
    notes_score = [0, 0, 0, 0]

    bg = pygame.image.load("images/menuscreen.png")
    screen.blit(bg, (0, 0))
    scrollbar = pygame.image.load("images/scrollbar2.png")
    screen.blit(scrollbar, (0,0))
    
    level5_button = Button('level5button.png', 'level5buttonselected.png', (0, 0), 0, 'level5')
    back_button = Button('backbutton.png', 'backbuttonselected.png', (0, 0), 1, 'menu1')

    buttons = [level5_button, back_button]

    # load buttons

    for x in range(0, 2):
        buttons[x].check_selection(screen, current_pos)

    # change current selected button

    for event in pygame.event.get():

        # increment position on screen

        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_UP or event.key == pygame.K_w) and current_pos > -1:
                current_pos -= 1
                # if the current position is off the screen, load the next menu page
                if current_pos == -1:
                    current_pos = 3
                    current_screen = 'levels'
            elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and current_pos < 1:
                current_pos +=1
            elif event.key == pygame.K_RETURN:
                hold = buttons[current_pos].action()
                current_pos = 0
                current_screen = hold

def tutorial(screen):
    global current_screen
    global keybind
    global discrepancy_sum
    global notes_score

    level_no = 0
    bg = pygame.image.load("images/level0screen.png")

    # turn off keybind during example sections

    keybind_temp = keybind
    keybind = None
    
    # blit starting text

    display_text(screen, 0, 5, keybind_temp)

    # display 1 = ex. expanding note

    sleep(2)

    example_notes = [Note(500, 4000)]

    start_time = pygame.time.get_ticks()
    for note in range(0, len(example_notes)):
        check_note(screen, example_notes[note], start_time, level_no, (250, 200))

    # reset screen

    screen.blit(bg, (0,0))
    pygame.display.flip()

    sleep(2)

    # display 2 = ex. hit notes

    display_text(screen, 5, 7, keybind_temp)

    example_notes = [tutorialNote(0, 3000), tutorialNote(3500, 6500), tutorialNote(7000, 10000)]

    start_time = pygame.time.get_ticks()
    for note in range(0, len(example_notes)):
        check_note(screen, example_notes[note], start_time, level_no, (250, 200))

    sleep(2)

    # display 3 = ex. hitting note

    # turn keybind back on for playing sections

    keybind = keybind_temp

    end = False

    while end == False:

        display_text(screen, 7, 10, keybind_temp)

        example_notes = [Note(0, 3000), Note(3500, 6500), Note(7000, 10000)]

        start_time = pygame.time.get_ticks()
        for note in range(0, len(example_notes)):
            check_note(screen, example_notes[note], start_time, level_no, (250, 200))

        sleep(2)

        # ask if repeat required

        display_text(screen, 10, 11, keybind_temp)

        text = small_font.render("Press Y to continue or N", True, (255, 138, 138))
        text2 = small_font.render("to repeat the last example.", True, (255, 138, 138))

        screen.blit(bg, (0,0))
        screen.blit(text, (40,60))
        screen.blit(text2, (40,80))

        pygame.display.flip()

        # check for user input

        end2 = False

        while not end2:
            clock.tick(20)

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        end = True
                        end2 = True
                    elif event.key == pygame.K_n:
                        end2 = True

    # display 4 = ex. harder notes

    example_notes = []

    start_time = pygame.time.get_ticks()

    for i in range(0, 3):
        new_notes = generate_notes(10, 30+(10*i), 10500*i)
        for x in range(0, len(new_notes)):
            example_notes.append(new_notes[x])

    display_text(screen, 11, 13, keybind_temp)

    start_time = pygame.time.get_ticks()

    for note in range(0, len(example_notes)):
        check_note(screen, example_notes[note], start_time, level_no, (250, 200))
    
    sleep(2)

    display_text(screen, 13, 14, keybind_temp)

    # display 5 = ex. hold notes

    display_text(screen, 14, 19, keybind_temp)

    example_notes = [tutorialHoldNote(100, 1600, 1000), tutorialHoldNote(3100, 4600, 1000), tutorialHoldNote(6100, 7600, 1000)]

    # set keybind to A for use within placeholderHoldNote

    keybind = pygame.K_a
    start_time = pygame.time.get_ticks()

    for note in range(0, len(example_notes)):
        check_note(screen, example_notes[note], start_time, level_no, (250, 200))

    sleep(2)

    # reset keybind for note playing sections

    keybind = keybind_temp

    # display 6 = ex. hitting hold notes

    display_text(screen, 21, 22, keybind_temp)

    example_notes = [holdNote(100, 1600, 1000), holdNote(3100, 4600, 1000), holdNote(6100, 7600, 1000)]

    start_time = pygame.time.get_ticks()

    for note in range(0, len(example_notes)):
        check_note(screen, example_notes[note], start_time, level_no, (250, 200))

    sleep(2)

    # ask if user wants to start level 1
    
    display_text(screen, 19, 21, keybind_temp)

    text = small_font.render("Press Y to go straight to", True, (255, 138, 138))
    text1 = small_font.render("level 1 or N to return to", True, (255, 138, 138))
    text2 = small_font.render("main menu.", True, (255, 138, 138))
    
    screen.blit(bg, (0,0))
    screen.blit(text, (40,60))
    screen.blit(text1, (40,80))
    screen.blit(text2, (40,100))

    pygame.display.flip()

    end = False

    while not end:
        clock.tick(20)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    # re-initialise scores
                    discrepancy_sum = 0
                    notes_score = [0, 0, 0, 0]
                    start_time = pygame.time.get_ticks()
                    levels(screen, start_time, '1')
                    current_screen = 'menu1'
                    end = True

                elif event.key == pygame.K_n:
                    current_screen = 'menu1'
                    end = True

def display_text(screen, x, y, keybind_temp):

    global current_screen

    next = small_font.render("Press any key to continue.", True, (255, 138, 138))
    bg = pygame.image.load("images/level0screen.png")

    text = [
            ["Welcome to Rhythm Rolls!"],
            ["Let's start by playing some", "beats."],
            ["Play notes using the " + pygame.key.name(keybind_temp), "button."],
            ["This playing key can be", "changed under Options >", "Keybind."],
            ["During the game, you will", "see two circles. Continue to", "see an example."],
            ["Press the playing key when", "the red inner circle reaches", "the pink outer circle."],
            ["Continue to see an example."],
            ["Are you ready to have a go?"],
            ["The moving circle will stop", "expanding when you 'play' it."],
            ["Let's start with three notes.", "Continue to begin!"],
            ["Are you ready to play some", "harder notes?"],
            ["Brave choice!"],
            ["Continue to start playing."],
            ["Well done!"],
            ["There is one type of note", "left to practice, the hold", "note."],
            ["Hold notes will be blue", "instead of red like normal", "notes."],
            ["When the inner circle", "reaches the outer circle,", "start holding the playing", "key."],
            ["A second circle will now", "appear. When this reaches the", "outer circle, let go of the", "playing key."],
            ["Continue to see an example."],
            ["You have completed the", "tutorial.", "Well done!"],
            ["You can replay the tutorial", "at any time through the", "main menu."],
            ["Continue to have a go", "practicing."]
            ]

    count = 0

    for i in range(x, y):

        end = False

        while not end:

            clock.tick(20)
            count += 1

            screen.blit(bg, (0,0))

            for j in range(0, len(text[i])):
                current = small_font.render((text[i][j]), True, (255, 138, 138)) 
                screen.blit(current, (40, 60+(20*j)))

            # flashing text
            
            if (-1)**(count // 10) == 1:
                screen.blit(next, (50, 350))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and count >= 20:
                    end = True

def levels(screen, start_time, level):

    # loading screen

    loading = pygame.image.load("images/loading.png")
    screen.blit(loading, (0,0))
    pygame.display.flip()

    # get info from database

    connection = sqlite3.connect("rhythmrolls.db")
    level, difficulty, track, height = get_level(connection, level)

    # get notes from function

    notes = levels_dict[level](start_time)

    # play level

    levelplay(screen, start_time, level, notes, track, (250, height), difficulty)

def levelplay(screen, start_time, level_no, notes, music, centre, difficulty):
    global current_pos
    global current_screen
    global start_flag
    global discrepancy_sum
    global notes_score
    global current_vol
    global last_played

    last_played = level_no
    
    bg = pygame.image.load("images/level" + str(level_no) + "screen.png")
    screen.blit(bg, (0, 0))

    # if first loop, set start_time

    if start_flag:
        for note in range(0, len(notes)):
            notes[note].centre_pos = centre
            start_time = pygame.time.get_ticks()
            start_flag = False

        print(start_time)

    # draw main circle
    pygame.draw.circle(screen, (239, 154, 154), centre, 50, width=3)

    if difficulty != 'tutorial':

        # change music

        pygame.mixer.music.pause()
        level_music = pygame.mixer.Sound(music)
        level_channel = pygame.mixer.Channel(1)
        level_channel.set_volume(current_vol)
        level_channel.play(level_music)

        for note in range(0, len(notes)):

            # display and score each note

            print(note)
            current_note = notes[note]
            check_note(screen, current_note, start_time, level_no, centre)

        # stop music

        start_flag = True
        level_channel.fadeout(5000)
        sleep(2.5)

        # show completed screen

        screen.blit(bg, (0, 0))
        complete_text = pygame.image.load("images/gamecomplete.png")
        screen.blit(complete_text, (0, -100))
        pygame.display.flip()

        # restart music after fadeout

        sleep(2.5)
        pygame.mixer.music.unpause()

        # show scores

        end = False
        count = 0

        while end == False:
            clock.tick(20)
            levelscore(screen, level_no, len(notes))
            count += 1
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and count >= 40:
                    end = True

        end = False
        count = 0
        current_pos = 0

        while end == False:

            clock.tick(120)
            pygame.display.flip()

            bg = pygame.image.load("images/scorebkg.png")
            screen.blit(bg, (0, 0))

            levels_button = Button('levelsbutton.png', 'levelsbuttonselected.png', (0, 120), 0, 'levels')
            accounts_button = Button('rankingsbutton.png', 'rankingsbuttonselected.png', (0, -80), 1, 'rankings')
            
            buttons = [levels_button, accounts_button]

            # load buttons

            info = font.render("Would you like to", True, (255, 138, 138))
            info2 = font.render("upload your score or", True, (255, 138, 138))
            info3 = font.render("play more levels?", True, (255, 138, 138))

            screen.blit(info, (40, 60))
            screen.blit(info2, (40, 80))
            screen.blit(info3, (40, 100))

            for x in range(0, 2):
                buttons[x].check_selection(screen, current_pos)

            # change current selected button

            for event in pygame.event.get():

                # increment position on screen

                if event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_UP or event.key == pygame.K_w) and current_pos > 0:
                        current_pos -= 1
                    elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and current_pos < 1:
                        current_pos +=1
                    elif event.key == pygame.K_RETURN:
                        hold = buttons[current_pos].action()
                        current_pos = 0
                        current_screen = hold
                        end = True
                    elif event.key == pygame.K_ESCAPE:
                        current_pos = 0
                        current_screen = 'levels'

def levelscore(screen, level_no, notes_no):
    global notes_score
    global discrepancy_sum
    global final_score

    # percentage difference equation

    multiplier = abs((500 * notes_no) - discrepancy_sum) / (500 * notes_no)

    # uses multiplier so that greater note discrepancy =  greater % difference = lower score

    final_score  = int(100000 * (multiplier))

    # load scores

    bg = pygame.image.load("images/scorebkg.png")

    main_score = font.render("Level " + str(level_no) + " score = " + str(final_score), True, (255, 138, 138))
    perfect = font.render("Perfect = " + str(notes_score[3]), True, (255, 138, 138))
    good = font.render("Good = " + str(notes_score[2]), True, (255, 138, 138))
    bad = font.render("Bad = " + str(notes_score[1]), True, (255, 138, 138))
    miss = font.render("Miss = " + str(notes_score[0]), True, (255, 138, 138))
    info = font.render("Press any key to exit", True, (255, 138, 138))

    # blit scores

    screen.blit(bg, (0, 0))
    screen.blit(main_score, (32, 60))
    screen.blit(perfect, (32, 125))
    screen.blit(good, (32, 200))
    screen.blit(bad, (32, 275))
    screen.blit(miss, (32, 350))
    screen.blit(info, (32, 415))  
  
def check_note(screen, current_note, start_time, level, centre):
    global current_pos
    global current_screen
    global keybind
    global discrepancy_sum
    global notes_score

    while not current_note.is_hit:

        bg = pygame.image.load("images/level" + str(level) + "screen.png")
        screen.blit(bg, (0, 0))

        # draw main circle
        pygame.draw.circle(screen, (239, 154, 154), centre, 50, width=3)

        # time into track
        current_time = pygame.time.get_ticks() - start_time

        delta_time = clock.tick(120)

        # draw expanding circle

        if current_time >= current_note.time:
            current_note.update_radius(screen, delta_time)

        # check if missed

        if current_time - current_note.hit_time >= 500:
            current_note.hit_check(screen, current_time, clock, level)
            discrepancy_sum, notes_score = current_note.update_score(screen, discrepancy_sum, notes_score)

        # check if hit

        for event in pygame.event.get():
                
                if current_time >= current_note.time:
                    if (event.type == pygame.KEYDOWN and event.key == keybind):
                        current_note.hit_check(screen, current_time, clock, level)
                        discrepancy_sum, notes_score = current_note.update_score(screen, discrepancy_sum, notes_score)
                
def rankings(screen):
    global final_score
    global last_played
    global current_screen
    global current_pos
    global logged_in
    global user
    global show_level
    global show_user

    show_level = 0
    show_user = ''

    bg = pygame.image.load("images/scorebkg.png")
    screen.blit(bg, (0,0))
    connection = sqlite3.connect("rhythmrolls.db")

    # if user not logged in, give chance to make an account before uploading score

    if logged_in == False and final_score != -1:

        info = font.render("You are not logged", True, (121,78,59))
        info2 = font.render("in! Enter to create", True, (121,78,59))
        info3 = font.render("an account.", True, (121,78,59))
        info4 = font.render("Press escape to skip.", True, (255, 138, 138))

        screen.blit(info, (40, 60))
        screen.blit(info2, (40, 80))
        screen.blit(info3, (40, 100))
        screen.blit(info4, (40, 380))
        pygame.display.flip()

        end = False
        count = 0
        while end == False:
            clock.tick(20)
            count += 1

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and count >= 20:
                    if event.key == pygame.K_ESCAPE:
                        end = True
                        final_score = -1
                        current_pos = 0
                    else:
                        end = True
                        current_pos = 0
                        create(screen)

    # check if user is trying to upload score

    if logged_in and final_score != -1:

        info = font.render("You are logged in as", True, (255, 138, 138))
        info2 = font.render("user " + str(user) + ".", True, (255, 138, 138))
        info3 = font.render("Enter to upload score", True, (121,78,59))
        info4 = font.render("for level" + str(last_played) + ".", True, (121,78,59))
        info5 = font.render("Press escape to skip.", True, (255, 138, 138))

        screen.blit(bg, (0,0))
        screen.blit(info, (40, 60))
        screen.blit(info2, (40, 90))
        screen.blit(info3, (40, 140))
        screen.blit(info4, (40, 170))
        screen.blit(info5, (40, 380))
        pygame.display.flip()

        end = False
        count = 0
        while end == False:
            clock.tick(20)
            count += 1

            for event in pygame.event.get():

                # skip upload if user clicks escape
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and count >= 20:
                    end = True
                    final_score = -1

                # for any other button, upload score
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and count >= 20:
                    end = True
                    add_score(connection, user, last_played, final_score)

                    info = font.render("Success! Score added.", True, (255, 138, 138))

                    screen.blit(bg, (0,0))
                    screen.blit(info, (40, 60))
                    pygame.display.flip()
                    final_score = -1

                    sleep(2)

    # show rankings options - top of all time, choose level or choose user

    # initialise buttons

    top_button = Button('topbutton.png', 'topbuttonselected.png', (0, 0), 0, 'topscores')
    choose_level = Button('chooselevelbutton.png', 'chooselevelbuttonselected.png', (0, 140), 1, 'levelrankings')
    choose_user = Button('chooseuserbutton.png', 'chooseuserbuttonselected.png', (0, 270), 2, 'userrankings')

    buttons = [top_button, choose_level, choose_user]

    # load buttons

    for x in range(0, 3):
        buttons[x].check_selection(screen, current_pos)

    # change current selected button

    for event in pygame.event.get():

        # increment position on screen

        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_UP or event.key == pygame.K_w) and current_pos > 0:
                current_pos -= 1
            elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and current_pos < 2:
                current_pos +=1

        # if the user clicks enter, carry out the function of the button

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                hold = buttons[current_pos].action()
                current_pos = 0
                current_screen = hold
            if event.key == pygame.K_ESCAPE:
                current_screen = 'menu1'

def topscores(screen):
    global current_pos
    global current_screen
    global show_level
    global show_user
    global user

    bg = pygame.image.load("images/rankingscreen.png")
    screen.blit(bg, (0,0))

    # load top scores

    connection = sqlite3.connect("rhythmrolls.db")

    if show_level == 0:
        scores = top_five(connection)
    elif show_level == -1:
        if show_user != None:
            scores = top_five_from_user(connection, show_user)
        else:
            error = pygame.image.load("images/error.png")
            screen.blit(error, (0, 130))
            pygame.display.flip()
            sleep(3)
            scores = []
            show_level = 0
    else:
        scores = top_five_from_level(connection, show_level)

    for i in range(0, min(len(scores), 5)):
        score = font.render(str(scores[i][0]), True, (255, 255, 255))
        screen.blit(score, (70, (100 + 60*i)))
        name = font.render(str(scores[i][1]), True, (255, 255, 255))
        screen.blit(name, (273, (100 + 60*i)))

    # create buttons

    filter = Button('filter.png', 'filterselected.png', (0, 0), 0, 'levelrankings')
    myscore = Button('myscore.png', 'myscoreselected.png', (0, 0), 1, '')
    back = Button('back.png', 'backselected.png', (0, 0), 2, 'rankings')

    buttons = [filter, myscore, back]

    # load buttons

    for x in range(0, 3):
        buttons[x].check_selection(screen, current_pos)

    # change current selected button

    for event in pygame.event.get():

        # increment position on screen

        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_UP or event.key == pygame.K_w) and current_pos > 0:
                current_pos -= 1
            elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and current_pos < 2:
                current_pos += 1
            elif event.key == pygame.K_RETURN:
                    if current_pos == 1:
                        show_level = -1
                        show_user = user
                    else:
                        hold = buttons[current_pos].action()
                        print(hold)
                        current_pos = 0
                        current_screen = hold

def levelrankings(screen):
    global current_pos
    global current_screen
    global show_level

    bg = pygame.image.load("images/scorebkg.png")
    screen.blit(bg, (0,0))
    waiting = True

    while waiting:
        clock.tick(120)

        info = font.render("Type the level no.", True, (255, 138, 138))
        info2 = font.render("you would like to", True, (255, 138, 138))
        info3 = font.render("see rankings for:", True, (255, 138, 138))
        screen.blit(info, (40, 60))
        screen.blit(info2, (40, 80))
        screen.blit(info3, (40, 100))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if 49 <= event.key and event.key <= 52:
                    show_level = pygame.key.name(event.key)
                    waiting = False
                    current_screen = 'topscores'
                if event.key == pygame.K_ESCAPE:
                    current_screen = 'rankings'
                    waiting = False
                else:
                    info4 = font.render("Invalid key.", True, (255, 138, 138))
                    screen.blit(info4, (40, 400))
                
def userrankings(screen):
    global show_user
    global show_level
    global current_screen
    
    show_level = -1
    connection = sqlite3.connect("rhythmrolls.db")

    waiting = True
    user_temp = ''
    box = pygame.Rect(60, 150, 370, 40)

    while waiting:
        clock.tick(120)

        bg = pygame.image.load("images/scorebkg.png")
        screen.blit(bg, (0,0))

        info = font.render("Type the username", True, (255, 138, 138))
        info2 = font.render("you would like to", True, (255, 138, 138))
        info3 = font.render("see rankings for:", True, (255, 138, 138))
        screen.blit(info, (40, 60))
        screen.blit(info2, (40, 80))
        screen.blit(info3, (40, 100))
        pygame.draw.rect(screen, (237, 200, 171), box)

        text = font.render(user_temp, True, (121,78,59))
        screen.blit(text, (80, 160))
        pygame.display.flip()



        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                # check if it is a valid username
                if event.key == pygame.K_RETURN:
                    # if not, allow to keep typing
                    if check_user(connection, user_temp):
                        info4 = font.render("User does not exist.", True, (255, 138, 138))
                        user_temp = ''
                        screen.blit(info4, (40, 400))
                        pygame.display.flip()
                        sleep(2)
                    # else pop off stack and go back to topscores
                    else:
                        show_user = user_temp
                        waiting = False
                        current_screen = 'topscores'
                elif event.key == pygame.K_BACKSPACE:
                    user_temp = user_temp[:-1]
                elif event.key != pygame.K_SPACE:
                    if len(user_temp) <= 15:
                        # add character to temp text
                        user_temp += event.unicode
                if event.key == pygame.K_ESCAPE:
                    current_screen = 'rankings'
                    waiting = False
                
def accounts(screen):
    global logged_in
    global current_screen
    global current_pos
    global user

    bg = pygame.image.load("images/scorebkg.png")
    screen.blit(bg, (0, 0))

    create_account = Button('createbutton.png', 'createbuttonselected.png', (0, 20), 0, 'create')

    if not logged_in:
        login = Button('loginbutton.png', 'loginbuttonselected.png', (0, 160), 1, 'login')
    else:
        login = Button('logoutbutton.png', 'logoutbuttonselected.png', (0, 160), 1, 'logout')

    back_button = Button('backbutton3.png', 'backbutton3selected.png', (0,-10), 2, 'menu1')

    buttons = [create_account, login, back_button]

    # load buttons

    for x in range(0, 3):
        buttons[x].check_selection(screen, current_pos)

    # change current selected button

    for event in pygame.event.get():

        # increment position on screen

        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_UP or event.key == pygame.K_w) and current_pos > 0:
                current_pos -= 1
            elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and current_pos < 2:
                current_pos +=1
            elif event.key == pygame.K_RETURN:
                hold = buttons[current_pos].action()
                current_pos = 0
                current_screen = hold

def create(screen):
    global logged_in
    global current_screen
    global current_pos
    global user

    bg = pygame.image.load("images/scorebkg.png")
    screen.blit(bg, (0, 0))
    pygame.display.flip()
    connection = sqlite3.connect("rhythmrolls.db")
    complete1 = False
    complete2 = False

    # initialise info for username input

    user_temp = ''
    info, info2 = "", ""
    box = pygame.Rect(60, 100, 370, 40)
    title = font.render("Username:", True, (68,32,17))
    specials = ['@', '#', '-', '_', '.', ':', '*', '~']

    while not complete1:

        # check if user cancels, backspaces or clicks enter, else type into text box.

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_temp = user_temp[:-1]
                elif event.key == pygame.K_ESCAPE:
                    user_temp = ''
                    complete1 = True
                    complete2 = True
                    current_screen = 'accounts'    
                elif event.key == pygame.K_RETURN:
                    if len(user_temp) >= 4 and len(user_temp) <= 15:
                        if check_user(connection, user_temp):
                            info, info2 = "", ""
                            # allow temporary username to be accepted
                            user = user_temp
                            complete1 = True
                        else:
                            info, info2 = "This username is taken,", "try another one."
                            sleep(1)
                            user_temp = ''
                    else:
                        info, info2 = "Length must be between", "4 and 15 characters."
                # do not allow user to add a space
                elif event.unicode.isdigit() or event.unicode.isalpha() or event.unicode in specials:
                    if len(user_temp) <= 15:
                        # add character to temp username
                        user_temp += event.unicode
                    else:
                        info, info2 = "Length cannot be more than", "15 characters."
                        pygame.display.flip()

        bg = pygame.image.load("images/scorebkg.png")
        screen.blit(bg, (0, 0))
        text = font.render(user_temp, True, (255, 138, 138))
        info_render = small_font.render(info, True, (121,78,59))
        info2_render = small_font.render(info2, True, (121,78,59))
        pygame.draw.rect(screen, (237, 200, 171), box)
        screen.blit(text, (80, 110))
        screen.blit(title, (80, 60))
        screen.blit(info_render, (50, 160))
        screen.blit(info2_render, (50, 180))
        pygame.display.flip()

    if user_temp != '':
        # success message for username input

        info = "Username is valid."
        info_render = font.render(info, True, (121,78,59))
        screen.blit(info_render, (60, 160))
        pygame.display.flip()
        sleep(2)
        
    # initialise info for password input

    pass_temp = ''
    info, info2  = "", ""
    box = pygame.Rect(60, 100, 370, 40)
    title = font.render("Password:", True, (68,32,17))

    while not complete2:

        # check if user cancels, backspaces or clicks enter, else type into text box.

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    pass_temp = pass_temp[:-1]
                elif event.key == pygame.K_ESCAPE:
                    pass_temp = ''
                    complete2 = True
                elif event.key == pygame.K_RETURN:
                    if len(pass_temp) >= 8 and len(pass_temp) <= 15:
                        # check if password contains a number and one special character
                        if any(char.isdigit() for char in pass_temp) and any(special in pass_temp for special in specials):
                            password = pass_temp
                            info, info2 = "", ""
                            complete2 = True
                        else:
                            info, info2 = "Must contain at least one", "number and special character"
                    else:
                        info, info2 = "Length must be between", "8 and 15 characters."
                elif event.unicode.isdigit() or event.unicode.isalpha() or event.unicode in specials:
                    if len(pass_temp) <= 15:
                        pass_temp += event.unicode
                    else:
                        info, info2 = "Length cannot be more than", "15 characters."
                        pygame.display.flip()

        bg = pygame.image.load("images/scorebkg.png")
        screen.blit(bg, (0, 0))
        text = font.render(pass_temp, True, (255, 138, 138))
        title = font.render("Password:", True, (68,32,17))
        info_render = small_font.render(info, True, (121,78,59))
        info2_render = small_font.render(info2, True, (121,78,59))
        pygame.draw.rect(screen, (237, 200, 171), box)
        screen.blit(text, (80, 110))
        screen.blit(title, (80, 60))
        screen.blit(info_render, (50, 160))
        screen.blit(info2_render, (50, 180))
        pygame.display.flip()

    if pass_temp != '':

        # success message for password input

        info = "Password is valid."
        info_render = font.render(info, True, (121,78,59))
        screen.blit(info_render, (60, 160))
        pygame.display.flip()
        sleep(2)

        # salt and hash password

        salt = bcrypt.gensalt()
        password = password.encode()
        pass_hash = bcrypt.hashpw(password, salt)

        # create account
        create_account(connection, user, pass_hash)

        info = "Success! Account created."
        logged_in = True

        info_render = small_font.render(info, True, (68,32,17))
        screen.blit(info_render, (60, 200))
        pygame.display.flip()
        sleep(3)

    connection.close()
    current_screen = 'accounts'

def login(screen):
    global logged_in
    global current_screen
    global current_pos
    global user

    connection = sqlite3.connect("rhythmrolls.db")

    bg = pygame.image.load("images/scorebkg.png")
    screen.blit(bg, (0, 0))

    box = pygame.Rect(60, 100, 370, 40)
    pygame.draw.rect(screen, (237, 200, 171), box)

    title = font.render("Username:", True, (68,32,17))
    screen.blit(title, (80, 60))
    complete1 = False
    user_input = ''
    info, info2 = '', ''
    complete2 = False
    count = 0
    specials = ['@', '#', '-', '_', '.', ':', '*', '~']

    while not complete1:

        # check if user cancels, backspaces or clicks enter, else type into text box.

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                elif event.key == pygame.K_ESCAPE:
                    user_input = ''
                    complete1 = True
                    complete2 = True
                    current_screen = 'accounts'    
                elif event.key == pygame.K_RETURN:
                    if not check_user(connection, user_input):
                        info, info2 = "", ""
                        # validate username as existing
                        complete1 = True
                    else:
                        info, info2 = "No account exists with", "this username."
                        user_input = ''
                # do not allow user to add a space
                elif event.unicode.isdigit() or event.unicode.isalpha() or event.unicode in specials:
                    if len(user_input) <= 15:
                        # add character to temp username
                        user_input += event.unicode

        bg = pygame.image.load("images/scorebkg.png")
        screen.blit(bg, (0, 0))
        text = font.render(user_input, True, (255, 138, 138))
        info_render = small_font.render(info, True, (121,78,59))
        info2_render = small_font.render(info2, True, (121,78,59))
        pygame.draw.rect(screen, (237, 200, 171), box)
        screen.blit(text, (80, 110))
        screen.blit(title, (80, 60))
        screen.blit(info_render, (50, 160))
        screen.blit(info2_render, (50, 180))
        pygame.display.flip()
    
    # success text for username

    if user_input != '':

        info = "Next, enter the password."
        info_render = small_font.render(info, True, (121,78,59))
        screen.blit(info_render, (60, 160))
        pygame.display.flip()
        sleep(2)

    # check password

    pass_input = ''
    title = font.render("Password:", True, (68,32,17))

    while not complete2:

    # check if user cancels, backspaces or clicks enter, else type into text box.

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    pass_input = pass_input[:-1]
                elif event.key == pygame.K_ESCAPE:
                    pass_input = ''
                    complete2 = True 
                    current_screen = 'accounts'   
                elif event.key == pygame.K_RETURN:
                    if check_password(connection, user_input, pass_input):
                        info, info2 = "", ""
                        # allow temporary username to be accepted
                        complete2 = True
                    else:
                        info, info2 = "Incorrect password.", "Please try again."
                        count += 1
                        pass_input = ''
                        if count >= 3:
                            info, info2 = "Too many incorrect attempts.", ""
                            pass_input = ''
                            current_screen = 'accounts'
                            complete2 = True
                # do not allow user to add a space
                elif event.unicode.isdigit() or event.unicode.isalpha() or event.unicode in specials:
                    if len(pass_input) <= 15:
                        # add character to temp username
                        pass_input += event.unicode

        bg = pygame.image.load("images/scorebkg.png")
        screen.blit(bg, (0, 0))
        text = font.render(pass_input, True, (255, 138, 138))
        info_render = small_font.render(info, True, (121,78,59))
        info2_render = small_font.render(info2, True, (121,78,59))
        pygame.draw.rect(screen, (237, 200, 171), box)
        screen.blit(text, (80, 110))
        screen.blit(title, (80, 60))
        screen.blit(info_render, (45, 160))
        screen.blit(info2_render, (45, 180))
        pygame.display.flip()

    if pass_input != '':
        # success message for username input

        info = "Successful login!"
        info_render = font.render(info, True, (121,78,59))
        screen.blit(info_render, (60, 160))
        pygame.display.flip()

        logged_in = True
        user = user_input
        print(user)

        current_screen = 'accounts'
    
    sleep(2)

def logout(screen):
    global logged_in
    global current_screen
    global current_pos
    global user

    bg = pygame.image.load("images/scorebkg.png")
    screen.blit(bg, (0, 0))

    logged_in = False
    user = None

    text1 = font.render("You have successfully been", True, (255, 138, 138))
    text2 = font.render("logged out.", True, (255, 138, 138))
    text3 = font.render("Press escape to exit.", True, (255, 138, 138))

    screen.blit(text1, (40, 60))
    screen.blit(text2, (40, 80))
    screen.blit(text3, (40, 380))

    for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    current_screen = 'accounts'

def placeholder(screen):
    global current_pos
    global current_screen

    bg = pygame.image.load("images/menuscreen.png")
    screen.blit(bg, (0, 0))

    back_button = Button('backbutton.png', 'backbuttonselected.png', (0, -105), 0, 'menu1')
    back_button.check_selection(screen, current_pos)

    for event in pygame.event.get():
         if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            current_pos = 0
            current_screen = back_button.action()

# setting up the main game

pygame.init()
screen = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()
pygame.display.set_caption("Rhythm Rolls")
current_pos = 0
discrepancy_sum = 0
notes_score = [0, 0, 0, 0]
final_score = -1
logged_in = False
user = None

current_screen = 'start'

# download font

font = pygame.font.Font("dogicapixel.ttf", 20)
small_font = pygame.font.Font("dogicapixel.ttf", 15)

# start time flag and variable

start_flag = True
start_time = 0

# play background music

pygame.mixer.music.load("music/background_music.mp3")
current_vol = 0.5
pygame.mixer.music.set_volume(current_vol)
pygame.mixer.music.play(-1)

# initialise keybind

keybind = pygame.K_SPACE

run = True

while run:
    clock.tick(120)

    # quit

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # screen functions

    if current_screen == 'start':
        start(screen)
    elif current_screen == 'menu1':
        menu1(screen)
    elif current_screen == 'menu2':
        menu2(screen)
    elif current_screen == 'levels':
        levelselect1(screen)
    elif current_screen == 'levelselect2':
        levelselect2(screen)
    elif current_screen == 'tutorial':
        tutorial(screen)
    elif current_screen == 'accounts':
        accounts(screen)
    elif current_screen == 'login':
        login(screen)
    elif current_screen == 'logout':
        logout(screen)
    elif current_screen == 'rankings':
        rankings(screen)
    elif current_screen == 'topscores':
        topscores(screen)
    elif current_screen == 'levelrankings':
        levelrankings(screen)
    elif current_screen == 'userrankings':
        userrankings(screen)        
    elif current_screen == 'create':
        create(screen)
    elif current_screen == 'options':
        options(screen)
    elif current_screen == 'quit':
        run = False

    pygame.display.update()

pygame.quit()