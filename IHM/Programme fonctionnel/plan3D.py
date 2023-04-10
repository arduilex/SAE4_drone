from mpl_toolkits.mplot3d.art3d import Line3D
import matplotlib.pyplot as plt
import numpy as np

class Map3D():
    def __init__(self, DroneControlApp):
        super().__init__()
        self.droneApp = DroneControlApp
        self.plot_drone = {}
        self.transparent = (0, 0, 0, 0)
        self.is_open = False
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
        self.plan = self.fig.add_subplot(111, projection='3d')
        # pour détecter la fermeture de la fenêtre 
        self.fig.canvas.mpl_connect('close_event', self.on_close)
        # Conserver le rapport d'aspect égal pour les axes
        self.plan.set_box_aspect([4.9, 6.67, 3])
        # Définir les limites des axes
        self.plan.set_xlim(-2.45, 2.45)
        self.plan.set_ylim(-3.35, 3.42)
        self.plan.set_zlim(0, 2)
        # Étiqueter les axes
        self.plan.set_xlabel('X')
        self.plan.set_ylabel('Y')
        self.plan.set_zlabel('Z')
        self.add_balise()
        self.add_drone()
        self.add_drone_trail()
        plt.legend(loc="upper left")
    def show_plan(self):
        self.is_open = True
        self.init_plot()
        self.update_drone_show()
        plt.show(block=False)
    def on_close(self, event):
        self.is_open = False
    def add_balise(self):
        for dict in self.coo_balise.items():
            X, Y, Z = [axe for axe in dict[1]]
            balise_color='#eab65d'
            balise_marker = "1"
            if "balise1"== dict[0]:
                balise_label = "balises" 
            else:
                balise_label=None
            self.plan.scatter(X, Y, Z, color=balise_color, marker=balise_marker, label=balise_label)
        # affiche un point au milieu 
        self.plan.scatter(0, 0, 0, color='green', marker='x', label="origine")
    def add_drone(self):
        self.plot_drone = {}
        for drone_name in self.droneApp.drone_data:
            X, Y, Z = (0, 0, 0)
            self.plot_drone[drone_name] = self.plan.scatter(X, Y, Z, color=self.transparent, marker="o")

    def add_drone_trail(self):
        self.drone_trail = {}
        for drone_name in self.droneApp.drone_data:
            trail_color = self.droneApp.drone_data[drone_name]["color"]
            trail, = self.plan.plot([], [], [], linestyle='--', color=trail_color, linewidth=1, alpha=0.8)
            self.drone_trail[drone_name] = trail
    def update_drone_show(self):
        if self.is_open:
            # on met tous les dornes en transparents
            for drone in self.droneApp.drone_data:
                self.plot_drone[drone].set_color(self.transparent)
            # On affiche les drones connectés
            for drone in self.droneApp.list_connected:
                self.plot_drone[drone].set_color(self.droneApp.drone_data[drone]["color"])
            self.update_drone_position()

    def update_drone_position(self):
        if self.is_open:
            for drone in self.droneApp.list_connected:
                new_pos = [axe/100 for axe in self.droneApp.drone_data[drone]["pos"]]
                x, y, z = new_pos
                self.plot_drone[drone]._offsets3d = [x], [y], [z]
                self.update_drone_trail(drone, new_pos)
                plt.draw()

    def update_drone_trail(self, drone, new_pos):
        if self.droneApp.trail_is_active:
            x_data, y_data, z_data = [data.tolist() for data in self.drone_trail[drone].get_data_3d()]
            new_x, new_y, new_z = new_pos
            x_data.append(new_x)
            y_data.append(new_y)
            z_data.append(new_z)
            self.drone_trail[drone].set_data_3d(np.array(x_data), np.array(y_data), np.array(z_data))
    def clear_trail(self):
        if self.is_open:
            for drone in self.droneApp.list_connected:
                self.drone_trail[drone].set_data_3d([np.array([]) for i in range(3)])
            plt.draw()