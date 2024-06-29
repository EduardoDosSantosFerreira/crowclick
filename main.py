import tkinter as tk
from tkinter import messagebox
import pyautogui
import threading
import keyboard
import time

class AutoClicker:
    def __init__(self, root):
        self.root = root
        self.root.title("Auto Clicker")
        self.root.attributes("-topmost", True)  # Mantém a janela no topo
        
        self.interval = tk.DoubleVar(value=0)  # Intervalo inicial (sem limitação)
        self.targets = []  # Lista de alvos para múltiplos cliques
        self.click_count = 0  # Contador de cliques
        self.running = False
        self.start_time = None
        
        self.create_widgets()
        self.thread = None
        self.update_timer()
        
        # Atalho de teclado para parar o auto-click
        keyboard.add_hotkey('ctrl+shift+s', self.stop_clicking)
        
    def create_widgets(self):
        # Frame para os controles principais
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=10)
        
        # Intervalo entre cliques
        tk.Label(control_frame, text="Intervalo entre cliques (segundos):").grid(row=0, column=0, padx=10, pady=5)
        self.interval_entry = tk.Entry(control_frame, textvariable=self.interval, width=10)
        self.interval_entry.grid(row=0, column=1, padx=10, pady=5)
        
        # Botões de controle
        tk.Button(control_frame, text="Adicionar Alvo", command=self.add_target).grid(row=1, column=0, columnspan=2, padx=10, pady=5)
        
        # Botão para adicionar 5 alvos
        tk.Button(control_frame, text="Inserir 5 Alvos", command=self.add_five_targets).grid(row=2, column=0, columnspan=2, padx=10, pady=5)
        
        self.start_button = tk.Button(control_frame, text="Iniciar", command=self.start_clicking)
        self.start_button.grid(row=3, column=0, padx=10, pady=5)
        
        self.stop_button = tk.Button(control_frame, text="Parar", command=self.stop_clicking, state=tk.DISABLED)
        self.stop_button.grid(row=3, column=1, padx=10, pady=5)
        
        # Botão para limpar alvos
        tk.Button(self.root, text="Limpar Alvos", command=self.clear_targets).pack(pady=10)
        
        # Botão para limpar tempo de execução e resetar contagem de clicks
        tk.Button(self.root, text="Limpar Tempo e Resetar Cliques", command=self.reset_stats).pack(pady=10)
        
        # Informações de execução
        info_frame = tk.Frame(self.root)
        info_frame.pack(pady=10)
        
        tk.Label(info_frame, text="Tempo de Execução:").grid(row=0, column=0, padx=10, pady=5)
        self.timer_label = tk.Label(info_frame, text="0s")
        self.timer_label.grid(row=0, column=1, padx=10, pady=5)
        
        self.target_count_label = tk.Label(info_frame, text="Número de Alvos: 0")
        self.target_count_label.grid(row=1, column=0, columnspan=2, padx=10, pady=5)
        
        tk.Label(info_frame, text="Contagem de Clicks:").grid(row=2, column=0, padx=10, pady=5)
        self.click_count_label = tk.Label(info_frame, text="0")
        self.click_count_label.grid(row=2, column=1, padx=10, pady=5)
    
    def add_target(self):
        messagebox.showinfo("Auto Clicker", "Clique no alvo na tela.")
        self.root.withdraw()  # Esconde a janela principal
        time.sleep(1)  # Dá um tempo para o usuário clicar na tela
        target_position = pyautogui.position()
        self.targets.append((target_position.x, target_position.y))
        self.root.deiconify()  # Mostra a janela principal
        self.show_targets()
        self.update_target_count()
        messagebox.showinfo("Auto Clicker", f"Alvo adicionado com sucesso! Coordenadas: ({target_position.x}, {target_position.y})")
    
    def add_five_targets(self):
        for _ in range(5):
            messagebox.showinfo("Auto Clicker", "Clique no alvo na tela.")
            self.root.withdraw()  # Esconde a janela principal
            time.sleep(1)  # Dá um tempo para o usuário clicar na tela
            target_position = pyautogui.position()
            self.targets.append((target_position.x, target_position.y))
            self.root.deiconify()  # Mostra a janela principal
        
        self.show_targets()
        self.update_target_count()
        messagebox.showinfo("Auto Clicker", "5 Alvos adicionados com sucesso!")
    
    def show_targets(self):
        # Desenha uma área vermelha nos alvos
        for target in self.targets:
            x, y = target
            pyautogui.moveTo(x, y)
            pyautogui.mouseDown()
            pyautogui.moveTo(x + 10, y, duration=0.25)
            pyautogui.moveTo(x, y + 10, duration=0.25)
            pyautogui.moveTo(x - 10, y, duration=0.25)
            pyautogui.moveTo(x, y - 10, duration=0.25)
            pyautogui.moveTo(x, y, duration=0.25)
            pyautogui.mouseUp()
    
    def auto_click(self):
        while self.running:
            for target in self.targets:
                pyautogui.click(target[0], target[1])
                self.click_count += 1
                self.update_click_count()
            time.sleep(self.interval.get())
    
    def start_clicking(self):
        if not self.running and self.targets:
            self.running = True
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.start_time = time.time()
            self.thread = threading.Thread(target=self.auto_click)
            self.thread.start()
    
    def stop_clicking(self):
        if self.running:
            self.running = False
            self.thread.join()
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            messagebox.showinfo("Auto Clicker", "Auto-click interrompido.")
    
    def update_timer(self):
        if self.running and self.start_time:
            elapsed_time = int(time.time() - self.start_time)
            self.timer_label.config(text=f"{elapsed_time}s")
        self.root.after(1000, self.update_timer)
    
    def update_target_count(self):
        count = len(self.targets)
        self.target_count_label.config(text=f"Número de Alvos: {count}")
    
    def update_click_count(self):
        self.click_count_label.config(text=str(self.click_count))
    
    def clear_targets(self):
        self.targets = []
        self.show_targets()
        self.update_target_count()
    
    def reset_stats(self):
        self.start_time = None
        self.click_count = 0
        self.timer_label.config(text="0s")
        self.click_count_label.config(text="0")
    
if __name__ == "__main__":
    root = tk.Tk()
    app = AutoClicker(root)
    root.mainloop()
