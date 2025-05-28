import tkinter as tk
from tkinter import ttk
from typing import List

class ProgressDialog(tk.Toplevel):
    def __init__(self, parent, title: str, messages: List[str]):
        super().__init__(parent)
        self.title(title)
        self.geometry("500x300")
        
        self.text_area = tk.Text(
            self, 
            wrap=tk.WORD, 
            font=('Consolas', 10),
            padx=10,
            pady=10
        )
        self.text_area.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(
            self,
            orient=tk.VERTICAL,
            command=self.text_area.yview
        )
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_area.config(yscrollcommand=scrollbar.set)
        
        for msg in messages:
            self.text_area.insert(tk.END, msg + "\n")
        
        close_btn = ttk.Button(
            self,
            text="Close",
            command=self.destroy
        )
        close_btn.pack(pady=10)
        
        self.text_area.config(state=tk.DISABLED)

class UrlEntry(ttk.Entry):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self._setup_validation()
        
    def _setup_validation(self):
        self.vcmd = (self.register(self._validate_url), '%P')
        self.configure(
            validate='key',
            validatecommand=self.vcmd
        )
        
    def _validate_url(self, text: str) -> bool:
        if not text:
            return True
        return text.startswith(('http://', 'https://'))