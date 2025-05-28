import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
from typing import Callable
from pathlib import Path
from core.downloader import WebsiteDownloader
from .components import ProgressDialog

class WebsiteDownloaderApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.setup_window()
        self.create_widgets()
        self.downloader = WebsiteDownloader(self.update_status)
        
    def setup_window(self):
        self.root.title("Website Downloader")
        self.root.geometry("600x400")
        self.root.minsize(500, 300)
        self.root.iconbitmap(self.find_icon())
        
        style = ttk.Style()
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0')
        
    def find_icon(self):
        icon_paths = [
            Path(__file__).parent.parent / 'assets' / 'icon.ico',
            Path('assets') / 'icon.ico',
            Path('icon.ico')
        ]
        for path in icon_paths:
            if path.exists():
                return str(path)
        return None
        
    def create_widgets(self):
        self.create_header()
        self.create_input_section()
        self.create_progress_section()
        self.create_action_buttons()
        
    def create_header(self):
        header_frame = ttk.Frame(self.root, padding=10)
        header_frame.pack(fill=tk.X)
        
        title = ttk.Label(
            header_frame, 
            text="Website Downloader", 
            font=('Helvetica', 16, 'bold')
        )
        title.pack()
        
        subtitle = ttk.Label(
            header_frame,
            text="Download complete websites with all assets",
            font=('Helvetica', 10)
        )
        subtitle.pack(pady=(0, 10))
        
    def create_input_section(self):
        input_frame = ttk.LabelFrame(
            self.root, 
            text="Website Details", 
            padding=(15, 10)
        )
        input_frame.pack(fill=tk.X, padx=10, pady=5)
        
        url_label = ttk.Label(input_frame, text="Website URL:")
        url_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        self.url_entry = ttk.Entry(
            input_frame, 
            width=50,
            font=('Helvetica', 10)
        )
        self.url_entry.grid(row=0, column=1, padx=5, pady=5)
        
        folder_label = ttk.Label(input_frame, text="Save Folder:")
        folder_label.grid(row=2, column=0, sticky=tk.W, pady=(10, 5))
        
        self.folder_entry = ttk.Entry(
            input_frame, 
            width=50,
            font=('Helvetica', 10)
        )
        self.folder_entry.grid(
            row=3, 
            column=0, 
            sticky=tk.EW, 
            padx=(0, 5))
        
        browse_btn = ttk.Button(
            input_frame, 
            text="Browse", 
            command=self.browse_folder,
            width=10
        )
        browse_btn.grid(row=3, column=1, sticky=tk.E)
        
        input_frame.columnconfigure(0, weight=1)
        
    def create_progress_section(self):
        progress_frame = ttk.LabelFrame(
            self.root, 
            text="Download Progress", 
            padding=(15, 10)
        )
        progress_frame.pack(
            fill=tk.BOTH, 
            expand=True, 
            padx=10, 
            pady=(5, 10))
        
        self.progress_bar = ttk.Progressbar(
            progress_frame, 
            mode='determinate',
            length=100
        )
        self.progress_bar.pack(fill=tk.X, pady=(0, 10))
        
        self.status_label = ttk.Label(
            progress_frame, 
            text="Ready to download",
            wraplength=400,
            justify=tk.LEFT
        )
        self.status_label.pack(fill=tk.X)
        
        self.details_button = ttk.Button(
            progress_frame,
            text="Show Details",
            command=self.show_download_details,
            state=tk.DISABLED
        )
        self.details_button.pack(pady=(10, 0))
        
    def create_action_buttons(self):
        button_frame = ttk.Frame(self.root, padding=10)
        button_frame.pack(fill=tk.X)
        
        self.download_btn = ttk.Button(
            button_frame,
            text="Download Website",
            command=self.start_download,
            style='Accent.TButton'
        )
        self.download_btn.pack(side=tk.RIGHT)
        
        ttk.Button(
            button_frame,
            text="Exit",
            command=self.root.quit
        ).pack(side=tk.RIGHT, padx=5)
        
    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_entry.delete(0, tk.END)
            self.folder_entry.insert(0, folder)
    
    def start_download(self):
        url = self.url_entry.get().strip()
        folder = self.folder_entry.get().strip() or "downloaded_site"
        
        if not url:
            messagebox.showerror("Error", "Please enter a valid website URL")
            return
            
        self.download_btn.config(state=tk.DISABLED)
        self.details_button.config(state=tk.DISABLED)
        self.progress_bar["value"] = 0
        self.status_label.config(text="Preparing download...")
        
        threading.Thread(
            target=self.execute_download,
            args=(url, folder),
            daemon=True
        ).start()
    
    def execute_download(self, url: str, folder: str):
        try:
            success, message = self.downloader.download(url, folder)
            self.root.after(0, self.download_complete, success, message)
        except Exception as e:
            self.root.after(0, self.download_failed, str(e))
    
    def update_status(self, progress: int, message: str):
        self.root.after(0, self._update_ui, progress, message)
    
    def _update_ui(self, progress: int, message: str):
        self.progress_bar["value"] = progress
        self.status_label.config(text=message)
        
    def download_complete(self, success: bool, message: str):
        self.progress_bar["value"] = 100
        self.download_btn.config(state=tk.NORMAL)
        self.details_button.config(state=tk.NORMAL)
        
        if success:
            self.status_label.config(text=f"Success! {message}")
            messagebox.showinfo("Download Complete", message)
        else:
            self.status_label.config(text=f"Error: {message}")
            messagebox.showerror("Download Failed", message)
    
    def download_failed(self, error: str):
        self.download_complete(False, error)
    
    def show_download_details(self):
        ProgressDialog(self.root, "Download Details", self.downloader.get_logs())