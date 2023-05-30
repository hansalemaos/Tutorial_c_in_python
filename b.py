r"""
void colorsearch(unsigned char *pic, unsigned char *colors, int width, int totallengthpic, int totallengthcolor, int *outputx, int *outputy, int *lastresult)
{
    int value = 0;
    for (int i=0; i <= totallengthcolor;i+=3)
                              {
        int r = colors[(i * 3)];
        int g = colors[(i * 3 + 1)];
        int b = colors[(i * 3 + 2)];
        for (int j =0; j <= totallengthpic; j+=3){
            if ((r == pic[j]) && (g == pic[j + 1]) && (b == pic[j + 2])){
                int dividend = (j / 3);
                int quotient = (dividend / width);
                int remainder = (dividend % width);
                int upcounter = value;
                outputx[upcounter] = quotient;
                outputy[upcounter] = remainder;
                lastresult[0] = upcounter;
                value++;
            }
        } }
}
// gcc -O2 -fPIC -shared -o ccode.so ccode.c
"""
import ctypes
import os

import cv2
import numpy as np
dllpath = r"C:\ccode.so"
cta = ctypes.cdll.LoadLibrary(dllpath)
colorsearch = cta.colorsearch

def search_colors(
        pic, colors, cpus=4,
):
    if not pic.flags['C_CONTIGUOUS']:
        pic=np.ascontiguousarray(pic)
    os.environ["OMP_NUM_THREADS"] = str(cpus)
    if not isinstance(colors, np.ndarray):
        colors = np.array(colors, dtype=np.uint8)
    if not colors.flags['C_CONTIGUOUS']:
        colors=np.ascontiguousarray(colors)
    totallengthcolor = (colors.shape[0] * colors.shape[1])-1
    totallenghtpic = (pic.shape[0] * pic.shape[1] * pic.shape[2])-1
    outputx = np.zeros(totallenghtpic, dtype=np.int32)
    outputy = np.zeros(totallenghtpic, dtype=np.int32)
    endresults = np.zeros(1, dtype=np.int32)
    width = pic.shape[1]

    picb = pic.ctypes.data_as(ctypes.POINTER(ctypes.c_uint8))
    colorsb = colors.ctypes.data_as(ctypes.POINTER(ctypes.c_uint8))
    totallengthpicb = ctypes.c_int(totallenghtpic)
    totallengthcolorcb = ctypes.c_int(totallengthcolor)
    outputxb = outputx.ctypes.data_as(ctypes.POINTER(ctypes.c_int))
    outputyb = outputy.ctypes.data_as(ctypes.POINTER(ctypes.c_int))
    endresultsb = endresults.ctypes.data_as(ctypes.POINTER(ctypes.c_int))
    widthb = ctypes.c_int(width)

    colorsearch(
        picb,
        colorsb,
        widthb,
        totallengthpicb,
        totallengthcolorcb,
        outputxb,
        outputyb,
        endresultsb,
    )
    return np.dstack([outputx[:endresults[0]+1], outputy[:endresults[0]+1]])[0]

pic = cv2.imread(r"C:\Users\hansc\Downloads\pexels-alex-andrews-2295744.jpg")
colors0 = np.array([[255, 255, 255]],dtype=np.uint8)
resus0 = search_colors(pic=pic, colors=colors0)

colors=np.array([(66,  71,  69),(62,  67,  65),(144, 155, 153),(52,  57,  55),(127, 138, 136),(53,  58,  56),(51,  56,  54),(32,  27,  18),(24,  17,   8),],dtype=np.uint8)
results=search_colors(pic, colors, cpus=4,)
print(results)