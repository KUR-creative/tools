import _pickle, cv2, h5py

def load(ox_list_path):
    with open(ox_list_path,'rb') as f:
        return _pickle.load(f)

def save(now_idx, ox_list, ox_list_path):
    with open(ox_list_path,'wb') as f:
        _pickle.dump((now_idx, ox_list),f)

def look_and_decide(image, window_title='o x 4 6 q'):
    while True:
        cv2.imshow(window_title,image)
        key = cv2.waitKey(1) & 0xFF
        if (key == ord('o') or # good crop
            key == ord('x') or # bad crop
            key == ord('6') or # next
            key == ord('4') or # prev
            key == ord('q')):  # exit
            return chr(key)

def print_state(ox_list, idx, num_checked, num_imgs):
    print(ox_list[idx], ':', idx,'/',num_imgs, ' | ', 
          num_checked,'/',num_imgs)
def classify(src_imgs_path, ox_list_path):
    # load
    # look_and_decide
    with h5py.File(src_imgs_path,'r') as f:
        images = f['images']
        num_imgs = images.shape[0]
        num_checked = 0
        ox_list = ['-'] * num_imgs
        idx = 0
        while True:
            cmd = look_and_decide(images[idx])
            if cmd == 'o' or cmd == 'x':
                ox_list[idx] = cmd
                print_state(ox_list, idx, num_checked, num_imgs)
                num_checked += 1
                idx += 1
                save(idx, ox_list, ox_list_path)
            elif cmd == '4':
                idx = ((idx - 1) + num_imgs) % num_imgs
                print_state(ox_list, idx, num_checked, num_imgs)
            elif cmd == '6':
                idx = ((idx + 1) + num_imgs) % num_imgs
                print_state(ox_list, idx, num_checked, num_imgs)
        look_and_decide(images[-1])

#import unittest, numpy as np
#class Test(unittest.TestCase):

if __name__ == '__main__':
    #unittest.main()
    classify('./mini_mini.h5', 'tmp_data')
