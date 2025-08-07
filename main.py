
from pandastable import Table
import tkinter as tk
import calculate
from constants import CONSTANTS


class DataFrameApp(tk.Frame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.parent.geometry('400x200')
        self.parent.title("PyTunnel by PlatonRaz")

        self._build_ui()

    def _build_ui(self):
        self._build_controls()
        self._build_slider()


    def _build_controls(self):
        self.button_frame = tk.Frame(self.parent)
        self.button_frame.pack(pady=20)

        self.button_tunnel = tk.Button(
            self.button_frame, text="Run by Tunnel Length", command=self.open_tunnel_window
        )
        self.button_tunnel.pack(side=tk.LEFT, padx=10)

        self.button_air_vel = tk.Button(
            self.button_frame, text="Run by Air Velocity", command=self.open_air_vel_window
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


    def open_new_window(self, df, title):
        new_window = tk.Toplevel(self)
        new_window.geometry('800x400')
        new_window.title(title)

        table_frame = tk.Frame(new_window)
        table_frame.pack(fill=tk.BOTH, expand=1)

        table = Table(table_frame, dataframe=df, showtoolbar=True, showstatusbar=True)
        table.rowheight = 50
        table.show()
        table.selectAll()
        table.plotSelected()

    def open_tunnel_window(self):
        max_length = self.slider_tunnel.get()
        df = calculate.iterate_tunnel_length(max_length)
        self.open_new_window(df, "Tunnel Length Data")

    def open_air_vel_window(self):
        df = calculate.iterate_air_vel()
        self.open_new_window(df, "Air Velocity Data")


if __name__ == "__main__":
    root = tk.Tk()
    app = DataFrameApp(parent=root)
    root.mainloop()
