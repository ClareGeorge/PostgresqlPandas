
import pandas as pd

df_csv = pd.read_csv("..\\testdata\\pokemon_data.csv")
print(df_csv.head())
print(type(df_csv.columns))
print("first 4 rows", df_csv['Name'][0:4])
print("all names" , df_csv.Name)
print(df_csv[['Name', 'Type 1', 'Speed']])
print("first 2 rows \n", df_csv.iloc[0:2])
print(" 4th row 1 nd position \n", df_csv.iloc[2,1] )
print("iterate thru rows")
for index, row in df_csv.iterrows():
    print(index, row['Name'])

print("apply filters")
print(df_csv.loc[df_csv['Type 1'] == "Grass" ])

print("describe")
print ( df_csv.describe())




