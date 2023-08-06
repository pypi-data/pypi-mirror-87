#!/usr/bin/env python
# coding: utf-8

# In[1]:


try:
    if get_ipython().__class__.__name__ == 'ZMQInteractiveShell':
        from IPython.display import display, Javascript
        display(Javascript('Jupyter.notebook.kernel.execute("nb_name = \'" + Jupyter.notebook.notebook_name + "\'");'));
except:
        pass


# In[3]:


version = '0.102'

import re
import tempfile
import os
import subprocess
import glob
from collections import OrderedDict
import base64
import shutil
import os
import stat
import pickle
import time


# # Helper Functions

# In[4]:


def is_testing():
    try:
        return nb_name == 'lx.ipynb'
    except:
        return False


# In[5]:


def isnotebook():
    try:
        return get_ipython().__class__.__name__ == 'ZMQInteractiveShell'
    except:
        pass
    return False


# In[6]:


def testPrint(*args):
    if is_testing():
        print(*args)


# # Inspect

# In[7]:


import inspect
def debugGetFileName():
    return inspect.stack()[1][1]
def debugGetLineNumber():
    return inspect.stack()[1][2]
def debugFunctionName():
    return inspect.stack()[1][3]


# In[8]:


debugGetFileName(), debugGetLineNumber(), debugFunctionName()


# # Shell

# In[9]:


def shell(cmd):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = result.stdout.decode()

    if len(out) > 0 and out[-1] == "\n":
        out = out[:-1]

    return out


# In[10]:


shell_template = """/bin/bash << EOF 2>&1
{cmd}
EOF"""

def bash(cmd, lineList=True):
    result = subprocess.run(shell_template.format(cmd=cmd), shell=True, stdout=subprocess.PIPE)
    out = result.stdout.decode()

    if len(out) > 0 and out[-1] == "\n":
        out = out[:-1]

    if lineList:
        return out.split('\n')
    else:
        return out


# # Timing

# In[11]:


timeSinceLastCallDict = {}


# In[12]:


def timeSinceLastCall(name):
    t = time.time()
    
    last_t = timeSinceLastCallDict.get(name, 0)
    timeSinceLastCallDict[name] = t
    
    time_s = "{:.2E}".format(t - last_t) if last_t > 0 else "-1"
    return name + ": " + time_s


# In[13]:


if is_testing():
    print(timeSinceLastCall('test marker'))


# In[14]:


import time

class tiTimeScope:    
    def __init__(self, name=None):
        if name is None:
            name = f"{debugGetFileName()}:{debugGetLineNumber()}"
        self.name = name
            
    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, *args):
        print(f"{self.name}: {time.time() - self.start:0.2f}s")

if is_testing():
    with tiTimeScope():
        time.sleep(0.05)
    with tiTimeScope('test'):
        time.sleep(0.05)
    


# # Requiremtns

# In[15]:


requirements = []

requirements.append('numpy')
import numpy as np

requirements.append('pandas')
import pandas as pd

requirements.append('natsort')
import natsort

requirements.append('opencv-python')
import cv2

requirements.append('Pillow')
from PIL import Image

requirements.append('urllib3')
from urllib.request import urlopen

requirements.append('ipython')
from IPython.core.display import display, HTML

requirements.append('PyYAML')
import yaml


# # Strings

# In[17]:


def sFloat0(f): return "{:0.0f}".format(f)
def sFloat1(f): return "{:0.1f}".format(f)
def sFloat2(f): return "{:0.2f}".format(f)
def sFloat3(f): return "{:0.3f}".format(f)
def sFloat4(f): return "{:0.4f}".format(f)
def sFloat5(f): return "{:0.5f}".format(f)
def sFloatSci0(f): return "{:0.0E}".format(f)
def sFloatSci1(f): return "{:0.1E}".format(f)
def sFloatSci2(f): return "{:0.2E}".format(f)
def sFloatSci3(f): return "{:0.3E}".format(f)
def sFloatSci4(f): return "{:0.4E}".format(f)
def sFloatSci5(f): return "{:0.5E}".format(f)

if is_testing():
    print(sFloat0(1.234567))
    print(sFloat1(1.234567))
    print(sFloat2(1.234567))
    print(sFloat3(1.234567))
    print(sFloat4(1.234567))
    print(sFloatSci0(1.234567))
    print(sFloatSci1(1.234567))
    print(sFloatSci2(1.234567))
    print(sFloatSci3(1.234567))
    print(sFloatSci4(1.234567))
    print(sFloatSci5(1.234567))


# In[18]:


def strUuid4():
    import uuid
    uuid_with_prefix = uuid.uuid4().urn
    uuid = uuid_with_prefix[9:]
    assert len(uuid) == 36
    return uuid


# In[19]:


if is_testing():
    print(strUuid4())


# In[20]:


def strRand(n, num=True, upperCase=True, lowerCase=True):
    import random
    pool = ""
    if num: pool += '0123456789'
    if upperCase: pool += 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    if lowerCase: pool += 'abcdefghijklmnopqrstuvwxyz'
    return ''.join(random.choice(pool) for _ in range(n))


# In[21]:


if is_testing():
    print(strRand(20))
    print(strRand(20, upperCase=False))
    print(strRand(20, upperCase=False, lowerCase=False))


# In[22]:


def strMd5Pickle4(obj):
    # Must convet to hashable object; This function uses pickle for that
    import hashlib
    md5 = hashlib.md5(pickle.dumps(obj, protocol=4))
    return md5.hexdigest()


# In[23]:


if is_testing():
    print(strMd5Pickle4(['a', 'b']))


# In[24]:


def strMd5String(s):
    import hashlib
    md5 = hashlib.md5(s.encode('utf-8'))
    return md5.hexdigest()


# In[25]:


if is_testing():
    print(strMd5String('s'))


# # Multiprocess / Thread

# In[26]:


def mapThread(func, args, n=8):
    from multiprocessing.pool import ThreadPool
    tPool = ThreadPool(n)
    res = tPool.map(func, args)
    tPool.close()
    return res

def mapProcess(func, args, n=8):
    from multiprocessing import Pool
    pPool = Pool(n)
    res = pPool.map(func, args)
    pPool.close()
    return res

if is_testing():
    print(mapProcess(str, range(10)))
    print(mapThread(str, range(10)))
    print(list(map(str, range(10))))


# # Lists

# In[27]:


def liChunks(l, chunk_size):
    return [l[i:i + chunk_size] for i in range(0, len(l), chunk_size)]


# In[28]:


if is_testing():
    print(liChunks(['a', 'b', 'c', 'd', 'e', 'f'], 1))
    print(liChunks(['a', 'b', 'c', 'd', 'e', 'f'], 2))
    print(liChunks(['a', 'b', 'c', 'd', 'e', 'f'], 3))


# In[29]:


def liSplit(a, number_of_splits):
    idxs = [int(np.round(idx)) for idx in np.linspace(0, len(a), num=number_of_splits + 1)]
    return [a[start:end] for start, end in zip(idxs[:-1], idxs[1:])]


# In[30]:


if is_testing():
    print(liSplit(['a', 'b', 'c', 'd', 'e'], 1))
    print(liSplit(['a', 'b', 'c', 'd', 'e'], 2))
    print(liSplit(['a', 'b', 'c', 'd', 'e'], 3))
    print(liSplit(['a', 'b', 'c', 'd', 'e'], 4))
    print(liSplit(['a', 'b', 'c', 'd', 'e'], 5))
    print(liSplit(['a', 'b', 'c', 'd', 'e'], 6))


# In[31]:


def liJoin(l):
    out = []
    for e in l:
        out += e
    return out


# In[32]:


if is_testing():
    print(liJoin([['a', 'b', 'c'], ['d', 'e', 'f']]))


# In[33]:


def liFlatten(l):
    if isinstance(l, list) or isinstance(l, tuple):
        out = []
        for e in l:
            flat = liFlatten(e)
            if isinstance(flat, list) or isinstance(flat, tuple):
                out += flat
            else:
                out.append(flat)
        return out
    else:
        return l


# In[34]:


if is_testing():
    print(liFlatten(['aa', ['bb', 'cc'], [['dd', ['ee', 'ff']]]]))
    print(liFlatten([1, ['bb', 3], [['dd', ['ee', 'ff']]]]))


# # List of Strings

# In[35]:


regex_cache = {}
def sListFilter(l, re_include=".*", re_exclude='^\b$'):
    regex_cache[re_include] = regex_cache.get(re_include, re.compile(re_include))
    regex_cache[re_exclude] = regex_cache.get(re_exclude, re.compile(re_exclude))
    return [e for e in l if regex_cache[re_include].search(e) and not regex_cache[re_exclude].search(e)]


# In[36]:


if is_testing():
    sListFilter(['good x', 'other good x', 'without the letter before y'])


# In[37]:


if is_testing():
    print(sListFilter(['good x', 'other good x', 'without the letter before y'], re_include='x'))


# In[38]:


if is_testing():
    print(sListFilter(['not enough x', 'enough xx', 'enough xx and also z'], re_include='xx+'))


# In[39]:


if is_testing():
    print(sListFilter(['not enough x', 'enough xx', 'enough xx and also z'], re_include='xx+', re_exclude='z'))


# In[40]:


def lCsv(l, force_oneline=False):
    
    if len(l) == 0:
        return ""
    
    if all([isinstance(e, (list, tuple)) for e in l]) and not force_oneline:
        length = len(l[0])
        if all([len(e) == length for e in l]):
            return "\n".join([lCsv(e, force_oneline=True) for e in l])
            
    return ", ".join([str(e) for e in l])


# In[41]:


if is_testing():
    print(lCsv(['a', 'b', 1, 3.14]))


# In[42]:


if is_testing():
    print(lCsv([['a', 'b'], 1, 3.14]))


# In[43]:


if is_testing():
    print(lCsv([['a', 'b', 1, 3.14], ['c', 'd', 2, 2.72]]))


# # Text files

# In[44]:


def txtread(path):
    if 'http://' in path or 'https://' in path:
        return urlopen(path).read().decode()
    elif 'gs://' in path:
        return gsTxtread(path)
    else:
        with open(path, 'r') as f:
            return f.read()

def txtwrite(path, txt):
    if 'gs://' in path:
        gsTxtwrite(path, txt)
    else:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            return f.write(txt)


# In[45]:


if is_testing():
    print(txtread('https://arxiv.org'))


# # YAML files

# In[46]:


def yamlwrite(path, obj):
    txtwrite(path, yaml.dump(obj))


# In[47]:


def yamlread(path):
    return yaml.safe_load(txtread(path=path))


# In[48]:


if is_testing():
    with tempfile.TemporaryDirectory() as dir_path:
        out_path = dir_path + '/test.yml'
        
        yamlwrite(out_path, {'a':['b', 'c']})
        print(yamlread(out_path))


# # List of Strings

# In[49]:


regex_cache = {}
def sListFilter(listOfStrings, re_include=".*", re_exclude='^\b$'):
    regex_cache[re_include] = regex_cache.get(re_include, re.compile(re_include))
    regex_cache[re_exclude] = regex_cache.get(re_exclude, re.compile(re_exclude))
    return [e for e in listOfStrings if regex_cache[re_include].search(e) and not regex_cache[re_exclude].search(e)]


# ### Examples

# In[50]:


if is_testing():
    print(sListFilter(['good x', 'other good x', 'without the letter before y']))


# In[51]:


if is_testing():
    print(sListFilter(['good x', 'other good x', 'without the letter before y'], re_include='x'))


# In[52]:


if is_testing():
    print(sListFilter(['not enough x', 'enough xx', 'enough xx and also z'], re_include='xx+'))


# In[53]:


if is_testing():
    print(sListFilter(['not enough x', 'enough xx', 'enough xx and also z'], re_include='xx+', re_exclude='z'))


# In[54]:


if is_testing():
    print(txtread('https://arxiv.org'))


# # GCP Google Cloud Platform

# In[55]:


import warnings
warnings.filterwarnings("ignore", "Your application has authenticated using end user credentials from Google Cloud SDK")

def _gsPathSplit(path):
    bucket = path.split("//")[1].split("/")[0]
    prefix = "/".join(path.split("//")[1].split("/")[1:])
    return bucket, prefix

def _gsClient():
    from google.cloud import storage
    client = storage.Client()
    
def _gsBlob(path):
    from google.cloud import storage
    bucket_name, prefix = _gsPathSplit(path)
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(prefix)
    return blob


# In[56]:


def gsGsToHttp(path):
    return path.replace("gs://", "https://storage.cloud.google.com/")

def gsHttpToGs(path):
    return path.replace("https://storage.cloud.google.com/", "gs://").split("?")[0] # "?" is for possible "?authuser=0"


# In[57]:


def gsLs(path):
    from google.cloud import storage
    bucket, prefix = _gsPathSplit(path)
    client = storage.Client().bucket(bucket)
    return ['gs://' + bucket + '/' + blob.name for blob in client.list_blobs(prefix=prefix)]


# In[58]:


def gsExists(path):
    from google.cloud import storage
    bucket, prefix = _gsPathSplit(path)
    client = storage.Client().bucket(bucket)
    return client.blob(prefix).exists()


# In[59]:


def gsUploadFile(gsPath, path):
    blob = _gsBlob(gsPath)
    blob.upload_from_filename(path)


# In[60]:


def gsTxtread(path):
    from google.cloud import storage
    bucket_name, source_blob_name = _gsPathSplit(path)
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    return blob.download_as_string().decode()


# In[61]:


def gsTxtwrite(path, s):
    blob = _gsBlob(path)
    return blob.upload_from_string(s)


# In[62]:


def gsImwrite(path, img):
    blob = _gsBlob(path)
    _, encimg = cv2.imencode('.png', img[:, :, [2, 1, 0]])
    blob.upload_from_string(encimg.tobytes())


# In[63]:


def gsImread(path):
    blob = _gsBlob(path)
    raw = np.asarray(bytearray(blob.download_as_string()), dtype="uint8")
    return cv2.imdecode(raw, 1)[:, :, [2, 1, 0]]


# In[64]:


def gsPklWrite(path, obj):
    blob = _gsBlob(path)
    return blob.upload_from_string(pickle.dumps(obj, protocol=4))


# In[65]:


def gsPklRead(path):
    blob = _gsBlob(path)
    return pickle.loads(blob.download_as_string())


# # Pickle

# In[66]:


def pklwrite(path, obj):
    if 'gs://' in path:
        return gsPklWrite(path, obj)
    else:
        if len(os.path.dirname(path)) > 0:
            os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'wb') as f:
            return pickle.dump(obj, f, protocol=4)


# In[67]:


def pklread(path):
    if 'gs://' in path:
        return gsPklRead(path)
    else:
        with open(path, 'rb') as f:
            return pickle.load(f)


# In[68]:


if is_testing():
    with tempfile.TemporaryDirectory() as dir_path:
        pkl_path = os.path.join(dir_path, 'test.pkl')
        
        pklwrite(pkl_path, 'test')
        print(pklread(pkl_path))


# # Images

# In[69]:


def _imreadSsh(path):
    with tempfile.TemporaryDirectory() as dir_path:
        out_path = os.path.join(dir_path, os.path.basename(path))
        bash(f'scp {path} {out_path}')
        return imread(out_path)

def imread(path):
    if isinstance(path, np.ndarray) and path.dtype == np.uint8:
        return path
    elif '@' in path and ':' in path:
        return _imreadSsh(path)
    elif 'http://' in path or 'https://' in path:
        raw = np.asarray(bytearray(urlopen(path).read()), dtype="uint8")
        img = cv2.imdecode(raw, cv2.IMREAD_COLOR)
    elif 'gs://' in path:
        return gsImread(path)
    elif os.path.isfile(path):
        img = cv2.imread(path, cv2.IMREAD_COLOR)
    else:
        raise RuntimeError("Image not found: ", path)
    return img[:, :, [2, 1, 0]] # This converts the cv2 colors to RGB

def imsread(paths):
    if isinstance(paths, str) and os.path.isdir(paths):
        return [imread(path) for path in fiFindByWildcard(os.path.join(paths, "*.png"))]
    assert isinstance(paths, list) or isinstance(paths, tuple), type(paths)
    return [imread(path) for path in paths]

def imwrite(path, img, jpeg_quality=95):
    if "gs://" in path:
        gsImwrite(path, img)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    
    if path[-4:] == '.jpg' or path[-4:] == '.jpeg':
        cv2.imwrite(path, img[:, :, [2, 1, 0]], [int(cv2.IMWRITE_JPEG_QUALITY), jpeg_quality])
    else:
        cv2.imwrite(path, img[:, :, [2, 1, 0]])

def imjoin(imgs, axis=1, pad=0):
    if pad > 0:
        if axis == 0:
            right=0
            bottom=pad
        elif axis == 1:
            right=pad
            bottom=0
        imgs_out = []
        for idx, img in enumerate(imgs):
            if idx < len(imgs) - 1:
                imgs_out.append(impad(img, right=right, bottom=bottom))
            else:
                imgs_out.append(img)
        imgs = imgs_out
    return np.concatenate(imgs, axis=axis)

def impad(img, top=0, bottom=0, left=0, right=0, color=255, mode='constant'):
    if mode =='constant':
        return np.pad(img, [(top, bottom), (left, right), (0, 0)], 'constant', constant_values=color)
    elif mode == 'reflect':
        return np.pad(img, [(top, bottom), (left, right), (0, 0)], 'reflect')
    else:
        raise RuntimeError(f"Mode '{mode}' not found")


# In[70]:


def imscaleNN(img, s):
    return cv2.resize(img, None, fx=s, fy=s, interpolation=cv2.INTER_NEAREST)

def imscaleBic(img, s):
    return cv2.resize(img, None, fx=s, fy=s, interpolation=cv2.INTER_CUBIC)




# In[71]:


def imshow(array, scale=1, force_nb=False):
    array = imread(array)
    if scale > 1:
        array = imscaleNN(array, scale)
        
    if force_nb or isnotebook():
        display(Image.fromarray(array))
    else:
        cv2.imshow('img', array[:, :, [2, 1, 0]])
        cv2.waitKey()


# In[72]:


def imNewNoise(height, width, scaleNN=1):
    return imscaleNN((255 * np.random.rand(height, width, 3)).astype(np.uint8), scaleNN)


# In[73]:


if is_testing():
    img = imNewNoise(20, 20, 10)
    imshow(impad(img, bottom=10, right=10, mode='reflect'))


# In[74]:


def imCropUniformBorder(img, color=255):
    mask = (img == color)
    out = img.copy()
    for axis in (0, 1):
        const_1d = mask.mean(axis=2).mean(axis=axis)
        diff = np.diff(const_1d)

        if const_1d[0] < 1:
            idx_start = 0
        else:
            idx_start = np.argmin(diff) + 1 # Diff between next and current

        if const_1d[-1] < 1:
            idx_end = 0
        else:
            idx_end = np.argmax(np.flip(diff)) + 1

        if axis == 0:
            out = out[:, idx_start: -idx_end or None]
        else:
            out = out[idx_start: -idx_end or None, :]
    return out

if is_testing():
    # Try the imCropUniformBorder for different paddings
    img_crop = imNewNoise(17, 5)
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    imgPad = impad(img_crop, top=i, left=j, right=k, bottom=l)
                    out = imCropUniformBorder(imgPad)
                    if not (out==img_crop).all():
                        raise RuntimeError('Crop did not work for ', i, j, k, l)


# In[75]:


def imDecodeBytes(imBytes):
    import cv2
    import numpy as np
    x = np.fromstring(imBytes, dtype='uint8') # to 1D uint8 numpy array
    img = cv2.imdecode(x, cv2.IMREAD_UNCHANGED)[:, :, [2, 1, 0]] # cv2 uses bgr
    return img


# In[76]:


#if is_testing():
#    img = imread('http://via.placeholder.com/70.png')
#    imshow(img)


# In[77]:


#if is_testing():
#    imshow('http://via.placeholder.com/70.png')


# In[78]:


if is_testing():
    with tempfile.TemporaryDirectory() as d:
        img = (255 * np.random.rand(20, 20, 3)).astype(np.uint8)
        img_path = os.path.join(d, 'test.png')
        imwrite(img_path, img)
        img_read = imread(img_path)
        
        out = imjoin([impad(img, right=5), img_read]) # join Images side by side

        out_large_pixaleted = imscaleNN(out, 8)
        imshow(out_large_pixaleted)

        out_large_interbic = imscaleBic(out, 8)
        imshow(out_large_interbic)


# In[79]:


def imRepeat(img, height, width):
    height_old, width_old, _ = img.shape

    _ceil = lambda x: int(np.ceil(x))

    img = np.concatenate([img]*_ceil(height/height_old), axis=0)[:height]
    img = np.concatenate([img]*_ceil(width/width_old), axis=1)[:, :width]
    
    return img


# In[80]:


if is_testing():
    img_random_color_3x5 = (np.random.rand(3, 5, 3)*255).astype(np.uint8)
    imshow(imRepeat(img_random_color_3x5, 7, 11), scale=10)


# In[81]:


def imNewWhite(height, width):
    return np.ones((height, width, 3)).astype(np.uint8) * 255


# In[82]:


if is_testing(): imshow(imNewWhite(10, 500) - 30)


# In[83]:


def imNewBlack(height, width):
    return np.zeros((height, width, 3)).astype(np.uint8)


# In[84]:


if is_testing(): imshow(imNewBlack(10, 500))


# In[85]:


def imAddNoiseGauss(img, std):
    assert img.dtype == np.uint8, img.dtype
    noise = np.random.randn(*img.shape) * std
    noisy = (np.clip(img.astype(np.float) + noise.astype(np.float), 0, 255)).astype(np.uint8)
    return noisy

if is_testing(): imshow(imAddNoiseGauss(imNewWhite(150, 150), 30))


# In[86]:


if is_testing():
    imwrite('/tmp/img.jpg', imscaleNN(imNewNoise(100, 100), 2), jpeg_quality=1)
    imshow('/tmp/img.jpg')


# In[87]:


def imJpgDegradation(img, quality):
    assert img.dtype == np.uint8, img.dtype
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
    _, encimg = cv2.imencode('.jpg', img, encode_param)
    decimg = cv2.imdecode(encimg, 1)
    return decimg

#if is_testing(): imshow(imJpgDegradation(imread('http://via.placeholder.com/150.png'), 15))


# In[88]:


def imCropCenter(img, size):
    h, w, c = img.shape

    h_start = max(h // 2 - size // 2, 0)
    h_end = min(h_start + size, h)

    w_start = max(w // 2 - size // 2, 0)
    w_end = min(w_start + size, w)

    return img[h_start:h_end, w_start:w_end]


# In[89]:


#if is_testing(): 
#    imshow(imCropCenter(imread('http://via.placeholder.com/40.png'), 10))


# In[90]:


#if is_testing(): 
#    imshow(imCropCenter(imread('http://via.placeholder.com/40.png'), 49))


# In[91]:


#if is_testing(): 
#    imshow(imCropCenter(imread('http://via.placeholder.com/40.png'), 50))


# In[92]:


#if is_testing(): 
#    imshow(imCropCenter(imread('http://via.placeholder.com/40.png'), 100))


# In[93]:


def imCropRandom(img, size, auto_size=True):
    h, w, c = img.shape

    if auto_size and h <= size:
        h_start = 0
        h_end = h
    else:
        h_start = np.random.randint(0, h-size)
        h_end = h_start + size

    if auto_size and w <= size:
        w_start = 0
        w_end = w
    else:
        w_start = np.random.randint(0, w-size)
        w_end = w_start + size

    return img[h_start:h_end, w_start:w_end]


# In[94]:


#if is_testing(): 
#    imshow(imCropRandom(imread('http://via.placeholder.com/40.png'), 10))
#    imshow(imCropRandom(imread('http://via.placeholder.com/40.png'), 39))
#    imshow(imCropRandom(imread('http://via.placeholder.com/40.png'), 40))
#    imshow(imCropRandom(imread('http://via.placeholder.com/40.png'), 41))


# In[95]:


def draw_rect(img, h_beg, h_end, w_beg, w_end, line_width, color=(0, 0, 0)):
    h, w, _ = img.shape
    h_beg = max(h_beg, line_width)
    w_beg = max(w_beg, line_width)
    h_end = min(h_end, h - line_width)
    w_end = min(w_end, w - line_width)

    # top
    img[h_beg - line_width: h_beg, w_beg - line_width:w_end + line_width] = color
    # bottom
    img[h_end: h_end + line_width, w_beg - line_width:w_end + line_width] = color
    # left
    img[h_beg - line_width:h_end + line_width, w_beg - line_width: w_beg] = color
    # right
    img[h_beg - line_width:h_end + line_width, w_end: w_end + line_width] = color

    return img


def imCropRandomSeed(img, sizes, idx, crop_idx, use_crop=True, use_minimap=False, scale=1):
    randState = np.random.get_state()

    np.random.seed(idx)

    h, w, _ = img.shape
    for i in range(crop_idx + 1):
        h_start = np.random.randint(0, h - sizes[0])
        w_start = np.random.randint(0, w - sizes[1])

    h_end = h_start + sizes[0]
    w_end = w_start + sizes[1]

    np.random.set_state(randState)

    crop = img[h_start:h_end, w_start:w_end]
    crop = imscaleNN(crop, scale)

    if use_minimap:
        img = img.copy()
        img = draw_rect(img, h_start, h_end, w_start, w_end, line_width=30, color=(200, 50, 50))

        size = min(img.shape[0], img.shape[1])

        shape = [size, size]
        ends = [None, None]
        starts = [None, None]
        crop_centers = ((h_end - h_start) // 2 + h_start, (w_end - w_start) // 2 + w_start)

        for dim in [0, 1]:
            starts[dim] = crop_centers[dim] - shape[dim] // 2
            if starts[dim] < 0:
                starts[dim] = 0
                ends[dim] = starts[dim] + shape[dim]
            elif starts[dim] + shape[dim] > img.shape[dim]:
                starts[dim] = img.shape[dim] - shape[dim]
                ends[dim] = img.shape[dim]
            else:
                ends[dim] = starts[dim] + shape[dim]
            assert starts[dim] >= 0
            assert ends[dim] <= img.shape[dim]
            assert ends[dim] - starts[dim] == shape[dim]

        img = img[starts[0]:ends[0], starts[1]:ends[1]]

        minimap_shape = (int(scale * sizes[0]), int(scale * sizes[1]))
        minimap = cv2.resize(img, minimap_shape)

        if not use_crop:
            return minimap
        else:
            return imjoin([crop, minimap], pad=5)
    else:
        return crop


# In[96]:


if is_testing():
    img = imscaleNN(imNewNoise(10, 20), 10)
    imshow(imCropRandomSeed(img, (20, 20), idx=0, crop_idx=0, use_crop=True, use_minimap=True), scale=3)


# In[97]:


def imGallery(imgs, pad=0, n_cols=None, n_rows=None):
    imgs = [imread(img) for img in imgs] # load if path or url
    
    n = len(imgs)
    if isinstance(n_cols, int):
        if n_rows is not None:
            raise RuntimeError("Can only fix rows or columns")
        nw = n_cols
        nh = int(np.ceil(n / nw))
    elif isinstance(n_rows, int):
        if n_cols is not None:
            raise RuntimeError("Can only fix rows or columns")
        nh = n_rows
        nw = int(np.ceil(n / nh))
    else:
        nw = int(np.ceil(np.sqrt(n)))
        nh = int(np.ceil(n / nw))
        
    img_h, img_w, _ = imgs[0].shape
    w = nw * img_w + (nw - 1) * pad
    h = nh * img_h + (nh - 1) * pad

    assert imgs[0].dtype == np.uint8
    assert all([img.shape[0] == img_h for img in imgs])
    assert all([img.shape[1] == img_w for img in imgs])
    out = np.ones((h, w, 3), dtype=np.uint8) * 255

    idx = 0
    for ih in range(nh):
        for iw in range(nw):
            if idx + 1 > len(imgs):
                break
            w_beg = (iw + 0) * (img_w + pad)
            w_end = (iw + 1) * (img_w + pad) - pad
            h_beg = (ih + 0) * (img_h + pad)
            h_end = (ih + 1) * (img_h + pad) - pad
            out[h_beg:h_end, w_beg:w_end] = imgs[idx]
            idx += 1
    return out


# In[98]:


if is_testing():
    # List of images from back to white
    listOfDummyImagesBlackToWhite = [imNewBlack(10, 10) + 25 * i for i in range(10)]


# In[99]:


if is_testing():
    imshow(imGallery(listOfDummyImagesBlackToWhite[:1]))
    imshow(imGallery(listOfDummyImagesBlackToWhite[:2]))
    imshow(imGallery(listOfDummyImagesBlackToWhite[:2], pad=1))
    imshow(imGallery(listOfDummyImagesBlackToWhite[:5], pad=1))
    imshow(imGallery(listOfDummyImagesBlackToWhite[:9], pad=1))
    imshow(imGallery(listOfDummyImagesBlackToWhite[:10], pad=1))
    imshow(imGallery(listOfDummyImagesBlackToWhite[:10], pad=1, n_cols=3))
    imshow(imGallery(listOfDummyImagesBlackToWhite[:10], pad=1, n_rows=2))


# In[100]:


#if is_testing():
#    img40x20 = imread("http://via.placeholder.com/40x20.png")
#    imshow(imGallery([img40x20, img40x20, img40x20], pad=1))


# In[101]:


def imAddTextHeader(img, text, h=None, size=None):
    from PIL import Image, ImageDraw, ImageFont
    
    if h is None:
        h = int(np.ceil(img.shape[0] * 0.1))
    if size is None:
        size = h
    
    text_img = np.ones((h, img.shape[1], img.shape[2]), dtype=img.dtype) * 255
    im = Image.fromarray(text_img)
    
    draw = ImageDraw.Draw(im)
    
    w = text_img.shape[1]
    h = text_img.shape[0]
    centered=True
    middle = True
    text_width, text_height = draw.textsize(text)
    # Top left corner of text (w, h)
    draw.text((w/2 - (text_width/2) * centered, h/2 - text_height/2), text, fill="black")
    
    text = np.array(im)[:, :, :3]
    
    img = np.concatenate([text, img], axis=0)
    
    return img

if is_testing():
    imshow(imAddTextHeader(imNewBlack(100, 100), 'black image'))
    imshow(imAddTextHeader(imNewBlack(100, 100), 'black image'))


# # Video

# In[102]:


#def imgsToVid(imgs, file_name='out.avi'):
#    import cv2
#    frame = imgs[0]
#    height, width, layers = frame.shape
#
#    fourcc = cv2.VideoWriter_fourcc(*'DIVX')
#    video = cv2.VideoWriter(file_name, fourcc, 24, (width,height))
#
#    for image in imgs:
#        video.write(image[:, :, [2, 1, 0]])
#
#    cv2.destroyAllWindows()
#    video.release()
#    
#imgsToVid(frames, 'test.avi')


# In[103]:


#ffmpeg -framerate 1/5 -i img%03d.png -c:v libx264 -r 30 -pix_fmt yuv420p out.mp4


# In[104]:


def imsToMp4(path, imgs, time_per_image, frame_rate_output_video=30, verbose=0):
    with tempfile.TemporaryDirectory() as d:
        for idx, img in enumerate(imgs):
            imwrite(os.path.join(d, f"img{idx:09d}.png"), img)
        out = bash(f"cd {d} && ls && ffmpeg -framerate {1/time_per_image} -i img%09d.png -c:v libx264 -r 30 -pix_fmt yuv420p {path} -y")
        if verbose:
            print(out)

if is_testing():
    imgs = [imNewNoise(40, 40) for _ in range(48)]
    path = '/tmp/out.mp4'
    imsToMp4(path, imgs, 1/10, verbose=1)
    print(path)


# # pytorch

# In[105]:


def ptT(img_np_uint8):
    import torch
    img = img_np_uint8
    assert img.dtype == np.uint8, img.dtype
    return torch.Tensor(np.expand_dims(img.transpose([2, 0, 1]), 0) / 255.0).to(torch.float32)

def ptUint8(img_tensor):
    import torch
    img = img_tensor
    assert img.dtype == torch.float32, img.dtype
    return np.clip(img.detach().cpu().numpy()[0].transpose([1, 2, 0]) * 255, 0, 255).astype(np.uint8)
    


# In[106]:


if is_testing():
    iOrig = imNewWhite(10, 10)
    t = ptT(iOrig)
    i = ptUint8(t)
    print('iOrig', np.min(iOrig), np.max(iOrig), iOrig.shape, 't', t.min(), t.max(), t.shape, 'i', i.min(), i.max(), i.shape, 'err', np.mean(np.abs(iOrig - i)))


# # Files

# In[107]:


def _fiFindByWildcardSsh(wildcard):
    login, path = wildcard.split(':')
    paths = bash(f"ssh {login} 'ls {path}'")
    return [f'{login}:{p}' for p in natsort.natsorted(paths)]

def fiFindByWildcard(wildcard):
    if '@' in wildcard and ':' in wildcard:
        return _fiFindByWildcardSsh(wildcard)
    return natsort.natsorted(glob.glob(os.path.expanduser(wildcard), recursive=True))

def fiFindImgs(dir_path, recursive=False, ext='png'):
    if recursive:
        wildcard = os.path.join(dir_path, f'**/*.{ext}')
    else:
        wildcard = os.path.join(dir_path, f'*.{ext}')
    return fiFindByWildcard(wildcard)


# In[108]:


import os
from os.path import join as pjoin
from os.path import dirname as pdirname
from os.path import basename as pfilename
from os.path import isfile as pisfile
from os.path import isdir as pisdir
from os.path import expanduser as pexpanduser
def pfilenameNoExt(p):
    splits = pfilename(p).split('.')
    assert len(splits) <= 2
    return splits[0]

if is_testing():
    print(pjoin('/tmp/', 'file.txt'))
    print(pdirname('/tmp/file.txt'))
    print(pfilename('/tmp/file.txt'))
    print(pfilenameNoExt('/tmp/file.txt'))
    print(pexpanduser('~/tmp/file.txt'))


# In[109]:


if is_testing():
    with tempfile.TemporaryDirectory() as d:
        listOfDummyImagesBlackToWhite = [imNewBlack(10, 10) + 25 * i for i in range(10)]
        
        out_dir = os.path.join(d, "sub_dir")
        
        imgs_write = []
        for i in range(10):
            img = imNewBlack(10, 10) + 25 * i
            imwrite(os.path.join(out_dir, "{}.png".format(i)), img)
            imgs_write.append(img)
        
        print("written images:")
        imshow(imGallery(imgs_write))
        
        print("found images:")
        img_paths = fiFindByWildcard(os.path.join(out_dir, "*"))
        imgs = imsread(img_paths)
        imshow(imGallery(imgs))
        
        print("found images:")
        img_paths = fiFindByWildcard(os.path.join(d, "**/*.png"))
        imgs = imsread(img_paths)
        imshow(imGallery(imgs))


# In[110]:


def fiRemove(path):
    os.remove(path)

def fiRemoveDir(path):
    shutil.rmtree(path)

def fiIsEmptyDir(path):
    return len(os.listdir(path)) == 0

def fiSize(path):
    return os.path.getsize(path)

def fiSizeMb(path):
    return os.path.getsize(path) / 2**20

def fiAgeSeconds(path):
    return time.time() - os.stat(path)[stat.ST_MTIME]

def fiAgeMinutes(path):
    return (time.time() - os.stat(path)[stat.ST_MTIME]) / 60

def fiAgeHours(path):
    return (time.time() - os.stat(path)[stat.ST_MTIME]) / 3600


# In[111]:


if is_testing():
    with tempfile.TemporaryDirectory() as d:
        listOfDummyImagesBlackToWhite = [imNewBlack(10, 10) + 25 * i for i in range(10)]
        
        out_dir = os.path.join(d, "sub_dir")
        
        imgs_write = []
        img = imNewBlack(100, 100)
        img_path = os.path.join(out_dir, "1.png")
        imwrite(img_path, img)
        
        if not fiIsEmptyDir(out_dir):
            print("out_dir not empty\n")
        print("\n".join(fiFindByWildcard(os.path.join(d, "**", "*"))))
        print("size: " + str(fiSizeMb(img_path)) + " MB")
        print("age: " + str(fiAgeSeconds(img_path)) + 's')
        print("age: " + str(fiAgeMinutes(img_path)) + 'min')
        print("age: " + str(fiAgeHours(img_path)) + 'h')
        
        print('\nrm 1.png')
        fiRemove(os.path.join(d, "sub_dir", "1.png"))
        print("files:\n" + "\n".join(fiFindByWildcard(os.path.join(d, "**", "*"))))
        
        if fiIsEmptyDir(out_dir):
            print("\nRemove empty dir")
            fiRemoveDir(out_dir)
        print("files: " + "\n".join(fiFindByWildcard(os.path.join(d, "**", "*"))))


# In[112]:


def fiUnzip(zip_path, out_dir=None, remove=False):
    import zipfile, shutil
    out_dir = zip_path.replace(".zip", "") if out_dir is None else out_dir
    assert out_dir != zip_path, zip_path
    
    if remove:
        shutil.rmtree(out_dir, ignore_errors=True)
        
    with zipfile.ZipFile(zip_path, 'r') as zip:
        zip.extractall(out_dir)


# In[113]:


def fiJoin(*args):
    return os.path.join(*args)

if is_testing():
    print(fiJoin('path', 'to'))


# # Jupyter

# In[114]:


def jnSettings():
    print('mkdir -p $(jupyter --data-dir)/nbextensions && cd $(jupyter --data-dir)/nbextensions && git clone https://github.com/lambdalisue/jupyter-vim-binding vim_binding && jupyter nbextension enable vim_binding/vim_binding && cd -')
    print('pip3 install jupyter_contrib_nbextensions && jupyter contrib nbextension install --user && jupyter nbextension enable execute_time/ExecuteTime && jupyter nbextension enable code_prettify/code_prettify && jupyter nbextension enable cell_filter/cell_filter')

if is_testing():
    jnSettings()


# In[115]:


def jnNbFullWidth():
    from IPython.core.display import display, HTML
    display(HTML("<style>.container { width:100% !important; }</style>"))

def jnPandasSettings():
    pd.set_option('display.max_rows', 100000)
    pd.set_option('display.max_columns', 10000)
    pd.set_option('display.width', 100000)
    pd.set_option('display.max_colwidth', 100000)


# In[116]:


def jnImageRenderingPixelated():
    """Do not interpolate images"""
    display(HTML('<style type = text/css> img { image-rendering: pixelated; } </style>'))
    
def jnImageRenderingAuto():
    """Interpolate images"""
    display(HTML('<style type = text/css> img { image-rendering: auto; } </style>'))


# In[117]:


def jnDefault():
    jnNbFullWidth()
    jnPandasSettings()
    jnImageRenderingPixelated

if is_testing():
    jnDefault()


# In[ ]:





# In[118]:


def jnHtmlRow(strList, width=100):
    to_col = lambda x: '<td style="text-align:center">' + x + '</td>'
    display(HTML('<table width="{width}%"><tr>{cols}</tr></table>'.format(width=width, cols="".join(map(to_col, strList)))))

if is_testing():
    jnHtmlRow(['text', 'looooooooooooong text', 'text'])
    jnHtmlRow(['text', 'looooooooooooong text', 'text'], width=50)
    


# In[119]:


def jnImgToHtmlB64(img):
    img = imread(img)
    _, encimg = cv2.imencode('.png', img[:, :, [2, 1, 0]])
    imgB64 = base64.b64encode(encimg).decode('utf-8')
    img_tag = '<img src="data:image/png;base64,{0}" style="display:block; margin:0 auto;">'.format(imgB64)
    return img_tag

#def jnHtmlImgsRow(imgs, names=None):

def jnImageRow(imgs, names=None, width=100, external=False, title_img=None, title=None):
    if isinstance(imgs, OrderedDict):
        names, imgs = list(zip(*imgs.items()))
        
    _row = lambda x: '<tr>' + x + '</tr>'
    _col = lambda x: '<td style="text-align:center; word-wrap:break-word;">' + x + '</td>'
    _nacols = lambda x: prefix_name + "".join(map(_col, x))
    
    prefix_name = "" if title is None else _col(title)
    prefix_img = "" if title is None else _col("")

    if external:
        _imcols = lambda x: prefix_img + "".join(map(_col, map(lambda y: '<img src="{}" style="display:block; margin:0 auto;">'.format(y), x)))
    else:
        _imcols = lambda x: prefix_img + "".join(map(_col, map(jnImgToHtmlB64, x)))
        
    _tab = lambda x: '<table width="{width}%">'.format(width=width) + x + '</table>'
    
    header = "" if names is None else _row(_nacols(names))
    html = _tab(header + _row(_imcols(imgs)))
    display(HTML(html))


# In[120]:


if is_testing():
    jnImageRow(imgs=[imNewBlack(20, 20), imNewBlack(40, 20), imNewBlack(20, 800)], names=["longWordNoSpace"*10, "b", "c"])
   


# In[121]:


if is_testing():
    imgs = OrderedDict()
    imgs['a'] = "http://via.placeholder.com/40x20.png"
    imgs['b'] = "http://via.placeholder.com/40x20.png"
    jnImageRow(imgs, external=True, title='test')


# In[122]:



if is_testing():
   jnImageRow(imgs=[imNewBlack(20, 20), imNewBlack(40, 20), imNewBlack(20, 800)])


# In[123]:


#def dfDisplayWithImgs(df):
#    html = df.to_html()
#    urls = list(set([m.group() for m in re.finditer('http://[-\w/_\.]*\.(jpg|jpeg|png)', html)]))
#    html_out = html
#    for url in urls:
#        url_new = f"<img src='{url}'>"
#        html_out = html_out.replace(url, url_new)
#        assert url_new in html_out, url_ne
#    display(HTML(html_out))


# # GIT

# In[124]:


def gitGetHash():
    return shell('git rev-parse HEAD').strip()

if is_testing():
    print(gitGetHash())


# In[125]:


def gitGetBranch():
    return shell('git rev-parse --abbrev-ref HEAD').strip()

if is_testing():
    print(gitGetBranch())


# In[126]:


def gitGetMessage():
    return shell('git log --format=%B -n 1 HEAD').strip()

if is_testing():
    print(gitGetMessage())


# In[127]:


def gitGetAllFiles():
    return shell('git ls-tree -r --name-only HEAD').split("\n")

if is_testing():
    print(gitGetAllFiles())


# In[128]:


def gitListByTime(path=None):
    cd = '' if path is None else 'cd ' + path + ' &&'
    
    _time = lambda x: shell(cd + 'git log -1 --format="%ad" --date=raw -- {filename}'.format(filename=x))
    paths = shell(cd + 'git ls-tree -r --name-only HEAD').split("\n")
    times = list(map(_time, paths))
    
    return [path for _, path in sorted(zip(times, paths))]
    
if is_testing():
    print(gitListByTime()[-3:])


# In[129]:


def gitTime(path):
    _time = lambda x: shell('cd $(dirname {filename}) && git log -1 --format="%ad" -- {filename}'.format(filename=x)).replace("\n", "")
    return _time(path)
    
if is_testing():
    print(gitTime("__init__.py"))


# In[130]:


def gitTimeRaw(path):
    _time = lambda x: shell('cd $(dirname {filename}) && git log -1 --format="%ad" --date=raw -- {filename}'.format(filename=x)).replace("\n", "")
    return _time(path)
    
if is_testing():
    print(gitTimeRaw("__init__.py"))


# In[131]:


def shellSortDirsBySize():
    return shell('du -h | sort -h')

if is_testing():
    print(shellSortDirsBySize())


# # Package Files

# In[132]:


if is_testing():
    package_files = {}


# In[133]:


def shell(cmd):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE)
    return result.stdout.decode()


# In[134]:


if is_testing():
    package_files['setup.py'] = r"""from distutils.core import setup
setup(
  name = 'lx',         # How you named your package folder (MyLib)
  packages = ['lx'],   # Chose the same as "name"
  version = '{version}',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'lx',   # Give a short description about your library
  author = 'lx',                   # Type in your name
  author_email = 'hx2983113@gmail.com',      # Type in your E-Mail
  #url = 'https://github.com/hx2983113/lx',   # Provide either the link to your github or to your website
  #download_url = 'https://github.com/hx2983113/lx/archive/0.20.tar.gz',    # I explain this later on
  keywords = [],   # Keywords that define your package best
  install_requires=[
      {requirements}
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)""".format(requirements=", ".join(["'" + r + "'" for r in requirements]), version=version)


# In[135]:


if is_testing():
    package_files['setup.cfg'] = r"""# Inside of setup.cfg
[metadata]
description-file = README.md
"""


# In[136]:


if is_testing():
    package_files['LICENSE.txt'] = r"""MIT License
Copyright (c) 2018 YOUR NAME
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE."""


# In[137]:


if is_testing():
    package_files['README.md'] = ""


# In[138]:


if is_testing():
    shell("jupyter nbconvert --to script lx.ipynb")
    package_files['lx/__init__.py'] = txtread("lx.py")
    
    output = shell("""python3 -c 'import importlib; lx = importlib.import_module(name=".", package="lx"); print(lx.version)'""")
    print(output.strip(), 'Version correct: ', output.strip() == version, "(", output.strip(), version, ")")


# In[139]:


if is_testing():
    package_files['MANIFEST'] = r"""# file GENERATED by distutils, do NOT edit
setup.cfg
setup.py
lx/__init__.py
"""


# In[140]:


if is_testing():
    with tempfile.TemporaryDirectory() as d:
        for key, value in package_files.items():
            txtwrite(os.path.join(d, key), value)

        print("\n".join(fiFindByWildcard(os.path.join(d, '**/*'))))
        
        output = shell("""python3 -c 'import importlib; lx = importlib.import_module(name=".", package="lx"); print(lx.version)'""")
        print(output.strip(), 'Version correct: ', output.strip() == version, "(", output.strip(), version, ")")
        
        if output.strip() == version:
            #print(shell("cd {d} && git status && git config user.name 'lx' && git config user.email 'lx' && git commit -a -m 'Add' && git log && git push && python setup.py sdist && twine upload dist/* --verbose".format(d=d)))
            print("\n".join(bash("cd {d} && python setup.py sdist && ~/miniconda3/bin/python -m twine upload dist/* --verbose".format(d=d))))


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




