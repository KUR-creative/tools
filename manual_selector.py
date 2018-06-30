import os, random, _pickle, cv2
from fp import pipe, curry, cmap, cfilter, crepeat
import utils

def load(job_records_path):
    with open(job_records_path,'rb') as f:
        return _pickle.load(f)

def save(now_idx, jobs, selected, job_records_name):
    with open(job_records_name,'wb') as f:
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


if __name__ == '__main__':
    select(4,980, './data/','tmp_data2')
    select(4,980, 'tmp_data2')
    _, _, selected = load('tmp_data2')
    print(selected)
