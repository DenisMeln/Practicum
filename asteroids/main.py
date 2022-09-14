from player import *
from asteroid import *

pygame.init()
pygame.display.set_caption("Астероиды")

player = Player()
bullets = []
asteroids = []
counter = 0
explosion = pygame.image.load("pics/explosion.png")
explosion = pygame.transform.scale(explosion, (80, 80))
bg = pygame.image.load("pics/spacebg.jpg")

run = True
clock = pygame.time.Clock()
gameover = False
lives = 3
score = 0
crash = False

window = pygame.display.set_mode((800, 800))

class Bullet(object):
    def __init__(self):
        self.point = player.top
        self.x, self.y = self.point
        self.width = 5
        self.height = 5
        self.cosinus = player.cosinus
        self.sinus = player.sinus

    def move(self):
        self.x += self.cosinus * 10
        self.y -= self.sinus * 10

    def draw(self, window):
        pygame.draw.rect(window, (255, 255, 255), [self.x, self.y, self.width, self.height])

    def BulletOutOfBorder(self):
        if self.x < 0 or self.x > 800 or self.y < 0 or self.y > 800:
            return True


def RedrawGameWindow():
    window.blit(bg, (0, 0))
    font = pygame.font.SysFont('arial', 32)
    livesText = font.render("Lives: " + str(lives), True, (92, 255, 38))
    scoreText = font.render("Score: " + str(score), True, (92, 255, 38))
    playAgainText = font.render("Нажмите Space, чтобы начать игру сначала", True, (92, 255, 38))
    player.draw(window)
    for j in asteroids:
        j.draw(window)
    for i in bullets:
        i.draw(window)
    window.blit(livesText, (20, 20))
    window.blit(scoreText, (800 - scoreText.get_width() - 20, 20))
    if crash:
        window.blit(explosion, (crash_x - 40, crash_y - 40))
    if gameover:
        window.blit(playAgainText, (400 - playAgainText.get_width() // 2, 400 - playAgainText.get_height() // 2))
    pygame.display.update()



while run:
    clock.tick(60)
    counter += 1
    if not gameover:
        if counter % 100 == 0:
            asteroids.append(Asteroid())
        player.checkBorders()
        for j in asteroids:
            j.checkBorders()
        for i in bullets:
            i.move()
            if i.BulletOutOfBorder():
                bullets.pop(bullets.index(i))

        for j in asteroids:
            j.x += j.x_new
            j.y += j.y_new

            if (player.x >= j.x and player.x <= j.x + j.width) or (player.x + player.width >= j.x and player.x + player.width <= j.x + j.width):
                if (player.y >= j.y and player.y <= j.y + j.height) or (player.y + player.height >= j.y and player.y + player.height <= j.y + j.height):
                    lives -= 1
                    asteroids.pop(asteroids.index(j))
                    break

            for i in bullets:
                if i.x >= j.x and i.x <= j.x + j.width or i.x + i.width >= j.x and i.x + i.width <= j.x + j.width:
                    if i.y >= j.y and i.y <= j.y + j.height or i.y + i.height >= j.y and i.y + i.height <= j.y + j.height:
                        score += 1
                        asteroids.pop(asteroids.index(j))
                        bullets.pop(bullets.index(i))
                        crash = True
                        crash_x = i.x
                        crash_y = i.y

        if lives == 0:
            gameover = True
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.left()
        if keys[pygame.K_RIGHT]:
            player.right()
        if keys[pygame.K_UP]:
            player.move()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not gameover:
                    bullets.append(Bullet())
                else:
                    gameover = False
                    lives = 3
                    score = 0
                    asteroids.clear()
                    crash = False
            if event.key == pygame.K_ESCAPE:
                run = False
    RedrawGameWindow()
pygame.quit()