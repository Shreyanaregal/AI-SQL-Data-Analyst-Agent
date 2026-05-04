from visualizer import fetch_data, auto_visualize

df = fetch_data("SELECT name, age FROM uploaded_file")
print(df)

fig = auto_visualize(df, title="Age of People")
fig.show()