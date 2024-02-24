"""
df = pd.read_excel(r"C:\Users\Kacper\Desktop\dane_profilowe\Profile\profil_równy.xlsx")

df_melted = df.melt(id_vars=['Date'], var_name='Hour', value_name='Value').dropna()
df_melted = df_melted.sort_values(by=['Date', 'Hour'])
print(df_melted)
"""