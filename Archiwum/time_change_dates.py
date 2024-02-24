from datetime import datetime, timedelta
TIME_CHANGE_DATES = {
    'spring_forward': {
        2017: datetime.strptime("26/03/2017", "%d/%m/%Y").date(),
        2018: datetime.strptime("25/03/2018", "%d/%m/%Y").date(),
        2019: datetime.strptime("31/03/2019", "%d/%m/%Y").date(),
        2020: datetime.strptime("29/03/2020", "%d/%m/%Y").date(),
        2021: datetime.strptime("28/03/2021", "%d/%m/%Y").date(),
        2022: datetime.strptime("27/03/2022", "%d/%m/%Y").date(),
        2023: datetime.strptime("26/03/2023", "%d/%m/%Y").date(),
        2024: datetime.strptime("31/03/2024", "%d/%m/%Y").date(),
        2025: datetime.strptime("30/03/2025", "%d/%m/%Y").date(),
        2026: datetime.strptime("29/03/2026", "%d/%m/%Y").date(),
        2027: datetime.strptime("28/03/2027", "%d/%m/%Y").date(),
        2028: datetime.strptime("26/03/2028", "%d/%m/%Y").date(),
        2029: datetime.strptime("25/03/2029", "%d/%m/%Y").date(),
        2030: datetime.strptime("31/03/2030", "%d/%m/%Y").date(),
        2031: datetime.strptime("30/03/2031", "%d/%m/%Y").date(),
        2032: datetime.strptime("28/03/2032", "%d/%m/%Y").date(),
    },
    'fall_back': {
        2017: datetime.strptime("29/10/2017", "%d/%m/%Y").date(),
        2018: datetime.strptime("28/10/2018", "%d/%m/%Y").date(),
        2019: datetime.strptime("27/10/2019", "%d/%m/%Y").date(),
        2020: datetime.strptime("25/10/2020", "%d/%m/%Y").date(),
        2021: datetime.strptime("31/10/2021", "%d/%m/%Y").date(),
        2022: datetime.strptime("30/10/2022", "%d/%m/%Y").date(),
        2023: datetime.strptime("29/10/2023", "%d/%m/%Y").date(),
        2024: datetime.strptime("27/10/2024", "%d/%m/%Y").date(),
        2025: datetime.strptime("26/10/2025", "%d/%m/%Y").date(),
        2026: datetime.strptime("25/10/2026", "%d/%m/%Y").date(),
        2027: datetime.strptime("31/10/2027", "%d/%m/%Y").date(),
        2028: datetime.strptime("29/10/2028", "%d/%m/%Y").date(),
        2029: datetime.strptime("28/10/2029", "%d/%m/%Y").date(),
        2030: datetime.strptime("27/10/2030", "%d/%m/%Y").date(),
        2031: datetime.strptime("26/10/2031", "%d/%m/%Y").date(),
        2032: datetime.strptime("31/10/2032", "%d/%m/%Y").date(),
    }
}
