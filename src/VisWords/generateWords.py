import numpy as np
from sklearn.cluster import KMeans
import h5py

def generateWords(featureH5File, groups, saveFile, wordsNum, feaDim=128):
    f = h5py.File(featureH5File, 'r')
    f_w = h5py.File(saveFile, 'w')
    feaSet = f.get('feaSet')

    for i in range(len(groups)):
        c = groups[i]
        if isinstance(c, str):
            feas = None
            feas = feaSet.get(c)
            feas = np.array(feas, dtype='float64')
            print 'cluctering class ' + c + ' with shape ' + str(feas.shape)

        if isinstance(c, list):
            feas = np.empty((0, feaDim), dtype='float64')
            for cs in c:
                feat = feaSet.get(cs)
                feat = np.array(feat, dtype='float64')
                feas = np.append(feas, feat, axis=0)
                print 'cluctering class ' + cs + ' with shape ' + str(feas.shape)

        kmeans = None
        Kmeans = KMeans(n_clusters=wordsNum, n_jobs=-1)
        Kmeans.fit(feas)
        cluster_centers = Kmeans.cluster_centers_
        inertia = Kmeans.inertia_
        cc = f_w.create_group(str(i+1))
        cc.attrs['inertia'] = inertia
        cc.create_dataset('words', cluster_centers.shape, 'f', cluster_centers)
    print saveFile + ' saved'
    return 0

if __name__ == '__main__':
    siftFeaFile = '../../Data/Features/type3_SIFTFeatures_256.hdf5'
    wordsNum = 500
    groups_h1 = ['1', ['2', '3']]
    groups_h2 = ['2', '3']
    f = h5py.File(siftFeaFile, 'r')
    for name in f:
        print name
    feaSet = f.get('feaSet')
    for c in feaSet:
        print c + str(feaSet[c].shape)

    saveFolder = '../../Data/Features/'
    saveName_h1 = 'SIFTWords_h1_256.hdf5'
    saveName_h2 = 'SIFTWords_h2_256.hdf5'
    generateWords(siftFeaFile, groups_h1, saveFolder+saveName_h1, wordsNum)
    generateWords(siftFeaFile, groups_h2, saveFolder+saveName_h2, wordsNum)
