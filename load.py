import tensorflow as tf
# 重新创建完全相同的模型，包括其权重和优化程序
import pickle

xtrainFile = open('./xtrain.pickle', 'rb')
xtrain = pickle.load(xtrainFile)
xtrainFile.close()

ytrainFile = open('./ytrain.pickle', 'rb')
ytrain = pickle.load(ytrainFile)
ytrainFile.close()

xtestFile = open('./xtest.pickle', 'rb')
xtest = pickle.load(xtestFile)
xtestFile.close()

ytestFile = open('./ytest.pickle', 'rb')
ytest = pickle.load(ytestFile)
ytestFile.close()
new_model = tf.keras.models.load_model('my_model.h5')
loss, acc = new_model.evaluate(xtest,  ytest, verbose=2)
print("Restored model, accuracy: {:5.2f}%".format(100*acc))