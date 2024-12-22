import pyxel
import random

WINDOW_WIDTH = 120
WINDOW_HEIGHT = 160

RECT_HEIGHT = 10
BALL_RADIUS = 2

INITIAL_LIVES = 5
BALL_SPEED_MIN = 1
BALL_SPEED_MAX = 3

class Ball:
    def __init__(self, x, y, dx, dy, color):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.color = color

    def update(self):
        self.x += self.dx
        self.y += self.dy

        # Reflect off the walls
        if self.x <= BALL_RADIUS or self.x >= WINDOW_WIDTH - BALL_RADIUS:
            self.dx *= -1
        if self.y <= BALL_RADIUS:
            self.dy *= -1

    def draw(self):
        pyxel.circ(self.x, self.y, BALL_RADIUS, self.color)

class Game:
    def __init__(self):
        pyxel.init(WINDOW_WIDTH, WINDOW_HEIGHT, title="Switch Match")
        self.show_title_screen = True
        self.reset_game()
        pyxel.run(self.update, self.draw)

    def reset_game(self):
        self.score = 0
        self.round = 1
        self.lives = INITIAL_LIVES
        self.rect_colors = [8, 11]  # [Left color (red), Right color (green)]
        self.is_reversed = False  # Tracks whether the rectangles are reversed
        self.balls = [
            Ball(
                random.randint(BALL_RADIUS, WINDOW_WIDTH - BALL_RADIUS),
                random.randint(BALL_RADIUS, WINDOW_HEIGHT - RECT_HEIGHT - BALL_RADIUS),
                BALL_SPEED_MIN,  # Fixed speed for first ball
                -BALL_SPEED_MIN,  # Fixed upward speed
                random.choice([8, 11])
            ),
            Ball(
                random.randint(BALL_RADIUS, WINDOW_WIDTH - BALL_RADIUS),
                random.randint(BALL_RADIUS, WINDOW_HEIGHT - RECT_HEIGHT - BALL_RADIUS),
                BALL_SPEED_MAX,  # Fixed speed for second ball, different from the first
                -BALL_SPEED_MAX,  # Fixed upward speed
                random.choice([8, 11])
            )
        ]
        self.is_game_over = False

    def update(self):
        if self.show_title_screen:
            if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) or pyxel.btnp(pyxel.KEY_SPACE):
                self.show_title_screen = False
            return

        if self.is_game_over:
            if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) or pyxel.btnp(pyxel.KEY_SPACE):
                self.reset_game()
                self.show_title_screen = True
            return

        # Swap rectangle colors on input
        if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.rect_colors.reverse()

        for ball in self.balls[:]:
            ball.update()

            # Check for collision with the top of the bottom rectangle
            if ball.y >= WINDOW_HEIGHT - RECT_HEIGHT - BALL_RADIUS and ball.y <= WINDOW_HEIGHT - RECT_HEIGHT:
                if ball.x < WINDOW_WIDTH // 2:  # Left side
                    if ball.color == self.rect_colors[0]:
                        self.score += 1  # Increment score when colors match
                    else:
                        self.lives -= 1  # Decrement lives when colors do not match
                else:  # Right side
                    if ball.color == self.rect_colors[1]:
                        self.score += 1  # Increment score when colors match
                    else:
                        self.lives -= 1  # Decrement lives when colors do not match

                if self.lives <= 0:
                    self.is_game_over = True

                # Reverse direction and change speed and color
                ball.dy *= -1
                ball.dx = random.choice([-1, 1]) * random.uniform(BALL_SPEED_MIN, BALL_SPEED_MAX)
                ball.dy = -random.uniform(BALL_SPEED_MIN, BALL_SPEED_MAX)
                ball.color = random.choice([8, 11])

        # Update round based on score
        new_round = self.score // 7 + 1
        if new_round > self.round:
            self.round = new_round
            if len(self.balls) < 5:  # Limit the number of balls to 5
                new_ball = Ball(
                    random.randint(BALL_RADIUS, WINDOW_WIDTH - BALL_RADIUS),
                    WINDOW_HEIGHT - RECT_HEIGHT - 3 * BALL_RADIUS,  # Positioned just above the rectangle
                    random.uniform(-BALL_SPEED_MAX, BALL_SPEED_MAX),  # Random horizontal speed
                    -random.uniform(BALL_SPEED_MIN, BALL_SPEED_MAX),  # Fixed upward initial speed
                    random.choice([8, 11])  # Random color
                )
                self.balls.append(new_ball)

    def draw(self):
        pyxel.cls(0)

        if self.show_title_screen:
            pyxel.text(32, 60, "SWITCH MATCH", 8)
            pyxel.text(35, 100, "TAP TO START", (pyxel.frame_count // 4) % 16)
            return

        if self.is_game_over:
            pyxel.text(40, 70, "GAME OVER", 8)
            pyxel.text(30, 90, "TAP TO RESTART", 7)
            pyxel.text(40, 110, f"02:SCORE: {self.score}", 7)
            return

        # Draw the bottom rectangle
        pyxel.rect(0, WINDOW_HEIGHT - RECT_HEIGHT, WINDOW_WIDTH // 2, RECT_HEIGHT, self.rect_colors[0])
        pyxel.rect(WINDOW_WIDTH // 2, WINDOW_HEIGHT - RECT_HEIGHT, WINDOW_WIDTH // 2, RECT_HEIGHT, self.rect_colors[1])

        # Draw balls
        for ball in self.balls:
            ball.draw()

        # Draw score and lives
        pyxel.text(5, 5, f"SCORE: {self.score}", 7)
        pyxel.text(30, 152, "Tup to Switch", 13)
        if self.round > 5:
            pyxel.text(5, 12, "LEVEL: MAX", 10)
        else:
            pyxel.text(5, 12, f"LEVEL: {self.round}", 7)

        for i in range(INITIAL_LIVES):
            x = WINDOW_WIDTH - 10 * (i + 1)
            y = 5
            if i < self.lives:
                pyxel.circ(x, y, 3, 7)  # Circle for remaining lives
            else:
                pyxel.text(x - 3, y - 3, "x", 8)  # "x" for lost lives

Game()
