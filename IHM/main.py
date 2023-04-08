import tkinter as tk
from tkinter import ttk
from random import randint
from plan3D import Map3D

class DroneControlApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CrayFlie IHM")
        self.geometry("328x363")
        self.drone_data = {}
        for i in range(9):
            dict = {
                "batterie": "??",
                "etat": "déconnecté",
                "signal": "??",
                "pos": [0, 0, 0]
            }
            self.drone_data[f"Drone {i+1}"] = dict
        self.total_connect = 0
        self.var_coo_x = tk.StringVar()
        self.var_coo_y = tk.StringVar()
        self.var_coo_z = tk.StringVar()
        self.set_position = [0]*3
        self.decollage = False
        self.solo_mode = True
        self.create_widgets()

    def create_widgets(self):
        # Créer un widget Notebook pour les onglets
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both") # ,expand=True)
        
        #### créer une frame ne bas our afficher les logs ####
        self.log_frame = tk.Frame(self)
        self.log_frame.pack()
        self.log_text = tk.Text(self.log_frame, wrap=tk.WORD, width=38)
        self.log_text.pack(side="left")
        self.log_text.tag_config('info', foreground="green")
        self.log_text.tag_config('warn', foreground="orange")
        self.log_text.tag_config('error', foreground="red")

        # cré une barre de scroll pour les log
        scrollbar = tk.Scrollbar(self.log_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.log_text.yview)
        self.log_text.insert(tk.END, "[info]", "info")
        self.log_text.insert(tk.END, "Ici, s'affiche les log")



        #### Créer l'onglet Select  ####
        select_tab = ttk.Frame(self.notebook)
        self.notebook.add(select_tab, text="Select")

        # Frame pour les boutons directionnels
        select_frame = tk.Frame(select_tab, bg="light blue", width=130, height=254)
        select_frame.grid(column=0, row=0, padx=18, pady=10)
        select_frame.pack_propagate(0)

        # Créer le titre Sélection
        pos_label = tk.Label(select_frame, text="Sélection", font=("Arial", 13), bg='#3FAADF')
        pos_label.pack(pady=6)

        # Ajouter un Frame pour contenir les check boxes
        check_boxes_frame = tk.Frame(select_frame)
        check_boxes_frame.pack(pady=3)

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

        action_frame = tk.Frame(select_tab, bg="light blue", width=130, height=254)
        action_frame.grid(column=1, row=0, padx=10, pady=10)

        action_frame.pack_propagate(0)

        action_title = tk.Label(action_frame, text="Action", font=("Arial", 13), bg='#3FAADF')
        action_title.pack(pady=6)
        connect_button = tk.Button(action_frame, text="Connecter",command=self.drone_connect, bg="light green")
        connect_button.pack(pady=4)
        disconnect_button = tk.Button(action_frame, text="Déconnecter",command=self.drone_disconnect, bg="#EC7063")
        disconnect_button.pack(pady=4)

        connected_button = tk.Button(action_frame, text="connecté(s)",command=self.select_connect, bg="light blue")
        connected_button.pack(pady=4, side='bottom')
        all_check_button = tk.Button(action_frame, text="TOUT",command=self.select_all, bg="light blue")
        all_check_button.pack(pady=4, side='bottom')

        ### Créer l'onglet Infos  ####
        info_tab = ttk.Frame(self.notebook)
        self.notebook.add(info_tab, text="Infos")

        # Ajouter une liste de drones à l'onglet Infos
        self.drone_list = tk.Listbox(info_tab)
        self.drone_list.grid(column=0, row=0, padx=10, pady=10)

        # Ajouter un événement de liaison à la liste des drones pour détecter les changements de sélection
        self.drone_list.bind("<<ListboxSelect>>", self.update_drone_info)

        # ajout d'une box à droite de la liste
        info_tab_box = tk.Frame(info_tab)
        info_tab_box.grid(column=1, row=0, padx=10, pady=20, sticky='n')

        # Ajouter l'information sur la batterie
        self.etat_label = tk.Label(info_tab_box, text="Etat : ??")
        self.battery_label = tk.Label(info_tab_box, text="Batterie : ??")
        self.signal_label = tk.Label(info_tab_box, text="Signal : ??")
        position_label = tk.Label(info_tab_box, text="Position:")
        self.position_value = tk.Label(info_tab_box, text="x: 0cm\ny: 0cm\nz: 0cm")
        self.etat_label.pack(anchor='w')
        self.battery_label.pack(anchor='w')
        self.signal_label.pack(anchor='w')
        position_label.pack(anchor='w')
        self.position_value.pack(side='left')


        #### Créer l'onglet position ####
        pos_tab = ttk.Frame(self.notebook)
        self.notebook.add(pos_tab, text="Position")

        # Frame pour les boutons directionnels
        frame1 = tk.Frame(pos_tab, bg="light blue", width=130, height=254)
        frame1.grid(column=0, row=0, padx=18, pady=10)
        frame1.pack_propagate(0)

        pos_label = tk.Label(frame1, text="MatPlotLib", font=("Arial", 13), bg='#3FAADF')
        pos_label.pack(pady=3)

        # bouton plan 3D
        plt_button = tk.Button(frame1, text="Plan 3D",command=self.open3D, width=8, height=2)
        plt_button.pack(pady=3)

        frame2 = tk.Frame(pos_tab, bg="light blue", width=130, height=254)
        frame2.grid(column=1, row=0, padx=10, pady=10)

        frame2.pack_propagate(0)

        pos_label = tk.Label(frame2, text="Coordonnées", font=("Arial", 13), bg='#3FAADF')
        pos_label.pack(pady=3)

        frame_xyz_set = tk.Frame(frame2)
        frame_xyz_set.pack(pady=3)
        # entrée coordonnées x
        frame_x_live = tk.Frame(frame_xyz_set)
        frame_x_live.pack()
        tk.Label(frame_x_live, text="X", font=("Arial", 14)).pack(side="left")
        entry_posx = tk.Entry(frame_x_live, show="12", width=6, textvariable=self.var_coo_x)
        entry_posx.pack(side="left")
        tk.Label(frame_x_live, text="cm", font=("Arial", 10)).pack(side="left")
        # entrée coordonnées y
        frame_y_live = tk.Frame(frame_xyz_set)
        frame_y_live.pack()
        tk.Label(frame_y_live, text="Y", font=("Arial", 14)).pack(side="left")
        entry_posy = tk.Entry(frame_y_live, width=6, textvariable=self.var_coo_y)
        entry_posy.pack(side="left")
        tk.Label(frame_y_live, text="cm", font=("Arial", 10)).pack(side="left")
        # entrée coordonnées z
        frame_z_live = tk.Frame(frame_xyz_set)
        frame_z_live.pack()
        tk.Label(frame_z_live, text="Z", font=("Arial", 14)).pack(side="left")
        entry_posz = tk.Entry(frame_z_live, width=6, textvariable=self.var_coo_z)
        entry_posz.pack(side="left")
        tk.Label(frame_z_live, text="cm", font=("Arial", 10)).pack(side="left")

        valide_coo_button = tk.Button(frame2, text="Valider", command=self.valide_coo, bg="light green")
        valide_coo_button.pack(pady=6)



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
        self.decol_button = tk.Button(direction_frame, text="Décollage", command=self.lift_off, width=button_width, height=button_height, bg='red')
        up_button         = tk.Button(direction_frame, text="Haut", command=self.up, width=button_width, height=button_height, bg='light blue')
        backward_button   = tk.Button(direction_frame, text="Bas", command=self.down, width=button_width, height=button_height, bg='light blue')
        left_button       = tk.Button(direction_frame, text="Gauche", command=self.left, width=button_width, height=button_height, bg='light green')
        forward_button    = tk.Button(direction_frame, text="Avant", command=self.forw, width=button_width, height=button_height, bg='light green')
        right_button      = tk.Button(direction_frame, text="Droite", command=self.right, width=button_width, height=button_height, bg='light green')
        down_button       = tk.Button(direction_frame, text="Arrière", command=self.backw, width=button_width, height=button_height, bg='light green')
        self.solo_button       = tk.Button(direction_frame, text="Solo", command=self.solo_groupe, width=button_width, height=button_height, bg='light yellow')
        self.decol_button.grid(row=0, column=1, padx=5, pady=5)
        up_button.grid(row=0, column=2, padx=5, pady=5)
        backward_button.grid(row=0, column=0, padx=5, pady=5)
        left_button.grid(row=1, column=0, padx=5, pady=5, rowspan=2)
        forward_button.grid(row=1, column=1, padx=5, pady=5)
        right_button.grid(row=1, column=2, padx=5, pady=5, rowspan=2)
        down_button.grid(row=2, column=1, padx=5, pady=5)
        self.solo_button.grid(row=3, column=2, padx=5, pady=5)
    def update_drone_info(self, event):
        # Exemple de données de batterie pour chaque drone
        # on vérifie d'abord que l'onglet actif est bien le 2eme, et qu'au moins 1 dorne est sélectionné 
        if self.notebook.index(self.notebook.select()) == 1 and self.is_check():
            self.selected_drone = self.drone_list.get(self.drone_list.curselection())
            self.drone_list.selection_anchor(0)
            self.etat_label.config(text="Etat : "+self.drone_data[self.selected_drone]["etat"])
            self.battery_label.config(text="Batterie: "+str(self.drone_data[self.selected_drone]["batterie"])+"%")
            self.signal_label.config(text="Signal: "+str(self.drone_data[self.selected_drone]["signal"]))
            x, y, z = [axe for axe in self.drone_data[self.selected_drone]["pos"]]
            self.position_value.config(text=f"x: {x}\n y: {y}\n z: {z}")
            self.log_message(self.selected_drone+" sélectionné")
        elif self.notebook.index(self.notebook.select()) == 1:
            self.selected_drone = None

    def up(self):
        if self.decollage:
            self.log_message("Déplacement vers le haut")
        else:
            self.log_message("Impossible sans décollage", "error")
    def down(self):
        if self.decollage:
            self.log_message("Déplacement vers le bas")
        else:
            self.log_message("Impossible sans décollage", "error")
    def left(self):
        if self.decollage:
            self.log_message("Déplacement à gauche")
        else:
            self.log_message("Impossible sans décollage", "error")
    def right(self):
        if self.decollage:
            self.log_message("Déplacement à droite")
        else:
            self.log_message("Impossible sans décollage", "error")
    def forw(self):
        if self.decollage:
            self.log_message("Déplacement en avant")
        else:
            self.log_message("Impossible sans décollage", "error")
    def backw(self):
        if self.decollage:
            self.log_message("Déplacement en arrière")
        else:
            self.log_message("Impossible sans décollage", "error")
    def solo_groupe(self):
        if self.solo_mode:
            self.solo_mode = False
            self.solo_button.config(text="Groupe", bg="yellow")
            self.log_message("Tous les drones connectés se déplaces ensembles", "warn")
        else:
            self.solo_mode = True
            self.solo_button.config(text="Solo", bg="light yellow")
            self.log_message("Seul le drone sélectionné se déplace", "warn")
    def lift_off(self):
        if self.decollage:
            self.decollage = False
            self.log_message("Atterrissage !", "warn")
            self.decol_button.config(text="Décollage", bg="red")
        elif self.total_connect:
            if not self.solo_mode or self.selected_drone:
                self.decollage = True
                self.log_message("Décollage !", "warn")
                self.decol_button.config(text="Atterrissage", bg="green")
            else:
                self.log_message("Aucun dorne sélectionné !", "error")
        else:
            self.log_message("Aucun drone connecté !", "error")
    def drone_connect(self):
        if self.is_check():
            total_check = 0
            for name in self.drone_check:
                if self.drone_check[name].get():
                    total_check += 1
                    self.drone_data[name]["etat"]   = "connecté"
                    self.drone_data[name]["batterie"] = randint(10, 100)
                    self.drone_data[name]["signal"] = ["médiocre", "mauvais", "moyen", "bon", "parfait"][randint(0, 4)]
            self.total_connect = self.count_connected()
            self.log_message(f"{total_check} drones ont été connectés")
            self.selected_drone = None
        else:
            self.log_message("Aucun drones sélectionnés", "error")
    def drone_disconnect(self):
        if self.is_check():
            total_check = 0
            for name in self.drone_check:
                if self.drone_check[name].get():
                    total_check += 1
                    self.drone_data[name]["etat"] = "déconnecté"
                    self.drone_data[name]["batterie"] = "??"
                    self.drone_data[name]["signal"] = "??"
            self.total_connect = self.count_connected()
            self.log_message(f"{total_check} drones ont été déconnectés")
            self.selected_drone = None
        else:
            self.log_message("Aucun drones sélectionnés", "error")
    def count_connected(self) -> int:
        total = 0
        for drone in self.drone_data.keys():
            if self.drone_data[drone]["etat"] == "connecté":
                total +=1
        return total
    def is_check(self):
        return sum([self.drone_check[name].get() for name in self.drone_check])
    def select_connect(self):
        for name in self.drone_check:
            if self.drone_data[name]["etat"] == "connecté":
                self.drone_check[name].set(True)
            else:
                self.drone_check[name].set(False)
        self.update_use_drone()
    def select_all(self):
        if self.is_check() == len(self.drone_data):
            for name in self.drone_check:
                self.drone_check[name].set(False)
        else:
            for name in self.drone_check:
                self.drone_check[name].set(True)
        self.update_use_drone()
    def update_use_drone(self):
        self.drone_list.delete(0, tk.END)
        for name in self.drone_check:
            if self.drone_check[name].get():
                self.drone_list.insert(tk.END, name)
    def valide_coo(self):
        try:
            self.set_position[0] = int(self.var_coo_x.get())
            self.set_position[1] = int(self.var_coo_y.get())
            self.set_position[2] = int(self.var_coo_z.get())
            self.log_message("nouvelles\ncoordonnées: "+str(self.set_position), 'info')
        except:
            self.log_message("coordonées non valide", "error")
    def open3D(self):
        self.log_message("ouverture de matplotlib...")
        matplotlib.open_plot()
    def log_message(self, message, level="info"):
        self.log_text.insert(tk.END, "\n["+level+"]", level)
        self.log_text.insert(tk.END, message)
        self.log_text.see(tk.END)

if __name__ == "__main__":
    app = DroneControlApp()
    matplotlib = Map3D(app)
    app.mainloop()


# si un drone va en dehors de la zone mettre un warn
# a faire : 
# géré le select lors du premier démarrage [OK]
# commencer a edit les positions sur matplot
#   -> plot les drones connectés 
#   -> possible de déplot un point ???