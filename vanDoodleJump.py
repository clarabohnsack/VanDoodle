import pygame
import random

pygame.init()
pygame.mixer.init()

# Constants
(width, height) = (500, 700)
size = (width, height)
timer = pygame.time.Clock()
fps = 70

# Sounds and music
jumpSound = pygame.mixer.Sound('jump.wav')
music = pygame.mixer.music.load("bgMusic.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.1)

buttonMusic = pygame.image.load('musicToggle.png')
buttonMusic = pygame.transform.scale(buttonMusic, (50, 50))


musicPaused = False

# Appearance
stemGreen = [127, 166, 68]
starryYellow = [201, 182, 58]
ashGrey = [242, 227, 182]
coralRed = [217, 90, 78]
bookCoverYellow = [191,160,65]
white = [255, 255, 255]
black = [0, 0, 0]
font = pygame.font.Font('PlaypenSans.ttf', 20)

# Score
score = 0
highscore = 0
gameOver = False

# Player
playerX, playerY = 175, 450
playerImage = pygame.image.load('doodle_vangogh.png')
playerImageInJump = pygame.image.load('doodle_vangogh_injump.png')
player = pygame.transform.scale(playerImage, (110, 110))

# GameOver
gameOverWindow = pygame.transform.scale(pygame.image.load('gameOverScreen.png'), (320, 220))
gameOverTextOne = font.render("Game Over", True, black)
gameOverTextTwo = font.render("Press Space to start again", True, black)

#game variables
platforms =[[175,600,100,20], [85, 370, 100, 20], [350, 100, 100, 20], [100,100,100,20], [350, 450, 100, 20], [300, 300, 100, 20]]
jump = False
yChange = 0
xChange = 0
playerSpeed = 5

superJump = 2
jumpLast = 0
# create screen
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Van Doodle')

#TO DO: Change to correct image
bg = pygame.image.load("BG.jpg")
bg = pygame.transform.scale(bg, (size))

bgTwo = pygame.image.load("BG2.jpg")
bgTwo = pygame.transform.scale(bgTwo, (size))

bgThree = pygame.image.load("BG3.jpg")
bgThree = pygame.transform.scale(bgThree, (size))

bgFour = pygame.image.load("BG4.jpg")
bgFour = pygame.transform.scale(bgFour, (size))

bgFive = pygame.image.load("BG5.jpg")
bgFive = pygame.transform.scale(bgFive, (size))



# check collision
def checkCollisions(rectList, j):
  global playerX
  global playerY
  global yChange
  for i in range(len(rectList)):
    if rectList[i].colliderect([playerX + 20, playerY + 60, 65, 50]) and jump == False and yChange > 0:
      j = True
      pygame.mixer.Sound.play(jumpSound)
  return j

''' if you want two types, make two different lists, one stationary and the other moving, and if a platform is in the moving category
change its x coordinate overtime with a timer and leave the stationary ones alone'''

# update player y position per loop
def update_player(yPos):
  global playerY
  global playerX
  global jump
  global yChange
  jump_height = 9
  gravity = .3
  if jump:
    yChange = -jump_height
    jump = False
  yPos += yChange
  yChange += gravity
  return yPos

# platform movement
def update_platforms(platList, yP, yCha):
  global score
  if yP < 650 and yCha < 0:
    for i in range(len(platList)):
      platList[i][1] -= yCha * 2
  else:
    pass
  for j in range(len(platList)):
    if platList[j][1] > 700:
      platList[j] = [random.randint(5, 450), random.randint(-50, -10), 100, 20]
      score += 10
  return platList


# Game Loop - Keeping the window running
running = True

while running:

  # Show content
  screen.blit(bg, (0, 0))

  #Changing background image
  if score > 500 and score <= 1000:
    screen.blit(bgTwo, (0, 0))
  
  if score > 1000 and score <= 1500:
    screen.blit(bgThree, (0, 0))

  if score > 1500 and score <= 2000:
    screen.blit(bgFour, (0, 0))

  if score > 2000:
    screen.blit(bgFive, (0, 0))

  recs = []

  for i in range(len(platforms)):

    if score <= 500:
      rec = pygame.draw.rect(screen, stemGreen, platforms[i], 0, 15)

    if score > 500 and score <= 1000:
      rec = pygame.draw.rect(screen, starryYellow, platforms[i], 0, 15)

    if score > 1000 and score <= 1500:
      rec = pygame.draw.rect(screen, ashGrey, platforms[i], 0, 15)

    if score > 1500 and score <= 2000:
      rec = pygame.draw.rect(screen, coralRed, platforms[i], 0, 15)

    if score > 2000:
      rec = pygame.draw.rect(screen, bookCoverYellow, platforms[i], 0, 15)

    recs.append(rec)

  # Draw player
  screen.blit(player, (playerX, playerY))

  # Draw text
  scoreText = font.render('Score: ' + str(score), True, white)
  screen.blit(scoreText, (380, 40))

  highScoreText = font.render('Highscore: ' + str(highscore), True, white)
  screen.blit(highScoreText, (345, 10))

  superJumpText = font.render('Super Jumps: ' + str(superJump), True, white)
  screen.blit(superJumpText, (305, 70))

  # Draw MusicToggle
  buttonMusicBox = pygame.draw.rect(screen, stemGreen, (423, 623, 45, 45))
  screen.blit(buttonMusic, (420, 620))

  # Check for input
  for event in pygame.event.get():

    # Quit through input
    if event.type == pygame.QUIT:

      running = False

    #Game Over logic
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_SPACE and gameOver:
        gameOver = False
        score = 0
        playerX = 175
        playerY = 450
        background = bg
        platforms =[[175,600,100,20], [85, 370, 100, 20], [350, 100, 100, 20], [100,100,100,20], [350, 450, 100, 20], [300, 300, 100, 20]]
        superJump = 3
        jumpLast = 0

      if event.key == pygame.K_SPACE and not gameOver and superJump > 0:
        superJump -= 1
        yChange = -15

      if event.key == pygame.K_a or event.key == pygame.K_LEFT:
        xChange = -playerSpeed

      if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
        xChange = playerSpeed

    if event.type == pygame.KEYUP:
      if event.key == pygame.K_a or event.key == pygame.K_LEFT:
        xChange = 0

      if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
        xChange = 0

    if event.type == pygame.MOUSEBUTTONDOWN:
      if buttonMusicBox.collidepoint(event.pos):
        # Toggle the boolean variable.
        musicPaused = not musicPaused
        if musicPaused:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()

  jump = checkCollisions(recs, jump)

  if playerY < 650:
    playerY = update_player(playerY)
  else:
    gameOver = True
    yChange = 0
    xChange = 0
    superJump = 2
    screen.blit(gameOverWindow, (100, 215))
    screen.blit(gameOverTextOne, (190, 335))
    screen.blit(gameOverTextTwo, (125, 370))

  if playerX < -20:
    playerX = 480
  elif playerX > 480:
    playerX = -20

  playerX += xChange
  platforms = update_platforms(platforms, playerY, yChange)

  if yChange > 0:
    player = pygame.transform.scale(playerImage, (110, 110))
    if xChange < 0:
      player = pygame.transform.flip(pygame.transform.scale(playerImage, (110, 110)), 1, 0)
  else:
    player = pygame.transform.scale(playerImageInJump, (110, 110))
    if xChange < 0:
      player = pygame.transform.flip(pygame.transform.scale(playerImageInJump, (110, 110)), 1, 0)

  if score > highscore:
    highscore = score

  if score - jumpLast > 500:
    jumpLast = score
    superJump += 1

  pygame.display.flip()
  timer.tick(fps)
      