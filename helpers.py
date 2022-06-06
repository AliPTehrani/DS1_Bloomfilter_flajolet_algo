import pandas as pd
import hashlib
import zlib
import numpy as np

# Hashfunctions
# https://github.com/lucasschmidtc/Probabilistic-Algorithms/blob/master/Probabilistic%20Algorithms.ipynb
def hash_CRC32(s):
    return zlib.crc32(s) & 0xffffff


def hash_Adler32(s):
    return zlib.adler32(s) & 0xffffff


def hash_MD5(s):
    return int(hashlib.md5(s).hexdigest(), 16) & 0xffffff


def hash_SHA(s):
    return int(hashlib.sha1(s).hexdigest(), 16) & 0xffffff


hash_functions = [hash_CRC32, hash_Adler32, hash_MD5, hash_SHA]


def load_dataset(path):
    """
    Loads a dataset in from csv format
    :param path:  Path of our csv dataset
    :return: Pandas dataframe
    """
    df = pd.read_csv(path)
    return df


def show_dataset(df,n_rows,n_columns = None):
    """
    :param df: Loaded dataset
    :param n_rows: How many rows should be shown
    :param n_columns: How many columns should be shown
    :return: print dataframe
    """
    with pd.option_context('display.max_rows', n_rows, 'display.max_columns', None):
        print(df)


def generate_bloom_filter(n):
    bloom_filter = np.zeros(n)
    return bloom_filter


def insert_into_bloom_filter(bloom_filter,value):
    for hash_function in hash_functions:
        index = hash_function(str(value).encode('utf8')) % len(bloom_filter)
        bloom_filter[index] = 1
    return bloom_filter


def query_bloom_filter(bloom_filter, value):
    for hash_function in hash_functions:
        index = hash_function(str(value).encode('utf8')) % len(bloom_filter)
        if bloom_filter[index] == 0:
            return 'miss'
    return 'match'

# Flajolet–Martin algorithm
#https://github.com/lucasschmidtc/Probabilistic-Algorithms/blob/master/Probabilistic%20Algorithms.ipynb
def least1(x, L):
    if x == 0:
        return 2**L
    return x & -x


def cardinality_FM(bitmap):
    return least1(~bitmap, 24)

def perform_flajolet_martin_algorithm(values):
    bitmaps = np.array([0] * 4)
    s = set([])
    for idx, w in enumerate(values):
        s.add(w)
        for i, hash_function in enumerate(hash_functions):
            bitmaps[i] |= least1(hash_function(str(w).encode('utf8')), 24)
    for i in range(len(bitmaps)):
        bitmaps[i] = cardinality_FM(bitmaps[i])

    print('Average Estimated:', np.mean(bitmaps))
    print('Actual', values.nunique())
    return(bitmaps)