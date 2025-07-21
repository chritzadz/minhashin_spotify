import os
import pandas as pd


genres_csv = pd.read_csv("all_genres.csv")
genres = genres_csv['genre']

for genre in genres:
    file_path = f'minhashing_res_genre/{genre}_minhash_res.csv'
    if os.path.exists(file_path):
        if os.path.getsize(file_path) == 0:
            os.remove(file_path)