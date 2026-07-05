import tkinter as tk
from tkinter import ttk
from datetime import datetime

from generated_protocol import ReceiverAck, SensorReading


class SensorReceiverApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Sensor to Receiver")
        self.root.geometry("560x360")
        self.root.configure(bg="#0b1f4a")

        self.status_var = tk.StringVar(value="Oczekuje na pomiar...")

        title = ttk.Label(
            root,
            text="FC Barcelona Sensor Live",
            font=("Segoe UI", 16, "bold"),
            foreground="#f4d35e",
            background="#0b1f4a",
        )
        title.pack(pady=(14, 4))

        subtitle = ttk.Label(
            root,
            text="Czujnik → Odbiornik",
            font=("Segoe UI", 11, "bold"),
            foreground="#a50044",
            background="#0b1f4a",
        )
        subtitle.pack(pady=(0, 8))

        status_frame = ttk.Frame(root, padding=10)
        status_frame.pack(fill="x", padx=16)
        status_frame.configure(style="Barca.TFrame")

        ttk.Label(
            status_frame,
            textvariable=self.status_var,
            font=("Segoe UI", 10, "bold"),
            foreground="#0b1f4a",
            background="#f4d35e",
        ).pack(fill="x")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Barca.TFrame", background="#f4d35e")
        style.configure("Barca.TButton", foreground="#ffffff", background="#a50044")
        style.map("Barca.TButton", background=[("active", "#d4004b")])
        style.configure("Barca.TLabel", background="#0b1f4a")

        ttk.Button(
            root,
            text="Wygeneruj pomiar",
            style="Barca.TButton",
            command=self.send_sample,
        ).pack(pady=10)

        frame = ttk.Frame(root, padding=10)
        frame.pack(fill="both", expand=True, padx=16, pady=(0, 12))
        frame.configure(style="Barca.TFrame")

        ttk.Label(frame, text="Log transmisji", foreground="#0b1f4a", background="#f4d35e", font=("Segoe UI", 10, "bold")).pack(anchor="w")
        log_widget = tk.Text(frame, height=10, width=60, bg="#fef8d8", fg="#0b1f4a", insertbackground="#0b1f4a")
        log_widget.pack(fill="both", expand=True, pady=(4, 0))
        log_widget.configure(state="disabled")
        self.log_widget = log_widget

    def append_log(self, message: str) -> None:
        self.log_widget.configure(state="normal")
        self.log_widget.insert(tk.END, message + "\n")
        self.log_widget.see(tk.END)
        self.log_widget.configure(state="disabled")

    def send_sample(self) -> None:
        reading = build_sample_reading()
        self.status_var.set(f"Wysyłam: {reading.sensor_id} | {reading.temperature_c:.1f} C")
        self.append_log(format_log_entry("send", f"Sensor {reading.sensor_id} wysyła pomiar"))

        ack = ReceiverAck(receiver_id="RX-01", status_code=0, message="Pomiar odebrany")
        self.append_log(format_log_entry("receive", f"Odbiornik: {ack.message}"))
        self.status_var.set("Pomyślnie odebrano pomiar")


def build_sample_reading() -> SensorReading:
    return SensorReading(
        sensor_id="S-001",
        location="Greenhouse-A",
        temperature_c=23.7,
        humidity_pct=61.2,
        timestamp=0,
        battery_pct=82,
    )


def format_log_entry(kind: str, message: str) -> str:
    now = datetime.now().strftime("%H:%M:%S")
    return f"[{now}] {kind}: {message}"


def main() -> None:
    root = tk.Tk()
    app = SensorReceiverApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
