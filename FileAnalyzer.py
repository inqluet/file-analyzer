import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

COLOR_BG = "#2b2b2b"        
COLOR_PANEL = "#3c3f41"     
COLOR_TEXT = "#ffffff"      
COLOR_ACCENT = "#4a90e2"    
COLOR_ACCENT_HOVER = "#357abd"
COLOR_INPUT = "#4b4b4b"     
COLOR_BORDER = "#555555"

class ModernAnalyzer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("File Analyzer")
        self.geometry("600x650")
        self.configure(bg=COLOR_BG)
        self.resizable(True, True)

        # Setup styles
        self._setup_styles()
        
        # Variables
        self.dir_path = tk.StringVar(value=os.getcwd())
        self.output_name = tk.StringVar(value="files.txt")
        self.limit_val = tk.IntVar(value=0)
        self.use_limit = tk.BooleanVar(value=False)
        
        self.keep_ext = tk.BooleanVar(value=True)
        self.include_folders = tk.BooleanVar(value=False)
        
        self.whitelist_str = tk.StringVar()
        self.blacklist_str = tk.StringVar()

        # Build UI
        self._build_ui()

    def _setup_styles(self):
        style = ttk.Style(self)
        style.theme_use('clam')
        
        style.configure(".", background=COLOR_BG, foreground=COLOR_TEXT, font=("Segoe UI", 11))
        style.configure("TLabel", background=COLOR_BG, foreground="#cccccc")
        style.configure("Header.TLabel", font=("Segoe UI", 14, "bold"), foreground="white")
        
        style.configure("Card.TFrame", background=COLOR_PANEL, relief="flat")
        
        style.configure("Action.TButton", background=COLOR_ACCENT, foreground="white", 
                        font=("Segoe UI", 11, "bold"), borderwidth=0)
        style.map("Action.TButton", background=[("active", COLOR_ACCENT_HOVER)])
        
        style.configure("Browse.TButton", background=COLOR_INPUT, foreground="white", borderwidth=0)
        style.map("Browse.TButton", background=[("active", "#666666")])

        style.configure("TCheckbutton", background=COLOR_PANEL, activebackground=COLOR_PANEL, 
                        foreground="white", font=("Segoe UI", 11))

        style.configure("TEntry", fieldbackground=COLOR_INPUT, foreground="white", 
                        insertcolor="white", borderwidth=0)

    def _build_ui(self):
        main_pad = ttk.Frame(self, padding=25)
        main_pad.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_pad, text="WHERE TO SEARCH?", style="Header.TLabel").pack(anchor="w", pady=(0, 5))
        path_frame = ttk.Frame(main_pad)
        path_frame.pack(fill=tk.X, pady=(0, 20))
        
        entry_path = ttk.Entry(path_frame, textvariable=self.dir_path, font=("Consolas", 10))
        entry_path.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=5, padx=(0, 10))
        
        btn_browse = ttk.Button(path_frame, text="📂 Browse", style="Browse.TButton", command=self.browse)
        btn_browse.pack(side=tk.RIGHT, ipadx=10, ipady=2)

        settings_frame = ttk.Frame(main_pad, style="Card.TFrame", padding=20)
        settings_frame.pack(fill=tk.BOTH, expand=True)

        columns = ttk.Frame(settings_frame, style="Card.TFrame")
        columns.pack(fill=tk.BOTH, expand=True)
        
        col_left = ttk.Frame(columns, style="Card.TFrame")
        col_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        col_right = ttk.Frame(columns, style="Card.TFrame")
        col_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))

        ttk.Label(col_left, text="FILTERS", style="Header.TLabel", background=COLOR_PANEL).pack(anchor="w", pady=(0,15))
        
        ttk.Label(col_left, text="Whitelist (Only these):", background=COLOR_PANEL, font=("Segoe UI", 9)).pack(anchor="w")
        ttk.Entry(col_left, textvariable=self.whitelist_str).pack(fill=tk.X, pady=(0, 10), ipady=3)
        ttk.Label(col_left, text="e.g.: .txt, .py", background=COLOR_PANEL, foreground="#888", font=("Segoe UI", 8)).pack(anchor="w", pady=(0, 10))
        ttk.Label(col_left, text="Blacklist (Exclude these):", background=COLOR_PANEL, font=("Segoe UI", 9)).pack(anchor="w")
        ttk.Entry(col_left, textvariable=self.blacklist_str).pack(fill=tk.X, pady=(0, 5), ipady=3)
        ttk.Label(col_left, text="e.g.: .exe, .tmp", background=COLOR_PANEL, foreground="#888", font=("Segoe UI", 8)).pack(anchor="w")

        ttk.Label(col_right, text="OPTIONS", style="Header.TLabel", background=COLOR_PANEL).pack(anchor="w", pady=(0,15))
        
        ttk.Checkbutton(col_right, text="Keep file extensions", variable=self.keep_ext).pack(anchor="w", pady=2)
        ttk.Checkbutton(col_right, text="Include folders", variable=self.include_folders).pack(anchor="w", pady=2)
        
        limit_frame = ttk.Frame(col_right, style="Card.TFrame")
        limit_frame.pack(anchor="w", pady=(15, 0))
        
        self.chk_limit = ttk.Checkbutton(limit_frame, text="Limit lines:", variable=self.use_limit, command=self.toggle_limit)
        self.chk_limit.pack(side=tk.LEFT)
        self.spin_limit = ttk.Spinbox(limit_frame, from_=1, to=99999, textvariable=self.limit_val, width=8, state="disabled")
        self.spin_limit.pack(side=tk.LEFT, padx=10)

        ttk.Separator(settings_frame, orient='horizontal').pack(fill='x', pady=20)
        
        name_frame = ttk.Frame(settings_frame, style="Card.TFrame")
        name_frame.pack(fill=tk.X)
        ttk.Label(name_frame, text="Output name:", background=COLOR_PANEL).pack(side=tk.LEFT)
        ttk.Entry(name_frame, textvariable=self.output_name, width=25).pack(side=tk.RIGHT, ipady=3)

        btn_run = ttk.Button(main_pad, text="GENERATE LIST", style="Action.TButton", command=self.run_analysis)
        btn_run.pack(fill=tk.X, pady=(20, 0), ipady=10)

    def browse(self):
        d = filedialog.askdirectory()
        if d: self.dir_path.set(d)

    def toggle_limit(self):
        st = "normal" if self.use_limit.get() else "disabled"
        self.spin_limit.config(state=st)

    def parse_list(self, s):
        if not s.strip(): return []
        return [x.strip().lower() for x in s.split(",") if x.strip()]

    def run_analysis(self):
        target_dir = self.dir_path.get()
        out_name = self.output_name.get()
        if not out_name.endswith(".txt"): out_name += ".txt"
        
        whitelist = self.parse_list(self.whitelist_str.get())
        blacklist = self.parse_list(self.blacklist_str.get())
        
        ignore_files = {os.path.basename(__file__), out_name}
        results = []
        
        try:
            items = os.listdir(target_dir)
            
            for item in items:
                full_path = os.path.join(target_dir, item)
                is_file = os.path.isfile(full_path)
                is_dir = os.path.isdir(full_path)

                if is_dir and not self.include_folders.get():
                    continue
                
                if item in ignore_files:
                    continue

                if is_file:
                    _, ext = os.path.splitext(item)
                    ext = ext.lower()
                    
                    if whitelist and ext not in whitelist:
                        continue
                    if blacklist and ext in blacklist:
                        continue

                display_name = item
                if is_file and not self.keep_ext.get():
                     display_name = os.path.splitext(item)[0]

                results.append(display_name)

            results.sort()

            if self.use_limit.get() and self.limit_val.get() > 0:
                results = results[:self.limit_val.get()]

            out_path = os.path.join(target_dir, out_name)
            with open(out_path, "w", encoding="utf-8") as f:
                f.write("\n".join(results))

            messagebox.showinfo("Success", f"Found {len(results)} items.\nSaved to: {out_name}")

        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    app = ModernAnalyzer()
    app.mainloop()