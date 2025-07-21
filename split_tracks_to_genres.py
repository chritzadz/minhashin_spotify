import pandas as pd
import re
import random
import csv

dp = pd.read_csv('tracks_with_genre.csv')
dg = pd.read_csv('all_genres.csv')

trackgenre_col = dp[['track_name', 'track_id', 'genre']]
genre_col = dg['genre']

for genre in genre_col:
    with open(f'track_seperated_by_genre/{genre}_track.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['track_name', 'track_id', 'genre'])
        for index, row in trackgenre_col.iterrows():
            name = row['track_name']
            id = row['track_id']
            track_genre = row['genre']

            if (track_genre == genre):
                writer.writerow([name, id, track_genre])
