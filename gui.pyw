import tkinter as tk
from tkinter import filedialog, messagebox
from main import *
from stwórz_parquet import stworz_parquet

class GuiGeneratorDanychDobowoGodzinowych:
    def __init__(self, master):
        self.master = master
        master.title("Generator danych dobowo-godzinowych")

        master.geometry('800x150')

        self.entry_path = tk.Entry(master, justify='center')
        self.entry_path.insert(0, "Kliknij tutaj, aby wybrać plik...")
        self.entry_path.bind("<Button-1>", lambda event: self.browse_file())
        self.entry_path.pack(fill=tk.X, padx=50, pady=10)

        self.process_button = tk.Button(master, text="Przetwarzaj", command=self.process_data)
        self.process_button.pack(pady=10)

        self.parquet_button = tk.Button(master, text="Wczytaj profile i strefy", command=self.create_parquet)
        self.parquet_button.pack(pady=10)

        wczytaj_dane()

    def browse_file(self):
        self.path = filedialog.askopenfilename(initialdir="_INPUT_")
        if self.path:
            self.entry_path.delete(0, tk.END)
            self.entry_path.insert(0, self.path)
        else:
            self.entry_path.delete(0, tk.END)
            self.entry_path.insert(0, "Nie wybrano pliku.")

    def process_data(self):
        path = self.entry_path.get()
        if path and path != "Kliknij tutaj, aby wybrać plik..." and path != "Nie wybrano pliku.":
            try:
                df = pd.read_excel(path)
                agregator = AgregatorGeneratorow(df)
                messagebox.showinfo("Sukces", "Dane wczytane i przetworzone pomyślnie.")
                self.ask_open_output_folder()
            except Exception as e:
                messagebox.showerror("Błąd", f"Wystąpił błąd: {e}")
    def create_parquet(self):
        try :
            stworz_parquet()
            wczytaj_dane()
            messagebox.showinfo("Sukces", "Wgrano aktualne strefy i profile")
            
        except Exception as e:
                messagebox.showerror("Błąd", f"Wystąpił błąd: {e}")

    def ask_open_output_folder(self):
        if messagebox.askyesno("Otwórz folder", "Czy chcesz otworzyć folder _OUTPUT_?"):
            self.open_output_folder()

    def open_output_folder(self):
        output_folder = "_OUTPUT_"
        try:
            os.startfile(output_folder)
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie można otworzyć folderu: {e}")


root = tk.Tk()
my_gui = GuiGeneratorDanychDobowoGodzinowych(root)
root.mainloop()
