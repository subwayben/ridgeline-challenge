from dashboard.data_loader import get_city_data

la = get_city_data("Los Angeles-Long Beach-Anaheim, CA")

print(la.head())
print(la.columns)
print(len(la))