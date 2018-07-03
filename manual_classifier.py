import os, sys, _pickle, cv2, h5py

def load(ox_list_path):
    with open(ox_list_path,'rb') as f:
        return _pickle.load(f)

def save(now_idx, num_checked, ox_list, ox_list_path):
    with open(ox_list_path,'wb') as f:
        _pickle.dump((now_idx, num_checked, ox_list),f)

def look_and_decide(image, window_title='o x 4 6 q'):
    while True:
        cv2.imshow(window_title,image)
        key = cv2.waitKey(1) & 0xFF
        if (key == ord('o') or # good crop
            key == ord('x') or # bad crop
            key == ord('6') or # next
            key == ord('4') or # prev
            key == ord('l') or # prev
            key == ord('q')):  # exit
            return chr(key)

def mod_add(augend,addend, mod_n):
    return ((augend + addend) + mod_n) % mod_n

def print_state(ox_list, idx, num_checked, num_imgs):
    print(ox_list[idx], ', idx:', idx,'/',num_imgs, ', checked:', 
          num_checked,'/',num_imgs)

def build_ox_list(images, ox_list_path,
                  idx, num_checked, ox_list=None):
    num_imgs = images.shape[0]
    if ox_list is None:
        ox_list = ['-'] * num_imgs
    while True:
        cmd = look_and_decide(images[idx])
        if cmd == 'o' or cmd == 'x':
            if num_checked < num_imgs and ox_list[idx] == '-':
                num_checked += 1
            elif ox_list[idx] != cmd:
                print('It overwirtes previous data!!!') 
                print(ox_list[idx], '->', cmd)
            ox_list[idx] = cmd
            print_state(ox_list, idx, num_checked, num_imgs)
            idx = mod_add(idx,+1, num_imgs)
            save(idx, num_checked, ox_list, ox_list_path)

        elif cmd == '4' of cmd == '6':
            val = -1 if cmd == '4' else +1
            idx = mod_add(idx, val, num_imgs)
            print_state(ox_list, idx, num_checked, num_imgs)

        elif cmd == 'l':
            for i, ch in enumerate(ox_list):
                print(i,ch,end='\t',flush=True)
            print()

        elif cmd == 'q':
            if num_checked < num_imgs:
                print('You have to check {} more images.'\
                      .format(num_imgs - num_checked))
            sys.exit(0)

def classify(src_imgs_path, ox_list_path):
    with h5py.File(src_imgs_path,'r') as f:
        if os.path.exists(ox_list_path):
            build_ox_list(f['images'], ox_list_path, 
                          *load(ox_list_path))
        else:
            build_ox_list(f['images'], ox_list_path, 0, 0)

if __name__ == '__main__':
    classify('./mini_mini.h5', 'tmp_data')
