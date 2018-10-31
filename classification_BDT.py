from ROOT import TMVA, TFile, TTree, TCut
import ROOT

# Setup TMVA
TMVA.Tools.Instance()
TMVA.PyMethodBase.PyInitialize()

output = TFile.Open('Classification.root', 'RECREATE')
factory = TMVA.Factory('TMVAClassification', output,
         '!V:!Silent:Color:DrawProgressBar:Transformations=D,G:AnalysisType=Classification')
 
data = TFile.Open('ML_train.root')
signal = data.Get('signal_train') #naming things signal breaks ROOT
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
		### numbers here chosen to keep nTrain_Signal/Total_Train = n_Test_Signal/Total_Test (equal ratios)
        #'nTest_Signal=2000:nTest_Background=2000:SplitMode=Random:NormMode=NumEvents:!V') # controlling testing populations
 
factory.BookMethod(dataloader, TMVA.Types.kBDT, "BDT", "MaxDepth=5:NTrees=1600:BoostType=AdaBoost:AdaBoostBeta=0.5" ) 

# Run training, test and evaluation
factory.TrainAllMethods()
factory.TestAllMethods()