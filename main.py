# main.py
import tkinter as tk
from tkinter import filedialog, messagebox
from wiper import wipe_multiple_files  # import backend function

class SecureDataWiperGUI:
    def __init__(self, master):
        self.master = master
        master.title("🛡️ Secure Data Wiper")
        master.geometry("500x400")

        self.files = []

        tk.Label(master, text="Secure Data Wiper", font=("Arial", 16, "bold")).pack(pady=10)
        tk.Button(master, text="Select Files", command=self.select_files).pack(pady=5)

        self.file_listbox = tk.Listbox(master, width=60, height=6)
        self.file_listbox.pack(pady=5)

        tk.Label(master, text="Overwrite Passes:").pack()
        self.passes_entry = tk.Entry(master)
        self.passes_entry.insert(0, "3")
        self.passes_entry.pack(pady=5)

        tk.Button(master, text="Start Wiping", command=self.start_wiping).pack(pady=10)

        tk.Label(master, text="Logs:").pack()
        self.log_text = tk.Text(master, width=60, height=10)
        self.log_text.pack(pady=5)

    def select_files(self):
        files = filedialog.askopenfilenames(title="Select files to wipe")
        self.files = list(files)
        self.file_listbox.delete(0, tk.END)
        for f in self.files:
            self.file_listbox.insert(tk.END, f)

    def start_wiping(self):
        try:
            passes = int(self.passes_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Passes must be an integer")
            return

        if not self.files:
            messagebox.showerror("Error", "No files selected")
            return

        self.log_text.insert(tk.END, f"Starting wipe for {len(self.files)} files...\n")
        self.master.update()

        # Call backend function
        wipe_multiple_files(self.files, passes)

        self.log_text.insert(tk.END, "✅ Wipe completed. See wipe_log.txt for details.\n")
        messagebox.showinfo("Success", "Wiping completed!")

if __name__ == "__main__":
    root = tk.Tk()
    app = SecureDataWiperGUI(root)
    root.mainloop()
