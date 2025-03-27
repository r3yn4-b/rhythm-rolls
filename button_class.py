import pygame

class Button():

    def __init__(self, image, selected_image, position, order, link):
        self.image = 'images/' + image
        self.selected_image = 'images/' + selected_image
        self.position = position
        self.order = order
        self.is_selected = False
        self.link = link


    def check_selection(self, screen, current_pos):
        if current_pos == self.order:
            selected_img = pygame.image.load(self.selected_image)
            screen.blit(selected_img, self.position)
        else:
            self.is_selected = False
            main_image = pygame.image.load(self.image)
            screen.blit(main_image, self.position)

    def action(self):
        return self.link


