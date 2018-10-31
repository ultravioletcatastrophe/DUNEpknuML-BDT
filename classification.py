from ROOT import TMVA, TFile, TTree, TCut
import ROOT

from keras.metrics import binary_accuracy
from keras.models import Sequential
from keras.layers.core import Dense, Activation
from keras.regularizers import l2
from keras.optimizers import SGD
from keras import initializers
import keras.backend as K #for custom metrics
#from keras.callbacks import ModelCheckpoint # for custom callbacks
from keras import models #to load the model back in along with the custom metrics

# Setup TMVA
TMVA.Tools.Instance()
TMVA.PyMethodBase.PyInitialize()

output = TFile.Open('Classification.root', 'RECREATE')
factory = TMVA.Factory('TMVAClassification', output,
         '!V:!Silent:Color:DrawProgressBar:Transformations=D,G:AnalysisType=Classification')
 
data = TFile.Open('ML_train.root')
signal = data.Get('signal_train')
background = data.Get('background_train')

dataloader = TMVA.DataLoader('dataset')
n = 0
for branch in signal.GetListOfBranches():
    dataloader.AddVariable(branch.GetName()) #loading data    
    n += 1
dataloader.AddSignalTree(signal, 1.0) ### second arg is weight
dataloader.AddBackgroundTree(background, 1.0)
dataloader.PrepareTrainingAndTestTree(TCut(''),
		'nTrain_Signal=25000:nTrain_Background=6716:SplitMode=Random:NormMode=NumEvents:!V') # controlling training populations
        #'nTest_Signal=2000:nTest_Background=2000:SplitMode=Random:NormMode=NumEvents:!V') # controlling testing populations

# Define model
model = Sequential()

model.add(Dense(23, kernel_initializer='glorot_uniform', activation='relu', input_dim=n)) #kernel_regularizer=l2(1e-5)
model.add(Dense(2, kernel_initializer='glorot_uniform', activation='softmax'))

# Set loss and optimizer
#model.compile(loss='categorical_crossentropy', optimizer=SGD(lr=0.01), metrics=['accuracy',])
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])#'accuracy' goes to categorical, 'binary_accuracy' goes to binary

# Store model to file
model.save('model.h5')
#model.summary()
 
#factory.BookMethod(dataloader, TMVA.Types.kFisher, 'Fisher',
        #'!H:!V:Fisher')
factory.BookMethod(dataloader, TMVA.Types.kPyKeras, 'PyKeras',
        'H:!V:VarTransform=D,G:FilenameModel=model.h5:NumEpochs=20:BatchSize=32') #:VarTransform=D,G

# Run training, test and evaluation
factory.TrainAllMethods()
factory.TestAllMethods()
#factory.EvaluateAllMethods()