from tkinter import *
import time
import random

# Window resolution: 1280x720
background_colour = '#72E8E8'
window_width = 1280
window_height = 720
box_size = 40
start_button = False
# Description of the ball
ball_speed_x = 0.2
ball_speed_y = 0.2
ball_colour = '#B00003'
# Boolean values for the game
paused_bool = False
paused = False
boss = False
chart_bool = False
ranking_bool = False
leaderboard_bool = False
over_bool = False
exit_bool = False
restart_bool = False
save_bool = False
setting_on = False
# cheat code count
cheat_count = 3
# Default player name
player = 'UNKNOWN'
# Brick on canvas
bricks1 = []
bricks2 = []
bricks3 = []
bricks4 = []
# Player ranking
rankings = []


def detectBorderPaddle():
    """getting the boundarieds for the paddle on canvas"""
    paddle_coordinates = canvas.bbox(paddle_on_canvas)
    return paddle_coordinates


def detectBorderBall():
    """getting the boundarieds for the moving ball object"""
    global ball
    ball_coordinates = canvas.bbox(ball)
    return ball_coordinates


def paddleRight(event):
    """Move the paddle to the right if right arrow key in pressed"""
    s = detectBorderPaddle()
    # Checking right windown edge for collision
    if s[2] > window_width:
        canvas.move(paddle_on_canvas, -5, 0)
    else:
        canvas.move(paddle_on_canvas, 50, 0)


def paddleLeft(event):
    """Move the paddle to the left if left arrow key in pressed"""
    s = detectBorderPaddle()
    # Checking left windown edge for collision
    if s[0] < 0:
        canvas.move(paddle_on_canvas, 5, 0)
    else:
        canvas.move(paddle_on_canvas, -50, 0)


def createBall():
    """Creating the ball object and placing it on canvas with collision detection and change of speed"""
    global ball_speed_x, ball_speed_y, ball, paused_bool, pause_img_on_canvas, chart_img, chart_img_on_canvas, chart_bool, bricks1, bricks2, bricks3, bricks4
    # Remeving unnecessary object from canvas
    settings_button.destroy()
    remove_start_button()
    play.destroy()
    canvas.delete(title_img_on_canvas)
    leaderboard_button.destroy()
    # Delay before the game starts
    time.sleep(1)
    ball = canvas.create_oval(100, 200, 100+box_size,
                              200+box_size, fill=ball_colour)
    # Initial ball speed
    # ball_speed_x = 0.2
    # ball_speed_y = 0.2
    # checking collison for game over
    check_collision_bottom()
    # Adding targets on canvas
    addBricks()
    while True:
        # Collsion detections
        brickCollision()
        paddleCollision()
        check_collision_bottom()
        paddleCollision()
        # Running game loop
        if not paused and not boss:
            moveBall()
            remove_Img()
            window.update()
            if endGame():
                canvas.delete(ball)
                break
            elif score >= 402:
                gameWon()
        # Pause game
        elif paused:
            pause_img = PhotoImage(file='pause.png')
            pause_img_on_canvas = canvas.create_image(
                531, 252, image=pause_img, anchor=NW)
            paused_bool = True
            window.update()
        # Boss key
        elif boss:
            chart_img = PhotoImage(file='boss.png')
            chart_img_on_canvas = canvas.create_image(
                0, 0, image=chart_img, anchor=NW)
            chart_bool = True
            window.update()
        else:
            window.update()


def remove_start_button():
    """Removing start button from canvas once pressed"""
    global start_button, play_game
    if start_button:
        play_game.destroy()


def remove_Img():
    """Removing images from canvas once keys are pressed"""
    global chart_img_on_canvas, pause_img_on_canvas
    if chart_bool:
        canvas.delete(chart_img_on_canvas)
    if paused_bool:
        canvas.delete(pause_img_on_canvas)


def bossHere(event):
    """Changing states of the BOSS event"""
    global boss
    if boss == True:
        boss = False
    else:
        boss = True


def remove_pauseImg():
    """Removing the pause image from canvas once the key in pressed"""
    global pause_img_on_canvas
    if paused_image:
        canvas.delete(pause_img_on_canvas)


def gameWon():
    """Congratulating the player if all the brick have been broken"""
    win = canvas.create_text(window_width/2, window_height/3, font=(
        'consolas', 70), text='YOU WON!', fill='black')
    win = canvas.create_text(window_width/2, window_height/2, font=(
        'consolas', 70), text='WELL DONE', fill='black')
    with open('leaderboard.txt', 'a') as f:
        s = str(score)
        f.write(s + ',' + player + '\n')
    time.sleep(2)
    window.destroy()


def pauseGame(event):
    """Changing states of the Pause event"""
    global paused
    if paused == True:
        paused = False
    else:
        paused = True


def endGame():
    """Detecting the button edge of the window to end the game"""
    ball_co = detectBorderBall()
    if ball_co[3] == window_height:
        return True


def addBricks():
    """Adding four layers of brick on canvas using for loop and filling them different colours"""
    global bricks
    # Initial posision of the brick
    brick_co_x = 0
    brick_co_y = 1
    brick1_x = 50
    brick1_y = 40
    brick2_x = 80
    brick2_y = 40
    brick3_x = 110
    brick3_y = 40
    brick4_x = 160
    brick4_y = 40
    # Bricks layer one
    for i in range(26):
        brick = canvas.create_rectangle(
            brick_co_x, brick_co_y, brick_co_x+brick1_x, brick_co_y+brick1_y, fill='pink')
        bricks1.append(brick)
        brick_co_x += brick1_x
    # Bricks layer two
    brick_co_x = 0
    brick_co_y = brick1_y+3
    for i in range(16):
        brick = canvas.create_rectangle(
            brick_co_x, brick_co_y, brick_co_x+brick2_x, brick_co_y+brick2_y, fill='violet')
        bricks2.append(brick)
        brick_co_x += brick2_x
    # Bricks layer three
    brick_co_x = 0
    brick_co_y = brick1_y+brick2_y+5
    for i in range(12):
        brick = canvas.create_rectangle(
            brick_co_x, brick_co_y, brick_co_x+brick3_x, brick_co_y+brick3_y, fill='yellow')
        bricks3.append(brick)
        brick_co_x += brick3_x
    # Bricks layer four
    brick_co_x = 0
    brick_co_y = brick1_y+brick2_y+brick3_y+5
    for i in range(8):
        brick = canvas.create_rectangle(
            brick_co_x, brick_co_y, brick_co_x+brick4_x, brick_co_y+brick4_y, fill='white')
        bricks4.append(brick)
        brick_co_x += brick4_x


def brickCollision():
    """Detecting ball-brick collison"""
    global bricks1, bricks2, bricks3, score
    # Fetching ball boundaries
    ball_co = detectBorderBall()
    # Getting ball boundaries of each brick in layer one
    for b in bricks1:
        brick_co = canvas.bbox(b)
        if brick_co[0] < ball_co[2] and brick_co[2] > ball_co[0] and brick_co[1] < ball_co[3] and brick_co[3] > ball_co[1]:
            score += 10
            score_label.config(text='Score:{}'.format(score))
            canvas.delete(b)
            bricks1.remove(b)
            return True
    # Getting ball boundaries of each brick in layer two
    for b in bricks2:
        brick_co = canvas.bbox(b)
        if brick_co[0] < ball_co[2] and brick_co[2] > ball_co[0] and brick_co[1] < ball_co[3] and brick_co[3] > ball_co[1]:
            score += 5
            score_label.config(text='Score:{}'.format(score))
            canvas.delete(b)
            bricks2.remove(b)
            return True
    # Getting ball boundaries of each brick in layer three
    for b in bricks3:
        brick_co = canvas.bbox(b)
        if brick_co[0] < ball_co[2] and brick_co[2] > ball_co[0] and brick_co[1] < ball_co[3] and brick_co[3] > ball_co[1]:
            score += 2
            score_label.config(text='Score:{}'.format(score))
            canvas.delete(b)
            bricks3.remove(b)
            return True
    # Getting ball boundaries of each brick in layer four
    for b in bricks4:
        brick_co = canvas.bbox(b)
        if brick_co[0] < ball_co[2] and brick_co[2] > ball_co[0] and brick_co[1] < ball_co[3] and brick_co[3] > ball_co[1]:
            score += 1
            score_label.config(text='Score:{}'.format(score))
            canvas.delete(b)
            bricks4.remove(b)
            return True


def moveBall():
    """Moving the ball on canvas in random direction, bouncing off the window edges, paddle and colliding with bricks"""
    global ball_speed_x, ball_speed_y
    # Fetching ball boundaries
    ball_co = detectBorderBall()
    # Ball collision on right and left hand side on the window
    if ball_co[2] >= (canvas.winfo_width()) or ball_co[0] < 0:
        ball_speed_x = -ball_speed_x
    # Ball collision on top edge of the window
    if ball_co[1] < 0:
        ball_speed_y = -ball_speed_y
    # Detecting brick collision
    brick_collision = brickCollision()
    if brick_collision:
        ball_speed_y = -ball_speed_y
    # Moving the ball according to the speeds above
    canvas.move(ball, ball_speed_x, ball_speed_y)
    # Detecting button edge collision
    check_collision_bottom()
    # Detecting paddle collision
    paddleCollision()


def moveBall_faster():
    """Speeding up the ball once speed up is applied"""
    global speed_ups, ball_speed_x, ball_speed_y
    # Speed ups count
    if speed_ups > 0:
        ball_speed_x += ball_speed_x
        speed_ups -= 1
        speed_label.config(text='Speed ups left: {}'.format(speed_ups))
    # Fetching ball boundaries
    ball_co = detectBorderBall()
    # Ball collision on right and left hand side on the window
    if ball_co[2] >= (canvas.winfo_width()) or ball_co[0] < 0:
        ball_speed_x = -ball_speed_x
    # Ball collision on top edge of the window
    if ball_co[1] < 0:
        ball_speed_y = -ball_speed_y
    # Detecting brick collision
    brick_collision = brickCollision()
    if brick_collision:
        ball_speed_y = -ball_speed_y
    # Moving the ball according to the speeds above
    canvas.move(ball, ball_speed_x, ball_speed_y)
    # Detecting button edge collision
    check_collision_bottom()
    # Detecting paddle collision
    paddleCollision()


def speedUp(event):
    """Applying the speed up on the ball"""
    moveBall_faster()


def paddleCollision():
    """Detecting the ball collision with paddle"""
    global ball_speed_x, ball_speed_y
    # Fetcing the ball boundaries
    ball_co = detectBorderBall()
    # Fetcing the paddle boundaries
    paddle_co = detectBorderPaddle()
    # Checking for collision
    if (paddle_co[1] < ball_co[1] < paddle_co[3]) and (paddle_co[0] < ball_co[2] < paddle_co[2] or paddle_co[0] < ball_co[0] < paddle_co[2]):
        ball_speed_y = -ball_speed_y


def check_collision_bottom():
    """Checking collision of ball with the button edge of the window"""
    # Fetcing ball boundaries
    ball_co = detectBorderBall()
    # Checking for collision
    if ball_co[3] == window_height:
        game_over()


def get_text():
    """Getting input nama from the player"""
    global player
    player = player_name.get()


def game_over():
    """Placing message on the canvas once ball collide the button, giving player option to save the score or exit the game """
    global over, _exit, restart, save
    # Game over message after ball hits buttom edge
    over = canvas.create_text(window_width/2, window_height/2, font=(
        'consolas', 70), text='GAME OVER', fill='black')
    # Exit game by destroying canvas
    _exit = Button(window, text="EXIT", bg='#00AAFF',
                   fg='white', height=5, width=10, command=close)
    _exit.place(x=480, y=550)
    restart = Button(window, text="AGAIN", bg='#00AAFF',
                     fg='white', height=5, width=10, command=play_again)
    restart.place(x=600, y=550)
    # Save score and name in text file
    save = Button(window, text="SAVE SCORE", bg='#00AAFF',
                  fg='white', height=5, width=10, command=saveScore)
    save.place(x=720, y=550)


def play_again():
    """Reseting all setting to start the game again"""
    global score, save, restart, _exit, speed_ups, cheat_count
    # Reseting the score
    score = 0
    score_label.config(text='Score:{}'.format(score))
    # Reseting the speed ups
    speed_ups = 2
    speed_label.config(text='Speed ups left: {}'.format(speed_ups))
    # Reseting the cheat count
    cheat_count = 3
    # Destroying objects
    save.destroy()
    restart.destroy()
    _exit.destroy()
    canvas.delete(over)
    createBall()


def remove_items():
    """Removing items from canvas if present"""
    global leaderboard_title, rankings, leaderboard_bool, ranking_bool, setting_on, bg_change, ball_change, bg_colour_1
    global bg_colour_2, ball_colour_1, ball_colour_2, speed_change, speed_1, speed_2
    # Check for ranking on the canvas
    if ranking_bool:
        for r in rankings:
            canvas.delete(r)
    # Check for leaderbool title on the canvas
    if leaderboard_bool:
        canvas.delete(leaderboard_title)
    # Destroying objects from settings page
    if setting_on:
        canvas.delete(bg_change)
        canvas.delete(ball_change)
        bg_colour_1.destroy()
        bg_colour_2.destroy()
        ball_colour_1.destroy()
        ball_colour_2.destroy()
        canvas.delete(speed_change)
        speed_1.destroy()
        speed_2.destroy()


def saveScore():
    """Saving the players score and name inside a text file"""
    global score, player
    # Getting inside the text file
    with open('leaderboard.txt', 'a') as f:
        if score > 0:
            if score < 100:
                # Adding leading zeros to compare score
                score = str(score)
                s = score.zfill(3)
                f.write(s + ',' + player + '\n')
            else:
                f.write(str(score)+','+player + '\n')
        else:
            pass


def cheat_code(event):
    """Implementing the cheat code as scores adding to the total"""
    global cheat_count, score
    if cheat_count > 0:
        score += 10
        # Changing configuration of the score when cheat code in applied
        score_label.config(text='Score:{}'.format(score))
        cheat_count -= 1


def close():
    """Closing the game when exit is pressed"""
    window.destroy()


def start_game():
    """Starting the game by deleting the unrequired image and texts"""
    # Removing user input text box
    player_name.destroy()
    get_player_name.destroy()
    # Removing item from learderboard page
    remove_items()
    # Switch to the game page
    createBall()


def leaderboard():
    """Implementing the leaderboard using data from text file"""
    global start_button, play_game, leaderboard_title, rankings, leaderboard_bool, ranking_bool
    # Making new window for leaderboard
    settings_button.destroy()
    player_name.destroy()
    get_player_name.destroy()
    leaderboard_button.destroy()
    play.destroy()
    canvas.delete(title_img_on_canvas)
    # Title for the page
    leaderboard_title = canvas.create_text(window_width/2, 50, font=(
        'consolas', 40), text='Leaderboard', fill='black')
    # Placing scores
    with open('leaderboard.txt') as file:
        file_string = file.read()
        scores = list(file_string.split())
        empty = 20
        place = 150
        count = 1
        for s in sorted(scores, reverse=True):
            if count < 11:
                ranking = canvas.create_text(window_width/2, place+empty, font=(
                    'consolas', 20), text=str(count) + '.  ' + s, fill='black')
                rankings.append(ranking)
                place += 40
                count += 1
    # New play button
    play_game = Button(window, text="Start Game", bg='#5C9C9C', font=('Arial', 10),
                       fg='white', height=5, width=20, command=start_game)
    play_game.place(x=50, y=400)
    start_button = True
    leaderboard_bool = True
    ranking_bool = True


def change_bg1():
    """Changing the background colour of the canvas"""
    background_colour = '#509FC7'
    canvas.config(bg=background_colour)


def change_bg2():
    """Changing the background colour of the canvas"""
    background_colour = '#36BF7D'
    canvas.config(bg=background_colour)


def change_ball1():
    """Change the colour of the ball"""
    global ball, ball_colour
    ball_colour = '#730047'


def change_ball2():
    """Change the colour of the ball"""
    global ball, ball_colour
    ball_colour = '#007302'


def change_speed1():
    """Halve the speed of the ball"""
    global ball_speed_x, ball_speed_y
    # Redefining the speed
    ball_speed_x = 0.1
    ball_speed_y = 0.1


def change_speed2():
    """Double the speed of the ball"""
    global ball_speed_x, ball_speed_y
    # Redefining the speed
    ball_speed_x = 0.3
    ball_speed_y = 0.3


def settings():
    """Allow the user to change the settings of the game, such as, background colour, ball colour and speed"""
    global start_button, play_game, leaderboard_title, rankings, leaderboard_bool, bg_change
    global ball_change, setting_on, bg_colour_1, bg_colour_2, ball_colour_1, ball_colour_2, speed_change, speed_1, speed_2
    # Making new window for leaderboard
    settings_button.destroy()
    player_name.destroy()
    get_player_name.destroy()
    leaderboard_button.destroy()
    play.destroy()
    canvas.delete(title_img_on_canvas)
    # Page Title
    leaderboard_title = canvas.create_text(window_width/2, 50, font=(
        'consolas', 40), text='Settings', fill='black')
    # Change settings
    # Change background colour
    bg_change = canvas.create_text(window_width/2, 150, font=(
        'Ariel', 17), text='Change Background Colour', fill='black')
    bg_colour_1 = Button(window, bg='#509FC7', height=2,
                         width=10, command=change_bg1)
    bg_colour_1.place(x=550, y=250)

    bg_colour_2 = Button(window, bg='#36BF7D', height=2,
                         width=10, command=change_bg2)
    bg_colour_2.place(x=650, y=250)
    # Change ball colour
    ball_change = canvas.create_text(window_width/2, 300, font=(
        'Ariel', 17), text='Change Ball Colour', fill='black')
    ball_colour_1 = Button(window, bg='#730047', height=2,
                           width=10, command=change_ball1)
    ball_colour_1.place(x=550, y=400)

    ball_colour_2 = Button(window, bg='#007302', height=2,
                           width=10, command=change_ball2)
    ball_colour_2.place(x=650, y=400)
    # Change ball speed
    speed_change = canvas.create_text(window_width/2, 450, font=(
        'Ariel', 17), text='Change Ball Speed', fill='black')
    speed_1 = Button(window, bg='#506FC7', height=2, fg='white', text='Slower',
                     width=10, command=change_speed1)
    speed_1.place(x=550, y=550)

    speed_2 = Button(window, bg='#506FC7', height=2, fg='white', text='Faster',
                     width=10, command=change_speed2)
    speed_2.place(x=650, y=550)
    # New play button
    play_game = Button(window, text="Start Game", bg='#5C9C9C', font=('Arial', 10),
                       fg='white', height=5, width=20, command=start_game)
    play_game.place(x=50, y=400)
    start_button = True
    leaderboard_bool = True
    setting_on = True


window = Tk()
window.title("B  R  E  A  K  O  U  T  ")
window.resizable(False, False)

# Score in the game
score = 0
score_label = Label(window, text='Score:{}'.format(score),
                    font=('Arial', 20))
score_label.pack()

# Spead ups
speed_ups = 2
speed_label = Label(window, text='Speed ups left: {}'.format(speed_ups),
                    font=('Arial', 20))
speed_label.pack()

# Canvas
canvas = Canvas(window, bg=background_colour,
                height=window_height, width=window_width)
canvas.pack()

# Moving Paddle on canvas
# Image taken from authorised source---------https://www.flaticon.com/free-icon/delete_271207?term=dash&page=1&position=1&page=1&position=1&related_id=271207&origin=search-------------
paddle = PhotoImage(file='paddle.png')
paddle_on_canvas = canvas.create_image(580, 600, image=paddle, anchor=NW)

# Move paddle
window.bind('<Right>', paddleRight)
window.bind('<Left>', paddleLeft)

# Pause Game
window.bind('<p>', pauseGame)

# Speed Up the ball
window.bind('<8>', speedUp)

# Cheat Code
window.bind('<+>', cheat_code)

# Boss key
window.bind('<b>', bossHere)

# start screen
# Game name
title_img = PhotoImage(file='breakout.png')
title_img_on_canvas = canvas.create_image(115, 0, image=title_img, anchor=NW)
# Getting input from user
player_name = Entry(window, width=28)
player_name.place(x=550, y=350)
get_player_name = Button(window, text="GET NAME", bg='#5C9C9C',
                         fg='white', height=2, width=10, command=get_text)
get_player_name.place(x=600, y=380)
# Play button
play = Button(window, text="Start", bg='#5C9C9C', font=('Arial', 10),
              fg='white', height=5, width=20, command=start_game)
play.place(x=550, y=450)
# Leaderboard button
leaderboard_button = Button(window, text="Leader Board", bg='#5C9C9C', font=('Arial', 10),
                            fg='white', height=5, width=20, command=leaderboard)
leaderboard_button.place(x=550, y=550)
# Customise Experience
settings_button = Button(window, text="Settings", bg='#5C9C9C', font=('Arial', 10),
                         fg='white', height=5, width=20, command=settings)
settings_button.place(x=550, y=650)
window.mainloop()
