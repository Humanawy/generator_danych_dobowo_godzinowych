import pandas as pd
from datetime import datetime, timedelta
import os

def dostosuj_profil(df):
    df_melted = df.melt(id_vars=['Date'], var_name='Hour', value_name='Value').dropna()
    df_melted = df_melted.sort_values(by=['Date', 'Hour'])
    return(df_melted)

def wczytaj_profile_z_katalogu_excel(sciezka_katalogu):
    dict_profile = {}
    for plik in os.listdir(sciezka_katalogu):
        if plik.endswith(".xlsx"):
            dict_profile[os.path.splitext(os.path.basename(plik))[0]] = dostosuj_profil(pd.read_excel(os.path.join(sciezka_katalogu, plik)))
    return dict_profile

def wczytaj_strefy_z_katalogu_excel(sciezka_katalogu):
    dict_strefy = {}
    for plik in os.listdir(sciezka_katalogu):
        if plik.endswith(".xlsx"):
            dict_strefy[os.path.splitext(os.path.basename(plik))[0]] = pd.read_excel(os.path.join(sciezka_katalogu, plik))  
    return dict_strefy

def wczytaj_profile_z_katalogu_parquet(sciezka_katalogu):
    dict_profile = {}
    for plik in os.listdir(sciezka_katalogu):
        if plik.endswith(".parquet"):
            dict_profile[os.path.splitext(os.path.basename(plik))[0]] = dostosuj_profil(pd.read_parquet(os.path.join(sciezka_katalogu, plik)))
    return dict_profile

def wczytaj_strefy_z_katalogu_parquet(sciezka_katalogu):
    dict_strefy = {}
    for plik in os.listdir(sciezka_katalogu):
        if plik.endswith(".parquet"):
            dict_strefy[os.path.splitext(os.path.basename(plik))[0]] = pd.read_parquet(os.path.join(sciezka_katalogu, plik))  
    return dict_strefy

class GeneratorDanychDobowoGodzinowych:
    def __init__(self, nazwa_pliku: str, okres_od, okres_do, wolumen: float, df_profil: pd.DataFrame, df_strefa: pd.DataFrame, df_szablon: pd.DataFrame, nazwa_rekordu: str, zaokraglenie_wyników: int = 100,):
        self.nazwa_pliku = nazwa_pliku
        self.okres_od = okres_od
        self.okres_do = okres_do
        self.zaokraglenie_wyników = zaokraglenie_wyników
        self.df_profil = df_profil
        self.df_strefa = df_strefa
        self.wolumen = wolumen
        self.df_szablon = df_szablon
        self.nazwa_rekordu = nazwa_rekordu
        self.wczytaj_dane_z_szablonu_na_okres()
        self.połącz_szablon_profil_strefe()
        self.suma_profilu = self.df[self.df['Value_strefa'] != 0]['Value_profil'].sum()
        self.rozłożenie_wolumenu_po_profilu()

    def wczytaj_dane_z_szablonu_na_okres(self):
        self.df_szablon['Datetime'] = pd.to_datetime(self.df_szablon['Datetime'])
        mask = (self.df_szablon['Datetime'] >= self.okres_od) & (self.df_szablon['Datetime'] <= self.okres_do) ### TU DO UZGODNIENIA ZAKRESY !!!!!!!!!!!!!!
        self.df_szablon = self.df_szablon.loc[mask]

    def połącz_szablon_profil_strefe(self):
        self.df = pd.merge(self.df_szablon, self.df_strefa[["Date", "Hour", "Value"]], on=["Date", "Hour"], how="left")
        self.df.rename(columns={'Value': 'Value_strefa'}, inplace=True)
        self.df = pd.merge(self.df, self.df_profil[["Date", "Hour", "Value"]], on=["Date", "Hour"], how="left")
        self.df.rename(columns={'Value': 'Value_profil'}, inplace=True)
        self.df["Record name"] = self.nazwa_rekordu
        

    def rozłożenie_wolumenu_po_profilu(self):
        aktywna_strefa = self.df['Value_strefa'] != 0
        self.df.loc[aktywna_strefa, "Value"] = self.wolumen / self.suma_profilu * self.df.loc[aktywna_strefa, "Value_profil"]
        self.df["Value"] = self.df["Value"].round(self.zaokraglenie_wyników)

class AgregatorGeneratorow:
    def __init__(self, df):
        self.wyniki = {}
        grupy = df.groupby('Nazwa pliku wyjściowego')
        for nazwa_pliku, grupa in grupy:
            wyniki_grupy = []
            for _, wiersz in grupa.iterrows():
                generator_args = {
                    'nazwa_pliku': wiersz['Nazwa pliku wyjściowego'],
                    'okres_od': wiersz['Okres od'],
                    'okres_do': wiersz['Okres do'],
                    'wolumen': wiersz['Wolumen'],
                    'df_profil': dict_profile[wiersz['Profil']],
                    'df_strefa': dict_strefy[wiersz['Strefa']],
                    'df_szablon': df_szablon,
                    'nazwa_rekordu': wiersz['Nazwa rekordu'],
                }
                if 'Zaokrąglenie' in wiersz:
                    generator_args['zaokraglenie_wyników'] = wiersz['Zaokrąglenie']

                generator = GeneratorDanychDobowoGodzinowych(**generator_args) 
                wyniki_grupy.append(generator.df)
                
            df_lista_wyników = pd.concat(wyniki_grupy).reset_index(drop=True)
            self.wyniki[nazwa_pliku] = {
                'grupa': grupa,
                'lista': df_lista_wyników,
                'lista scalona': df_lista_wyników.groupby(['Datetime','Date', 'Hour', 'Day of Week', 'Hour Range'], as_index=False)['Value'].sum(),
                'tabela przestawna': self.tworzenie_pivot_table(df_lista_wyników)
            }
        self.zapis_wyników()

    def zapis_wyników(self):
        for nazwa_pliku, dane in self.wyniki.items():
            tabela_przestawna = dane['tabela przestawna']
            lista_scalona = dane["lista scalona"]
            lista = dane['lista']
            grupa = dane['grupa']
            
            with pd.ExcelWriter(f"_OUTPUT_\\{nazwa_pliku}.xlsx", engine='openpyxl') as writer:
                tabela_przestawna.to_excel(writer, sheet_name='Tabela przestawna')
                lista_scalona.to_excel(writer, sheet_name='Lista scalona')
                lista.to_excel(writer, sheet_name='Lista')
                grupa.to_excel(writer, sheet_name='Dane źródłowe')

    def tworzenie_pivot_table(self,df):
        pivot_table = df.pivot_table(index='Date', columns='Hour', values='Value', fill_value="", aggfunc='sum')

        if '03:00A' in pivot_table.columns:
            cols = list(pivot_table.columns)
            cols.append(cols.pop(cols.index('03:00A')))
            pivot_table = pivot_table[cols]
        return pivot_table

def wczytaj_dane():
    global dict_profile
    global dict_strefy
    global df_szablon

    print("Wczytywanie profilów...")
    dict_profile = wczytaj_profile_z_katalogu_parquet("Profile/Parquet_Files")
    print("Profil wczytany.")

    print("Wczytywanie stref...")
    dict_strefy = wczytaj_strefy_z_katalogu_parquet("Strefy/Parquet_Files")
    print("Strefy wczytane.")

    print("Wczytywanie szablonu płachty godzinowej...")
    df_szablon = pd.read_parquet("Płachta godzinowa/Parquet_Files/plachta_godzinowa.parquet")
    print("Szablon płachty godzinowej wczytany.")
def main():
    wczytaj_dane()
    while True:
        print("Oczekiwanie na wprowadzenie ścieżki do pliku z danymi...")
        path = input("Podaj ścieżkę do pliku z danymi: ")
        if path == "":
            print("Nie podano ścieżki. Używanie domyślnej ścieżki do pliku.")
            path = "_INPUT_\input_szablon.xlsx"
        try:
            print(f"Wczytywanie danych z pliku: {path}")
            df = pd.read_excel(path)
            print("Dane wczytane pomyślnie.")
            
            print("Przetwarzanie daych...")
            agregator = AgregatorGeneratorow(df)
            print("Pliki stworzone pomyślnie.")
            
        except Exception as e:
            print(f"Wystąpił błąd podczas wczytywania danych: {e}")

if __name__ == '__main__':
    main()



