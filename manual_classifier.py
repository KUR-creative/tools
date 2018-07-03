import cv2, h5py
def main():
    # load
    # look_and_decide
    with h5py.File('./mini_128x_1crop_32.h5','r') as f:
        images = f['images']
        for img in images:
            cv2.imshow('img',img);cv2.waitKey(0)

if __name__ == '__main__':
    main()
