from paddle import *
from ball import *
from collisionhandler import *
from wall import *
from highscore import *

import inputbox

import random
import pygame

def main():
    pygame.init()
    
    try:
        w = 640
        h = 480

        screen = pygame.display.set_mode((w, h))
        font = pygame.font.SysFont('Arial Black', 17)
        pygame.mouse.set_visible(False)
        clock = pygame.time.Clock()
        ch = CollisionHandler()

        TIMEEVENT = USEREVENT + 1
        pygame.time.set_timer(TIMEEVENT, 15)

        # Load our balls and add them to collision handler
        balls = Ball.createRandomBallsAsList(5, screen)
        for ball in balls:
            ch.addBall(ball)

        # Insert walls and add them to collision handler
        walls = [
            Wall( screen, (0,30), (10, screen.get_height()) ), # Left wall
            Wall( screen, (screen.get_width()-10,30), (10, screen.get_height()) ), # Right wall
            Wall( screen, (0,30), (screen.get_width(), 10) ) # Top wall
        ]
        for wall in walls:
            ch.addObject(wall)
        
        # Create paddle and add it to collision handler
        paddle = Paddle(screen)
        ch.addObject(paddle)
        
        # Game variables
        run = True
        pause = False
        gameover = False
        viewHighScore = False;
        lifes = len(balls)
        time = 0
        name = ""
        score = 0

        # Initialize highscore
        highscore = Highscore(screen)
		
        # Load scoreboard
        scoreBoard = font.render("Life: " + str(lifes) + " Score: ", True, (255, 0, 0))
        
        while not gameover:
        
            # Check for quits
            for event in pygame.event.get():
            
                if event.type == pygame.QUIT:
                    gameover = True
                    cursor.close()
                    connection.commit()
                    connection.close()
                    
                if event.type == TIMEEVENT and not pause:
                    time += 1
                
                # Key presses
                if event.type == KEYUP:
                    if event.key == K_i:
                        pause = not pause
                        
                        font2 = pygame.font.SysFont('Arial Black', 40)
                        #pygame.draw.rect(surface, (255,255,255), (surface.get_width()/2-129, 79,302, 462), 0)
                        trans = pygame.Surface((300, 350))
                        trans.fill((0,0,0))
                        pygame.Surface.convert_alpha(trans)
                        trans.set_alpha(128)

                        screen.blit(trans, (screen.get_width()/2-130,80))                                
                        
                        gameOverImg = font2.render("Game Over", True, (255, 0, 0))
                        highScoreImg = font.render("Name      Score", True, (255, 0, 0))
                        pressSpaceImg = font.render("Press space to try again", True, (255, 0, 0))
                        
                        screen.blit(gameOverImg, (screen.get_width()/2-120, 70))
                        screen.blit(highScoreImg, (screen.get_width()/2-100, 140))
                        screen.blit(pressSpaceImg, (screen.get_width()-250, screen.get_height()-30))
                        print "Instructions placed as long as key i is pressed"
                        
                    if event.key == K_SPACE and not(run):
                        run = True
                        gameover = False
                        viewHighScore = False;
                        lifes = len(balls)
                        time = 0
                        name = ""
                        score = 0
                        pygame.time.set_timer(TIMEEVENT, 15)
                        
                        # Load our balls and add them to collision handler
                        balls = Ball.createRandomBallsAsList(5, screen)
                        
                        for ball in balls:
                            ch.addBall(ball)
            
            if not pause:
                # Update positions for balls
                for ball in balls: 
                    if ball.update(): # Returns true if ball goes below paddle-level
                        lifes -= 1
            
            # Update positions for paddle
            paddle.update()

            # Update collision handler
            if ch.update():
                score += 1
                
            # Draw background
            screen.fill((0, 0, 0))
            
            # Draw walls
            for wall in walls:
                wall.draw()
                
            # Draw paddle
            paddle.draw()    
            
            # Draw balls
            for ball in balls:
                ball.draw()

            #Draw scoreboard
            if run:
                scoreBoard = font.render("Life: " + str(lifes) + " Score: " + str(score), True, (255, 0, 0))

            pygame.draw.rect(screen, (0, 255, 255), (0, 0, time, 30))
            screen.blit(scoreBoard, (10, 5)) 

            # Level up!
            if time >= screen.get_width():
                time = 0
                action = random.randint(0, 2) # Randomize action
                
                if action == 0:
                    # Add new ball
                    balls.append(ch.addBall(Ball(screen, (random.randint(50, 550), random.randint(50, 200)), (randsign()*random.uniform(1.0,3.0),random.uniform(1.0,3.0)) )))
                elif action == 1 or action == 2:
                    # Add new wall, vertical or horizontal
                    if random.randint(0, 1):
                        walls.append(ch.addObject(Wall(screen, (random.randint(50, 550), random.randint(50, 200)), (200,10) )))
                    else:
                        walls.append(ch.addObject(Wall(screen, (random.randint(50, 550), random.randint(50, 200)), (10,200) )))
                    # Add bonus item here
                    
            # If lifes = 0    
            if lifes <= 0 and run:
                player = []
                pygame.time.set_timer(TIMEEVENT, 0)
                finalScore = score
                viewHighScore = True
                run = False
                name = inputbox.ask(screen, "Your name ")
                scoreBoard = font.render("Life: 0 Score: " + str(finalScore), True, (255, 0, 0))
                player = highscore.update(name, finalScore, font)
                
            if viewHighScore:
                highscore.draw(player, font)
                
            # Update screen
            pygame.display.flip()

            clock.tick(60)
            
    finally:
        pygame.quit()
        
        # Try close database connection
        try:
            highscore.db.close()
        except NameError:
            print "Ooops, no connection"

if __name__ == "__main__":
    main()
