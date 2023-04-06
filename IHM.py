import tkinter as tk
from tkinter import ttk
from random import randint

class DroneControlApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Drone Control")
        self.geometry("328x350")
        self.drone_data = {}
        for i in range(9):
            dict = {
                "batterie":randint(0, 100),
                "etat": "déconnecté",
                "signal":0
            }
            self.drone_data[f"Drone {i+1}"] = dict
        self.var_coo_x = tk.StringVar()
        self.var_coo_y = tk.StringVar()
        self.var_coo_z = tk.StringVar()
        self.create_widgets()
        
    def create_widgets(self):
        # Créer un widget Notebook pour les onglets
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)

        #### Créer l'onglet Select ####

        select_tab = ttk.Frame(self.notebook)
        self.notebook.add(select_tab, text="Select")

        select_title = tk.Label(select_tab, text="Sélection drones", font=("Arial", 12), bg='#3FAADF')
        select_title.grid(column=0, row=0, padx=10, pady=5)
        # Ajouter un Frame pour contenir les check boxes

        check_boxes_frame = ttk.Frame(select_tab)
        check_boxes_frame.grid(column=0, row=1)

        # Créer et ajouter des check boxes pour chaque drone
        self.drone_check = {}
        for name in self.drone_data:
            drone_var = tk.BooleanVar()
            drone_check_box = ttk.Checkbutton(
                check_boxes_frame,
                text=name,
                variable=drone_var,
                command=self.update_use_drone)
            drone_check_box.pack()
            self.drone_check[name] = drone_var

        #### Créer l'onglet Infos  ####
        info_tab = ttk.Frame(self.notebook)
        self.notebook.add(info_tab, text="Infos")

        # Ajouter une liste de drones à l'onglet Infos
        self.drone_list = tk.Listbox(info_tab)
        self.drone_list.grid(column=0, row=0, padx=10, pady=10)

        # Ajouter un événement de liaison à la liste des drones pour détecter les changements de sélection
        self.drone_list.bind("<<ListboxSelect>>", self.update_drone_info)

        # ajout d'une box à droite de la liste
        info_tab_box = tk.Frame(info_tab)
        info_tab_box.grid(column=1, row=0, padx=10, pady=40, sticky='n')

        # Ajouter l'information sur la batterie
        self.etat_label = tk.Label(info_tab_box, text="Etat : ??")
        self.battery_label = tk.Label(info_tab_box, text="Batterie : ??")
        self.signal_label = tk.Label(info_tab_box, text="Signal : ??")
        self.etat_label.pack(anchor='w')
        self.battery_label.pack(anchor='w')
        self.signal_label.pack(anchor='w')


        #### Créer l'onglet position ####
        pos_tab = ttk.Frame(self.notebook)
        self.notebook.add(pos_tab, text="Position")

        # Frame pour les boutons directionnels
        frame1 = tk.Frame(pos_tab, bg="light blue", width=130, height=300)
        frame1.grid(column=0, row=0, padx=18, pady=10)
        frame1.pack_propagate(0)

        pos_label = tk.Label(frame1, text="MatPlotLib", font=("Arial", 13), bg='#3FAADF')
        pos_label.pack(pady=3)

        # bouton plan 3D
        plt_button = tk.Button(frame1, text="Plan 3D", width=8, height=2)
        plt_button.pack()

        frame2 = tk.Frame(pos_tab, bg="light blue", width=130, height=300)
        frame2.grid(column=1, row=0, padx=10, pady=10)

        frame2.pack_propagate(0)

        pos_label = tk.Label(frame2, text="Commande", font=("Arial", 13), bg='#3FAADF')
        pos_label.pack(pady=3)

        frame_xyz = tk.Frame(frame2)
        frame_xyz.pack(pady=3)
        # entrée coordonnées x
        frame_x = tk.Frame(frame_xyz)
        frame_x.pack()
        tk.Label(frame_x, text="X", font=("Arial", 14)).pack(side="left")
        entry_posx = tk.Entry(frame_x, width=8, textvariable=self.var_coo_x)
        entry_posx.pack(side="left")
        # entrée coordonnées y
        frame_y = tk.Frame(frame_xyz)
        frame_y.pack()
        tk.Label(frame_y, text="Y", font=("Arial", 14)).pack(side="left")
        entry_posy = tk.Entry(frame_y, width=8, textvariable=self.var_coo_y)
        entry_posy.pack(side="left")
        # entrée coordonnées z
        frame_z = tk.Frame(frame_xyz)
        frame_z.pack()
        tk.Label(frame_z, text="Z", font=("Arial", 14)).pack(side="left")
        entry_posz = tk.Entry(frame_z, width=8, textvariable=self.var_coo_z)
        entry_posz.pack(side="left")

        #### Créer l'onglet Controle ####
        map_tab = ttk.Frame(self.notebook)
        self.notebook.add(map_tab, text="Controle")    

        # Frame pour les boutons directionnels
        direction_frame = tk.Frame(map_tab)
        direction_frame.grid(column=0, row=0, padx=10, pady=10)

        # Paramètres de style pour les boutons
        button_width = 8
        button_height = 2

        # Boutons directionnels
        up_button = tk.Button(direction_frame, text="Haut", command=self.up, width=button_width, height=button_height, bg='gray')
        up_button.grid(row=0, column=1, padx=5, pady=5)

        left_button = tk.Button(direction_frame, text="Gauche", command=self.left, width=button_width, height=button_height, bg='gray')
        left_button.grid(row=1, column=0, padx=5, pady=5)

        forward_button = tk.Button(direction_frame, text="Avant", command=self.forw, width=button_width, height=button_height, bg='gray')
        forward_button.grid(row=1, column=1, padx=5, pady=5)

        right_button = tk.Button(direction_frame, text="Droite", command=self.right, width=button_width, height=button_height, bg='gray')
        right_button.grid(row=1, column=2, padx=5, pady=5)

        down_button = tk.Button(direction_frame, text="Recul", command=self.backw, width=button_width, height=button_height, bg='gray')
        down_button.grid(row=2, column=1, padx=5, pady=5)

        backward_button = tk.Button(direction_frame, text="Bas", command=self.down, width=button_width, height=button_height, bg='gray')
        backward_button.grid(row=3, column=1, padx=5, pady=5)
    
    def update_drone_info(self, event):
        # Exemple de données de batterie pour chaque drone
        selected_drone = self.drone_list.get(self.drone_list.curselection())
        self.etat_label.config(text="Etat : "+self.drone_data[selected_drone]["etat"])
        self.battery_label.config(text="Batterie: "+str(self.drone_data[selected_drone]["batterie"])+"%")
        self.signal_label.config(text="Signal: "+str(self.drone_data[selected_drone]["signal"]))

    # Exemple de fonctions pour les boutons directionnels
    def up(self):
        print("Drone moving up")
    def down(self):
        print("Drone moving down")
    def left(self):
        print("Drone moving left")
    def right(self):
        print("Drone moving right")
    def forw(self):
        print("Drone moving forward")
    def backw(self):
        print("Drone moving backward")

    def update_use_drone(self):
        self.drone_list.delete(0, tk.END)
        for name in self.drone_check:
            if self.drone_check[name].get():
                self.drone_list.insert(tk.END, name)

if __name__ == "__main__":
    app = DroneControlApp()
    app.mainloop()
