from db_loader import load_csv_to_sqlite, get_table_info

# Use any small CSV you have
with open("data/test.csv", "w") as f:
    f.write("Name,Age,City\nAlice,30,NYC\nBob,25,LA\nCharlie,35,Chicago\n")

result = load_csv_to_sqlite("data/test.csv")
print(result)

info = get_table_info()
print(info)