#coding:utf-8 
import math
import sys
import numpy as np
import pickle
# 采用TF-IDF 算法对选取得到的特征进行计算权重
DocumentCount = 200 # 每个类别选取200篇文档

ClassCode = ['C000007', 'C000008', 'C000010', 'C000013','C000014', 'C000016', 'C000020', 'C000022', 'C000024']
# 构建每个类别的词Set
# 分词后的文件路径
textCutBasePath = sys.path[0] + "/SogouCC/"
def readFeature(featureName):
    featureFile = open(featureName, 'r')
    featureContent = featureFile.read().split('\n')
    featureFile.close()
    feature = list()
    for eachfeature in featureContent:
        eachfeature = eachfeature.split(" ")
        if (len(eachfeature)==2):
            feature.append(eachfeature[1])
    return feature

# 读取所有类别的训练样本到字典中,每个文档是一个list
def readFileToList(textCutBasePath, ClassCode, DocumentCount):
    dic = dict()
    for eachclass in ClassCode:
        currClassPath = textCutBasePath + eachclass + "/"
        eachclasslist = list()
        for i in range(DocumentCount):
            eachfile = open(currClassPath+str(i)+".cut")
            eachfilecontent = eachfile.read()
            eachfilewords = eachfilecontent.split(" ")
            eachclasslist.append(eachfilewords)
            # print(eachfilewords)
        dic[eachclass] = eachclasslist
    return dic

# 计算特征的逆文档频率
def featureIDF(dic, feature, dffilename):

    totaldoccount=DocumentCount*len(ClassCode)

    dffile = open(dffilename, "w")
    dffile.close()
    dffile = open(dffilename, "a")
    idffeature = dict()
    dffeature = dict()
    for eachfeature in feature:
        docfeature = 0
        for key in dic:
            classfiles = dic[key]
            for eachfile in classfiles:
                if eachfeature in eachfile:
                    docfeature = docfeature + 1
        # 计算特征的逆文档频率
        featurevalue = math.log(float(totaldoccount)/(docfeature+1))
        dffeature[eachfeature] = docfeature
        # 写入文件，特征的文档频率
        dffile.write(eachfeature + " " + str(docfeature)+"\n")
        idffeature[eachfeature] = featurevalue
    dffile.close()
    return idffeature

# 计算Feature's TF-IDF 值
def TFIDFCal(feature, dic,idffeature):
    tfidf_data = []
    train_label = []
    for key in dic:
        classFiles = dic[key]
        # 谨记字典的键是无序的
        classid = ClassCode.index(key)
        for eachfile in classFiles:
            # 对每个文件进行特征向量转化
            docfeature_value = [0]*len(feature)

            for i in range(len(feature)):
                if feature[i] in eachfile:
                    currentfeature = feature[i]
                    featurecount = eachfile.count(feature[i])
                    tf = float(featurecount)/(len(eachfile))
                    # 计算逆文档频率
                    featurevalue = idffeature[currentfeature]*tf
                    docfeature_value[i]=featurevalue

            tfidf_data.append(docfeature_value)
            train_label.append(classid)
    return tfidf_data,train_label

dic = readFileToList(textCutBasePath, ClassCode, DocumentCount)
feature = readFeature("SVMFeature.txt")
#print(len(feature))
idffeature = featureIDF(dic, feature, "dffeature.txt")
tfidf_data,train_label=TFIDFCal(feature, dic,idffeature)
pickle.dump(tfidf_data,open('tfidf_data.pkl','wb'))
pickle.dump(train_label,open('train_label.pkl','wb'))


tfidf_data=np.array(tfidf_data)
np.savetxt('tfidf_data.txt',tfidf_data)
# file=open('tfidf_data.dat','wb')
# file.write(str(tfidf_data))
# file.close()
