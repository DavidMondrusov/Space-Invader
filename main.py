import random
import math
from typing import ParamSpecArgs
import pygame
from pygame import MOUSEBUTTONDOWN, mixer

SCREENWIDTH, SCREENHEIGHT = 800, 600
FPS = 40
speed = 1
pygame.init()
font = pygame.font.Font("resources/AUSTRALIA-TITLE.otf", 32)
started = False
disSco = 0
PURPLE = (170, 75, 189)


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Space Invaders")
        icon = pygame.image.load("resources/ufo.png")
        pygame.display.set_icon(icon)

        self.gameStateManager = GameStateManager("menu")
        self.menu = Menu(self.screen, self.gameStateManager)
        self.options = Options(self.screen, self.gameStateManager)
        self.start = Start(self.screen, self.gameStateManager)

        self.states = {"menu": self.menu, "start": self.start, "options": self.options}

    def run(self):
        self.running = True
        while self.running:
            event_list = pygame.event.get()
            for event in event_list:
                if event.type == pygame.QUIT:
                    self.running = False
            self.states[self.gameStateManager.get()].run(event_list)

            pygame.display.update()
            self.clock.tick(FPS)


class Menu:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager
        self.background = pygame.image.load("resources/Cockpit.jpg")
        self.bigFont = pygame.font.Font("resources/AUSTRALIA-TITLE.otf", 95)
        self.smallFont = pygame.font.Font("resources/AUSTRALIA-TITLE.otf", 31)
        self.startButton = pygame.Rect(200, 140, 400, 125)
        self.ridButton = pygame.Rect(200, 290, 185, 60)
        self.ludButton = pygame.Rect(415, 290, 185, 60)
        self.startSurf = self.bigFont.render("START GAME", True, "White")
        self.ridSurf = self.smallFont.render("RIDICULOUS SPEED", True, "White")
        self.ludSurf = self.smallFont.render("LUDICROUS SPEED", True, "White")
        self.textRect = self.startSurf.get_rect(center=self.startButton.center)
        self.ridTextRect = self.ridSurf.get_rect(center=self.ridButton.center)
        self.ludTextRect = self.ludSurf.get_rect(center=self.ludButton.center)

    def run(self, eventList):
        global speed
        self.display.blit(self.background, (-50, 0))
        for event in eventList:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.startButton.collidepoint(event.pos):
                    self.gameStateManager.set("start")
                    speed = 1
                if self.ridButton.collidepoint(event.pos):
                    self.gameStateManager.set("start")
                    speed = 1.8
                if self.ludButton.collidepoint(event.pos):
                    self.gameStateManager.set("start")
                    speed = 2.6

        a, b = pygame.mouse.get_pos()
        if (
            self.startButton.x <= a <= self.startButton.x + 400
            and self.startButton.y <= b <= self.startButton.y + 125
        ):
            pygame.draw.rect(self.display, (180, 180, 180), self.startButton)
        else:
            pygame.draw.rect(self.display, PURPLE, self.startButton)
        if (
            self.ridButton.x <= a <= self.ridButton.x + 185
            and self.ridButton.y <= b <= self.ridButton.y + 60
        ):
            pygame.draw.rect(self.display, (180, 180, 180), self.ridButton)
        else:
            pygame.draw.rect(self.display, PURPLE, self.ridButton)
        if (
            self.ludButton.x <= a <= self.ludButton.x + 185
            and self.ludButton.y <= b <= self.ludButton.y + 60
        ):
            pygame.draw.rect(self.display, (180, 180, 180), self.ludButton)
        else:
            pygame.draw.rect(self.display, PURPLE, self.ludButton)

        self.display.blit(self.startSurf, self.textRect)
        self.display.blit(self.ridSurf, self.ridTextRect)
        self.display.blit(self.ludSurf, self.ludTextRect)


class Options:
    def __init__(self, display, gameStateManager):
        self.score = 0
        self.textX, self.textY = 305, 330
        self.display = display
        self.gameStateManager = gameStateManager
        self.background = pygame.image.load("resources/background.jpeg").convert()
        self.background.set_alpha(210)
        self.font = pygame.font.Font("resources/AUSTRALIA-TITLE.otf", 75)
        self.resetButton = pygame.Rect(300, 100, 200, 95)
        self.menuButton = pygame.Rect(300, 225, 200, 95)
        self.resetSurf = self.font.render("RESET", True, "White")
        self.menuSurf = self.font.render("MENU", True, "White")
        self.resetTextRect = self.resetSurf.get_rect(center=self.resetButton.center)
        self.menuTextRect = self.menuSurf.get_rect(center=self.menuButton.center)

    def run(self, eventList):
        global started
        if started:
            global disSco
            self.score = disSco

            started = False

        def showScore(x, y):
            scoreVis = self.font.render(
                "SCORE: " + str(self.score), True, (255, 255, 255)
            )
            self.display.blit(scoreVis, (x, y))

        self.display.fill("White")
        self.display.blit(self.background, (0, 0))
        for event in eventList:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.resetButton.collidepoint(event.pos):
                    self.gameStateManager.set("start")
                if self.menuButton.collidepoint(event.pos):
                    self.gameStateManager.set("menu")
        a, b = pygame.mouse.get_pos()
        if (
            self.resetButton.x <= a <= self.resetButton.x + 200
            and self.resetButton.y <= b <= self.resetButton.y + 130
        ):
            pygame.draw.rect(self.display, (180, 180, 180), self.resetButton)
        else:
            pygame.draw.rect(self.display, PURPLE, self.resetButton)
        if (
            self.menuButton.x <= a <= self.menuButton.x + 200
            and self.menuButton.y <= b <= self.menuButton.y + 130
        ):
            pygame.draw.rect(self.display, (180, 180, 180), self.menuButton)
        else:
            pygame.draw.rect(self.display, PURPLE, self.menuButton)
        self.display.blit(self.resetSurf, self.resetTextRect)
        self.display.blit(self.menuSurf, self.menuTextRect)
        showScore(self.textX, self.textY)


class Start:
    def __init__(self, display, gameStateManager):
        self.score = 0
        self.textX, self.textY = 17, 5
        self.display = display
        self.gameStateManager = gameStateManager
        self.background = pygame.image.load("resources/background.jpeg")
        mixer.music.load("resources/background.wav")
        mixer.music.play(-1)
        self.playerImg = pygame.image.load("resources/player.png")
        self.playerX, self.playerY = 370, 480
        self.playerXchange = 0
        self.numEnemies = 6
        self.enemyImg = []
        self.enemyX, self.enemyY = [], []
        self.enemyXchange, self.enemyYchange = [], []

        for i in range(self.numEnemies):
            self.enemyImg.append(pygame.image.load("resources/alien.png"))
            self.enemyX.append(random.randint(0, 735))
            self.enemyY.append(random.randint(50, 150))
            self.enemyXchange.append(4)
            self.enemyYchange.append(40)

        self.bulletImg = pygame.image.load("resources/bullet.png")
        self.bulletX, self.bulletY = 0, 480
        self.bulletYchange = 10
        self.bulletState = (
            "ready"  # ready -> can't see bullet. fire -> bullet is moving
        )

    # -1 plays on loop

    def run(self, eventList):

        def showScore(x, y):
            scoreVis = font.render("SCORE: " + str(self.score), True, (255, 255, 255))
            self.display.blit(scoreVis, (x, y))

        def player(x, y):
            self.display.blit(self.playerImg, (x, y))  # blit = draw

        def enemy(x, y, i):
            self.display.blit(self.enemyImg[i], (x, y))

        def fireBullet(x, y):
            self.bulletState = "fire"
            self.display.blit(self.bulletImg, (x + 16, y + 10))

        def isCollision(enemyX, enemyY, bulletX, bulletY):
            distance = math.sqrt(
                math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2)
            )
            return distance < 27

        def gameOver():
            self.bulletState = "ready"
            self.playerX = 370
            self.gameStateManager.set("options")

        self.display.blit(self.background, (0, 0))
        global started
        if started:
            for i in range(self.numEnemies):
                self.enemyXchange[i] = speed * 5
            started = False
            self.score = 0

        for event in eventList:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.gameStateManager.set("options")
                if event.key == pygame.K_LEFT:
                    self.playerXchange = -7 * speed
                if event.key == pygame.K_RIGHT:
                    self.playerXchange = 7 * speed
                if event.key == pygame.K_SPACE:
                    if self.bulletState == "ready":
                        bulletSound = mixer.Sound("resources/laser.wav")
                        bulletSound.play()
                        self.bulletX = self.playerX
                        fireBullet(self.bulletX, self.bulletY)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    self.playerXchange = 0

        self.playerX += self.playerXchange

        if self.playerX <= 0:
            self.playerX = 0
        elif self.playerX >= 736:
            self.playerX = 736

        for i in range(self.numEnemies):
            if self.enemyY[i] > 430:
                for j in range(self.numEnemies):
                    self.enemyY[j] = random.randint(50, 150)
                global disSco
                disSco = self.score
                gameOver()
                break

            self.enemyX[i] += self.enemyXchange[i]
            if self.enemyX[i] <= 0:
                self.enemyXchange[i] = 5 * speed
                self.enemyY[i] += self.enemyYchange[i]
            elif self.enemyX[i] >= 736:
                self.enemyXchange[i] = -5 * speed
                self.enemyY[i] += self.enemyYchange[i]

            collision = isCollision(
                self.enemyX[i], self.enemyY[i], self.bulletX, self.bulletY
            )
            if collision:
                collisionSound = mixer.Sound("resources/explosion.wav")
                collisionSound.play()
                self.bulletY = 480
                self.bulletState = "ready"
                self.score += 1
                self.enemyX[i], self.enemyY[i] = random.randint(0, 735), random.randint(
                    50, 150
                )
            enemy(self.enemyX[i], self.enemyY[i], i)

        if self.bulletY <= 0:
            self.bulletY = 480
            self.bulletState = "ready"

        if self.bulletState == "fire":
            fireBullet(self.bulletX, self.bulletY)
            self.bulletY -= self.bulletYchange * speed

        player(self.playerX, self.playerY)
        showScore(self.textX, self.textY)
        pygame.display.update()


class GameStateManager:
    def __init__(self, currentState):
        self.currentState = currentState

    def get(self):
        return self.currentState

    def set(self, state):
        self.currentState = state
        global started
        started = True


if __name__ == "__main__":
    game = Game()
    game.run()
