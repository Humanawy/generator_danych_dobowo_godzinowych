import pandas as pd
from datetime import datetime, timedelta
from time_change_dates import TIME_CHANGE_DATES

# Start and end dates
start_date = datetime.strptime("01/01/2017", "%d/%m/%Y")
end_date = datetime.strptime("31/12/2032", "%d/%m/%Y")

# Initialize the current date
current_date = start_date

# List to hold the datetime records
datetime_records = []

while current_date <= end_date:
    year = current_date.year
    if current_date.date() == TIME_CHANGE_DATES['spring_forward'][year]:
        for hour in range(24):
            if hour != 2:  # Skip 2 AM for spring forward
                datetime_records.append((current_date, hour))
    elif current_date.date() == TIME_CHANGE_DATES['fall_back'][year]:
        for hour in range(25):
            if hour == 24:  # Duplicate 2 AM for fall back
                datetime_records.append((current_date, 2))
            else:
                datetime_records.append((current_date, hour))
    else:
        for hour in range(24):
            datetime_records.append((current_date, hour))
    current_date += timedelta(days=1)

data = {
    #"Datetime": [dt.strftime("%d/%m/%Y") for dt, hr in datetime_records],
    "Date": [dt.strftime("%Y-%m-%d") for dt, hr in datetime_records],
    "Hour": [f"{hr+1:02}:00" for dt, hr in datetime_records],
    "Day of Week": [dt.strftime("%A") for dt, hr in datetime_records],
    "Hour Range": [f"{hr}-{(hr+1)%24}" for dt, hr in datetime_records]
}

# Map days of the week from English to Polish
days_map = {
    "Monday": "Poniedziałek",
    "Tuesday": "Wtorek",
    "Wednesday": "Środa",
    "Thursday": "Czwartek",
    "Friday": "Piątek",
    "Saturday": "Sobota",
    "Sunday": "Niedziela"
}
data["Day of Week"] = [days_map[day] for day in data["Day of Week"]]

df = pd.DataFrame(data)
#df['Datetime'] = pd.to_datetime(df['Datetime'], format='%d/%m/%Y')

df.loc[df.duplicated(['Date', 'Hour'], keep='first'), 'Hour'] = df['Hour'] + 'A'

df.to_excel("test.xlsx", index=False)

# Dodanie kolumny z datą bez godziny i kolumny z godziną

# Tworzenie tabeli przestawnej z uwzględnieniem zmiany czasu
pivot_table_tz = df.pivot_table(index='Date', columns='Hour', values='Day of Week', aggfunc=lambda x: 1, fill_value="")

if '03:00A' in pivot_table_tz.columns:
    # Przeniesienie kolumny '03:00A' na koniec
    cols = list(pivot_table_tz.columns)
    cols.append(cols.pop(cols.index('03:00A')))
    pivot_table_tz = pivot_table_tz[cols]

# Ścieżka do zapisu tabeli przestawnej w pliku Excel
pivot_table_path_tz = 'tabela_przestawna_godziny_zmiana_czasu.xlsx'

# Zapisywanie tabeli przestawnej do pliku Excel
pivot_table_tz.to_excel(pivot_table_path_tz)
