import cv2
import manual_selector

now_idx, jobs, selected = manual_selector.load('./job_records')
for path,name in selected:
    print(path, ' | ', name)
    img = cv2.imread(path)
    cv2.imshow('img',img); cv2.waitKey(0)
