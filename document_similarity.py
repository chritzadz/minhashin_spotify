import pandas as pd
import re
import random
import csv

def shingling(k, word):
    word = str(word).lower()

    regex = re.compile('[^a-zA-Z0-9 ]')
    word = regex.sub('', word)

    shingle = word.split(" ")

    if (k > len(shingle)):
        return []

    result = set()
    count = len(shingle) - k + 1

    for i in range(0, count):
        selected_word = " ".join(shingle[i:i+k])
        result.add(selected_word)
        all_words.add(selected_word)
    return result

def sim(set1, set2):
    if(len(set1) != len(set2)):
        return -1

    res = 0
    for e1, e2 in zip(set1, set2):
        if (e1 == e2):
            res = res + 1
    return res/len(set1)


dg = pd.read_csv('all_genres.csv')
genre_col = dg['genre']
for genre in genre_col:
    all_words = set()
    all_words_hm = dict()
    ####################################################################################################################################
    dp = pd.read_csv(f'track_seperated_by_genre/{genre}_track.csv', encoding='ISO-8859-1')

    pd_col = dp['track_name']
    pv_col = dp['track_id']

    tracks = dp[['track_name', 'track_id']]

    n_perm = 100
    ####################################################################################################################################

    hm = dict()
    for track_id, track_name in zip(pv_col, pd_col):
        hm[track_id] = shingling(1, track_name)

    all_words = list(all_words)

    #this is for building signature matrix
    sig_matrix = []
    for i in range(0, n_perm):
        #randomize the perm
        random.shuffle(all_words)

        #print(f"permutation{i+1}")
        #print(all_words)

        sig_matrix_row = []
        #for each docs in hm
        for doc_name, elements in zip(hm.keys(), hm.values()):
            count = 0
            for e in all_words:
                count = count + 1
                if (e in elements):
                    #print(f"{doc_name}: {count}")
                    break
            sig_matrix_row.append(count)
        #print(sig_matrix_row)
        sig_matrix.append(sig_matrix_row)

        #print('\n')


    # for i in range(0, n_perm):
    #     print(sig_matrix[i])

    #input to csv
    with open(f'minhashing_res_genre/{genre}_minhash_res.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for i in range(0, len(hm)):
            for j in range(i + 1, len(hm)):
                sig1 = []
                sig2 = []
                #put into array sig1 using i
                for k in range(0, n_perm):
                    sig1.append(sig_matrix[k][i])

                #put into array sig2 using j
                for k in range(0, n_perm):
                    sig2.append(sig_matrix[k][j])

                sim_ = sim(sig1, sig2)

                if sim_ != 0:
                    track_id1 = list(hm.keys())[i]
                    track_id2 = list(hm.keys())[j]
                    track_name1 = tracks.loc[tracks['track_id'] == track_id1, 'track_name'].iloc[0]
                    track_name2 = tracks.loc[tracks['track_id'] == track_id2, 'track_name'].iloc[0]

                    writer.writerow([track_id1, track_id2, track_name1, track_name2, sim_])


















