import tkinter as tk
from PIL import Image, ImageTk
import random
#initialize the main window
root=tk.Tk()
# Set the title of the window
root.title("Catch-the-Egg")
window_width=800
window_height=600
root.geometry(f"{window_width}x{window_height}")# Set the size of the window
root.resizable(False, False)

#creating canvas
canvas = tk.Canvas(root, width=800, height=600, bg="lightblue")
# Draw the sky (top half)
canvas.create_rectangle(0, 0, 800, 400, fill="lightblue", outline="")
# Draw the ground (bottom half)
canvas.create_rectangle(0, 500, 800, 600, fill="lightgreen", outline="")

score = 0  # initialize score
score_text = canvas.create_text(650, 30, text=f"Score: {score}", font=("Helvetica", 24), fill="black")

lives = 3
lives_text = canvas.create_text(100, 30, text=f"Lives: {lives}", font=("Helvetica", 24), fill="black")

game_over_text = None  # Initialize game over text variable

game_running = False
game_over_text = None
play_button = None
play_again_button = None


#loading clouds
original5 = Image.open("Images/cloud.png")
resized5 = original5.resize((260, 100))  # Width x Height in pixels
cloud = ImageTk.PhotoImage(resized5)
Cloud = canvas.create_image(400, 130, anchor="s", image=cloud)

resized6 = original5.resize((180, 70))  # Width x Height in pixels
cloud1 = ImageTk.PhotoImage(resized6)
Cloud1 = canvas.create_image(200, 180, anchor="s", image=cloud1)

resized7 = original5.resize((140, 40))  # Width x Height in pixels
cloud2 = ImageTk.PhotoImage(resized7)
Cloud2 = canvas.create_image(600, 110, anchor="s", image=cloud2)

# Load the image (after converting to .png)
original = Image.open("Images/hen4.png")
resized = original.resize((200, 130))  # Width x Height in pixels
# Convert to PhotoImage for Tkinter
hen_image = ImageTk.PhotoImage(resized)
# Place the image on the canvas — bottom-right, just above red ground
hen = canvas.create_image(400, 105, anchor="s", image=hen_image)


#place the barn
original2 = Image.open("Images/barn.png")
resized2 = original2.resize((450, 320))  # Width x Height in pixels
barn = ImageTk.PhotoImage(resized2)
Barn = canvas.create_image(630, 540, anchor="s", image=barn)

#loading second hen image
original1 = Image.open("Images/hen3.png")
resized1 = original1.resize((120, 120))  # Width x Height in pixels
hen_image1 = ImageTk.PhotoImage(resized1)
hen1 = canvas.create_image(740, 530, anchor="s", image=hen_image1)

#place the tractor
original3 = Image.open("Images/tractor.png")
resized3 = original3.resize((350, 260))  # Width x Height in pixels
tractor = ImageTk.PhotoImage(resized3)
Tractor = canvas.create_image(200, 530, anchor="s", image=tractor)

#place the tree
original4 = Image.open("Images/tree.png")
resized4 = original4.resize((500, 600))  # Width x Height in pixels
tree = ImageTk.PhotoImage(resized4)
Tree = canvas.create_image(180, 650, anchor="s", image=tree)
canvas.pack()

#loading egg image
egg_img_raw = Image.open("Images/egg.png")
egg_img_resized = egg_img_raw.resize((50, 60))
egg_image = ImageTk.PhotoImage(egg_img_resized)

# Load and resize basket image
basket_raw = Image.open("Images/basket.png")
basket_resized = basket_raw.resize((150, 100))  # adjust size if needed
basket_image = ImageTk.PhotoImage(basket_resized)

# Place basket at bottom center
basket_x = window_width // 2
basket_y = window_height - 30
basket = canvas.create_image(basket_x, basket_y, anchor="s", image=basket_image)

def animate_game_over(count=0):
    colors = ["red", "black"]
    canvas.itemconfig(game_over_text, fill=colors[count % 2])
    if count < 10:  # Flash 5 times
        root.after(300, animate_game_over, count + 1)




def bounce_score(size=24, grow=True):
    canvas.itemconfig(score_text, font=("Helvetica", size))
    if grow and size < 32:
        root.after(50, bounce_score, size + 2, True)
    elif not grow and size > 24:
        root.after(50, bounce_score, size - 2, False)
    elif grow:
        root.after(50, bounce_score, size, False)

bounce_score()

def random_egg_drop():
    if not game_running:
        return
    drop_egg()
    delay = random.randint(1000, 3000)
    root.after(delay, random_egg_drop)


def start_game():
    global game_running, score, lives, play_button, play_again_button, score_text, lives_text

    # Reset values
    game_running = True
    score = 0
    lives = 3

    # Remove any previous game over text or play again button
    if play_button:
        canvas.delete(play_button)
        play_button = None
    if play_again_button:
        canvas.delete(play_again_button)
        play_again_button = None
    if game_over_text:
        canvas.delete(game_over_text)

    # Reset score and lives on canvas
    canvas.itemconfig(score_text, text=f"Score: {score}")
    canvas.itemconfig(lives_text, text=f"Lives: {lives}")

    # Start dropping eggs
    random_egg_drop()
    move_hen()  # Restart hen movement



# Set initial movement direction and speed
hen_direction = 1  # 1 = right, -1 = left
hen_speed = 5      # pixels per step
# Get canvas dimensions
canvas_width = 800

def move_hen():
    global hen_direction
    if not game_running:
        return  # Stop moving hen if game is not running

    canvas.move(hen, hen_direction * hen_speed, 0)
    hen_x = canvas.coords(hen)[0]

    if hen_x >= canvas_width - 115:
        hen_direction = -1
    elif hen_x <= 115 // 2:
        hen_direction = 1

    canvas.after(30, move_hen)

move_hen()

def drop_egg():
    global score

    egg_x = canvas.coords(hen)[0]
    egg_y = 130  # start just below the hen

    # Use image instead of oval
    egg = canvas.create_image(egg_x, egg_y, image=egg_image)

    def fall():
        
        global lives, score, game_running, game_over_text, play_again_button
        nonlocal egg_y
        if not game_running:
            canvas.delete(egg)
            return
        egg_y += 5
        canvas.move(egg, 0, 5)

        egg_coords = canvas.coords(egg)
        if not egg_coords:
            return  # Egg was deleted before

        egg_x_center, egg_y_center = egg_coords
        basket_x, basket_y = canvas.coords(basket)

                # Collision check for catching
                # Catch condition
        if (abs(egg_x_center - basket_x) < 60) and (abs(egg_y_center - basket_y) < 60):
            canvas.delete(egg)
            score += 1
            canvas.itemconfig(score_text, text=f"Score: {score}")
            bounce_score()  # <-- Animate score on catch
            return



        if egg_y_center < window_height - 10:
            canvas.after(30, fall)
        else:
            canvas.delete(egg)
            lives -= 1
            canvas.itemconfig(lives_text, text=f"Lives: {lives}")
            
        if lives == 0:
            game_running = False

            if game_over_text:
                canvas.delete(game_over_text)
            if play_again_button:
                canvas.delete(play_again_button)

            game_over_text = canvas.create_text(400, 300, text="Game Over!", font=("Helvetica", 48, "bold"), fill="red")
            animate_game_over()
            play_again_button = canvas.create_text(400, 360, text="▶ Play Again", font=("Helvetica", 28, "bold"), fill="darkgreen")
            canvas.tag_bind(play_again_button, "<Button-1>", lambda e: start_game())
            return

    fall()


# Sta
import random

random_egg_drop()

basket_speed = 30  # pixels per move

def move_basket(event):
    global basket
    x, y = canvas.coords(basket)
    
    if event.keysym == 'Left' and x - basket_speed >= 50:
        canvas.move(basket, -basket_speed, 0)
    elif event.keysym == 'Right' and x + basket_speed <= window_width - 50:
        canvas.move(basket, basket_speed, 0)

# Bind keys
root.bind('<Left>', move_basket)
root.bind('<Right>', move_basket)

play_button = canvas.create_text(400, 300, text="▶ Play", font=("Helvetica", 36, "bold"), fill="darkblue")
canvas.tag_bind(play_button, "<Button-1>", lambda e: start_game())

root.mainloop()# Start the main loop to run the application
