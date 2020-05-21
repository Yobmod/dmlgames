
import random
import pygame
import sys
from pygame.locals import QUIT, K_ESCAPE, KEYUP, MOUSEMOTION, MOUSEBUTTONUP
# import os
# import dotenv
# import toolz
# import itertools
# import more_itertools
# import functools
# from mypy_extensions import TypedDict
# from types import MappingProxyType

from typing import (Union,
                    Optional as Opt,
                    # Mapping,
                    # Dict,
                    List,
                    Tuple,
                    # Any,
                    )

iconType = Tuple[str, Tuple[int, int, int]]
boardType = List[List[iconType]]
boxType = Tuple[int, int]

FPS = 30  # frames per second, the general speed of the program
WINDOWWIDTH = 640  # size of window's width in pixels
WINDOWHEIGHT = 480  # size of windows' height in pixels
REVEALSPEED = 8  # speed boxes' sliding reveals and covers
BOXSIZE = 40  # size of box height & width in pixels
GAPSIZE = 10  # size of gap between boxes in pixels
BOARDWIDTH = 3  # number of columns of icons
BOARDHEIGHT = 2  # number of rows of icons
assert (BOARDWIDTH * BOARDHEIGHT) % 2 == 0, 'Board needs to have an even number of boxes for pairs of matches.'
XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 2)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) / 2)

#            R    G    B
GRAY = (100, 100, 100)
NAVYBLUE = (60, 60, 100)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)

BGCOLOR = NAVYBLUE
LIGHTBGCOLOR = GRAY
BOXCOLOR = WHITE
HIGHLIGHTCOLOR = BLUE

DONUT = 'donut'
SQUARE = 'square'
DIAMOND = 'diamond'
LINES = 'lines'
OVAL = 'oval'

ALLCOLORS: Tuple[Tuple[int, int, int], ...] = (RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN)
ALLSHAPES: Tuple[str, str, str, str, str] = (DONUT, SQUARE, DIAMOND, LINES, OVAL)
assert len(ALLCOLORS) * len(ALLSHAPES) * 2 >= BOARDWIDTH * BOARDHEIGHT, "Board is too big for the number of shapes/colors defined."


class MemoryGame():
    """"""

    def __init__(self) -> None:
        self.FPSCLOCK = pygame.time.Clock()
        self.DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
        self.board = self.getRandomizedBoard()
        pygame.init()
        pygame.display.set_caption('Memory Game')
        self.DISPLAYSURF.fill(BGCOLOR)

    def main(self) -> None:
        mousex = 0  # used to store x coordinate of mouse event
        mousey = 0  # used to store y coordinate of mouse event

        mainBoard = self.getRandomizedBoard()
        revealedBoxes = self.generateRevealedBoxesData(False)

        firstSelection: Opt[Tuple[int, int]] = None  # stores the (x, y) of the first box clicked.
        self.startGameAnimation(mainBoard)

        while True:  # main game loop
            mouseClicked = False

            self.DISPLAYSURF.fill(BGCOLOR)  # drawing the window
            self.drawBoard(mainBoard, revealedBoxes)

            for event in pygame.event.get():  # event handling loop
                if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEMOTION:
                    mousex, mousey = event.pos
                elif event.type == MOUSEBUTTONUP:
                    mousex, mousey = event.pos
                    mouseClicked = True

            boxx, boxy = self.getBoxAtPixel(mousex, mousey)
            if boxx is not None and boxy is not None:  # The mouse is currently over a box.
                if not revealedBoxes[boxx][boxy]:  # and box is not already revealed
                    self.drawHighlightBox(boxx, boxy)  # draw highlight on box

                if not revealedBoxes[boxx][boxy] and mouseClicked:  # ifbox is not already revealed and clicked on
                    self.revealBoxesAnimation(mainBoard, [(boxx, boxy)])  # reveal the box
                    revealedBoxes[boxx][boxy] = True  # set the box as "revealed"
                    if firstSelection is None:  # the current box was the first box clicked
                        firstSelection = (boxx, boxy)
                    else:  # the current box was the second box clicked
                        secondSelection = (boxx, boxy)
                        got_a_match = self.check_match(mainBoard, firstSelection, secondSelection)
                        # Check if there is a match between the two icons.
                        if got_a_match is False:
                            self.no_match_reset(mainBoard, revealedBoxes, firstSelection, secondSelection)
                        elif self.hasWon(revealedBoxes):  # if there is a match, check if all pairs found
                            self.win_reset(mainBoard)  # show win animaition TODO ask to play again

                            play_again = True
                            if play_again:
                                mainBoard = self.getRandomizedBoard()  # Reset the board
                                revealedBoxes = self.generateRevealedBoxesData(False)
                                self.drawBoard(mainBoard, revealedBoxes)  # Show the fully unrevealed board for a second.
                                pygame.display.update()
                                pygame.time.wait(1000)
                                self.startGameAnimation(mainBoard)    # Replay the start game animation.
                            else:
                                break  # TODO
                        firstSelection = None  # reset firstSelection variable

            # Redraw the screen and wait a clock tick.
            pygame.display.update()
            self.FPSCLOCK.tick(FPS)

    def check_match(self, board: boardType, firstbox: boxType, secondbox: boxType) -> bool:
        icon1shape, icon1color = self.getShapeAndColor(board, firstbox[0], firstbox[1])
        icon2shape, icon2color = self.getShapeAndColor(board, secondbox[0], secondbox[1])
        if icon1shape != icon2shape or icon1color != icon2color:  # no match!
            return False
        else:
            return True

    def no_match_reset(self, board: boardType, revealed: List[List[bool]], firstbox: boxType, secondbox: boxType) -> None:
        pygame.time.wait(1000)  # leave failed match revealed 1 sec  TODO alter with difficulty
        self.coverBoxesAnimation(board, [(firstbox[0], firstbox[1]), (secondbox[0], secondbox[1])], )
        revealed[firstbox[0]][firstbox[1]] = False
        revealed[secondbox[0]][secondbox[1]] = False  # set the 2 failed match boxes to hidden

    def win_reset(self, board: boardType) -> None:
        self.gameWonAnimation(board)
        pygame.time.wait(2000)

    def generateRevealedBoxesData(self, val: bool) -> List[List[bool]]:
        revealedBoxes = []
        for _ in range(BOARDWIDTH):
            revealedBoxes.append([val] * BOARDHEIGHT)
        return revealedBoxes

    def getRandomizedBoard(self) -> boardType:
        # Get a list of every possible shape in every possible color.
        icon: iconType
        icons: List[iconType] = []
        for color in ALLCOLORS:
            for shape in ALLSHAPES:
                icons.append((shape, color))

        random.shuffle(icons)  # randomize the order of the icons list
        numIconsUsed = int(BOARDWIDTH * BOARDHEIGHT / 2)  # calculate how many icons are needed
        icons = icons[:numIconsUsed] * 2  # make two of each
        random.shuffle(icons)

        # Create the board data structure, with randomly placed icons.
        board: boardType = []
        for _ in range(BOARDWIDTH):
            column: List[iconType] = []
            for __ in range(BOARDHEIGHT):
                column.append(icons[0])
                del icons[0]  # remove the icons as we assign them
            board.append(column)
        return board

    def splitBoxesIntoGroupsOf(self, groupSize: int, theList: List[boxType]) -> List[List[boxType]]:
        # splits a list into a list of lists, where the inner lists have at
        # most groupSize number of items.
        result = []
        for i in range(0, len(theList), groupSize):
            result.append(theList[i:i + groupSize])
        return result

    def leftTopCoordsOfBox(self, boxx: int, boxy: int) -> Tuple[int, int]:
        # Convert board coordinates to pixel coordinates
        left = boxx * (BOXSIZE + GAPSIZE) + XMARGIN
        top = boxy * (BOXSIZE + GAPSIZE) + YMARGIN
        return (left, top)

    def getBoxAtPixel(self, x: int, y: int) -> Union[boxType, Tuple[None, None]]:
        for boxx in range(BOARDWIDTH):
            for boxy in range(BOARDHEIGHT):
                left, top = self.leftTopCoordsOfBox(boxx, boxy)
                boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
                if boxRect.collidepoint(x, y):
                    return (boxx, boxy)
        return (None, None)

    def drawIcon(self, shape: str, color: Tuple[int, int, int], boxx: int, boxy: int) -> None:
        quarter = int(BOXSIZE * 0.25)  # syntactic sugar
        half = int(BOXSIZE * 0.5)  # syntactic sugar

        left, top = self.leftTopCoordsOfBox(boxx, boxy)  # get pixel coords from board coords
        # Draw the shapes
        if shape == DONUT:
            pygame.draw.circle(self.DISPLAYSURF, color, (left + half, top + half), half - 5)
            pygame.draw.circle(self.DISPLAYSURF, BGCOLOR, (left + half, top + half), quarter - 5)
        elif shape == SQUARE:
            pygame.draw.rect(self.DISPLAYSURF, color, (left + quarter, top + quarter, BOXSIZE - half, BOXSIZE - half))
        elif shape == DIAMOND:
            pygame.draw.polygon(self.DISPLAYSURF, color, ((left + half, top), (left + BOXSIZE - 1, top + half),
                                                          (left + half, top + BOXSIZE - 1), (left, top + half)))
        elif shape == LINES:
            for i in range(0, BOXSIZE, 4):
                pygame.draw.line(self.DISPLAYSURF, color, (left, top + i), (left + i, top))
                pygame.draw.line(self.DISPLAYSURF, color, (left + i, top + BOXSIZE - 1), (left + BOXSIZE - 1, top + i))
        elif shape == OVAL:
            pygame.draw.ellipse(self.DISPLAYSURF, color, (left, top + quarter, BOXSIZE, half))

    def getShapeAndColor(self, board: boardType, boxx: int, boxy: int) -> iconType:
        board_shape = board[boxx][boxy][0]
        board_color = board[boxx][boxy][1]
        return (board_shape, board_color)

    def drawBoxCovers(self, board: boardType, boxes: List[boxType], coverage: int) -> None:
        # Draws boxes being covered/revealed. "boxes" is a list
        # of two-item tuples?lists, which have the x & y spot of the box.
        for box in boxes:
            left, top = self.leftTopCoordsOfBox(box[0], box[1])
            pygame.draw.rect(self.DISPLAYSURF, BGCOLOR, (left, top, BOXSIZE, BOXSIZE))
            shape, color = self.getShapeAndColor(board, box[0], box[1])
            self.drawIcon(shape, color, box[0], box[1])
            if coverage > 0:  # only draw the cover if there is an coverage
                pygame.draw.rect(self.DISPLAYSURF, BOXCOLOR, (left, top, coverage, BOXSIZE))
        pygame.display.update()
        self.FPSCLOCK.tick(FPS)

    def revealBoxesAnimation(self, board: boardType, boxesToReveal: List[boxType]) -> None:
        # Do the "box reveal" animation.
        for coverage in range(BOXSIZE, (-REVEALSPEED) - 1, -REVEALSPEED):
            self.drawBoxCovers(board, boxesToReveal, coverage)

    def coverBoxesAnimation(self, board: boardType, boxesToCover: List[boxType]) -> None:
        # Do the "box cover" animation.
        for coverage in range(0, BOXSIZE + REVEALSPEED, REVEALSPEED):
            self.drawBoxCovers(board, boxesToCover, coverage)

    def drawBoard(self, board: boardType, revealed: List[List[bool]]) -> None:
        # Draws all of the boxes in their covered or revealed state.
        for boxx in range(BOARDWIDTH):
            for boxy in range(BOARDHEIGHT):
                left, top = self.leftTopCoordsOfBox(boxx, boxy)
                if not revealed[boxx][boxy]:
                    # Draw a covered box.
                    pygame.draw.rect(self.DISPLAYSURF, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE))
                else:
                    # Draw the (revealed) icon.
                    shape, color = self.getShapeAndColor(board, boxx, boxy)
                    self.drawIcon(shape, color, boxx, boxy)

    def drawHighlightBox(self, boxx: int, boxy: int) -> None:
        left, top = self.leftTopCoordsOfBox(boxx, boxy)
        pygame.draw.rect(self.DISPLAYSURF, HIGHLIGHTCOLOR, (left - 5, top - 5, BOXSIZE + 10, BOXSIZE + 10), 4)

    def startGameAnimation(self, board: boardType) -> None:
        # Randomly reveal the boxes 8 at a time.
        coveredBoxes = self.generateRevealedBoxesData(False)
        boxes = []
        for x in range(BOARDWIDTH):
            for y in range(BOARDHEIGHT):
                boxes.append((x, y))
        random.shuffle(boxes)
        boxGroups = self.splitBoxesIntoGroupsOf(8, boxes)

        self.drawBoard(board, coveredBoxes)
        for boxGroup in boxGroups:
            self.revealBoxesAnimation(board, boxGroup)
            self.coverBoxesAnimation(board, boxGroup)

    def gameWonAnimation(self, board: boardType) -> None:
        # flash the background color when the player has won
        coveredBoxes = self.generateRevealedBoxesData(True)
        color1 = LIGHTBGCOLOR
        color2 = BGCOLOR

        for _ in range(13):
            color1, color2 = color2, color1  # swap colors
            self.DISPLAYSURF.fill(color1)
            self.drawBoard(board, coveredBoxes)
            pygame.display.update()
            pygame.time.wait(300)

    def hasWon(self, revealedBoxes: List[List[bool]]) -> bool:
        # Returns True if all the boxes have been revealed, otherwise False
        for i in revealedBoxes:
            if False in i:
                return False  # return False if any boxes are covered.
        return True


if __name__ == '__main__':
    game = MemoryGame()
    game.main()
