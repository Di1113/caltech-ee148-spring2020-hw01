import os
import numpy as np
import json
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import ntpath

# utility functions 
def padimage(image, kernel, stride):
    s = stride
    ir, ic = image.shape
    kr, kc = kernel.shape
    pr = kr + (ir - 1)*s - ir 
    pc = kc + (ic - 1)*s - ic 
    newimg = np.zeros((ir+pr, ic+pc))
    newimg[0:ir, 0:ic] = image 
    return newimg 

def correlate2d(image, kernel, stride):
    paddedimage = padimage(image, kernel, stride)
    ir, ic = paddedimage.shape
    result = np.zeros(image.shape)
    kr, kc = kernel.shape
    sr, sc = (0, 0)
    corrsum = 0
    for i in range(0, ir-kr+1, stride):
        for j in range(0, ic-kc+1, stride):
            for k in range(0, kr):
                ii = k + i 
                rsum = np.dot(paddedimage[ii,j:(j+kc)], kernel[k,:])
                corrsum += rsum 
                # print(rsum)
            # finished computing one kenerl-size correlation, store in new image array 
            result[ii-kr+1,j] = corrsum 
    return result 

def detect_red_light(I, file_name):
    '''
    This function takes a numpy array <I> and returns a list <bounding_boxes>.
    The list <bounding_boxes> should have one element for each red light in the 
    image. Each element of <bounding_boxes> should itself be a list, containing 
    four integers that specify a bounding box: the row and column index of the 
    top left corner and the row and column index of the bottom right corner (in
    that order). See the code below for an example.
    
    Note that PIL loads images in RGB order, so:
    I[:,:,0] is the red channel
    I[:,:,1] is the green channel
    I[:,:,2] is the blue channel
    '''
    
    
    bounding_boxes = [] # This should be a list of lists, each of length 4. See format example below. 
    
    # prepare kernel for correlation 
    # read in a red circle mask 
    circlemask = Image.open('redcircle.png')

    # convert circlemask to numpy array and copy to cm 
    cm_R = np.asarray(circlemask).copy()

    # get a 2d array with pixels outside circle to be 0 
    cm_R = cm_R[:, :, 1] * (-1) + 255
        
    box_height, box_width = cm_R.shape

    cm_R = cm_R/255 


    # read in image for red light detection dataset 
    target = I
    # convert to greyscale image 
    target = target.dot([0.5, 0.1, 0.1])
    # save image shape 
    tr, tc = target.shape
    # filter out not-so red pixels after thresholding, 
    # red lights should be the bright spots on the image 
    thresh =150
    target[target < thresh] = 0 

    # do matched filtering on current target image with the circle mask 
    result = correlate2d(target, cm_R, 1)
    # ind returns the maximum value pixel's indices in the image 
    # ind is used as the top left corner coordinate to draw bounding box
    ind = np.unravel_index(np.argmax(result, axis=None), result.shape)

    """ code to save image with bounding box
    # bounding box top left and bottom right coordinates 
    x0, y0, x1, y1 = ind[0], ind[1], ind[0]+box_height, ind[1]+box_width 

    # draw bounding box on original image
    rimg = Image.fromarray(I)
    draw = ImageDraw.Draw(rimg)
    draw.rectangle([x0, y0, x1, y1], fill=None, outline=(255, 0, 0))

    # save image to destinated folder 
    folderpath = "../data/RedLights2011_Medium/result-imgs"
    imgfilename = ntpath.basename(img_path)
    resfn = 'oneredlight_%s' % (file_name)
    rimg.save(os.path.join(folderpath, resfn))
    """

    '''
    As an example, here's code that generates between 1 and 5 random boxes
    of fixed size and returns the results in the proper format.
    '''
    
    # num_boxes = 334
    # for i in range(num_boxes):
    #     (n_rows,n_cols,n_channels) = np.shape(I)
        
    tl_row = int(ind[0])
    tl_col = int(ind[1])
    br_row = int(tl_row + box_height)
    br_col = int(tl_col + box_width)
    
    bounding_boxes.append([tl_row,tl_col,br_row,br_col]) 
    
    '''
    END YOUR CODE
    '''
    
    for i in range(len(bounding_boxes)):
        assert len(bounding_boxes[i]) == 4
    
    return bounding_boxes

# set the path to the downloaded data: 
data_path = '../data/RedLights2011_Medium'

# set a path for saving predictions: 
preds_path = '../data/hw01_preds' 
os.makedirs(preds_path,exist_ok=True) # create directory if needed 

# get sorted list of files: 
file_names = sorted(os.listdir(data_path)) 

# remove any non-JPEG files: 
file_names = [f for f in file_names if '.jpg' in f] 

preds = {}
for i in range(len(file_names)):
    
    # read image using PIL:
    img_path = os.path.join(data_path,file_names[i])
    I = Image.open(img_path)
    
    # convert to numpy array:
    I = np.asarray(I)
    
    preds[file_names[i]] = detect_red_light(I, file_names[i])

    print("drew " + str(i) + " boxes.")
    if(i % 5 == 0):
        # save preds (overwrites any previous predictions!)
        ff = open(os.path.join(preds_path,('preds%s.json' % (str(i)))),'w+')
        with ff:
            json.dump(preds,ff)

# save preds (overwrites any previous predictions!)
with open(os.path.join(preds_path,'preds.json'),'w') as f:
    json.dump(preds,f)
