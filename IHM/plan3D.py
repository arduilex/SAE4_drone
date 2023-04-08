import matplotlib
# attention, sur linux installer:
# sudo apt-get install python3-pil.imagetk
matplotlib.use('TkAgg') 
import matplotlib.pyplot as plt
import numpy as np

class Map3D():
    def __init__(self, app):
        super().__init__()
        self.coo_drone = app.set_position
        # Coordonnée des 6 balises
        self.coo_balise = {
            "balise1": [-2.45, -3.35, 0],
            "balise2": [-2.45, 2.6, 0],
            "balise3": [2.45, 0, 0],
            "balise4": [2.45, -2.6, 2],
            "balsie5": [-2.45, 0, 2],
            "balise6": [2.45, 3.42 ,2]
        }

    def init_plot(self):
        # Créer une figure et un axe 3D
        self.fig = plt.figure(figsize=(5, 4))
        self.ax = self.fig.add_subplot(111, projection='3d')
        # Conserver le rapport d'aspect égal pour les axes
        self.ax.set_box_aspect([4.9, 6.67, 3])
        # Définir les limites des axes
        self.ax.set_xlim(-2.45, 2.45)
        self.ax.set_ylim(-3.35, 3.42)
        self.ax.set_zlim(0, 2)
        # Étiqueter les axes
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        self.add_balise()
        plt.legend(loc="upper left")

    def add_balise(self):
        for dict in self.coo_balise.items():
            X, Y, Z = [axe for axe in dict[1]]
            if Z==0:
                balise_color='red'
                balise_marker = "^"
            else:
                balise_color="blue"
                balise_marker="v"
            if "balise1"== dict[0]:
                balise_label = "balise sol"
            elif "balise4"== dict[0]:
                balise_label = "balise plafond"
            else:
                balise_label=None
            self.ax.scatter(X, Y, Z, color=balise_color, marker=balise_marker, label=balise_label)
        # affiche un point au milieu 
        self.ax.scatter(0, 0, 0, color='green', marker='x', label="Origine")
    def add_drone(self):
        pass
    def open_plot(self):
        self.init_plot()
        plt.show(block=False)
