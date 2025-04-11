import tkinter as tk
from tkinter import messagebox, font
import random

class ResponsiveHangman:
    def __init__(self, root):
        self.create_style_guide()
        self.root = root
        self.setup_window()
        self.load_game_data()
        self.create_widgets()
        self.setup_responsive_behavior()
        self.start_new_game()
    
    def create_style_guide(self):
        """Define o guia de estilo consistente"""
        self.colors = {
            "background": "#f8f9fa",
            "primary": "#2c3e50",
            "secondary": "#3498db",
            "success": "#2ecc71",
            "danger": "#e74c3c",
            "warning": "#f39c12",
            "text": "#2c3e50",
            "text_light": "#7f8c8d"
        }
        
        self.fonts = {
            "title": ("Helvetica", 24, "bold"),
            "heading": ("Helvetica", 18, "bold"),
            "subheading": ("Helvetica", 14),
            "default": ("Helvetica", 12),
            "word_display": ("Courier", 32)
        }
        
        self.spacing = {
            "small": 5,
            "medium": 10,
            "large": 20,
            "xlarge": 30
        }
    
    def setup_window(self):
        """Configura a janela principal"""
        self.root.title("Jogo da Forca")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        self.root.configure(bg=self.colors["background"])
        self.root.option_add('*Font', self.fonts["default"])
    
    def load_game_data(self):
        """Carrega as palavras e categorias"""
        self.word_categories = {
            "Frutas": ["ABACAXI", "BANANA", "MORANGO", "LARANJA", "UVA", "MELANCIA"],
            "Países": ["BRASIL", "CANADÁ", "JAPÃO", "ITÁLIA", "FRANÇA", "ALEMANHA"],
            "Animais": ["ELEFANTE", "GIRAFA", "TIGRE", "LEÃO", "ZEBRA", "RINOCERONTE"]
        }
        self.current_category = ""
        self.secret_word = ""
        self.guessed_letters = []
        self.wrong_attempts = 0
        self.max_attempts = 6
    
    def create_widgets(self):
        """Cria todos os elementos da interface"""
        self.create_main_container()
        self.create_header()
        self.create_game_area()
        self.create_control_panel()
    
    def create_main_container(self):
        """Cria o container principal com grid responsivo"""
        self.main_frame = tk.Frame(
            self.root, 
            bg=self.colors["background"],
            padx=self.spacing["large"],
            pady=self.spacing["large"]
        )
        self.main_frame.pack(fill="both", expand=True)
        
        self.main_frame.grid_rowconfigure(0, weight=0)
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(2, weight=0)
        self.main_frame.grid_columnconfigure(0, weight=1)
    
    def create_header(self):
        """Cria o cabeçalho do jogo"""
        header_frame = tk.Frame(
            self.main_frame,
            bg=self.colors["background"]
        )
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, self.spacing["large"]))
        
        self.title_label = tk.Label(
            header_frame,
            text="Jogo da Forca",
            font=self.fonts["title"],
            fg=self.colors["primary"],
            bg=self.colors["background"]
        )
        self.title_label.pack(side="left")
        
        self.category_label = tk.Label(
            header_frame,
            text="Categoria: ",
            font=self.fonts["subheading"],
            fg=self.colors["text"],
            bg=self.colors["background"]
        )
        self.category_label.pack(side="right")
    
    def create_game_area(self):
        """Cria a área principal do jogo"""
        game_frame = tk.Frame(
            self.main_frame,
            bg=self.colors["background"]
        )
        game_frame.grid(row=1, column=0, sticky="nsew")
        
        game_frame.grid_rowconfigure(0, weight=1)
        game_frame.grid_columnconfigure(0, weight=1)
        game_frame.grid_columnconfigure(1, weight=1)
        
        self.hangman_frame = tk.Frame(
            game_frame,
            bg=self.colors["background"]
        )
        self.hangman_frame.grid(row=0, column=0, sticky="nsew", padx=self.spacing["medium"])
        
        self.hangman_canvas = tk.Canvas(
            self.hangman_frame,
            bg=self.colors["background"],
            highlightthickness=0
        )
        self.hangman_canvas.pack(fill="both", expand=True)
        
        game_panel = tk.Frame(
            game_frame,
            bg=self.colors["background"]
        )
        game_panel.grid(row=0, column=1, sticky="nsew", padx=self.spacing["medium"])
        
        self.word_frame = tk.Frame(
            game_panel,
            bg=self.colors["background"]
        )
        self.word_frame.pack(fill="x", pady=(0, self.spacing["xlarge"]))
        
        self.word_label = tk.Label(
            self.word_frame,
            text="",
            font=self.fonts["word_display"],
            fg=self.colors["primary"],
            bg=self.colors["background"]
        )
        self.word_label.pack()
        
        self.used_letters_frame = tk.Frame(
            game_panel,
            bg=self.colors["background"]
        )
        self.used_letters_frame.pack(fill="x", pady=(0, self.spacing["large"]))
        
        self.used_letters_label = tk.Label(
            self.used_letters_frame,
            text="Letras usadas: ",
            font=self.fonts["subheading"],
            fg=self.colors["text_light"],
            bg=self.colors["background"]
        )
        self.used_letters_label.pack()
        
        self.attempts_frame = tk.Frame(
            game_panel,
            bg=self.colors["background"]
        )
        self.attempts_frame.pack(fill="x", pady=(0, self.spacing["xlarge"]))
        
        self.attempts_label = tk.Label(
            self.attempts_frame,
            text="Tentativas: 0/6",
            font=self.fonts["subheading"],
            fg=self.colors["danger"],
            bg=self.colors["background"]
        )
        self.attempts_label.pack()
    
    def create_control_panel(self):
        """Cria os botões de controle"""
        control_frame = tk.Frame(
            self.main_frame,
            bg=self.colors["background"]
        )
        control_frame.grid(row=2, column=0, sticky="ew", pady=(self.spacing["large"], 0))
        
        self.hint_button = tk.Button(
            control_frame,
            text="Dica",
            command=self.give_hint,
            font=self.fonts["subheading"],
            bg=self.colors["secondary"],
            fg="white",
            activebackground="#2980b9",
            relief="flat",
            padx=self.spacing["medium"],
            pady=self.spacing["small"]
        )
        self.hint_button.pack(side="left", padx=self.spacing["medium"])
        
        self.new_game_button = tk.Button(
            control_frame,
            text="Novo Jogo",
            command=self.start_new_game,
            font=self.fonts["subheading"],
            bg=self.colors["success"],
            fg="white",
            activebackground="#27ae60",
            relief="flat",
            padx=self.spacing["medium"],
            pady=self.spacing["small"]
        )
        self.new_game_button.pack(side="right", padx=self.spacing["medium"])
    
    def setup_responsive_behavior(self):
        """Configura comportamentos responsivos"""
        self.root.bind("<Configure>", self.on_window_resize)
        self.root.bind("<Key>", self.key_pressed)
    
    def on_window_resize(self, event):
        """Redimensiona elementos quando a janela muda de tamanho"""
        self.draw_hangman()
        
        window_height = self.root.winfo_height()
        base_font_size = max(10, window_height // 40)
        
        self.fonts["default"] = ("Helvetica", base_font_size)
        self.fonts["subheading"] = ("Helvetica", base_font_size + 2)
        self.fonts["heading"] = ("Helvetica", base_font_size + 6, "bold")
        self.fonts["title"] = ("Helvetica", base_font_size + 12, "bold")
        
        self.update_fonts()
    
    def update_fonts(self):
        """Atualiza todas as fontes da interface"""
        widgets = [
            (self.title_label, self.fonts["title"]),
            (self.category_label, self.fonts["subheading"]),
            (self.word_label, self.fonts["word_display"]),
            (self.used_letters_label, self.fonts["subheading"]),
            (self.attempts_label, self.fonts["subheading"]),
            (self.hint_button, self.fonts["subheading"]),
            (self.new_game_button, self.fonts["subheading"])
        ]
        
        for widget, font_spec in widgets:
            widget.config(font=font_spec)
    
    def draw_hangman(self):
        """Desenha a forca de forma responsiva"""
        self.hangman_canvas.delete("all")
        
        canvas_width = self.hangman_canvas.winfo_width()
        canvas_height = self.hangman_canvas.winfo_height()
        
        base_y = canvas_height * 0.8
        top_y = canvas_height * 0.2
        center_x = canvas_width * 0.5
        
        self.hangman_canvas.create_line(
            center_x - 100, base_y,
            center_x + 100, base_y,
            width=3
        )
        self.hangman_canvas.create_line(
            center_x, base_y,
            center_x, top_y,
            width=3
        )
        self.hangman_canvas.create_line(
            center_x, top_y,
            center_x + 100, top_y,
            width=3
        )
        self.hangman_canvas.create_line(
            center_x + 100, top_y,
            center_x + 100, top_y + 50,
            width=3
        )
        
        head_radius = min(30, canvas_width * 0.1)
        if self.wrong_attempts >= 1:
            self.hangman_canvas.create_oval(
                center_x + 100 - head_radius, top_y + 50,
                center_x + 100 + head_radius, top_y + 50 + 2*head_radius,
                width=3
            )
        if self.wrong_attempts >= 2:
            self.hangman_canvas.create_line(
                center_x + 100, top_y + 50 + 2*head_radius,
                center_x + 100, top_y + 50 + 4*head_radius,
                width=3
            )
        if self.wrong_attempts >= 3:
            self.hangman_canvas.create_line(
                center_x + 100, top_y + 50 + 2.2*head_radius,
                center_x + 70, top_y + 50 + 3*head_radius,
                width=3
            )
        if self.wrong_attempts >= 4:
            self.hangman_canvas.create_line(
                center_x + 100, top_y + 50 + 2.2*head_radius,
                center_x + 130, top_y + 50 + 3*head_radius,
                width=3
            )
        if self.wrong_attempts >= 5:
            self.hangman_canvas.create_line(
                center_x + 100, top_y + 50 + 4*head_radius,
                center_x + 70, top_y + 50 + 5.5*head_radius,
                width=3
            )
        if self.wrong_attempts >= 6:
            self.hangman_canvas.create_line(
                center_x + 100, top_y + 50 + 4*head_radius,
                center_x + 130, top_y + 50 + 5.5*head_radius,
                width=3
            )
    
    def start_new_game(self):
        """Inicia um novo jogo"""
        self.current_category = random.choice(list(self.word_categories.keys()))
        self.secret_word = random.choice(self.word_categories[self.current_category])
        self.guessed_letters = []
        self.wrong_attempts = 0
        
        self.category_label.config(text=f"Categoria: {self.current_category}")
        self.update_word_display()
        self.draw_hangman()
        self.update_attempts_display()
        self.update_used_letters()
        self.hint_button.config(state="normal")
        self.word_label.config(fg=self.colors["primary"])
    
    def update_word_display(self):
        """Atualiza a exibição da palavra oculta"""
        display_word = []
        for letter in self.secret_word:
            if letter in self.guessed_letters:
                display_word.append(letter)
            else:
                display_word.append("_")
        
        self.word_label.config(text=" ".join(display_word))
    
    def update_attempts_display(self):
        """Atualiza o contador de tentativas"""
        self.attempts_label.config(
            text=f"Tentativas: {self.wrong_attempts}/{self.max_attempts}",
            fg=self.colors["danger"] if self.wrong_attempts > 3 else self.colors["text"]
        )
    
    def update_used_letters(self):
        """Atualiza a exibição das letras usadas"""
        wrong_letters = [l for l in self.guessed_letters if l not in self.secret_word]
        
        if wrong_letters:
            self.used_letters_label.config(
                text=f"Letras usadas: {', '.join(sorted(wrong_letters))}",
                fg=self.colors["danger"]
            )
        else:
            self.used_letters_label.config(
                text="Letras usadas: Nenhuma",
                fg=self.colors["text_light"]
            )
    
    def key_pressed(self, event):
        """Lida com pressionamento de teclas"""
        if not event.char.isalpha():
            return
            
        letter = event.char.upper()
        
        if letter in self.guessed_letters:
            messagebox.showinfo("Letra repetida", f"Você já tentou a letra {letter}!")
            return
            
        self.guessed_letters.append(letter)
        
        if letter in self.secret_word:
            self.update_word_display()
            self.root.update()  # Atualiza a interface imediatamente
            
            # Verifica vitória após atualizar a tela
            if all(l in self.guessed_letters for l in self.secret_word):
                self.root.after(500, self.game_won)  # Pequeno delay para mostrar a letra
        else:
            self.wrong_attempts += 1
            self.draw_hangman()
            
            if self.wrong_attempts >= self.max_attempts:
                self.draw_hangman()
                self.root.update()
                self.root.after(500, self.game_lost)  # Pequeno delay para mostrar o desenho completo
        
        self.update_attempts_display()
        self.update_used_letters()
    
    def give_hint(self):
        """Fornece uma dica ao jogador"""
        undiscovered = [l for l in self.secret_word if l not in self.guessed_letters]
        
        if undiscovered:
            hint_letter = random.choice(undiscovered)
            self.guessed_letters.append(hint_letter)
            
            self.update_word_display()
            self.update_used_letters()
            
            if all(l in self.guessed_letters for l in self.secret_word):
                self.root.after(500, self.game_won)
            
            self.hint_button.config(state="disabled")
            self.word_label.config(fg=self.colors["success"])
            self.root.after(500, lambda: self.word_label.config(fg=self.colors["primary"]))
        else:
            messagebox.showinfo("Sem dicas", "Você já descobriu todas as letras!")
    
    def game_won(self):
        """Lida com a vitória do jogador"""
        self.word_label.config(fg=self.colors["success"])
        messagebox.showinfo(
            "Parabéns!", 
            f"Você venceu!\nA palavra era: {self.secret_word}"
        )
        self.start_new_game()
    
    def game_lost(self):
        """Lida com a derrota do jogador"""
        self.word_label.config(fg=self.colors["danger"])
        messagebox.showinfo(
            "Fim de jogo", 
            f"Você perdeu!\nA palavra era: {self.secret_word}"
        )
        self.start_new_game()

if __name__ == "__main__":
    root = tk.Tk()
    game = ResponsiveHangman(root)
    root.mainloop()