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

def load(job_records_path):
    with open(job_records_path,'rb') as f:
        return _pickle.load(f)

def save(now_idx, jobs, selected, job_records_name):
    with open(job_records_name,'wb') as f:
        _pickle.dump((now_idx,jobs,selected),f)


def job_records(rootpath, cache=False):
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
        return load(rootpath)

    dirnames = os.listdir(rootpath)
    filepaths = \
    pipe(cmap(lambda filename: os.path.join(rootpath,filename)),
         cmap(utils.file_paths),
         cmap(list))
    return 0, list(zip(dirnames, filepaths(dirnames))), []

def look_and_decide(window_title,image,monitor_h):
    ''' 
    o: save this image
    x: nope
    j: if height of image > height of monitor, press j to 
       look lower part of image. and the press o or x.
    '''

    img_h = img.shape[0]
    top = True
    checked = (img_h < monitor_h)
    while True:
        cv2.imshow(window_title,
                   img[:monitor_h] if top 
                   else img[img_h - monitor_h:]);

        key = cv2.waitKey(1) & 0xFF
        if key == ord('j') and img_h > monitor_h:
            top = not top
            checked = True
        if (key == ord('o') or key == ord('x')) and checked:
            return chr(key)

#now_idx, jobs, selected = job_records('./data/')
#_, _, selected = job_records('tmp_data2',cache=True)
#print(selected)

def select(data_path, max_selection, monitor_height, cache=False):
    now_idx, jobs, selected = job_records(data_path, cache=True)
    print(selected)
    #max_selection = 2
    for title, imgpaths in jobs[now_idx:]:
        print(title)
        random.shuffle(imgpaths)
        num_selection = 0
        for imgpath in imgpaths:
            img = cv2.imread(imgpath); 
            if img is not None:
                if 'o' == look_and_decide('o x j',img,980):
                    selected.append(
                        (imgpath, imgpath.replace('/','_'))
                    )
                    num_selection += 1
            if num_selection == max_selection:
                break
        now_idx += 1

        save(now_idx,jobs,selected, data_path)
        #_, _, arr = job_records(data_path,cache=True);print(arr)

#select('./data/', 4, 980)
select('tmp_data', 4, 980, cache=True)
_, _, selected = job_records('tmp_data', cache=True)
print(selected)


'''
data = job_records('./data/')
with open('tmp_data','wb') as f:
    _pickle.dump(data,f)
import unittest
class Test_cache(unittest.TestCase):
    def test_cache(self):
        expected = job_records('data')
        with open('tmp_data','wb') as f:
            _pickle.dump(expected,f)
        actual = job_records('tmp_data',cache=True)
        self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()
'''
