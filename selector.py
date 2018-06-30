import os, random, cv2
import utils
from fp import pipe, curry, cmap, cfilter, crepeat

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
    return <dirname,<filepath>arr>arr 

    rootpath directory structure:
    rootpath
      dirname1 
        filepath1 
        filepath2 
        filepath3
      dirname2 
        filepath1
        ...
      dirname3 
        filepath1 
        filepath2
      ...
    '''
    dirnames = os.listdir(rootpath)
    filepaths = \
    pipe(cmap(lambda filename: os.path.join(rootpath,filename)),
         cmap(utils.file_paths),
         cmap(list))
    return zip(dirnames, filepaths(dirnames))
    
         


import unittest
class Test_cache(unittest.TestCase):
    def test_cache(self):
        self.assertEqual(list(dirname_filepaths_arr('data')),
                         list(dir)
        '''
        for dirname,filepath in dirname_filepaths_arr('data'):
            print(dirname)
            print(filepath)
        '''




if __name__ == '__main__':
    unittest.main()
