import os, random, _pickle, cv2
from fp import pipe, curry, cmap, cfilter, crepeat
import utils

utils.help_option(
'''
manual_selector: 
    select 'N' images from 'imgs_dir' 
    and save image name and paths into 'job_records_path'.
    'monitor_height' is maximum height size of ui

if you create new job_records
  python manual_selector N imgs_dir imgs_dir job_records_path

if you use existing job_records
  python manual_selector N imgs_dir job_records_path

ex1. create new records)    
python manual_selector 2 ./mangas/ job_records.bin
ex2. use existing records)  
python manual_selector 2 job_records.bin 
'''
)

def load(job_records_path):
    with open(job_records_path,'rb') as f:
        return _pickle.load(f)

def save(now_idx, jobs, selected, job_records_path):
    with open(job_records_path,'wb') as f:
        _pickle.dump((now_idx,jobs,selected),f)


def new_job_records(rootpath):
    ''' 
    rootpath is root of directory structure like below
    rootpath
      dirname1 
        filepath1 
        filepath2 
        ...
      dirname2 
        filepath1
      ...

    return (now_index, list<dirname,list<filepath>>, selected)
    now_index is last worked index.
    selected is empty list. img paths would be saved.
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

def select(max_selection, monitor_height,
           data_path, job_records_path=None):
    print('?1')
    if job_records_path:
        now_idx, jobs, selected = new_job_records(data_path)
    else:
        now_idx, jobs, selected = load(data_path)
    print('?2')
    for title, imgpaths in jobs[now_idx:]:
        print(title)
        random.shuffle(imgpaths)
        num_selection = 0
        #print(imgpaths)
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

        if job_records_path:
            save(now_idx,jobs,selected, job_records_path)
        else:
            save(now_idx,jobs,selected, data_path)


import sys
if __name__ == '__main__':
    max_selection = int(sys.argv[1])
    monitor_height = int(sys.argv[2])

    if len(sys.argv) == 4+1:
        imgs_dir = sys.argv[3]
        job_records_path = sys.argv[4]
        select(max_selection, monitor_height, 
               imgs_dir, job_records_path)
    elif len(sys.argv) == 3+1:
        job_records_path = sys.argv[3]
        select(max_selection, monitor_height, job_records_path)
    else:
        print('invalid number of arguments!')

    _, _, selected = load(job_records_path)
    print(selected)
