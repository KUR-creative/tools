import utils

utils.help_option(
'''
mask_maker 
  make answer data from 'job_records' 
  and then save them into 'answer_dir'
  
  if you want to start specific 'index' of job records,
  (want to rewrite some answers) pass integer as 4th argument.
  
synopsis
  python mask_maker.py job_records answer_dir
  python mask_maker.py job_records answer_dir index

example
  python mask_maker.py ./job_records.bin ./answers
  python mask_maker.py ./job_records.bin ./answers 13
'''
)

import manual_selector, textMaskMakerUI 
import sys, shutil, os, cv2

def is_done(imgpath_imgname):
    return (len(imgpath_imgname) == 3)

def main(job_records_path, answer_dir, goto=None):
    now_idx, jobs, selected = manual_selector.load(job_records_path)
    
    if goto is not None:
        assert (0 <= goto < len(selected))

    try:
        os.mkdir(answer_dir)
    except:
        pass # make it anyway!

    skip_done = goto is None
    start = 0 if skip_done else goto

    for idx,imgpath_imgname in enumerate(selected[start:]):
        idx += start
        if skip_done and is_done(imgpath_imgname):
            continue
        else:
            imgpath, imgname = imgpath_imgname[:2]
            imgpath = imgpath.replace('\\',os.sep) # in case of windows path..
            origin_name = imgname            
            imgname = os.path.splitext(imgname)[0]
            print(idx,'[2]',imgpath,'|',imgname,'|',origin_name)
            ret = textMaskMakerUI.main(imgpath, 
                                       os.path.join(answer_dir, imgname))
            if ret != 'q':                           
                shutil.copyfile(imgpath, os.path.join(answer_dir, origin_name))
            selected[idx] = (imgpath, imgname, True)
            manual_selector.save(now_idx, jobs, selected, job_records_path)
  
if __name__ == '__main__':
    if len(sys.argv) == 1+2:
        main(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 1+3:
        main(sys.argv[1], sys.argv[2], int(sys.argv[3]))
