import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv(".env")

host=os.getenv("HOST")
port=os.getenv("PORT")
database=os.getenv("DATABASE")
user=os.getenv("USER")
password=os.getenv("PASSWORD")
sslmode="require"  # Esto es obligatorio en Supabase

engine = create_engine(
    f"postgresql://postgres.jokmangkrjfipixrkeil:{password}@{host}:{port}/{database}?sslmode=require"
)

df = pd.read_sql("SELECT * FROM dim_vehiculo", engine)
print(df.head())
'''
df["marca"] = df["marca"].str.upper()
df = df.drop_duplicates()

df.to_sql("dim_vehiculo_clean", engine, if_exists="replace", index=False)
'''

#Change from ubuntu KI