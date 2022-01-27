import time
import pygame as pg
import sys
from pygame.locals import *


class tictactoe:

    def __init__(self):
        self.XO = 'x'
        self.winner = None
        self.draw = False
        self.width = 400
        self.height = 400
        self.white = (255, 255, 255)
        self.line_color = (10, 10, 10)
        self.TTT = [[None] * 3, [None] * 3, [None] * 3]
        self.fps = 30
        self.CLOCK = pg.time.Clock()
        self.screen = pg.display.set_mode((self.width, self.height + 100), 0, 32)
        # images and backgrounds
        self.opening = pg.image.load('tic tac opening.png')
        self.x_img = pg.image.load('x.png')
        self.o_img = pg.image.load('o.png')
        self.initialize_game()
        self.resize_images()
        self.game_opening()
        self.reload()

    def initialize_game(self):
        pg.init()
        pg.display.set_caption("Tic Tac Toe Game")

    def resize_images(self):
        self.x_img = pg.transform.scale(self.x_img, (80, 80))
        self.o_img = pg.transform.scale(self.o_img, (80, 80))
        self.opening = pg.transform.scale(self.opening, (self.width, self.height + 100))

    def game_opening(self):
        self.screen.blit(self.opening, (0, 0))
        pg.display.update()
        time.sleep(1)
        self.screen.fill(self.white)

        # Drawing vertical lines
        pg.draw.line(self.screen, self.line_color, (self.width / 3, 0), (self.width / 3, self.height), 7)
        pg.draw.line(self.screen, self.line_color, (self.width / 3 * 2, 0), (self.width / 3 * 2, self.height), 7)
        # Drawing horizontal lines
        pg.draw.line(self.screen, self.line_color, (0, self.height / 3), (self.width, self.height / 3), 7)
        pg.draw.line(self.screen, self.line_color, (0, self.height / 3 * 2), (self.width, self.height / 3 * 2), 7)
        self.draw_status()

    def draw_status(self):
        if self.winner is None:
            message = self.XO.upper() + "'s Turn"
        else:
            message = self.winner.upper() + " won!"
        if self.draw:
            message = 'Game Draw!'
        font = pg.font.Font(None, 30)
        text = font.render(message, True, (255, 255, 255))

        # copy the rendered message onto the board
        self.screen.fill((0, 0, 0), (0, 400, 500, 100))
        text_rect = text.get_rect(center=(self.width / 2, 500 - 50))
        self.screen.blit(text, text_rect)
        pg.display.update()

    def check_win(self):
        # check for winning rows
        for row in range(0, 3):
            if (self.TTT[row][0] == self.TTT[row][1] == self.TTT[row][2]) and (self.TTT[row][0] is not None):
                # this row won
                self.winner = self.TTT[row][0]
                pg.draw.line(self.screen, (250, 0, 0), (0, (row + 1) * self.height / 3 - self.height / 6),
                             (self.width, (row + 1) * self.height / 3 - self.height / 6), 4)
                break

        # check for winning columns
        for col in range(0, 3):
            if (self.TTT[0][col] == self.TTT[1][col] == self.TTT[2][col]) and (self.TTT[0][col] is not None):
                # this column won
                self.winner = self.TTT[0][col]
                # draw winning line
                pg.draw.line(self.screen, (250, 0, 0), ((col + 1) * self.width / 3 - self.width / 6, 0),
                             ((col + 1) * self.width / 3 - self.width / 6, self.height), 4)
                break

        # check for diagonal winners
        if (self.TTT[0][0] == self.TTT[1][1] == self.TTT[2][2]) and (self.TTT[0][0] is not None):
            # game won diagonally left to right
            self.winner = self.TTT[0][0]
            pg.draw.line(self.screen, (250, 70, 70), (50, 50), (350, 350), 4)

        if (self.TTT[0][2] == self.TTT[1][1] == self.TTT[2][0]) and (self.TTT[0][2] is not None):
            # game won diagonally right to left
            self.winner = self.TTT[0][2]
            pg.draw.line(self.screen, (250, 70, 70), (350, 50), (50, 350), 4)

        if all([all(row) for row in self.TTT]) and self.winner is None:
            self.draw = True
        self.draw_status()

    def drawXO(self, row, col):
        posx = 0
        posy = 0
        if row == 1:
            posx = 30
        if row == 2:
            posx = self.width / 3 + 30
        if row == 3:
            posx = self.width / 3 * 2 + 30

        if col == 1:
            posy = 30
        if col == 2:
            posy = self.height / 3 + 30
        if col == 3:
            posy = self.height / 3 * 2 + 30
        self.TTT[row - 1][col - 1] = self.XO
        if self.XO == 'x':
            self.screen.blit(self.x_img, (posy, posx))
            self.XO = 'o'
        else:
            self.screen.blit(self.o_img, (posy, posx))
            self.XO = 'x'
        pg.display.update()

    def userClick(self):
        # get coordinates of mouse click
        x, y = pg.mouse.get_pos()

        # get column of mouse click (1-3)
        if x < self.width / 3:
            col = 1
        elif x < self.width / 3 * 2:
            col = 2
        elif x < self.width:
            col = 3
        else:
            col = None

        # get row of mouse click (1-3)
        if y < self.height / 3:
            row = 1
        elif y < self.height / 3 * 2:
            row = 2
        elif y < self.height:
            row = 3
        else:
            row = None
        # print(row,col)

        if row and col and self.TTT[row - 1][col - 1] is None:
            # draw the x or o on screen
            self.drawXO(row, col)
            self.check_win()

    def reset_game(self):
        time.sleep(3)
        self.XO = 'x'
        self.draw = False
        self.game_opening()
        self.winner = None
        self.TTT = [[None] * 3, [None] * 3, [None] * 3]

    def reload(self):
        while True:
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    # the user clicked; place an X or O
                    self.userClick()
                    if self.winner or self.draw:
                        self.reset_game()

            pg.display.update()
            self.CLOCK.tick(self.fps)


my_game = tictactoe()
