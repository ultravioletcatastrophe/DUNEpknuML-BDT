from ROOT import TMVA, TFile, TString
from array import array
import ROOT

data = TFile.Open('ML_test.root')
signal = data.Get('signal_test')
background = data.Get('background_test') #load data to evaluate our model against it

TMVA.Tools.Instance()
TMVA.PyMethodBase.PyInitialize() #need this to make reader work goddamn it fuck what a waste of time
reader = TMVA.Reader("Color:!Silent")

branches = {}
for branch in signal.GetListOfBranches():
	branchName = branch.GetName()
	branches[branchName] = array('f', [0]) #WHY???? you can't add double arrays to reader for some reason
	reader.AddVariable(branchName, branches[branchName])
	signal.SetBranchAddress(branchName, branches[branchName])
	background.SetBranchAddress(branchName, branches[branchName])

reader.BookMVA("PyKeras","dataset/weights/TMVAClassification_PyKeras.weights.xml") #load our weights

hist_signal = ROOT.TH1D("output","Blue=Signal, Red=Background;EvaluateMVA;Probability",200,0,1)
hist_background = ROOT.TH1D("output_b","", 200,0,1)

sig = 0
max_sig = 0
for i in xrange(signal.GetEntries()):
	signal.GetEntry(i)
	k = reader.EvaluateMVA("PyKeras")
	#print "Signal " + str(k)
	hist_signal.Fill(k)
	#sig += k
	#if k > max_sig:
		#max_sig = k

bkg = 0
max_bkg = 0
for i in xrange(background.GetEntries()):
	background.GetEntry(i)
	k = reader.EvaluateMVA("PyKeras")
	#if k <= .75 and k >= .65:
		#print k
		#print branches
	#print "Background " + str(k)
	hist_background.Fill(k)
	#bkg += k
	#if k > max_bkg:
		#max_bkg = k

"""print ""
print "Average EvaluateMVA output for Signal: " + str(sig/signal.GetEntries())
print "Average EvaluateMVA output for Background: " + str(bkg/background.GetEntries())
print ""
print "Maximum EvaluateMVA output for Signal: " + str(max_sig)
print "Maximum EvaluateMVA output for Background: " + str(max_bkg)
print ""
"""
hist_signal.Scale(1./hist_signal.Integral()) #normalization
hist_background.Scale(1./hist_background.Integral())

bins = 200
cut_signal = ROOT.TH1D("cut","Blue=Signal, Red=Background;Cut location;Efficiency",bins,0,1)
cut_background = ROOT.TH1D("cut_background","",bins,0,1)
for x in xrange(bins+1): #check indexing
	cut_signal.SetBinContent(x,hist_signal.Integral(x,bins))
	cut_background.SetBinContent(x,hist_background.Integral(x,bins))

c = ROOT.TCanvas()
hist_signal.Draw("hist")
hist_background.SetLineColor(ROOT.kRed)
hist_background.Draw("hist same")
c.Print("eff.png")

cut_signal.Draw("hist")
cut_background.SetLineColor(ROOT.kRed)
cut_background.Draw("hist same")
c.SetLogy()
#cut_signal.SetMinimum(.00005)#TK
c.Print("cut efficiency.png")

g = ROOT.TGraph()
g.GetXaxis().SetTitle( 'Signal Efficiency' )
g.GetYaxis().SetTitle( 'Background Rejection' )
for b in xrange(bins+1):
	x = hist_signal.Integral(b,bins)
	y = hist_background.Integral(b,bins)
	g.SetPoint( b, x, y )
g.Draw("APC")
#g.SetMinimum(.00005)
c.Print("signalvbackground.png")