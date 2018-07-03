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
            key == ord('q')):
            return chr(key)

def main():
    # load
    # look_and_decide
    with h5py.File('./mini_128x_1crop_32.h5','r') as f:
        images = f['images']
        for img in images:
            print(look_and_decide(img))

if __name__ == '__main__':
    main()
