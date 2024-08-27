import tkinter as tk
from tkinter import messagebox
import random


class HangmanGame:
    def __init__(self, root):
        self.root = root
        self.root.title("AHORCADO")
        self.root.configure(bg="darkred")

        self.players = []
        self.current_player = 0
        self.word_to_guess = ""
        self.hidden_word = ""
        self.max_attempts = 6
        self.attempts = 0
        self.correct_guesses = 0
        self.rounds = 0
        self.used_letters = set()
        self.scores = [0, 0]

        self.create_widgets()

    def create_widgets(self):
        self.title_label = tk.Label(self.root, text="AHORCADO", font=("Arial", 24), bg="darkred", fg="white")
        self.title_label.pack(pady=10)

        self.instructions = tk.Label(self.root, text="Ingrese los nombres de los jugadores.", bg="darkred", fg="white")
        self.instructions.pack(pady=10)

        self.name_frame = tk.Frame(self.root, bg="darkred")
        self.name_frame.pack(pady=10)

        self.player1_label = tk.Label(self.name_frame, text="Nombre del Jugador 1:", bg="darkred", fg="white")
        self.player1_label.grid(row=0, column=0, padx=10)

        self.player1_entry = tk.Entry(self.name_frame)
        self.player1_entry.grid(row=0, column=1, padx=10)

        self.player2_label = tk.Label(self.name_frame, text="Nombre del Jugador 2:", bg="darkred", fg="white")
        self.player2_label.grid(row=1, column=0, padx=10)

        self.player2_entry = tk.Entry(self.name_frame)
        self.player2_entry.grid(row=1, column=1, padx=10)

        self.start_button = tk.Button(self.root, text="Comenzar Juego", command=self.start_game)
        self.start_button.pack(pady=10)

    def start_game(self):
        player1 = self.player1_entry.get()
        player2 = self.player2_entry.get()

        if not player1 or not player2:
            messagebox.showwarning("Advertencia", "Por favor, ingresa los nombres de ambos jugadores.")
            return

        self.players = [player1, player2]
        self.current_player = 0
        self.attempts = 0
        self.rounds = 0
        self.correct_guesses = 0
        self.scores = [0, 0]
        self.used_letters.clear()

        self.show_game_screen()

    def show_game_screen(self):
        self.clear_widgets()

        self.word_label = tk.Label(self.root,
                                   text=f"Turno de {self.players[self.current_player]}: Ingrese una palabra para que el otro jugador la adivine:",
                                   bg="darkred", fg="white")
        self.word_label.pack(pady=10)

        self.word_entry = tk.Entry(self.root, show="*")
        self.word_entry.pack(pady=10)

        self.submit_word_button = tk.Button(self.root, text="Enviar Palabra", command=self.submit_word)
        self.submit_word_button.pack(pady=10)

    def submit_word(self):
        self.word_to_guess = self.word_entry.get().strip().upper()
        if len(self.word_to_guess) > 15:
            messagebox.showwarning("Advertencia", "La palabra no puede exceder los 15 caracteres.")
            return

        if not self.word_to_guess.isalpha():
            messagebox.showwarning("Advertencia", "La palabra solo puede contener letras.")
            return

        self.hidden_word = "_" * len(self.word_to_guess)
        self.attempts = 0
        self.correct_guesses = 0
        self.used_letters.clear()
        self.show_guess_screen()

    def show_guess_screen(self):
        self.clear_widgets()

        self.word_display = tk.Label(self.root, text=self.hidden_word, font=("Arial", 24), bg="darkred", fg="white")
        self.word_display.pack(pady=10)

        self.guess_label = tk.Label(self.root,
                                    text=f"Turno de {self.players[1 - self.current_player]}: Ingresa una letra para adivinar la palabra.",
                                    bg="darkred", fg="white")
        self.guess_label.pack(pady=10)

        self.guess_entry = tk.Entry(self.root)
        self.guess_entry.pack(pady=10)

        self.submit_guess_button = tk.Button(self.root, text="Enviar Letra", command=self.submit_guess)
        self.submit_guess_button.pack(pady=10)

        self.help_button = tk.Button(self.root, text="Ayuda", command=self.use_help)
        self.help_button.pack(pady=10)

        self.info_label = tk.Label(self.root, text=f"Intentos restantes: {self.max_attempts - self.attempts}",
                                   bg="darkred", fg="white")
        self.info_label.pack(pady=10)

        self.used_letters_label = tk.Label(self.root, text="Letras utilizadas: ", bg="darkred", fg="white")
        self.used_letters_label.pack(pady=10)

        self.hangman_canvas = tk.Canvas(self.root, width=200, height=200, bg="white")
        self.hangman_canvas.pack(pady=10)
        self.draw_hangman()

        self.score_label = tk.Label(self.root,
                                    text=f"Puntuación: {self.players[0]} - {self.scores[0]} | {self.players[1]} - {self.scores[1]}",
                                    bg="darkred", fg="white")
        self.score_label.pack(pady=10)

        self.end_button = tk.Button(self.root, text="Finalizar Juego", command=self.end_game)
        self.end_button.pack(pady=10)

    def submit_guess(self):
        guess = self.guess_entry.get().strip().upper()
        if len(guess) != 1 or not guess.isalpha():
            messagebox.showwarning("Advertencia", "Ingresa solo una letra.")
            return

        if guess in self.used_letters:
            messagebox.showwarning("Advertencia", "Ya has usado esta letra.")
            return

        self.used_letters.add(guess)
        self.update_used_letters()

        if guess in self.word_to_guess:
            self.update_hidden_word(guess)
        else:
            self.attempts += 1
            self.draw_hangman()

        self.guess_entry.delete(0, tk.END)
        self.update_info()

        if self.hidden_word == self.word_to_guess:
            messagebox.showinfo("¡Felicidades!",
                                f"{self.players[1 - self.current_player]} adivinó la palabra correctamente.")
            self.scores[1 - self.current_player] += 1
            self.end_round()
        elif self.attempts >= self.max_attempts:
            messagebox.showwarning("Fin del Juego",
                                   f"{self.players[1 - self.current_player]} ha perdido. La palabra era: {self.word_to_guess}.")
            self.end_round()

    def update_hidden_word(self, guess):
        updated_word = list(self.hidden_word)
        for i, letter in enumerate(self.word_to_guess):
            if letter == guess:
                updated_word[i] = guess
                self.correct_guesses += 1
        self.hidden_word = "".join(updated_word)
        self.word_display.config(text=self.hidden_word)

    def use_help(self):
        remaining_letters = [c for c in self.word_to_guess if c not in self.hidden_word]
        if remaining_letters:
            hint_letter = random.choice(remaining_letters)
            messagebox.showinfo("Ayuda", f"Letra sugerida: {hint_letter}")

    def update_info(self):
        self.info_label.config(text=f"Intentos restantes: {self.max_attempts - self.attempts}")

    def update_used_letters(self):
        self.used_letters_label.config(text=f"Letras utilizadas: {', '.join(sorted(self.used_letters))}")

    def draw_hangman(self):
        self.hangman_canvas.delete("all")
        if self.attempts > 0:
            self.hangman_canvas.create_line(50, 150, 150, 150)  # Base
        if self.attempts > 1:
            self.hangman_canvas.create_line(100, 150, 100, 50)  # Poste vertical
        if self.attempts > 2:
            self.hangman_canvas.create_line(100, 50, 150, 50)  # Poste horizontal
        if self.attempts > 3:
            self.hangman_canvas.create_line(150, 50, 150, 70)  # Cuerda
        if self.attempts > 4:
            self.hangman_canvas.create_oval(140, 70, 160, 90)  # Cabeza
        if self.attempts > 5:
            self.hangman_canvas.create_line(150, 90, 150, 130)  # Cuerpo
        if self.attempts > 6:
            self.hangman_canvas.create_line(150, 100, 140, 110)  # Brazo izquierdo
        if self.attempts > 7:
            self.hangman_canvas.create_line(150, 100, 160, 110)  # Brazo derecho
        if self.attempts > 8:
            self.hangman_canvas.create_line(150, 130, 140, 140)  # Pierna izquierda
        if self.attempts > 9:
            self.hangman_canvas.create_line(150, 130, 160, 140)  # Pierna derecha

    def end_round(self):
        self.rounds += 1
        self.current_player = 1 - self.current_player
        if messagebox.askyesno("Fin de la Ronda", "¿Desean continuar jugando?"):
            self.show_game_screen()
        else:
            self.end_game()

    def end_game(self):
        winner = "Empate"
        if self.scores[0] > self.scores[1]:
            winner = self.players[0]
        elif self.scores[1] > self.scores[0]:
            winner = self.players[1]

        messagebox.showinfo("Fin del Juego", f"Juego terminado.\nGanador: {winner}\n\nPuntuaciones:\n{self.players[0]}: {self.scores[0]}\n{self.players[1]}: {self.scores[1]}")
        self.save_game_results()
        self.root.destroy()

    def save_game_results(self):
        with open("resultados_ahorcado.txt", "w") as file:
            file.write(f"Resultados del Juego Ahorcado\n\n")
            file.write(f"Jugador 1: {self.players[0]} - Puntuación: {self.scores[0]}\n")
            file.write(f"Jugador 2: {self.players[1]} - Puntuación: {self.scores[1]}\n")
            file.write(f"Rondas Jugadas: {self.rounds}\n")
            file.write(f"Ganador: {self.players[0] if self.scores[0] > self.scores[1] else (self.players[1] if self.scores[1] > self.scores[0] else 'Empate')}\n")

    def clear_widgets(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    game = HangmanGame(root)
    root.mainloop()

