import os, random, _pickle, cv2
from fp import pipe, curry, cmap, cfilter, crepeat
import utils

#li = list(utils.file_paths('./data/'))
#print(li)

'''
titles_path = 'data'
for title in os.listdir(titles_path):
    paths = list(utils.file_paths(os.path.join(titles_path,
                                               title)))
    random.shuffle(paths)
    for path in paths:
        img = cv2.imread(path); 
        print(img.shape)
        cv2.imshow('img',img[:980]);
        cv2.waitKey(0)
'''

# opt1. just N imgs from 1 title
# opt2. all editable imgs

def dirname_filepaths_arr(rootpath, cache=False):
    ''' 
    rootpath is 
      cached pickle file name (cache=True) or
      root of directory structure like below
        rootpath
          dirname1 
            filepath1 
            filepath2 
            ...
          dirname2 
            filepath1
          ...

    return (now_index,list<dirname,list<filepath>>)
    now_index is last worked index.
    '''
    if cache:
        with open(rootpath,'rb') as f:
            return _pickle.load(f)

    dirnames = os.listdir(rootpath)
    filepaths = \
    pipe(cmap(lambda filename: os.path.join(rootpath,filename)),
         cmap(utils.file_paths),
         cmap(list))
    return 0, list(zip(dirnames, filepaths(dirnames)))


import unittest
class Test_cache(unittest.TestCase):
    def test_cache(self):
        expected = dirname_filepaths_arr('data')
        with open('tmp_data','wb') as f:
            _pickle.dump(expected,f)
        actual = dirname_filepaths_arr('tmp_data',cache=True)
        self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()
