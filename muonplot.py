import ROOT
from ROOT import TFile

signal = ROOT.TFile("signal.root") #Original files to extract from
signaltree = signal.Get("NDKAna/Event")
background = ROOT.TFile("background.root")
backgroundtree = background.Get("NDKAna/Event")

hist_signal = ROOT.TH1D("output","Blue=Signal, Red=Background;Track Length;Probability",200,0,250)
hist_background = ROOT.TH1D("output_b","", 200,0,250)

#max_sig = 0
for entry in signaltree:
	if entry.n_reco_tracks != 2:
		continue
	if entry.track_mcPDG[0] != -13 and entry.track_mcPDG[0] != 321:
		continue
	elif entry.track_mcPDG[1] != -13 and entry.track_mcPDG[1] != 321: #restricts to p Knu decays
		continue
	longest = 0.
	for i in xrange(entry.n_reco_tracks): #determines the longest track and its length, along with beginning/ending information
		if entry.track_length[i] > longest:
			longest = entry.track_length[i]
	
	hist_signal.Fill(longest)
	#if longest > max_sig:
		#max_sig = longest

#max_bkg = 0
for entry in backgroundtree:
	if entry.n_reco_tracks != 2:
		continue
	longest = 0.
	for i in xrange(entry.n_reco_tracks): #determines the longest track and its length, along with beginning/ending information
		if entry.track_length[i] > longest:
			longest = entry.track_length[i]
	
	hist_background.Fill(longest)
	#if longest > max_bkg:
		#max_bkg = longest

#print max_sig
#print max_bkg

hist_signal.Scale(1./hist_signal.Integral()) #normalization
hist_background.Scale(1./hist_background.Integral())

c = ROOT.TCanvas() #printing histograms
hist_signal.Draw("hist")
hist_background.SetLineColor(ROOT.kRed)
hist_background.Draw("hist same")
c.Print("muon.png")