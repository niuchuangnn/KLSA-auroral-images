import numpy as np
import src.VisWords.VisWordsAnalysis as vwa
import matplotlib.pyplot as plt
import src.local_feature.extractDSiftFeatures as extSift
import src.util.paseLabeledFile as plf
import h5py
from scipy.misc import imread, imresize
import copy
import sys
sys.path.insert(0, '../../caffe/python')
import caffe
import src.local_feature.autoencoder as AE
import src.preprocess.esg as esg
import src.local_feature.extractSDAEFeatures as extSDAE
import src.local_feature.extractLBPFeatures as extlbp

def genImgLocalFeas(imgFile, feaType, gridSize, sizeRange, imResize=None, sdaePara=None):

    if feaType == 'SIFT':
        feaVectors, posVectors = extSift.calImgDSift(imgFile, gridSize, sizeRange, imResize=imResize)

    if feaType == 'LBP':
        feaVectors, posVectors = extlbp.calImgLBPFeatures(imgFile, gridSize, sizeRange, imResize=None)

    if feaType == 'SDAE':
        weight = sdaePara['weight']
        net = sdaePara['net']
        meanFile = sdaePara['meanFile']
        inputShape = sdaePara['inputShape']
        channels = inputShape[1]

        f_mean = open(meanFile, 'r')
        patch_mean = float(f_mean.readline().split(' ')[1])
        f_mean.close()

        with open(net, 'w') as f1:
            layerNeuronNum = sdaePara['layerNeuronNum']
            f1.write(str(AE.defineTestNet(inputShape, layerNeuronNum)))

        caffe.set_mode_gpu()
        model = caffe.Net(net, weight, caffe.TEST)

        feaVectors, posVectors = extSDAE.calImgSDAEFea(imgFile, model, gridSize, sizeRange, channels, patch_mean)

    return feaVectors, posVectors

if __name__ == '__main__':
    labelFile = '../../Data/balanceSampleFrom_one_in_minute.txt'
    imagesFolder = '../../Data/labeled2003_38044/'
    imgType = '.bmp'
    gridSize = np.array([10, 10])
    sizeRange = (28, 28)
    imResize = (256, 256)

    imgName = 'N20031223G125731'
    imgFile = imagesFolder + imgName + imgType

    # define SDAE parameters
    sdaePara = {}
    sdaePara['weight'] = '../../Data/autoEncoder/final_0.01.caffemodel'
    sdaePara['net'] = '../../Data/autoEncoder/test_net.prototxt'
    sdaePara['meanFile'] = '../../Data/patchData_mean.txt'
    channels = 1
    layerNeuronNum = [28 * 28, 2000, 1000, 500, 128]
    sdaePara['layerNeuronNum'] = layerNeuronNum
    _, gl, _ = esg.generateGridPatchData(imgFile, gridSize, sizeRange)
    batchSize = len(gl)
    inputShape = (batchSize, channels, 28, 28)
    sdaePara['inputShape'] = inputShape

    feas_sift, pos_sift = genImgLocalFeas(imgFile, 'SIFT', gridSize, sizeRange)
    feas_lbp, pos_lbp = genImgLocalFeas(imgFile, 'LBP', gridSize, sizeRange)
    feas_sdae, pos_sdae = genImgLocalFeas(imgFile, 'SDAE', gridSize, sizeRange, sdaePara=sdaePara)