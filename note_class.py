import pygame
from time import sleep

class Note():

    def __init__(self, time, hit_time):
        self.time = time
        self.hit_time = hit_time
        self.is_hit = False
        self.timeplayed = 0
        self.centre_pos = (250, 200)
        self.max_radius = 60
        self.speed = 50/(hit_time - time)
        self.current_radius = 0
        self.color = (183, 28, 28)
        self.font = pygame.font.Font("dogicapixel.ttf", 15)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.centre_pos, self.current_radius, width=3)
        pygame.display.flip()

    def hit_check(self, screen, current_time, clock, level): 
        if current_time - self.hit_time >= 500:
            # checks if current time is more than 500ms greater ie. note has been missed
            self.is_hit = True
            self.current_radius = 0
            self.draw(screen)
        else:
            self.is_hit = True
            self.current_radius = 0
            self.draw(screen)
            self.timeplayed = current_time

    
    def update_score(self, screen, discrepancy_sum, notes_score):
        # discrepancy_sum = total of note discrepancies 
        discrepancy = abs(self.timeplayed - self.hit_time)
        discrepancy_sum += min(discrepancy, 500)
        if discrepancy <= 100:
            # perfect note
            score = 'Perfect!'
            notes_score[3] += 1
        elif discrepancy <= 250:
            # good note
            score = 'Good!'
            notes_score[2] += 1
        elif discrepancy <= 500:
            # bad note
            score = 'Bad!'
            notes_score[1] += 1
        else:
            score = 'Miss!'
            notes_score[0] += 1

        text = self.font.render(score, True, (255, 138, 138))
        screen.blit(text, (40, 60)) 
        pygame.display.flip()

        return discrepancy_sum, notes_score

    def update_radius(self, screen, delta_time):
        if not self.is_hit and self.current_radius < self.max_radius:
            self.current_radius += (self.speed)*delta_time
            self.draw(screen)

    def reset_note(self):
        self.is_hit = False
        self.current_radius = 0

class hardNote(Note):

    def update_score(self, screen, discrepancy_sum, notes_score):
        # discrepancy_sum = total of note discrepancies 
        discrepancy = abs(self.timeplayed - self.hit_time)
        discrepancy_sum += min(discrepancy, 300)
        if discrepancy <= 30:
            # perfect note
            score = 'Perfect!'
            notes_score[3] += 1
        elif discrepancy <= 100:
            # good note
            score = 'Good!'
            notes_score[2] += 1
        elif discrepancy <= 300:
            # bad note
            score = 'Bad!'
            notes_score[1] += 1
        else:
            score = 'Miss!'
            notes_score[0] += 1

        text = self.font.render(score, True, (255, 138, 138))
        screen.blit(text, (40, 60)) 
        pygame.display.flip()

        return discrepancy_sum, notes_score
    
class tutorialNote(Note):

    def __init__(self, time, hit_time):
        super().__init__(time, hit_time)
        self.max_radius = 50

    def update_score(self, screen, discrepancy_sum, notes_score):
        return 0, [0, 0, 0, 0]

    def update_radius(self, screen, delta_time):
        super().update_radius(screen, delta_time)
        if self.current_radius >= 50:
            self.is_hit = True
            small_font = pygame.font.Font("dogicapixel.ttf", 15)
            current = small_font.render("Hit!", True, (255, 138, 138)) 
            screen.blit(current, (40, 60)) 
            pygame.display.flip()
            
class placeholderNote(Note):

    # do not add score like normal notes, score calculated within holdNote

    def __init__(self, time, hit_time):
        super().__init__(time, hit_time)
        self.color = (111, 206, 211)

    def update_score(self, screen, discrepancy_sum, notes_score):
        return 0, [0, 0, 0, 0]

class holdNote(Note):
     
    def __init__(self, time, hit_time, hold_time):
        super().__init__(time, hit_time)
        self.color = (111, 206, 211)
        self.hold_time = hold_time
        self.time_held = 0

    def hit_check(self, screen, current_time, clock, level):

        if current_time - self.hit_time >= 500:
                # checks if current time is more than 500ms greater ie. note has been missed
                self.is_hit = True
                self.timeplayed = current_time
                self.current_radius = 0
                self.draw(screen)
        else:
            end = False

            # initialise required variables

            # time when started holding
            start_time = pygame.time.get_ticks() - current_time
            placeholder = placeholderNote(0, self.hold_time)

            while not end and self.current_radius > 0:

                # tracks time from holding until current
            
                self.time_held = pygame.time.get_ticks() - start_time - current_time

                # render background

                bg = pygame.image.load("images/level" + str(level) + "screen.png")
                screen.blit(bg, (0, 0))
                text = self.font.render('Holding...', True, (255, 138, 138))
                screen.blit(text, (40, 60)) 
                
                # expand second circle

                pygame.draw.circle(screen, (239, 154, 154), (250, 200), 50, width=3)
                delta_time = clock.tick(120)
                placeholder.update_radius(screen, delta_time)
                
                # check if missed end - if current time is more than hit_time + hold_time + 500

                if self.time_held > (self.hold_time + 500):
                    self.time_held = pygame.time.get_ticks() - start_time - current_time
                    end = True
                    self.is_hit = True

                # check if key unpressed

                for event in pygame.event.get():
                    if event.type == pygame.KEYUP:
                        self.time_held = pygame.time.get_ticks() - start_time - current_time
                        self.is_hit = True
                        end = True
                        placeholder.current_radius = 0
                        self.current_radius = 0
                        self.speed = 0
                        screen.blit(bg, (0, 0))

    def update_score(self, screen, discrepancy_sum, notes_score):
        # on percentage of time held for compared to time meant to be held for
        if self.time_held == 0:
            discrepancy = 500
        else:
            discrepancy = abs(self.hold_time - self.time_held)/self.hold_time * 500

        discrepancy_sum += min(discrepancy, 500)

        if discrepancy <= 100:
            # perfect note
            score = 'Perfect!'
            notes_score[3] += 1
        elif discrepancy <= 300:
            # good note
            score = 'Good!'
            notes_score[2] += 1
        elif discrepancy < 500:
            # bad note
            score = 'Bad!'
            notes_score[1] += 1
        else:
            score = 'Miss!'
            notes_score[0] += 1


        text = self.font.render(score, True, (255, 138, 138))
        screen.blit(text, (40, 60)) 
        pygame.display.flip()

        return discrepancy_sum, notes_score
    
class tutorialHoldNote(holdNote, tutorialNote):

    def __init__(self, time, hit_time, hold_time):
        holdNote.__init__(self, time, hit_time, hold_time)

    def update_score(self, screen, discrepancy_sum, notes_score):
        return tutorialNote.update_score(self, screen, discrepancy_sum, notes_score)
    
    def update_radius(self, screen, delta_time):
        tutorialNote.update_radius(self, screen, delta_time)
        placeholder_press = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_a})
        pygame.event.post(placeholder_press)

    
    def hit_check(self, screen, current_time, clock, level):
            
        if self.is_hit:

            end = False

            # initialise required variables

            # time when started holding
            start_time = pygame.time.get_ticks() - current_time
            placeholder = placeholderNote(0, self.hold_time)

            while not end:
                
                # tracks time from holding until current
            
                self.time_held = pygame.time.get_ticks() - start_time - current_time

                # render background

                bg = pygame.image.load("images/level" + str(level) + "screen.png")
                screen.blit(bg, (0, 0))
                text = self.font.render('Holding...', True, (255, 138, 138))
                screen.blit(text, (40, 60)) 
                
                # expand second circle

                pygame.draw.circle(screen, (239, 154, 154), (250, 200), 50, width=3)
                delta_time = clock.tick(120)
                placeholder.update_radius(screen, delta_time)

                # check if end - if time held = hold time 
                if self.time_held >= self.hold_time:
                    self.time_held = pygame.time.get_ticks() - start_time - current_time
                    end = True
