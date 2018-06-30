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


def new_job_records(rootpath):
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

    img_h = image.shape[0]
    top = True
    checked = (img_h < monitor_h)
    while True:
        cv2.imshow(window_title,
                   image[:monitor_h] if top 
                   else image[img_h - monitor_h:]);

        key = cv2.waitKey(1) & 0xFF
        if key == ord('j') and img_h > monitor_h:
            top = not top
            checked = True
        if (key == ord('o') or key == ord('x')) and checked:
            return chr(key)

#now_idx, jobs, selected = new_job_records('./data/')
#_, _, selected = new_job_records('tmp_data2',cache=True)
#print(selected)

def select(max_selection, monitor_height,
           data_path, job_records_name=None):
    if job_records_name:
        now_idx, jobs, selected = new_job_records(data_path)
    else:
        now_idx, jobs, selected = load(data_path)
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

        if job_records_name:
            save(now_idx,jobs,selected, job_records_name)
        else:
            save(now_idx,jobs,selected, data_path)

select(4,980, './data/','tmp_data2')
select(4,980, 'tmp_data2')
_, _, selected = load('tmp_data2')
print(selected)


'''
data = new_job_records('./data/')
with open('tmp_data','wb') as f:
    _pickle.dump(data,f)
import unittest
class Test_cache(unittest.TestCase):
    def test_cache(self):
        expected = new_job_records('data')
        with open('tmp_data','wb') as f:
            _pickle.dump(expected,f)
        actual = new_job_records('tmp_data',cache=True)
        self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()
'''
