from tkinter import *
import random
import tkinter as tk
from tkinter import messagebox
import pygame

# Initialize Pygame
pygame.init()

# Game settings
WINDOW_WIDTH = 700  # Adjust as needed
WINDOW_HEIGHT = 800  # Adjust as needed
GAME_WIDTH = 700
GAME_HEIGHT = 700
SPEED = 100
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "#1E90FF"
HEAD_COLOR = "#1FFFF0"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"
# Global declarations
again_button = None
label2 = None
window = None
score = 0
direction = "down"
canvas = None
label = None
song = 0
# Represents the Snake
class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])
        
   
        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake") # type: ignore
            self.squares.append(square)


# Represents the Food
class Food:

    def __init__(self):
        # Calculate the maximum valid x and y positions within the game grid
        max_x = (GAME_WIDTH // SPACE_SIZE) - 1
        max_y = (GAME_HEIGHT // SPACE_SIZE) - 1

        # Generate random coordinates within the valid range
        x = random.randint(0, max_x) * SPACE_SIZE
        y = random.randint(0, max_y) * SPACE_SIZE

        self.coordinates = [x, y]

        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food") # type: ignore


# Moves the snake and updates the game state
def next_turn(snake, food):
    x, y = snake.coordinates[0]

     # Adjusts the snake's position according to the chosen direction
    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    # Wrap the snake's head around the screen boundaries
    if x < 0:
        x = GAME_WIDTH - SPACE_SIZE
    elif x >= GAME_WIDTH:
        x = 0
    elif y < 0:
        y = GAME_HEIGHT - SPACE_SIZE
    elif y >= GAME_HEIGHT:
        y = 0

    snake.coordinates.insert(0, (x, y))
    
    # Make the head
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill= HEAD_COLOR) # type: ignore
    snake.squares.insert(0, square)
    # Change the color of the rest parts of the snake 
    for i in range(1,len(snake.squares)):
         canvas.itemconfig(snake.squares[i], fill=SNAKE_COLOR) # type: ignore

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        label.config(text="Score: {}".format(score)) # type: ignore

        canvas.delete("food") # type: ignore

        food = Food()
        play_music()
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1]) # type: ignore
        del snake.squares[-1]
        

    if check_collisions(snake):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food) # type: ignore

def check_collisions(snake):
    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            print("GAME OVER")
            return True

    return False

def change_direction(new_direction):
    global direction

    if new_direction == "left":
        if direction != "right":
            direction = new_direction
    elif new_direction == "right":
        if direction != "left":
            direction = new_direction
    elif new_direction == "up":
        if direction != "down":
            direction = new_direction
    elif new_direction == "down":
        if direction != "up":
            direction = new_direction

def game_over():
    global again_button, score  # Declare again_button as a global variable
    pygame.mixer.music.stop()

    canvas.delete(ALL) # type: ignore
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2, # type: ignore
                       font=("consolas", 70), text="GAME OVER", fill="crimson", tag="gameover")
    again_button = Button(window, text="PLAY AGAIN", command=again, bg="darkorchid2", font=("consolas", 15))
    # Position the button at the bottom of the window
    again_button.pack(side="bottom")
    # Update the highest score and display it
    highest_score = update_highest_score(score)
    display_highest_score()

def again():
    global score, direction
    canvas.delete(ALL) # type: ignore
    score = 0
    direction = "down"
    label.config(text="Score: {}".format(score)) # type: ignore
    snake = Snake()
    food = Food()
    play_music()
    next_turn(snake, food)
    # Destroy the "PLAY AGAIN" button
    again_button.destroy()

def background():
    global BACKGROUND_COLOR
    if BACKGROUND_COLOR == "#000000":
        BACKGROUND_COLOR = "#ffffff"
        canvas.config(bg='white') # type: ignore
    else:
        BACKGROUND_COLOR = "#000000"
        canvas.config(bg='black') # type: ignore

def play():
    global window, canvas, label, score, direction, highest_score_label  # Use the global window variable

    # Call the function to play the music 
    play_music()


    # Create the main window if it doesn't exist
    if window is None:
        window = tk.Toplevel(root)
        window.title("Snake Game")
        window.configure(bg='springgreen')

        # Set the window size
        window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

        canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
        canvas.pack()
        canvas.place(x=(WINDOW_WIDTH - GAME_WIDTH) // 2, y=(WINDOW_HEIGHT - GAME_HEIGHT) // 2)

        label = Label(window, text="Score: {}".format(score), font=('consolas', 28), bg="springgreen")
        label.pack()

        # Bind the arrow keys to the change_direction function
        window.bind('<Left>', lambda event: change_direction('left'))
        window.bind('<Right>', lambda event: change_direction('right'))
        window.bind('<Up>', lambda event: change_direction('up'))
        window.bind('<Down>', lambda event: change_direction('down'))

        # Load an image
        image_file = tk.PhotoImage(file="C:\\Users\\User\\Pictures\\ForPrograms\\61136.png")

        # Create a button with the image
        image_button = tk.Button(window, image=image_file, command=background, width=35, height=35)
        image_button.image = image_file  # type: ignore # Keep a reference to the image to prevent garbage collection

        image_button.pack()
        image_button.place(x=WINDOW_WIDTH - 50, y=4.5)  # Adjust the values as needed
        # Initialize the game state
        score = 0
        direction = "down"
        label.config(text="Score: {}".format(score))
        highest_score_label = Label(window, text="", font=('consolas', 15), bg="springgreen")
        highest_score_label.pack()
        highest_score_label.place(x=10, y=10)
        # Display the highest score
        display_highest_score()

        # Create the snake and food
        snake = Snake()
        food = Food()

        # Start the game loop
        next_turn(snake, food)
        # Sets the function to be called when the window is closed
        window.protocol("WM_DELETE_WINDOW", on_closing)  


def update_highest_score(score):
    try:
        with open("highest_score.txt", "r") as file:
            current_highest_score = int(file.read())
    except FileNotFoundError:
        current_highest_score = 0

    if score > current_highest_score:
        with open("highest_score.txt", "w") as file:
            file.write(str(score))

    try:
        with open("highest_score.txt", "r") as file:
            highest_score = int(file.read())
    except FileNotFoundError:
        highest_score = 0

    return highest_score

# Function to display the highest score
def display_highest_score():
    try:
        with open("highest_score.txt", "r") as file:
            highest_score = int(file.read())
    except FileNotFoundError:
        highest_score = 0

    highest_score_label.config(text=f"Highest Score: {highest_score}")

def on_closing():
    global window
    if messagebox.askyesno("Quit", "Do you want to quit?"):
        window.destroy()
        window = None  # Set the global variable to None after the window is destroyed


def play_music():
    global song
    # Stop the currently playing music
    pygame.mixer.music.stop()

    # Load and play the new music
    song = (song + 1)%6
    if song == 0:
        pygame.mixer.music.load("C:\\Users\\User\\SnakeGamePython\\songs\\allTheRoads.mp3")
    elif song == 1:
        pygame.mixer.music.load("C:\\Users\\User\\SnakeGamePython\\songs\\andAll.mp3")
    elif song == 2:
        pygame.mixer.music.load("C:\\Users\\User\\SnakeGamePython\\songs\\atonement.mp3")
    elif song == 3:
        pygame.mixer.music.load("C:\\Users\\User\\SnakeGamePython\\songs\\fightForYou.mp3")
    elif song == 4:
        pygame.mixer.music.load("C:\\Users\\User\\SnakeGamePython\\songs\\gatesOftears.mp3")
    elif song == 5:
        pygame.mixer.music.load("C:\\Users\\User\\SnakeGamePython\\songs\\willNotForget.mp3")

    pygame.mixer.music.play(-1)  # The '-1' plays the music on loop. '0' would play the music once.



root = Tk()
root.title("Snake Game")
root.configure(bg='springgreen')
root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

playButton = tk.Button(root, text="PLAY", command=play, bg="darkorchid2", font=("consolas", 30))
playButton.pack()
playButton.place(relx=0.5,rely=0.5,anchor=CENTER) 


root.mainloop()