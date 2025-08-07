import tkinter as tk
from tkinter import ttk
import calculate
from constants import CONSTANTS
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import MultipleLocator
import numpy as np


class DataFrameApp(tk.Frame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.parent.geometry('500x250')
        self.parent.title("PyTunnel by PlatonRaz")

        self._build_ui()

    def _build_ui(self):
        self._build_controls()
        self._build_slider()

    def _build_controls(self):
        self.button_frame = tk.Frame(self.parent)
        self.button_frame.pack(pady=20)

        self.button_tunnel = tk.Button(
            self.button_frame, 
            text="Run by Tunnel Length", 
            command=self.open_tunnel_window
        )
        self.button_tunnel.pack(side=tk.LEFT, padx=10)

        self.use_subplots = tk.BooleanVar(value=False)  # default to single plot

        self.checkbox_subplots = tk.Checkbutton(
            self.button_frame,
            text="Show 2x2 Subplots",
            variable=self.use_subplots
        )
        self.checkbox_subplots.pack(side=tk.LEFT, padx=10)


        self.button_air_vel = tk.Button(
            self.button_frame, 
            text="Run by Air Velocity", 
            command=self.open_air_vel_window
        )
        self.button_air_vel.pack(side=tk.LEFT, padx=10)

    def _build_slider(self):
        self.slider_label = tk.Label(self.parent, text="Max Tunnel Length (m):")
        self.slider_label.pack()

        self.slider_tunnel = tk.Scale(
            self.parent, from_=0, to=10000, orient=tk.HORIZONTAL,
            resolution=100, length=300
        )
        self.slider_tunnel.pack(pady=10)

        self.info_label = tk.Label(
            self.parent,
            text="Note: 'Iterate Air Velocity' uses default mean air velocity\nof 2.0 m/s as defined in constants.py",
            font=("Arial", 9),
            justify="center"
        )
        self.info_label.pack(pady=5)

    def _display_data(self, df, title):
        new_window = tk.Toplevel(self.parent)
        new_window.geometry('1200x700')
        new_window.title(title)
        
        # Create a frame for the table
        table_frame = tk.Frame(new_window)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create a treeview widget for the table
        tree = ttk.Treeview(table_frame)
        tree["columns"] = list(df.columns)
        tree["show"] = "headings"
        
        # Add columns
        for col in df.columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor=tk.CENTER)
        
        # Add data rows
        for i, row in df.iterrows():
            tree.insert("", tk.END, values=list(row))
        
        # Add scrollbars
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        # Grid layout
        tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        
        # Configure grid weights
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        # Create a frame for the plot
        plot_frame = tk.Frame(new_window)
        plot_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create matplotlib figure
        if self.use_subplots.get():
            fig, axs = plt.subplots(2, 2, figsize=(15, 10))
            axs = axs.flatten()

            # Define unique colours (customise as needed)
            colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red']

            x = df.iloc[:, 0]
            for i, col in enumerate(df.columns[1:]):
                ax = axs[i]
                y = df[col]
                ax.plot(x, y, marker='o', linestyle='-', linewidth=1.5, color=colors[i], label=col)
                ax.set_title(col, fontsize=12)
                ax.set_xlabel(df.columns[0])
                ax.set_ylabel("Temperature (°C)")
                ax.legend()
                ax.grid(True)
                ax.yaxis.set_major_locator(MultipleLocator(2))
                ax.yaxis.set_minor_locator(MultipleLocator(1))
                ax.tick_params(axis='both', which='major', labelsize=10)

           

        else:
            fig, ax = plt.subplots(figsize=(15, 8))
            x = df.iloc[:, 0]
            for col in df.columns[1:]:
                y = df[col]
                ax.plot(x, y, marker='o', linestyle='-', linewidth=1.5, label=col)
            ax.set_xlabel(df.columns[0], fontsize=12)
            ax.set_ylabel("Temperature (°C)", fontsize=12)
            ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)
            ax.set_title(title, fontsize=14)
            all_y = np.concatenate([df[col].values for col in df.columns[1:]])
            y_min = np.floor(all_y.min())
            y_max = np.ceil(all_y.max())
            if (y_max - y_min) < 10:
                center = (y_max + y_min) / 2
                y_min = center - 5
                y_max = center + 5
            ax.set_ylim(y_min, y_max)
            ax.yaxis.set_major_locator(MultipleLocator(2))
            ax.yaxis.set_minor_locator(MultipleLocator(1))
            ax.grid(True, which='major', linestyle='-', linewidth=0.7, alpha=0.7)
            ax.grid(True, which='minor', linestyle=':', linewidth=0.5, alpha=0.4)

        fig.tight_layout()



        
        # Embed the plot in the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def open_tunnel_window(self):
        max_length = self.slider_tunnel.get()
        df = calculate.iterate_tunnel_length(max_length)
        self._display_data(df, "Temperature vs Tunnel Length")

    def open_air_vel_window(self):
        df = calculate.iterate_air_vel()
        self._display_data(df, "Temperature vs Air Velocity")


if __name__ == "__main__":
    root = tk.Tk()
    app = DataFrameApp(parent=root)
    root.mainloop()