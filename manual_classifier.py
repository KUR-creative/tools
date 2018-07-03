import cv2, h5py

def look_and_decide(image,
                    window_title='o x 4 6 q'):
    while True:
        cv2.imshow(window_title,image)
        key = cv2.waitKey(1) & 0xFF
        if (key == ord('o') or # good crop
            key == ord('x') or # bad crop
            key == ord('6') or # next
            key == ord('4') or # prev
            key == ord('q')):  # exit
            return chr(key)

def main():
    # load
    # look_and_decide
    with h5py.File('./mini_mini.h5','r') as f:
        images = f['images']
        num_imgs = images.shape[0]
        idx = 0
        while 0 <= idx < num_imgs:
            print(look_and_decide(images[idx]))
            idx += 1
            print(idx)
        print(idx)
        look_and_decide(images[-1])

if __name__ == '__main__':
    main()
