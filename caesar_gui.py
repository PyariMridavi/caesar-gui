#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk

ALPHABET = "abcdefghijklmnopqrstuvwxyz"


def shift_text(message, key):
    result = []
    for char in message:
        lower = char.lower()
        if lower in ALPHABET:
            new_char = ALPHABET[(ALPHABET.index(lower) + key) % len(ALPHABET)]
            result.append(new_char.upper() if char.isupper() else new_char)
        else:
            result.append(char)
    return "".join(result)


class CaesarApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Caesar Cipher")
        self.geometry("520x460")
        self.minsize(400, 380)

        self.mode = tk.StringVar(value="encrypt")
        self.key = tk.IntVar(value=3)

        main = ttk.Frame(self, padding=12)
        main.pack(fill="both", expand=True)

        ttk.Label(main, text="Input").pack(anchor="w")
        self.input_box = tk.Text(main, height=7, wrap="word")
        self.input_box.pack(fill="both", expand=True, pady=(2, 10))

        controls = ttk.Frame(main)
        controls.pack(fill="x", pady=(0, 10))

        ttk.Label(controls, text="Key:").pack(side="left")
        ttk.Spinbox(
            controls, from_=-25, to=25, width=5,
            textvariable=self.key, command=self.update_output,
        ).pack(side="left", padx=(4, 16))

        ttk.Radiobutton(
            controls, text="Encrypt", value="encrypt",
            variable=self.mode, command=self.update_output,
        ).pack(side="left")
        ttk.Radiobutton(
            controls, text="Decrypt", value="decrypt",
            variable=self.mode, command=self.update_output,
        ).pack(side="left", padx=(8, 0))

        ttk.Label(main, text="Output").pack(anchor="w")
        self.output_box = tk.Text(main, height=7, wrap="word", state="disabled")
        self.output_box.pack(fill="both", expand=True, pady=(2, 10))

        buttons = ttk.Frame(main)
        buttons.pack(fill="x")
        ttk.Button(buttons, text="Copy output", command=self.copy_output).pack(side="left")
        ttk.Button(buttons, text="Use output as input", command=self.swap).pack(side="left", padx=8)
        ttk.Button(buttons, text="Clear", command=self.clear).pack(side="left")

        self.status = ttk.Label(main, text="", foreground="gray")
        self.status.pack(anchor="w", pady=(8, 0))

        self.input_box.bind("<<Modified>>", self.on_text_modified)
        self.key.trace_add("write", lambda *_: self.update_output())

    def on_text_modified(self, event=None):
        if self.input_box.edit_modified():
            self.update_output()
            self.input_box.edit_modified(False)

    def get_key(self):
        try:
            return self.key.get()
        except tk.TclError:
            return None

    def update_output(self):
        key = self.get_key()
        if key is None:
            self.status.config(text="Key must be a whole number.")
            return
        self.status.config(text="")

        text = self.input_box.get("1.0", "end-1c")
        if self.mode.get() == "decrypt":
            key = -key
        result = shift_text(text, key)

        self.output_box.config(state="normal")
        self.output_box.delete("1.0", "end")
        self.output_box.insert("1.0", result)
        self.output_box.config(state="disabled")

    def copy_output(self):
        self.clipboard_clear()
        self.clipboard_append(self.output_box.get("1.0", "end-1c"))
        self.status.config(text="Copied to clipboard.")

    def swap(self):
        result = self.output_box.get("1.0", "end-1c")
        self.input_box.delete("1.0", "end")
        self.input_box.insert("1.0", result)
        self.mode.set("decrypt" if self.mode.get() == "encrypt" else "encrypt")
        self.update_output()

    def clear(self):
        self.input_box.delete("1.0", "end")
        self.update_output()


if __name__ == "__main__":
    CaesarApp().mainloop()
