
# split a video into clips with the input of a list of start and end index
import cv2

def get_clips(v_path, out_dir, seg_range):
    # vidPath = '/path/foo/video.mp4'
    # shotsPath = '/path/foo/video/%d.avi' # output path (must be avi, otherwize choose other codecs)
    # segRange = [(0,40),(50,100),(200,400)] # a list of starting/ending frame indices pairs

    v_name = v_path.split("/")[-1]
    cap = cv2.VideoCapture(v_path)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    # choose proper codec
    v_format = v_path.split(".")[-1].lower()
    if v_format == "avi":
        codec = "XVID"
    elif v_format == "mp4":
        codec = "MJPG" 
    elif v_format == "mkv":
        codec = "X264"
    fourcc = int(cv2.VideoWriter_fourcc(*codec))

    for idx,(begFidx,endFidx) in enumerate(seg_range):
        writer = cv2.VideoWriter(out_dir+"/"+"_".join([v_name, str(begFidx, endFidx)]),fourcc,fps,size)
        cap.set(cv2.CAP_PROP_POS_FRAMES,begFidx)
        ret = True # has frame returned
        while(cap.isOpened() and ret and writer.isOpened()):
            ret, frame = cap.read()
            frame_number = cap.get(cv2.CAP_PROP_POS_FRAMES) - 1
            if frame_number < endFidx:
                writer.write(frame)
            else:
                break
        writer.release()