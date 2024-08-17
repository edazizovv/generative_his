try:
    import cPickle as pickle
except ImportError:  # Python 3.x
    import pickle

with open('NONO.p', 'rb') as fp:
    data_1 = pickle.load(fp)
