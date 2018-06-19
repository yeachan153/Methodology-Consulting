# from structshape import structshape
from collections import Counter
import os
import json

print_steps = True
def step(message):
    if print_steps:
        print("\n" + "*"*70 + '\n{:*^70}\n'.format(message))

def split_text(text):
    return text.split(',')

def get_file_freqs(filename):
    freqs = Counter()
    with open(filename, 'r') as file:
        # line below is a string obj like 'hello my name is' 
        for line in file: 
            words = split_text(line) 
            freqs.update(words)
    return freqs

def freqs_to_vector(freqs, vocabulary):
    vocabulary2 = vocabulary.copy()
    keys_list = [each_key for each_key in freqs if each_key in vocabulary2]
    for index, word in enumerate(vocabulary2):
        for each_key in keys_list:
            if word == each_key:
                vocabulary2[index] = freqs[each_key]
    for idx, each in enumerate(vocabulary2):
        if type(each) == str:
            vocabulary2[idx] = 0
    return vocabulary2

def norm(vector):
    import math
    return math.sqrt(sum([number**2 for number in vector]))

def similarity(A,B):
    if len(A) != len(B):
        print("Length A and B don't match")
        return
    else:
        return sum([A[i]*B[i] for i in range(len(A))]) / (norm(A) * norm(B))

def text_to_vector(text, vocabulary):
    return freqs_to_vector(Counter(split_text(text)), vocabulary)

def rank_documents(query_vector, corpus, num=100):
    similarities = {}
    for doc_id, info in corpus.items():
        freq_vect = corpus[doc_id]['freq_vect']
        similarities[doc_id] = similarity(query_vector, freq_vect)

    ranked_ids = sorted(similarities, key=lambda i: similarities[i], reverse=True)
    ranked_sims = [similarities[id] for id in ranked_ids]
    return ranked_ids[:num], ranked_sims[:num]








