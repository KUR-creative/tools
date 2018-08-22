import os, random, _pickle, cv2
from fp import pipe, cmap
import utils

utils.help_option(
'''
manual_selector
  select 'N' images from 'imgs_dir' 
  and save image name and paths into 'job_records_path'.
  'monitor_height' is maximum height size of ui

  if 'job_records_path' already exists,
  continue with this, append to selected.

synopsis
  python manual_selector.py N monitor_height imgs_dir job_records_path

example
  python manual_selector.py 2 980 ./mangas/ job_records.bin

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
        if key == ord('q'):
            return 'q'
        if key == ord('r'):
            return 'r'

def select(max_selection, monitor_height,
           data_path, job_records_path=None):
    if job_records_path:
        now_idx, jobs, selected = new_job_records(data_path)
    else:
        now_idx, jobs, selected = load(data_path)
    for title, imgpaths in jobs[now_idx:]:
        print(title)
        random.shuffle(imgpaths)
        num_selection = 0
        #print(imgpaths)
        for imgpath in imgpaths:
            img = cv2.imread(imgpath); 
            if img is not None:
                cmd = look_and_decide('o x j',img,monitor_height)
                if cmd == 'o':
                    selected.append(
                        (imgpath, imgpath.replace(os.sep,'_'))
                    )
                    num_selection += 1
                elif cmd == 'q':
                    num_last_jobs = len(jobs) - now_idx
                    num_last_imgs = num_last_jobs * max_selection
                    print('You have to choose {}jobs * {}imgs = {} more images.'\
                          .format(num_last_jobs, max_selection,
                                  num_last_jobs * max_selection))
                    sys.exit()
                elif cmd == 'r':
                    num_selection = max_selection # it means "SKIP this title"
                    print('---> skip this title!')
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
    imgs_dir = sys.argv[3]
    job_records_path = sys.argv[4]
    
    if os.path.exists(job_records_path): # if cache exists,
        select(max_selection, monitor_height, job_records_path)
    else:
        select(max_selection, monitor_height, imgs_dir, job_records_path)

    _, _, selected = load(job_records_path)
    print(selected)
