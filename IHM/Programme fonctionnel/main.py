import tkinter as tk
from tkinter import ttk
import numpy as np
from random import randint
from plan3D import Map3D

class DroneControlApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CrazyFlie IHM")
        self.geometry("328x363")
        self.drone_data = {}
        colors = [
            "#FF0000",  # Rouge
            "#00FF00",  # Vert
            "#0000FF",  # Bleu
            "#FFFF00",  # Jaune
            "#00FFFF",  # Cyan
            "#FF00FF",  # Magenta
            "#FFA500",  # Orange
            "#800080",  # Violet
            "#A52A2A"   # Marron
            ]
        for i in range(9):
            parametre = {
                "batterie": "??",
                "etat": "déconnecté",
                "signal": "??",
                "moteur":"arrêt",
                "pos": [0, 0, 0],
                "color": colors[i]
            }
            self.drone_data[f"Drone {i+1}"] = parametre
        self.list_connected = []
        self.selected_drone = None
        self.trail_is_active = True
        self.var_coo_x = tk.StringVar()
        self.var_coo_y = tk.StringVar()
        self.var_coo_z = tk.StringVar()
        self.groupe_mode = False
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

        #### Créer l'onglet Connect  ####
        select_tab = ttk.Frame(self.notebook)
        self.notebook.add(select_tab, text="Connect")

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

        ### Créer l'onglet Selection  ####
        info_tab = ttk.Frame(self.notebook)
        self.notebook.add(info_tab, text="Select")

        # Ajouter une liste de drones à l'onglet Infos
        self.drone_list = tk.Listbox(info_tab)
        self.drone_list.grid(column=0, row=0, padx=10, pady=10)

        # Ajouter un événement de liaison à la liste des drones pour détecter les changements de sélection
        self.drone_list.bind("<<ListboxSelect>>", self.event_select_drone)

        # ajout d'une box à droite de la liste
        info_tab_box = tk.Frame(info_tab)
        info_tab_box.grid(column=1, row=0, padx=10, pady=20, sticky='n')

        # Ajouter l'information sur la batterie
        self.etat_label =     tk.Label(info_tab_box, text="Etat : ??")
        self.battery_label =  tk.Label(info_tab_box, text="Batterie : ??")
        self.signal_label =   tk.Label(info_tab_box, text="Signal : ??")
        self.moteur_label =   tk.Label(info_tab_box, text="Moteur : arrêt")
        position_label =      tk.Label(info_tab_box, text="Position:")
        self.position_value_x = tk.Label(info_tab_box, text="x: 0cm")
        self.position_value_y = tk.Label(info_tab_box, text="y: 0cm")
        self.position_value_z = tk.Label(info_tab_box, text="z: 0cm")
        self.etat_label.pack(anchor='w')
        self.battery_label.pack(anchor='w')
        self.signal_label.pack(anchor='w')
        self.moteur_label.pack(anchor='w')
        position_label.pack(anchor='w')
        self.position_value_x.pack(anchor='w')
        self.position_value_y.pack(anchor='w')
        self.position_value_z.pack(anchor='w')

        #### Créer l'onglet position ####
        pos_tab = ttk.Frame(self.notebook)
        self.notebook.add(pos_tab, text="Position")

        # Frame pour les boutons directionnels
        frame_left = tk.Frame(pos_tab, bg="light blue", width=130, height=254)
        frame_left.grid(column=0, row=0, padx=18, pady=10)
        frame_left.pack_propagate(0)

        pos_label = tk.Label(frame_left, text="Plan 3D", font=("Arial", 13), bg='#3FAADF')
        pos_label.pack(pady=3)

        # bouton plan 3D
        plt_button = tk.Button(frame_left, text="Ouvrir",command=self.open3D, width=8, height=1)
        plt_button.pack()

        # button clear trail
        self.trail_button = tk.Button(frame_left, text="Trace OFF",command=self.trail_on_off, width=8, height=1)
        self.trail_button.pack(pady=2)

        drone_label_title = tk.Label(frame_left, text="Légendes", font=("Arial", 13), bg='#3FAADF')
        drone_label_title.pack(pady=4)

        drone_label_frame = tk.Frame(frame_left)
        drone_label_frame.pack()

        # frame des drones connecté
        frame_connected_drone = tk.Frame(frame_left, bg="light blue")
        frame_connected_drone.pack()
        self.legend_label = []
        for name, data in self.drone_data.items():
            self.legend_label.append(tk.Label(frame_connected_drone, text=name, bg=data["color"]))
        # dexieme partie (droite) de la fenêtre
        frame_right = tk.Frame(pos_tab, bg="light blue", width=130, height=254)
        frame_right.grid(column=1, row=0, padx=10, pady=10)

        frame_right.pack_propagate(0)

        pos_label = tk.Label(frame_right, text="Coordonnées", font=("Arial", 13), bg='#3FAADF')
        pos_label.pack(pady=3)

        frame_xyz_set = tk.Frame(frame_right)
        frame_xyz_set.pack(pady=3)
        # entrée coordonnées x
        frame_x_live = tk.Frame(frame_xyz_set)
        frame_x_live.pack()
        tk.Label(frame_x_live, text="X", font=("Arial", 14)).pack(side="left")
        entry_posx = tk.Entry(frame_x_live, width=6, textvariable=self.var_coo_x)
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

        valide_coo_button = tk.Button(frame_right, text="Valider", command=self.valide_coo, bg="light green")
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
        self.lift_button  = tk.Button(direction_frame, text="Décollage", command=self.lift_off, width=button_width, height=button_height, bg='red')
        up_button         = tk.Button(direction_frame, text="Haut", command=self.up, width=button_width, height=button_height, bg='light blue')
        backward_button   = tk.Button(direction_frame, text="Bas", command=self.down, width=button_width, height=button_height, bg='light blue')
        left_button       = tk.Button(direction_frame, text="Gauche", command=self.left, width=button_width, height=button_height, bg='light green')
        forward_button    = tk.Button(direction_frame, text="Avant", command=self.forw, width=button_width, height=button_height, bg='light green')
        right_button      = tk.Button(direction_frame, text="Droite", command=self.right, width=button_width, height=button_height, bg='light green')
        down_button       = tk.Button(direction_frame, text="Arrière", command=self.backw, width=button_width, height=button_height, bg='light green')
        self.solo_button  = tk.Button(direction_frame, text="Solo", command=self.solo_groupe, width=button_width, height=button_height, bg='light yellow')
        up_button       .grid(row=0, column=1, padx=5, pady=5)
        backward_button .grid(row=0, column=2, padx=5, pady=5)
        left_button     .grid(row=1, column=0, padx=5, pady=5, rowspan=2)
        right_button    .grid(row=1, column=2, padx=5, pady=5, rowspan=2)
        forward_button  .grid(row=1, column=1, padx=5, pady=5)
        down_button     .grid(row=2, column=1, padx=5, pady=5)
        self.lift_button.grid(row=0, column=0, padx=5, pady=5)
        self.solo_button.grid(row=3, column=2, padx=5, pady=5)
    def event_select_drone(self, event):
        # on vérifie d'abord que l'onglet actif est bien le 2eme, et qu'au moins 1 drone est sélectionné 
        if self.notebook.index(self.notebook.select()) == 1 and self.is_check():
            self.selected_drone = self.drone_list.get(self.drone_list.curselection())
            self.update_drone_info()
            self.update_decollage_info()
            self.log_message(self.selected_drone+" sélectionné")
    def update_drone_info(self):
        self.drone_list.selection_anchor(0)
        self.etat_label.config(text="Etat : "+self.drone_data[self.selected_drone]["etat"])
        self.battery_label.config(text="Batterie: "+str(self.drone_data[self.selected_drone]["batterie"])+"%")
        self.signal_label.config(text="Signal: "+str(self.drone_data[self.selected_drone]["signal"]))
        self.moteur_label.config(text="Moteur: "+str(self.drone_data[self.selected_drone]["moteur"]))
        x, y, z = [axe for axe in self.drone_data[self.selected_drone]["pos"]]
        self.position_value_x.config(text=f"x: {x}cm")
        self.position_value_y.config(text=f"y: {y}cm")
        self.position_value_z.config(text=f"z: {z}cm")
    def up(self):
        self.create_move("haut", [0, 0, 1])
    def down(self):
        self.create_move("bas", [0, 0, -1])
    def left(self):
        self.create_move("gauche", [-1, 0, 0])
    def right(self):
        self.create_move("droit", [1, 0, 0])
    def forw(self):
        self.create_move("avant", [0, 1, 0])
    def backw(self):
        self.create_move("arrière", [0, -1, 0])
    def create_move(self, direction, matrice):
        if self.groupe_mode:
            if len(self.list_connected):
                self.move_drone(matrice, self.list_connected)
                self.log_message("Déplacement "+direction, "info")
            else:
                self.log_message("Aucun drone connecté...", "error")
        else:
            if self.selected_drone:
                if self.drone_data[self.selected_drone]["moteur"] == "en vol":
                    used = self.selected_drone
                    self.move_drone(matrice, [used])
                    self.update_drone_info()
                    self.log_message(f"Déplacement {used} {direction}", "info")
                    self.log_message(f"Nouvelle position {self.drone_data[used]['pos']}")
                else:
                   self.log_message("Décollage requis...", "error")
            else:
                self.log_message("Aucun drone sélectionné...", "error")
    def move_drone(self, matrice, move_list):
        for drone in move_list:
            if self.drone_data[drone]["moteur"] == "en vol":
                matrice_drone = np.array(self.drone_data[drone]["pos"])
                matrice_move = np.array(matrice)
                # On se déplace de 10 cm par axe
                self.drone_data[drone]["pos"] = matrice_drone+matrice_move*10
        plan3D.update_drone_position()
    def solo_groupe(self):
        if self.groupe_mode:
            self.groupe_mode = False
            self.selected_drone = None
            self.solo_button.config(text="Solo", bg="light yellow")
            self.log_message("Seul le drone sélectionné se déplace", "warn")
        else:
            self.groupe_mode = True
            self.selected_drone = None
            self.solo_button.config(text="Groupe", bg="yellow")
            self.log_message("Tous les drones connectés se déplaces ensembles", "warn")
    def lift_off(self):
        if not self.groupe_mode:
            if self.selected_drone:
                if self.drone_data[self.selected_drone]["etat"] == "connecté":
                    if self.drone_data[self.selected_drone]["moteur"] == "en vol":
                        self.log_message("Atterrissage !", "warn")
                        self.drone_data[self.selected_drone]["moteur"] = "arrêt"
                        self.drone_data[self.selected_drone]["pos"][2] = 0
                    else:
                        self.log_message("Décollage !", "warn")
                        self.drone_data[self.selected_drone]["moteur"] = "en vol"
                    self.update_decollage_info()
                    self.update_drone_info()
                    plan3D.update_drone_position()
                else:
                    self.log_message("Le drone sélectionné est déconnecté !", "error")
            else:
                self.log_message("Aucun drone sélectionné !", "error")
        else:
            self.log_message("Impossible avec un groupe de drone !", "error")
    def update_decollage_info(self):
        if self.drone_data[self.selected_drone]["moteur"] == "en vol":
            self.lift_button.config(text="Atterrissage", bg="green")
        else:
            self.lift_button.config(text="Décollage", bg="red")
    def drone_connect(self):
        if self.is_check():
            total_check = 0
            for name in self.drone_check:
                if self.drone_check[name].get():
                    total_check += 1
                    self.drone_data[name]["etat"]   = "connecté"
                    self.drone_data[name]["batterie"] = randint(10, 100)
                    self.drone_data[name]["signal"] = ["médiocre", "mauvais", "moyen", "bon", "parfait"][randint(0, 4)]
            self.count_connected()
            self.show_legend_drone()
            plan3D.update_drone_show()
            self.log_message(f"{total_check} drones ont été connectés")
            self.selected_drone = None
        else:
            self.log_message("Aucun drones sélectionnés", "error")
    def drone_disconnect(self):
        if self.is_check():
            total_check = 0
            # je veux mourir 
            for name in self.drone_check:
                if self.drone_check[name].get():
                    total_check += 1
                    self.drone_data[name]["etat"] = "déconnecté"
                    self.drone_data[name]["batterie"] = "??"
                    self.drone_data[name]["signal"] = "??"
            self.count_connected()
            plan3D.update_drone_show()
            self.log_message(f"{total_check} drones ont été déconnectés")
            self.show_legend_drone()
            self.selected_drone = None
        else:
            self.log_message("Aucun drones sélectionnés", "error")
    def count_connected(self):
        self.list_connected = []
        for drone in self.drone_data.keys():
            if self.drone_data[drone]["etat"] == "connecté":
                self.list_connected.append(drone)
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
    def show_legend_drone(self):
        self.hide_legend_drone()
        i = 0
        for label_name in self.legend_label:
            if label_name.cget("text") in self.list_connected:
                if i < 5:
                    label_name.grid(column=0, row=i)
                else:
                    label_name.grid(column=1, row=i-5)
                i += 1
    def hide_legend_drone(self):
        for label in self.legend_label:
            label.grid_forget()
    def update_use_drone(self):
        self.selected_drone = None
        self.drone_list.delete(0, tk.END)
        for name in self.drone_check:
            if self.drone_check[name].get():
                self.drone_list.insert(tk.END, name)
    def valide_coo(self):
        try:
            set_position = [0]*3
            set_position[0] = int(self.var_coo_x.get())
            set_position[1] = int(self.var_coo_y.get())
            set_position[2] = int(self.var_coo_z.get())
            if len(self.list_connected) and self.selected_drone:
                if self.drone_data[self.selected_drone]["etat"] == "connecté":
                    if self.drone_data[self.selected_drone]["moteur"] == "en vol":
                        self.drone_data[self.selected_drone]["pos"] = set_position
                        self.log_message("nouvelle position "+str(set_position), 'info')
                        self.update_drone_info()
                        plan3D.update_drone_position()
                    else:
                        self.log_message("Décollage requis !", "error")
                else:
                    self.log_message("Le drone sélectionné est déconnecté !", "error")
            else:
                self.log_message("Connexion ou sélection manquante !", "error")
        except:
                self.log_message("coordonées non valide", "error")
    def open3D(self):
        self.log_message("ouverture de matplotlib...")
        plan3D.show_plan()
    def trail_on_off(self):
        # self.log_message("Supression des traces...")
        if self.trail_is_active:
            plan3D.clear_trail()
            self.trail_is_active = False
            self.trail_button.config(text="Trace ON")
            self.log_message("Les traces sont désactivés", "info")
        else:
            self.trail_is_active = True
            self.trail_button.config(text="Trace OFF")
            self.log_message("Les traces sont activés", "info")
        
    def log_message(self, message, level="info"):
        self.log_text.insert(tk.END, "\n["+level+"]", level)
        self.log_text.insert(tk.END, message)
        self.log_text.see(tk.END)

if __name__ == "__main__":
    app = DroneControlApp()
    plan3D = Map3D(app)
    app.mainloop()


# si un drone va en dehors de la zone mettre un warn
# à faire : 
# gérer le select lors du premier démarrage [OK]
# commencer a edit les positions sur matplot
#   -> plot les drones connectés 
#   -> possible de déplot un point ???
#   -> gérer quelle drone est touché dans l'onglet conntrôle...