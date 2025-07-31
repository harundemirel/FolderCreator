
import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import subprocess
import platform

class FolderCreatorApp:
    def __init__(self, master):
        self.master = master
        self.language = "en"
        self.theme = "light"
        self.colors = {
            "light": {"bg": "#f0f0f0", "fg": "#000000", "button_bg": "#4CAF50", "button_fg": "#ffffff"},
            "dark": {"bg": "#2e2e2e", "fg": "#ffffff", "button_bg": "#444444", "button_fg": "#ffffff"}
        }
        self.translations = {
            "en": {
                "destination": "Folder Location:",
                "project_name": "Project Folder Name:",
                "subfolders": "Subfolders:",
                "add": "Add",
                "remove": "Remove",
                "clear": "Clear",
                "create": "Create",
                "success": "Folder structure created successfully.",
                "warning_select": "Please select a destination directory.",
                "warning_name": "Please enter a project folder name.",
                "error": "An error occurred:",
                "add_subfolder": "Subfolder name:",
                "settings": "Settings",
                "language": "Language",
                "theme": "Theme",
                "english": "English",
                "turkish": "Turkish",
                "light": "Light",
                "dark": "Dark"
            },
            "tr": {
                "destination": "Klasör Konumu:",
                "project_name": "Proje Klasör İsmi:",
                "subfolders": "Alt Klasörler:",
                "add": "Ekle",
                "remove": "Sil",
                "clear": "Temizle",
                "create": "Oluştur",
                "success": "Klasör yapısı başarıyla oluşturuldu.",
                "warning_select": "Lütfen hedef klasör seçin.",
                "warning_name": "Lütfen proje klasör ismi girin.",
                "error": "Bir hata oluştu:",
                "add_subfolder": "Alt klasör adı:",
                "settings": "Ayarlar",
                "language": "Dil",
                "theme": "Mod",
                "english": "İngilizce",
                "turkish": "Türkçe",
                "light": "Açık",
                "dark": "Koyu"
            }
        }
        self.build_ui()

    def t(self, key):
        return self.translations[self.language][key]

    def build_ui(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        self.master.configure(bg=self.colors[self.theme]["bg"])
        self.master.geometry("480x450")

        menu = tk.Menu(self.master)
        self.master.config(menu=menu)
        settings_menu = tk.Menu(menu, tearoff=0)
        settings_menu.add_command(label=self.t("language"), command=self.open_language_settings)
        settings_menu.add_command(label=self.t("theme"), command=self.open_theme_settings)
        menu.add_cascade(label=self.t("settings"), menu=settings_menu)

        tk.Label(self.master, text=self.t("destination"), bg=self.colors[self.theme]["bg"], fg=self.colors[self.theme]["fg"]).pack(pady=(10,0))
        frame = tk.Frame(self.master, bg=self.colors[self.theme]["bg"])
        frame.pack(fill="x", padx=10)
        self.dest_var = tk.StringVar()
        tk.Entry(frame, textvariable=self.dest_var).pack(side="left", fill="x", expand=True)
        tk.Button(frame, text="Browse", command=self.browse_dest).pack(side="left", padx=5)

        tk.Label(self.master, text=self.t("project_name"), bg=self.colors[self.theme]["bg"], fg=self.colors[self.theme]["fg"]).pack(pady=(10,0))
        self.name_var = tk.StringVar()
        tk.Entry(self.master, textvariable=self.name_var).pack(fill="x", padx=10)

        tk.Label(self.master, text=self.t("subfolders"), bg=self.colors[self.theme]["bg"], fg=self.colors[self.theme]["fg"]).pack(pady=(10,0))
        self.listbox = tk.Listbox(self.master)
        self.listbox.pack(fill="both", padx=10, pady=(0,5), expand=True)

        btn_frame = tk.Frame(self.master, bg=self.colors[self.theme]["bg"])
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text=self.t("add"), command=self.add_subfolder).pack(side="left", padx=5)
        tk.Button(btn_frame, text=self.t("remove"), command=self.remove_subfolder).pack(side="left", padx=5)
        tk.Button(btn_frame, text=self.t("clear"), command=self.clear_subfolders).pack(side="left", padx=5)

        tk.Button(self.master, text=self.t("create"), command=self.create_structure,
                  bg=self.colors[self.theme]["button_bg"], fg=self.colors[self.theme]["button_fg"]).pack(pady=10)

    def browse_dest(self):
        directory = filedialog.askdirectory()
        if directory:
            self.dest_var.set(directory)

    def add_subfolder(self):
        name = simpledialog.askstring(self.t("add"), self.t("add_subfolder"))
        if name:
            self.listbox.insert("end", name)

    def remove_subfolder(self):
        selection = self.listbox.curselection()
        if selection:
            self.listbox.delete(selection)

    def clear_subfolders(self):
        self.listbox.delete(0, "end")

    def open_language_settings(self):
        lang_window = tk.Toplevel(self.master)
        lang_window.title(self.t("language"))
        lang_window.geometry("200x100")
        tk.Button(lang_window, text=self.t("english"), command=lambda: self.set_language("en", lang_window)).pack(pady=5)
        tk.Button(lang_window, text=self.t("turkish"), command=lambda: self.set_language("tr", lang_window)).pack(pady=5)

    def open_theme_settings(self):
        theme_window = tk.Toplevel(self.master)
        theme_window.title(self.t("theme"))
        theme_window.geometry("200x100")
        tk.Button(theme_window, text=self.t("light"), command=lambda: self.set_theme("light", theme_window)).pack(pady=5)
        tk.Button(theme_window, text=self.t("dark"), command=lambda: self.set_theme("dark", theme_window)).pack(pady=5)

    def set_language(self, lang, window):
        self.language = lang
        window.destroy()
        self.build_ui()

    def set_theme(self, theme, window):
        self.theme = theme
        window.destroy()
        self.build_ui()

    def open_folder(self, path):
        if platform.system() == "Windows":
            os.startfile(path)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", path])
        elif platform.system() == "Linux":
            subprocess.Popen(["xdg-open", path])

    def create_structure(self):
        dest = self.dest_var.get().strip()
        name = self.name_var.get().strip()
        if not dest:
            messagebox.showwarning("Warning", self.t("warning_select"))
            return
        if not name:
            messagebox.showwarning("Warning", self.t("warning_name"))
            return
        path = os.path.join(dest, name)
        try:
            os.makedirs(path, exist_ok=True)
            for i in range(self.listbox.size()):
                sub = self.listbox.get(i)
                os.makedirs(os.path.join(path, sub), exist_ok=True)
            messagebox.showinfo("Success", self.t("success"))
            self.open_folder(path)
        except Exception as e:
            messagebox.showerror("Error", f"{self.t('error')}\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Folder Creator")
    app = FolderCreatorApp(root)
    root.mainloop()
