import os
import cv2
import numpy as np
import pandas as pd

def draw_line_plot(video,tracking_csv,bodypart):
    inputDf = pd.read_csv(tracking_csv, error_bad_lines=False)
    videopath = os.path.basename(video).split('.')[0] + '_pathplot.mp4'
    videopath = os.path.join(os.path.dirname(video),videopath)

    #datacleaning
    colHeads = [bodypart + '_x', bodypart + '_y', bodypart + '_p']
    df = inputDf[colHeads].copy()

    #convert to int
    widthlist = df[colHeads[0]].astype(float).astype(int)
    heightlist = df[colHeads[1]].astype(float).astype(int)
    circletup = tuple(zip(widthlist,heightlist))

    # get resolution of video
    vcap = cv2.VideoCapture(video)
    if vcap.isOpened():
        width = int(vcap.get(cv2.CAP_PROP_FRAME_WIDTH))  # float
        height = int(vcap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # float
        fps = int(vcap.get(cv2.CAP_PROP_FPS))

    # make white background
    img = np.zeros([height, width, 3])
    img.fill(255)
    img = np.uint8(img)


    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    out = cv2.VideoWriter(videopath, fourcc, fps, (width,height))
    counter=0
    while (vcap.isOpened()):
        ret,frame = vcap.read()
        if ret == True:
            if counter !=0:
                cv2.line(img,circletup[counter-1],circletup[counter],5)

            lineWithCircle = img.copy()
            cv2.circle(lineWithCircle, circletup[counter],5,[0,0,255],-1)



            out.write(lineWithCircle)
            counter+=1

        else:
            break

    vcap.release()
    cv2.destroyAllWindows()
    print('Video generated.')