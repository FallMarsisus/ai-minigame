import os
from dotenv import load_dotenv
import google.generativeai as genai
import tkinter as tk
import tkinter.ttk as ttk


def game():
  """
  This function starts the game and handles the game logic.

  It increases the difficulty level, updates the game screen, sends a question to the chat session,
  waits for the user's response, and updates the game screen accordingly.

  Parameters:
    None

  Returns:
    None
  """
  global is_waiting, text_answer, difficulty
  if difficulty<10: difficulty+= 1
  home_screen_frame.pack_forget()
  game_frame.pack()
  anwser_text.config(text = "")
  next_button.pack_forget()
  response = chat_session.send_message(f"You are going to ask another difficult question, that you can anwser with true or false, in around 10 seconds, but it has to be tricky, in a ladder from 0 to 20, use difficulty {difficulty+10}")
  is_waiting = True
  question_text.config(text= response.text)
  while is_waiting:
    window.update()
  next_button.pack()
  anwser_text.config(text=text_answer)
    
    


def ansTrue():
  global is_waiting, text_answer

  if is_waiting:
    response = chat_session.send_message("1")
    is_waiting = False
    text_answer = response.text

def ansFalse():
  global is_waiting, text_answer

  if is_waiting:
    response = chat_session.send_message("2")
    is_waiting = False
    text_answer = response.text


load_dotenv()
is_waiting = False
text_answer = ""
api_key = os.getenv("API_KEY")
difficulty = 0

window = tk.Tk()

p = ttk.Progressbar(window,orient=tk.HORIZONTAL,length=200,mode="determinate",takefocus=True,maximum=100)
p.start()
p.pack()


genai.configure(api_key=api_key)

# Create the model
generation_config = {
  "temperature": 1.2,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  system_instruction="We are going to play a game : the player will have to choose between two options, it will choose the first option (or true) by typing 1, or the second option  (or false) by typing 2. Your goal is to trick the player into choosing the wrong option. If you succeed, you win. If you fail, the player wins. If something else than 1 or 2 is typed, take it as requests from the game master. When a question is asked, type just the question, without text decorations. When the player gives his answer, please tell him if he's wrong or not, you can also shortly explain why, but dont ask another question until asked specifically"
)

chat_session = model.start_chat(
  history=[
  ]
)

p.pack_forget()

home_screen_frame = tk.Frame(window)
home_screen_frame.pack()
welcome_text = tk.Label(home_screen_frame, text='Welcome to the AI Quiz, a quiz about luck, and mainly logic !')
welcome_text.pack()

start_button = tk.Button(home_screen_frame, text='Start', command=game)
start_button.pack()

game_frame = tk.Frame(window)

question_text = tk.Label(game_frame)
question_text.pack()

button_true = tk.Button(game_frame, text="True", command=ansTrue)
button_true.pack()

button_false = tk.Button(game_frame, text="False", command=ansFalse)
button_false.pack()

anwser_text = tk.Label(game_frame)
anwser_text.pack()
next_button = tk.Button(game_frame, text="Next", command=game)


    



window.mainloop()