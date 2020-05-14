{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {},
   "outputs": [],
   "source": [
    "import cv2  \n",
    "import numpy as np \n",
    "from PIL import ImageFilter \n",
    "from PIL import Image\n",
    "from IPython.display import clear_output\n",
    "import matplotlib.pyplot as plt\n",
    "import random\n",
    "import imutils\n",
    "from os import listdir\n",
    "import os\n",
    "\n",
    "DATASET_PATH = '/home/souhila/nvme-storage/RA_V2/tmp'\n",
    "#img = cv2.imread(DATASET_PATH,cv2.COLOR_BGR2GRAY)\n",
    "\n",
    "\n",
    "def flou_plane( img, alpha=10 ):\n",
    "\n",
    "    h, w = img.shape\n",
    "    # Define mask \n",
    "    mask = 255*np.ones(img.shape, dtype='uint8')\n",
    "            \n",
    "    zstalck =[]\n",
    "    #6 focal plane\n",
    "    ss = np.linspace(1,-1,6)\n",
    "    for s in ss:\n",
    "\n",
    "        t=np.repeat(np.linspace(-1,1,h),w).reshape(h,w)\n",
    "        kernel = np.ones((h,w))\n",
    "        ker = kernel*np.exp((-(t-s)**2-(t-s)**2)/0.2)\n",
    "        ker2 = abs(np.ceil((ker-np.max(ker))*100))\n",
    "\n",
    "\n",
    "        img_float = img.copy().astype('float') \n",
    "        # Create output image that is the same as the original \n",
    "        filtered = img.copy()\n",
    "\n",
    "        for y in range(h): \n",
    "            for x in range(w): \n",
    "                mask_val=np.ceil(ker2[y,x]/10) \n",
    "                beginx = x-int(mask_val/2) \n",
    "                if beginx < 0: \n",
    "                    beginx = 0 \n",
    "\n",
    "                beginy = y-int(mask_val/2) \n",
    "                if beginy < 0: \n",
    "                    beginy = 0 \n",
    "\n",
    "                endx = x+int(mask_val/2) \n",
    "                if endx >= w: \n",
    "                    endx= w-1 \n",
    "\n",
    "                endy = y+int(mask_val/2) \n",
    "                if endy >= h: \n",
    "                    endy = h-1 \n",
    "\n",
    "                xvals = np.arange(beginx, endx+1) \n",
    "                yvals = np.arange(beginy, endy+1) \n",
    "                (col_neigh,row_neigh) = np.meshgrid(xvals, yvals) \n",
    "                col_neigh = col_neigh.astype('int') \n",
    "                row_neigh = row_neigh.astype('int') \n",
    "\n",
    "                \n",
    "                # Calculate the average and set it to be the output \n",
    "                filtered[y,x] = int(np.mean(pix)) \n",
    "\n",
    "        zstalck.append(filtered)\n",
    "        \n",
    "    return(zstalck)\n",
    "\n",
    "def rot_image_img(img,angle):\n",
    "    #img = cv2.imread(path,cv2.COLOR_BGR2GRAY)\n",
    "    #mask = np.zeros_like(img)-1\n",
    "    \n",
    "    #rotation mask et image\n",
    "    mask_rot = np.ones(img.shape,np.uint8)\n",
    "    \n",
    "    img_rot = imutils.rotate_bound(img, angle)\n",
    "    mask_rot = imutils.rotate_bound(mask_rot, angle)\n",
    "    \n",
    "    #erosion mask\n",
    "    mask_erod =np.zeros_like(img_rot,np.uint8)\n",
    "    kernel_size = 5\n",
    "    kernel = np.ones((kernel_size,kernel_size),np.uint8)\n",
    "    mask_erod = cv2.erode(mask_rot,kernel,iterations = 1)\n",
    "    \n",
    "    #pixels erodé\n",
    "    erod = (mask_rot - mask_erod)*255\n",
    "    \n",
    "    #erod_img[erod==255] = img_rot[erod==255]\n",
    "\n",
    "    fond_moyen = []\n",
    "    fond_moyen = img_rot[erod!=0]\n",
    "    fond_moyen = int(np.ma.median(fond_moyen))\n",
    "    img_rot[mask_erod == 0] = fond_moyen\n",
    "\n",
    "\n",
    "    return(img_rot)\n",
    "\n",
    "\n",
    "files = [f for f in listdir(DATASET_PATH) if os.path.isfile(os.path.join(DATASET_PATH, f))]\n",
    "list_files = random.sample(files,10)\n",
    "\n",
    "for file in list_files:\n",
    "    angle = random.randint(0,180)\n",
    "    img = cv2.imread(os.path.join(DATASET_PATH +'/'+ file),cv2.COLOR_BGR2GRAY)\n",
    "    img_rot = rot_image_img(img,angle)\n",
    "    zstalck = flou_plane(img_rot,alpha=10 )\n",
    "    angle = random.randint(0,90)\n",
    "    for i in range(6):\n",
    "        img2 = rot_image_img(zstalck[i],angle)\n",
    "        cv2.imwrite(os.path.join('/home/souhila/nvme-storage/RA_V2/tmp2/' + file.split('_')[1] + '_'+os.path.splitext(file.split('_')[2])[0] + '_' +str(i) + '.png') , img2)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.6.9"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}