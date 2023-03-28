import tkinter as tk
from tkinter import ttk

class DroneControlApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Drone Control")
        self.geometry("600x450")

        self.create_widgets()

    def create_widgets(self):
        # Créer un widget Notebook pour les onglets
        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=0, column=0)

        # Créer l'onglet Drones
        self.drones_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.drones_tab, text="Drones")

        # Ajouter une liste de drones à l'onglet Drones
        self.drone_list = tk.Listbox(self.drones_tab)
        self.drone_list.pack(side="left", fill="y", padx=10, pady=10)
        self.populate_drone_list()
        
        # Créer l'onglet Map
        self.map_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.map_tab, text="Map 2D")

        # créer un canva pour le contrôle des boutons 
        self.control_canvas = tk.Canvas(self.map_tab, bg="red")
        self.control_canvas.grid(row=0, column=0, rowspan=1)

        # Créer les boutons directionnels
        self.up_button = tk.Button(self.control_canvas, text="  Up  ", command=self.up)
        self.down_button = tk.Button(self.control_canvas, text="Down", command=self.down)
        self.left_button = tk.Button(self.control_canvas, text="Left", command=self.left)
        self.right_button = tk.Button(self.control_canvas, text="Right", command=self.right)

        # Positionner les boutons directionnels
        self.up_button.grid(row=0, column=1)
        self.down_button.grid(row=2, column=1)
        self.left_button.grid(row=1, column=0)
        self.right_button.grid(row=1, column=2)

        # Créer un canvas pour remplacer l'image
        self.map_canvas = tk.Canvas(self.map_tab, width=400, height=400, bg="white")
        self.map_canvas.grid(row=0, column=3, rowspan=3)

    def populate_drone_list(self):
        drones = ["Drone 1", "Drone 2", "Drone 3", "Drone 4", "Drone 5", "Drone 6", "Drone 7", "Drone 8", "Drone 9"]
        for drone in drones:
            self.drone_list.insert(tk.END, drone)

    # Exemple de fonctions pour les boutons directionnels
    def up(self):
        print("Drone moving up")

    def down(self):
        print("Drone moving down")

    def left(self):
        print("Drone moving left")

    def right(self):
        print("Drone moving right")

if __name__ == "__main__":
    app = DroneControlApp()
    app.mainloop()
