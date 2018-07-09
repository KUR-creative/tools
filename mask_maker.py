import utils

utils.help_option(
'''
mask_maker 
  make answer data from 'job_records' 
  and then save them into 'answer_dir'
  
synopsis
  python mask_maker.py job_records answer_dir

example
  python mask_maker.py ./job_records.bin ./answers
'''
)

import manual_selector, textMaskMakerUI 
import sys, os, cv2

def main(job_records_path, answer_dir):
    now_idx, jobs, selected = manual_selector.load(job_records_path)

    try:
        os.mkdir(answer_dir)
    except:
        pass # make it anyway!

    for imgpath, imgname in selected:
        print(imgname)
        textMaskMakerUI.main(imgpath,
                             os.path.join(answer_dir,imgname))
        #img = cv2.imread(imgpath)
        #cv2.imshow('img',img); cv2.waitKey(0)                
  
if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
