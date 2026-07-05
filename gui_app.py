import tkinter as tk
from tkinter import ttk
from datetime import datetime

from generated_protocol import ReceiverAck, SensorReading


class SensorReceiverApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Sensor to Receiver")
        self.root.geometry("520x320")

        self.status_var = tk.StringVar(value="Oczekuje na pomiar...")
        self.log_text = tk.StringVar(value="")

        ttk.Label(root, text="Czujnik -> Odbiornik", font=("Segoe UI", 14, "bold")).pack(pady=(12, 8))

        ttk.Label(root, textvariable=self.status_var, foreground="navy").pack(pady=6)

        ttk.Button(root, text="Wygeneruj pomiar", command=self.send_sample).pack(pady=8)

        frame = ttk.Frame(root, padding=10)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Log:").pack(anchor="w")
        log_widget = tk.Text(frame, height=10, width=60)
        log_widget.pack(fill="both", expand=True)
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
