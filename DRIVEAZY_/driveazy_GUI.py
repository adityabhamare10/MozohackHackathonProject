import tkinter as tk
import subprocess
window = tk.Tk()

window.title("Driver Assistance Suite")
window.geometry("500x300")
window.configure(bg="#1C1F33")

text = tk.Label(window, text="Driver Assistance Suite", fg="#8075FF", bg="#1C1F33", font=('Roboto Flex', 15))
text.pack(pady=5)


def button1_clicked():
    subprocess.Popen(["python", "sleep_detection.py"])


def button2_clicked():
    subprocess.Popen(["python", "object_detection.py"])


button1 = tk.Button(window, text="Sleep Detection", font=("Roboto Flex", 10), bg="#9AD4D6", fg="#000", command=button1_clicked)
button1.place(width=500, height=100)
button1.config(width=30, height=2)
button1.pack(pady=10)
button2 = tk.Button(window, text="Object Detection", font=("Roboto Flex", 10), bg="#9AD4D6", fg="#000", command=button2_clicked)
button2.place(width=500, height=100)
button2.config(width=30, height=2)
button2.pack(pady=10)

window.mainloop()