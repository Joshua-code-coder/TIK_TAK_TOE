import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import random
import sys
import os
import time

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")

        self.player_symbols = {'X': '', 'O': ''}
        self.current_player = 'X'
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.bot_mode = False
        self.custom_button_color = "white"
        self.rounds_played = 0
        self.player_wins = {'X': 0, 'O': 0}

        # Initialize round_label
        self.round_label = tk.Label(self.root, text='', font=('Arial', 16))
        self.round_label.grid(row=6, column=0, columnspan=3, pady=10)

        self.create_main_window()
        self.overall_draw_label = None
        self.round_label = None
        self.draw_count = 0
        
    def on_button_click(self, row, col):
        if self.board[row][col] == '' and not self.check_winner(row, col):
            self.board[row][col] = self.current_player
            self.buttons[row][col].config(text=self.current_player, state='disabled', disabledforeground='red',
                                           bg=self.custom_button_color)  # Set the button color

            if self.check_winner(row, col):
                self.highlight_winning_combination()
                self.show_winner_message()
                self.player_wins[self.current_player] += 1
                self.rounds_played += 1
                if self.player_wins[self.current_player] == 2:
                    self.show_overall_winner()
                else:
                    self.show_round_winner()
                    self.root.after(1000, self.play_next_round)  # Reduced delay to 1000 milliseconds (1 second)
            elif self.check_draw():
                self.show_draw_message()
                self.rounds_played += 1
                if self.rounds_played == 3:
                    self.show_overall_draw()
                else:
                    self.root.after(1000, self.play_next_round)  # Reduced delay to 1000 milliseconds (1 second)
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'
                self.update_status_label()

                if self.bot_mode and self.current_player == 'O':
                    self.play_bot()
 


    def create_main_window(self):
        self.get_usernames()

    def get_usernames(self):
        label1 = tk.Label(self.root, text="Enter username for Player 1:")
        label1.grid(row=0, column=0, padx=10, pady=5)

        entry1 = tk.Entry(self.root)
        entry1.grid(row=0, column=1, padx=10, pady=5)

        label2 = tk.Label(self.root, text="Enter username for Player 2:")
        label2.grid(row=1, column=0, padx=10, pady=5)

        entry2 = tk.Entry(self.root)
        entry2.grid(row=1, column=1, padx=10, pady=5)

        bot_mode_button = tk.Button(self.root, text="Bot Mode", command=lambda: self.set_usernames(entry1.get(), entry2.get(), bot_mode=True))
        bot_mode_button.grid(row=2, column=0, pady=10)

        one_vs_one_button = tk.Button(self.root, text="1v1", command=lambda: self.set_usernames(entry1.get(), entry2.get(), bot_mode=False))
        one_vs_one_button.grid(row=2, column=1, pady=10)

    def set_usernames(self, player1_name, player2_name, bot_mode):
        self.player_symbols['X'] = player1_name
        self.player_symbols['O'] = player2_name
        self.bot_mode = bot_mode

        for widget in self.root.winfo_children():
            widget.destroy()

        self.create_game_widgets()
        self.update_status_label()

    def create_game_widgets(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(self.root, text='', font=('Arial', 24), width=4, height=2,
                                              command=lambda row=i, col=j: self.on_button_click(row, col))
                self.buttons[i][j].grid(row=i + 3, column=j)

        self.winning_label = tk.Label(self.root, text='', font=('Arial', 16))
        self.winning_label.grid(row=6, column=0, columnspan=3, pady=10)

        restart_round_button = tk.Button(self.root, text="Restart Round", command=self.restart_round)
        restart_round_button.grid(row=7, column=0, pady=10)

        exit_button = tk.Button(self.root, text="Exit", command=self.root.destroy)
        exit_button.grid(row=7, column=1, pady=10)

        restart_game_button = tk.Button(self.root, text="Restart Game", command=self.restart_game)
        restart_game_button.grid(row=7, column=2, pady=10)

        customize_button = tk.Button(self.root, text="Customize", command=self.open_customize_window)
        customize_button.grid(row=8, column=0, columnspan=3, pady=10)

        self.update_status_label()

    def on_button_click(self, row, col):
        if self.board[row][col] == '' and not self.check_winner(row, col):
            self.board[row][col] = self.current_player
            self.buttons[row][col].config(text=self.current_player, state='disabled', disabledforeground='red',
                                           bg=self.custom_button_color)  # Set the button color

            if self.check_winner(row, col):
                self.highlight_winning_combination()
                self.show_winner_message()
                self.player_wins[self.current_player] += 1
                self.rounds_played += 1
                if self.player_wins[self.current_player] == 2:
                    self.show_overall_winner()
                else:
                    self.show_round_winner()
                    self.root.after(1000, self.play_next_round)  # Reduced delay to 1000 milliseconds (1 second)
            elif self.check_draw():
                self.show_draw_message()
                self.rounds_played += 1
                if self.rounds_played == 3:
                    self.show_overall_winner()
                else:
                    self.root.after(1000, self.play_next_round)  # Reduced delay to 1000 milliseconds (1 second)
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'
                self.update_status_label()

                if self.bot_mode and self.current_player == 'O':
                    self.play_bot()

    def play_bot(self):
        available_moves = [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == '']
        
        if available_moves:
            best_score = float('-inf')
            best_move = None

            for move in available_moves:
                row, col = move
                self.board[row][col] = self.current_player
                score = self.minimax(self.board, 0, False)
                self.board[row][col] = ''  # Undo the move

                if score > best_score:
                    best_score = score
                    best_move = move

            row, col = best_move
            self.on_button_click(row, col)

    def minimax(self, board, depth, is_maximizing):
        scores = {'X': -1, 'O': 1, 'draw': 0}

        winner = self.check_winner_minimax(board)
        if winner:
            return scores[winner]

        if is_maximizing:
            best_score = float('-inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == '':
                        board[i][j] = 'O'
                        score = self.minimax(board, depth + 1, False)
                        board[i][j] = ''  # Undo the move
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == '':
                        board[i][j] = 'X'
                        score = self.minimax(board, depth + 1, True)
                        board[i][j] = ''  # Undo the move
                        best_score = min(score, best_score)
            return best_score

    def check_winner_minimax(self, board):
        for i in range(3):
            # Check row
            if board[i][0] == board[i][1] == board[i][2] != '':
                return board[i][0]
            # Check column
            if board[0][i] == board[1][i] == board[2][i] != '':
                return board[0][i]

        # Check diagonals
        if board[0][0] == board[1][1] == board[2][2] != '':
            return board[0][0]
        if board[0][2] == board[1][1] == board[2][0] != '':
            return board[0][2]

        # Check for a draw
        if all(cell != '' for row in board for cell in row):
            return 'draw'

        # No winner yet
        return None

    def update_status_label(self):
        if self.bot_mode:
            current_player_label = f"{self.player_symbols[self.current_player] if self.current_player == 'X' else 'Bot'}'s turn"
        else:
            current_player_label = f"{self.player_symbols[self.current_player]}'s turn"

        self.winning_label.config(text=f"Round {self.rounds_played + 1}: {current_player_label}")

# ... (Previous code above this line remains unchanged)

    def check_winner(self, row, col):
        # Check row
        if all(self.board[row][j] == self.current_player for j in range(3)):
            return True
        # Check column
        if all(self.board[i][col] == self.current_player for i in range(3)):
            return True
        # Check diagonals
        if all(self.board[i][i] == self.current_player for i in range(3)):
            return True
        if all(self.board[i][2 - i] == self.current_player for i in range(3)):
            return True
        return False

    def check_draw(self):
        if all(all(cell != '' for cell in row) for row in self.board):
            return True
        return False

    def show_winner_message(self):
        winner = f"{self.player_symbols[self.current_player]} wins the round!"
        self.winning_label.config(text=winner)

    def show_draw_message(self):
        self.winning_label.config(text="It's a draw!")

    def reset_board(self):
        self.winning_label.config(text='')
        for i in range(3):
            for j in range(3):
                self.board[i][j] = ''
                self.buttons[i][j].config(text='', state='normal', bg='SystemButtonFace', disabledforeground='black')

        # Ensure X starts the second round
        if self.rounds_played % 2 == 1:
            self.current_player = 'X'

        self.update_status_label()

        if self.bot_mode and self.current_player == 'O':
            self.play_bot()
    def open_customize_window(self):
        customize_window = tk.Toplevel(self.root)
        customize_window.title("Customize")

        color_label = tk.Label(customize_window, text="Choose button background color:")
        color_label.pack(pady=10)

        color_var = tk.StringVar()
        color_var.set(self.custom_button_color)  # Set the current color

        color_entry = ttk.Combobox(customize_window, textvariable=color_var, values=["white", "lightblue", "lightgreen", "black"])
        color_entry.pack(pady=10)

        apply_button = tk.Button(customize_window, text="Apply", command=lambda: self.apply_customization(color_var.get()))
        apply_button.pack(pady=10)

    def apply_customization(self, button_color):
        self.custom_button_color = button_color
        text_color = 'red'  # Change text color to red
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(bg=self.custom_button_color, disabledforeground=text_color)

    def highlight_winning_combination(self):
        # Check row
        for j in range(3):
            if all(self.board[j][i] == self.current_player for i in range(3)):
                self.highlight_cells([(j, i) for i in range(3)])
                return
        # Check column
        for i in range(3):
            if all(self.board[j][i] == self.current_player for j in range(3)):
                self.highlight_cells([(j, i) for j in range(3)])

        if all(self.board[i][i] == self.current_player for i in range(3)):
            self.highlight_cells([(i, i) for i in range(3)])

        if all(self.board[i][2 - i] == self.current_player for i in range(3)):
            self.highlight_cells([(i, 2 - i) for i in range(3)])

    def highlight_cells(self, cells):
        for i, j in cells:
            self.buttons[i][j].config(bg='yellow')

    def show_round_winner(self):
        winner = f"{self.player_symbols[self.current_player]} wins Round {self.rounds_played}!"
        self.round_label = tk.Label(self.root, text=winner, font=('Arial', 16, 'bold'))
        self.round_label.grid(row=0, column=0, columnspan=3, pady=10)
        self.root.after(1000, self.hide_round_winner)  # Reduced delay to 1000 milliseconds (1 second)

    def hide_round_winner(self):
        self.round_label.grid_forget()



    def show_overall_winner(self):
        if self.player_wins['X'] == self.player_wins['O']:
            overall_winner = "It's a complete draw!"
        else:
            overall_winner = f"{self.player_symbols[max(self.player_wins, key=self.player_wins.get)]} wins the game!"

        if self.draw_count == 3:
            overall_winner = "Overall draw. Play again! Bye!"
        else:
            self.draw_count += 1

        if self.round_label is None:
            self.round_label = tk.Label(self.root, text="", font=('Arial', 16, 'bold'))
            self.round_label.grid(row=0, column=0, columnspan=3, pady=10)

        self.round_label.config(text=overall_winner)
        messagebox.showinfo("Game Over", overall_winner + "\n\nThank you for playing!")


    def next_round(self):
        self.update_status_label()
        self.reset_board()

    def play_next_round(self):
        if self.rounds_played < 3:
            self.reset_board()
            self.update_status_label()  # Added to ensure correct player label
            if self.bot_mode and self.current_player == 'O':
                self.play_bot()
        else:
            self.show_overall_winner()
    def restart_game(self):
        self.root.destroy()  # Close the current program

        # Start a new instance of the program
        python = sys.executable
        os.system(f'{python} "{__file__}"')

    def restart_round(self):
        self.update_status_label()
        self.reset_board()

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
