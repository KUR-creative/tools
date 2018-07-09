import utils

utils.help_option(
'''
mask_maker 
  make answer data from 'job_records' 
  and then save them into 'answer_dir'
  
  if you want to start specific 'index' of job records,
  (want to rewrite answer) pass integer as 4th argument.
  
synopsis
  python mask_maker.py job_records answer_dir
  python mask_maker.py job_records answer_dir index

example
  python mask_maker.py ./job_records.bin ./answers
  python mask_maker.py ./job_records.bin ./answers 13
'''
)

import manual_selector, textMaskMakerUI 
import sys, os, cv2

def unworked_job(imgpath_imgname):
    return (len(imgpath_imgname) == 2)

def main(job_records_path, answer_dir, goto=None):
    now_idx, jobs, selected = manual_selector.load(job_records_path)

    try:
        os.mkdir(answer_dir)
    except:
        pass # make it anyway!

    if goto is None:
        for idx,imgpath_imgname in enumerate(selected):
            if unworked_job(imgpath_imgname):
                imgpath, imgname = imgpath_imgname[:2]
                imgname = os.path.splitext(imgname)[0]
                print(idx,imgname)
                textMaskMakerUI.main(imgpath,
                                     os.path.join(answer_dir, imgname))
                selected[idx] = (imgpath, imgname, True)
                manual_selector.save(now_idx, jobs, selected, job_records_path)
    else:
        for idx,imgpath_imgname in enumerate(selected[goto:]):
            imgpath, imgname = imgpath_imgname[:2]
            imgname = os.path.splitext(imgname)[0]
            print(idx,imgname)
            textMaskMakerUI.main(imgpath,
                                 os.path.join(answer_dir, imgname))
            selected[idx] = (imgpath, imgname, True)
            manual_selector.save(now_idx, jobs, selected, job_records_path)
  
if __name__ == '__main__':
    if len(sys.argv) == 1+2:
        main(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 1+3:
        main(sys.argv[1], sys.argv[2], int(sys.argv[3]))
