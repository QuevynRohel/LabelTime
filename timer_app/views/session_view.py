import tkinter as tk
import time
from controllers.csv_controller import CSVController
from utils.constants import VIEW_MAIN_MENU
from views.navigation import navigate_to
from utils.translations import _

class SessionView:
    def __init__(self, root):
        self.root = root
        self.category = tk.StringVar()
        self.timer_running = False
        self.elapsed_time = 0
        self.is_mini_mode = False  # Flag pour vérifier si on est en mode mini
        self.create_session_view()

    def create_session_view(self):
        self.clear_window()
        self.add_navigation_bar()

        # Style global
        bg_color = "#f5f5f5"
        btn_color = "#4CAF50"
        disabled_btn_color = "#D3D3D3"  # Gris clair pour les boutons désactivés
        self.root.configure(bg=bg_color)

        # Bandeau de message initialement transparent
        self.message_label = tk.Label(self.root, text="", font=("Helvetica", 12), bg=bg_color, fg="black")
        self.message_label.pack(fill="x")

        # Conteneur centré pour les éléments principaux
        self.container = tk.Frame(self.root, bg=bg_color)
        self.container.place(relx=0.5, rely=0.5, anchor="center")

        # Minuterie avec style moderne
        timer_frame = tk.Frame(self.container, bd=2, relief="groove", bg="white", padx=50, pady=10)
        self.timer_label = tk.Label(timer_frame, text="0:00:00", font=("Helvetica", 36, "bold"), fg="#333", bg="white")
        self.timer_label.pack(pady=10)
        timer_frame.pack(pady=(0, 20), fill="x", padx=0, anchor="center")

        # Conteneur pour les boutons Play/Pause et Stop côte à côte avec styles
        button_frame = tk.Frame(self.container, bg=bg_color)
        button_frame.pack(anchor="center")

        self.btn_play_pause = tk.Button(
            button_frame, text=_("\u25B6 Play"), command=self.toggle_timer, state="disabled",
            font=("Helvetica", 14), fg="white", bg=btn_color, activebackground="#45a049",
            relief="flat", width=8, padx=5, pady=5, cursor="hand2", disabledforeground=disabled_btn_color
        )
        self.btn_play_pause.grid(row=0, column=0, padx=(0, 10))

        self.btn_stop = tk.Button(
            button_frame, text=_("\u25A0 Stop"), command=self.stop_timer, state="disabled",
            font=("Helvetica", 14), fg="white", bg="#f44336", activebackground="#e53935",
            relief="flat", width=8, padx=5, pady=5, cursor="hand2", disabledforeground=disabled_btn_color
        )
        self.btn_stop.grid(row=0, column=1)

        # Séparateur
        separator = tk.Frame(self.container, height=1, bd=0, bg="#e0e0e0")
        separator.pack(fill="x", padx=20, pady=(30, 30))

        # Champ "Catégorie"
        tk.Label(self.container, text=_("Catégorie"), font=("Helvetica", 12), bg=bg_color).pack(anchor="center", pady=(20, 5))
        self.category_entry = tk.Entry(self.container, textvariable=self.category, width=50, font=("Helvetica", 12),
                                       relief="flat", highlightthickness=1, highlightbackground="#ccc")
        self.category_entry.pack(pady=5)

        # Activer le bouton Play dès que l'utilisateur tape dans le champ
        self.category_entry.bind("<KeyRelease>", self.check_category_entry)

        # Chargement des boutons de catégories existantes
        self.load_category_buttons(self.container)

        # Champ "Description"
        tk.Label(self.container, text=_("Description"), font=("Helvetica", 12), bg=bg_color).pack(anchor="center", pady=(20, 5))
        self.description_entry = tk.Text(self.container, width=50, height=4, font=("Helvetica", 12),
                                         relief="flat", highlightthickness=1, highlightbackground="#ccc")
        self.description_entry.pack(pady=5)

    def add_navigation_bar(self):
        nav_bar = tk.Frame(self.root, height=40, bg="#e0e0e0")
        nav_bar.pack(fill="x", side="top")

        btn_back = tk.Button(nav_bar, text=_("Retour"), command=lambda: navigate_to(self.root, VIEW_MAIN_MENU),
                             font=("Helvetica", 12), bg="#e0e0e0", relief="flat", activebackground="#dcdcdc",
                             cursor="hand2", highlightthickness=0)
        btn_back.pack(side="right", padx=10, pady=5)

        # Bouton pour changer de mode (fenêtre normale ou mini)
        btn_mini_mode = tk.Button(nav_bar, text=_("Mode Mini"), command=self.toggle_mini_mode,
                                  font=("Helvetica", 12), bg="#e0e0e0", relief="flat", activebackground="#dcdcdc",
                                  cursor="hand2", highlightthickness=0)
        btn_mini_mode.pack(side="left", padx=10, pady=5)

    def load_category_buttons(self, container):
        # Chargement des catégories existantes avec bouton
        controller = CSVController()
        categories_frame = tk.Frame(container, bg="#f5f5f5")
        categories_frame.pack(pady=10)

        for cat in controller.get_categories():
            btn = tk.Button(
                categories_frame, text=cat, command=lambda c=cat: self.select_category(c),
                font=("Helvetica", 10), bg="#ddd", fg="#333", activebackground="#ccc",
                relief="flat", padx=10, pady=5, cursor="hand2"
            )
            btn.pack(side="left", padx=5)

    def select_category(self, category):
        # Sélectionne la catégorie et active le bouton Play
        self.category.set(category)
        self.check_category_entry(None)

    def check_category_entry(self, event):
        # Active le bouton Play dès qu'une catégorie est entrée
        if self.category.get():
            self.btn_play_pause.config(state="normal")
        else:
            self.btn_play_pause.config(state="disabled")

    def toggle_timer(self):
        # Toggle entre Play et Pause
        if not self.timer_running:
            self.start_time = time.time() - self.elapsed_time
            self.update_timer()
            self.timer_running = True
            self.btn_stop.config(state="normal")
            self.btn_play_pause.config(text=_("\u23F8 Pause"))  # Icône Pause
        else:
            self.root.after_cancel(self.timer_update)
            self.timer_running = False
            self.btn_play_pause.config(text=_("\u25B6 Play"))  # Icône Play

    def update_timer(self):
        self.elapsed_time = time.time() - self.start_time
        self.timer_label.config(text=self.format_time(self.elapsed_time))
        self.timer_update = self.root.after(1000, self.update_timer)

    def stop_timer(self):
        if self.timer_running:
            self.root.after_cancel(self.timer_update)
        self.timer_running = False
        description = self.description_entry.get("1.0", tk.END).strip()
        CSVController().save_entry(self.category.get(), description, int(self.elapsed_time))
        # Afficher le message de succès avec les informations réelles de la session
        self.show_message(_("Temps de {time} sur '{category}' enregistré avec succès !").format(
            time=self.format_time(self.elapsed_time), category=self.category.get()), bg_color="#4CAF50")
        self.reset_fields()

    def toggle_mini_mode(self):
        """Basculer entre le mode normal et le mode mini."""
        if self.is_mini_mode:
            # Revenir à la fenêtre normale
            self.root.overrideredirect(False)  # Restaurer les boutons système
            self.root.geometry("800x600")
            self.root.minsize(800, 800)
            self.root.attributes("-topmost", False)
            self.container.pack()  # Restaurer les éléments normaux
            # Supprimer la liaison des événements de déplacement
            self.root.unbind("<Button-1>")
            self.root.unbind("<B1-Motion>")
        else:
            self.root.overrideredirect(True)  # Supprimer les boutons système

            # Passer en mode mini (petite fenêtre au-dessus des autres)
            self.root.geometry("200x50")
            
            self.root.minsize(400, 100)
            self.root.attributes("-topmost", True)  # Toujours au-dessus
            self.container.pack_forget()  # Masquer les éléments de la vue normale
            self.create_mini_view()  # Créer la vue mini
            # Lier les événements pour permettre le déplacement
            self.root.bind("<Button-1>", self.start_move)
            self.root.bind("<B1-Motion>", self.do_move)

        self.is_mini_mode = not self.is_mini_mode

    def create_mini_view(self):
        """Crée la vue mini avec juste le chronomètre et les boutons de contrôle."""
        mini_frame = tk.Frame(self.root, bg="#f5f5f5")
        mini_frame.pack(fill="both", expand=True)

        # Chronomètre affiché
        self.timer_label = tk.Label(mini_frame, text=self.format_time(self.elapsed_time), font=("Helvetica", 18), fg="#333", bg="white")
        self.timer_label.pack(side="left", padx=10)

        # Boutons Play/Pause et Stop en mini mode
        self.btn_play_pause = tk.Button(
            mini_frame, text=_("\u25B6 Play"), command=self.toggle_timer,
            font=("Helvetica", 10), fg="white", bg="#4CAF50", relief="flat", width=6
        )
        self.btn_play_pause.pack(side="left", padx=(10, 5))

        self.btn_stop = tk.Button(
            mini_frame, text=_("\u25A0 Stop"), command=self.stop_timer,
            font=("Helvetica", 10), fg="white", bg="#f44336", relief="flat", width=6
        )
        self.btn_stop.pack(side="left", padx=(5, 10))

        # Catégorie non modifiable dans la vue mini
        category_label = tk.Label(mini_frame, text=self.category.get(), font=("Helvetica", 10), fg="#333", bg="#f5f5f5")
        category_label.pack(side="right", padx=(10, 5))

    def show_message(self, message, bg_color="#ffeb3b"):
        """Affiche un message dans le bandeau avec une couleur de fond."""
        self.message_label.config(text=message, bg=bg_color)
        self.root.after(15000, lambda: self.message_label.config(text="", bg="#f5f5f5"))  # Effacer le message après 15 secondes

    def reset_fields(self):
        self.elapsed_time = 0
        self.timer_label.config(text="0:00:00")
        self.category.set("")
        self.description_entry.delete("1.0", tk.END)
        self.btn_stop.config(state="disabled")
        self.btn_play_pause.config(state="disabled", text=_("\u25B6 Play"))

    def format_time(self, seconds):
        hours, rem = divmod(seconds, 3600)
        minutes, seconds = divmod(rem, 60)
        return f"{int(hours)}:{int(minutes):02}:{int(seconds):02}"

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    def start_move(self, event):
        self.x_offset = event.x
        self.y_offset = event.y

    def do_move(self, event):
        x = self.root.winfo_pointerx() - self.x_offset
        y = self.root.winfo_pointery() - self.y_offset
        self.root.geometry(f"+{x}+{y}")