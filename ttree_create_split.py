import ROOT
from array import array
from numpy import mean, median, sqrt, std, random

frac_train = .7 #free parameter to separate our data into one tree for training and one tree for testing

signal = ROOT.TFile("signal.root") #Original files to extract from
signaltree = signal.Get("NDKAna/Event")
background = ROOT.TFile("background.root")
backgroundtree = background.Get("NDKAna/Event")

train_tfile = ROOT.TFile( "ML_train.root", "RECREATE" )# new file to fill

signal_train_ttree = ROOT.TTree( "signal_train", "signal" ) #trees in training file
background_train_ttree = ROOT.TTree( "background_train", "background" )

test_tfile = ROOT.TFile("ML_test.root", "RECREATE" ) #if you declare tfiles in the wrong place ROOT breaks

signal_test_ttree = ROOT.TTree( "signal_test", "signal" )
background_test_ttree = ROOT.TTree( "background_test", "background" )

def rms(input_list): #calculates the root mean square of a list
	quad = 0
	for entry in input_list:
		quad += entry**2
	return sqrt(quad/len(input_list))

dEdx_s_1 = array( 'f', [0] ) #initializing arrays to fill with data to write to the TTrees
dEdx_s_2 = array( 'f', [0] )
dEdx_s_3 = array( 'f', [0] )
dEdx_s_4 = array( 'f', [0] )
dEdx_s_5 = array( 'f', [0] )
dEdx_s_6 = array( 'f', [0] )
dEdx_s_7 = array( 'f', [0] )
dEdx_s_8 = array( 'f', [0] )
dEdx_s_9 = array( 'f', [0] )
dEdx_s_10 = array( 'f', [0] )
dEdx_s_minus_1 = array( 'f', [0] )
dEdx_s_minus_2 = array( 'f', [0] )
dEdx_s_minus_3 = array( 'f', [0] )
dEdx_s_minus_4 = array( 'f', [0] )
dEdx_s_minus_5 = array( 'f', [0] )
dEdx_s_minus_6 = array( 'f', [0] )
dEdx_s_minus_7 = array( 'f', [0] )
dEdx_s_minus_8 = array( 'f', [0] )
dEdx_s_minus_9 = array( 'f', [0] )
dEdx_s_minus_10 = array( 'f', [0] )
s_longest_track = array( 'f', [0] )
s_shortest_track = array( 'f', [0] )
s_len_dEdx = array( 'f', [0] )

s_mean_dE_dx = array('f', [0] )
s_median_dE_dx = array('f', [0] )
s_RMS_dE_dx = array('f', [0] )
s_std_dE_dx = array('f', [0] )

s_n_showers = array('f', [0])
s_EM_e = array('f', [0])
s_trk_e = array('f', [0])

signal_train_ttree.Branch('dEdx_first', dEdx_s_1, 'dEdx_1/F' ) #adding branches to the ttrees
signal_train_ttree.Branch('dEdx_second', dEdx_s_2, 'dEdx_2/F' )
signal_train_ttree.Branch('dEdx_third', dEdx_s_3, 'dEdx_3/F' )
signal_train_ttree.Branch('dEdx_fourth', dEdx_s_4, 'dEdx_4/F' )
signal_train_ttree.Branch('dEdx_fifth', dEdx_s_5, 'dEdx_5/F' )
signal_train_ttree.Branch('dEdx_sixth', dEdx_s_6, 'dEdx_6/F' )
signal_train_ttree.Branch('dEdx_seventh', dEdx_s_7, 'dEdx_7/F' )
signal_train_ttree.Branch('dEdx_eighth', dEdx_s_8, 'dEdx_8/F' )
signal_train_ttree.Branch('dEdx_ninth', dEdx_s_9, 'dEdx_9/F' )
signal_train_ttree.Branch('dEdx_tenth', dEdx_s_10, 'dEdx_10/F' )
signal_train_ttree.Branch('dEdx_last', dEdx_s_minus_1, 'dEdx_-1/F' )
signal_train_ttree.Branch('dEdx_second_to_last', dEdx_s_minus_2, 'dEdx_-2/F' )
signal_train_ttree.Branch('dEdx_third_to_last', dEdx_s_minus_3, 'dEdx_-3/F' )
signal_train_ttree.Branch('dEdx_fourth_to_last', dEdx_s_minus_4, 'dEdx_-4/F' )
signal_train_ttree.Branch('dEdx_fifth_to_last', dEdx_s_minus_5, 'dEdx_-5/F' )
signal_train_ttree.Branch('dEdx_sixth_to_last', dEdx_s_minus_6, 'dEdx_-6/F' )
signal_train_ttree.Branch('dEdx_seventh_to_last', dEdx_s_minus_7, 'dEdx_-7/F' )
signal_train_ttree.Branch('dEdx_eighth_to_last', dEdx_s_minus_8, 'dEdx_-8/F' )
signal_train_ttree.Branch('dEdx_ninth_to_last', dEdx_s_minus_9, 'dEdx_-9/F' )
signal_train_ttree.Branch('dEdx_tenth_to_last', dEdx_s_minus_10, 'dEdx_-10/F' )
signal_train_ttree.Branch('suspected_muon', s_longest_track, 'suspected_muon/F' ) #We fill this with the longest track since we are assuming that the muon track will be the longest one
signal_train_ttree.Branch('shortest_track', s_shortest_track, 'shortest_track/F' )
signal_train_ttree.Branch('len_dEdx', s_len_dEdx, 'len_dEdx/F' )

signal_train_ttree.Branch('mean', s_mean_dE_dx, 'mean/F')
signal_train_ttree.Branch('median', s_median_dE_dx, 'median/F')
signal_train_ttree.Branch('RMS', s_RMS_dE_dx, 'RMS/F')
signal_train_ttree.Branch('std', s_std_dE_dx, 'std/F')

signal_train_ttree.Branch('n_showers', s_n_showers, 'n_showers/F')
signal_train_ttree.Branch('EM_e', s_EM_e, 'EM_e/F')
signal_train_ttree.Branch('trk_e', s_trk_e, 'trk_e/F')

signal_test_ttree.Branch('dEdx_first', dEdx_s_1, 'dEdx_1/F' )
signal_test_ttree.Branch('dEdx_second', dEdx_s_2, 'dEdx_2/F' )
signal_test_ttree.Branch('dEdx_third', dEdx_s_3, 'dEdx_3/F' )
signal_test_ttree.Branch('dEdx_fourth', dEdx_s_4, 'dEdx_4/F' )
signal_test_ttree.Branch('dEdx_fifth', dEdx_s_5, 'dEdx_5/F' )
signal_test_ttree.Branch('dEdx_sixth', dEdx_s_6, 'dEdx_6/F' )
signal_test_ttree.Branch('dEdx_seventh', dEdx_s_7, 'dEdx_7/F' )
signal_test_ttree.Branch('dEdx_eighth', dEdx_s_8, 'dEdx_8/F' )
signal_test_ttree.Branch('dEdx_ninth', dEdx_s_9, 'dEdx_9/F' )
signal_test_ttree.Branch('dEdx_tenth', dEdx_s_10, 'dEdx_10/F' )
signal_test_ttree.Branch('dEdx_last', dEdx_s_minus_1, 'dEdx_-1/F' )
signal_test_ttree.Branch('dEdx_second_to_last', dEdx_s_minus_2, 'dEdx_-2/F' )
signal_test_ttree.Branch('dEdx_third_to_last', dEdx_s_minus_3, 'dEdx_-3/F' )
signal_test_ttree.Branch('dEdx_fourth_to_last', dEdx_s_minus_4, 'dEdx_-4/F' )
signal_test_ttree.Branch('dEdx_fifth_to_last', dEdx_s_minus_5, 'dEdx_-5/F' )
signal_test_ttree.Branch('dEdx_sixth_to_last', dEdx_s_minus_6, 'dEdx_-6/F' )
signal_test_ttree.Branch('dEdx_seventh_to_last', dEdx_s_minus_7, 'dEdx_-7/F' )
signal_test_ttree.Branch('dEdx_eighth_to_last', dEdx_s_minus_8, 'dEdx_-8/F' )
signal_test_ttree.Branch('dEdx_ninth_to_last', dEdx_s_minus_9, 'dEdx_-9/F' )
signal_test_ttree.Branch('dEdx_tenth_to_last', dEdx_s_minus_10, 'dEdx_-10/F' )
signal_test_ttree.Branch('suspected_muon', s_longest_track, 'suspected_muon/F' )
signal_test_ttree.Branch('shortest_track', s_shortest_track, 'shortest_track/F' )
signal_test_ttree.Branch('len_dEdx', s_len_dEdx, 'len_dEdx/F' )

signal_test_ttree.Branch('mean', s_mean_dE_dx, 'mean/F')
signal_test_ttree.Branch('median', s_median_dE_dx, 'median/F')
signal_test_ttree.Branch('RMS', s_RMS_dE_dx, 'RMS/F')
signal_test_ttree.Branch('std', s_std_dE_dx, 'std/F')

signal_test_ttree.Branch('n_showers', s_n_showers, 'n_showers/F')
signal_test_ttree.Branch('EM_e', s_EM_e, 'EM_e/F')
signal_test_ttree.Branch('trk_e', s_trk_e, 'trk_e/F')

for entry in signaltree:
	cut = False
	#or deposit in entry.track_dE_dx:
		#if deposit > 200: #cut on unreasonably high energy deposits
			#cut = True
	if entry.n_reco_tracks != 2: #if the number of reconstructed tracks isn't 2, skip
		cut = True
	if cut == True:
		continue

	if entry.track_mcPDG[0] != -13 and entry.track_mcPDG[0] != 321:
		cut = True
	elif entry.track_mcPDG[1] != -13 and entry.track_mcPDG[1] != 321: #restricts to p Knu decay case
		cut = True
	if cut == True:
		continue

	longest = 0.
	longestidx = -1 # last by default
	for i in xrange(entry.n_reco_tracks): #determines the longest track and its length, along with beginning/ending information
		if entry.track_length[i] > longest:
			longestidx = i
			longest = entry.track_length[i]
			mu_start = ROOT.TVector3( entry.track_startX[i], entry.track_startY[i], entry.track_startZ[i] )
			mu_end = ROOT.TVector3( entry.track_endX[i], entry.track_endY[i], entry.track_endZ[i] ) #vector defining the longest and therefore the muon track
	
	s_longest_track[0] = longest

	shortest = longest #initialization
	shortestidx = 0 #by default
	for i in xrange(entry.n_reco_tracks): #determines the shortest track and its length
		if entry.track_length[i] < shortest:
			shortestidx = i
			shortest = entry.track_length[i]
			
	s_shortest_track[0] = shortest

	if entry.idx_cal_end[shortestidx] - entry.idx_cal_start[shortestidx] < 10: #cut on track length
		cut = True
	if cut == True:
		continue

	list_dE_dx = []
	for x in xrange(entry.idx_cal_start[shortestidx],entry.idx_cal_end[shortestidx]):
		list_dE_dx.append(entry.track_dE_dx[x]) #only appends the proton/kaon dEdx hits to our list

	length = len(list_dE_dx)

	p_start = ROOT.TVector3( entry.track_startX[shortestidx], entry.track_startY[shortestidx], entry.track_startZ[shortestidx] )
	p_end = ROOT.TVector3( entry.track_endX[shortestidx], entry.track_endY[shortestidx], entry.track_endZ[shortestidx] )

	min_start = min( (p_start-mu_start).Mag(), (p_end-mu_start).Mag() )
	min_end = min( (p_start-mu_end).Mag(), (p_end-mu_end).Mag() )

	if min_start < min_end: # muon direction is correct, which we don't directly care about but is relevant to deciding if proton/kaon direction is correct
		if (p_start-mu_start).Mag() > (p_end-mu_start).Mag(): # proton is backwards
			list_dE_dx.reverse()
	else: # track is near muon endpoint, so muon must be backwards
		if (p_start-mu_end).Mag() > (p_end-mu_end).Mag(): # proton is backwards
			list_dE_dx.reverse()

	s_len_dEdx[0] = float(length)

	s_n_showers[0] = entry.n_showers
	s_EM_e[0] = entry.Em_e
	s_trk_e = entry.trk_e

	dEdx_s_1[0] = list_dE_dx[0] #filling the dEdx nodes from our properly oriented and preselected list
	dEdx_s_2[0] = list_dE_dx[1]
	dEdx_s_3[0] = list_dE_dx[2]
	dEdx_s_4[0] = list_dE_dx[3]
	dEdx_s_5[0] = list_dE_dx[4]
	dEdx_s_6[0] = list_dE_dx[5]
	dEdx_s_7[0] = list_dE_dx[6]
	dEdx_s_8[0] = list_dE_dx[7]
	dEdx_s_9[0] = list_dE_dx[8]
	dEdx_s_10[0] = list_dE_dx[9]
	dEdx_s_minus_1[0] = list_dE_dx[length-1]
	dEdx_s_minus_2[0] = list_dE_dx[length-2]
	dEdx_s_minus_3[0] = list_dE_dx[length-3]
	dEdx_s_minus_4[0] = list_dE_dx[length-4]
	dEdx_s_minus_5[0] = list_dE_dx[length-5]
	dEdx_s_minus_6[0] = list_dE_dx[length-6]
	dEdx_s_minus_7[0] = list_dE_dx[length-7]
	dEdx_s_minus_8[0] = list_dE_dx[length-8]
	dEdx_s_minus_9[0] = list_dE_dx[length-9]
	dEdx_s_minus_10[0] = list_dE_dx[length-10]

	
	del list_dE_dx[length-10:length]
	del list_dE_dx[0:10] #remove end nodes from list because we want the "average" nodes to condense the middle of the data into just a couple of points

	if len(list_dE_dx) > 0:
		s_mean_dE_dx[0] = mean(list_dE_dx)
		s_median_dE_dx[0] = median(list_dE_dx)
		s_RMS_dE_dx[0] = rms(list_dE_dx)
		s_std_dE_dx[0] = std(list_dE_dx)

	else:
		s_mean_dE_dx[0] = 0
		s_median_dE_dx[0] = 0
		s_RMS_dE_dx[0] = 0
		s_std_dE_dx[0] = 0

	if random.random() < frac_train: #sort data into the two files
		signal_train_ttree.Fill()
	else:
		signal_test_ttree.Fill()

dEdx_b_1 = array( 'f', [0] ) #this is a carbon copy of the above 200 lines of code, but for the background trees
dEdx_b_2 = array( 'f', [0] )
dEdx_b_3 = array( 'f', [0] )
dEdx_b_4 = array( 'f', [0] )
dEdx_b_5 = array( 'f', [0] )
dEdx_b_6 = array( 'f', [0] )
dEdx_b_7 = array( 'f', [0] )
dEdx_b_8 = array( 'f', [0] )
dEdx_b_9 = array( 'f', [0] )
dEdx_b_10 = array( 'f', [0] )
dEdx_b_minus_1 = array( 'f', [0] )
dEdx_b_minus_2 = array( 'f', [0] )
dEdx_b_minus_3 = array( 'f', [0] )
dEdx_b_minus_4 = array( 'f', [0] )
dEdx_b_minus_5 = array( 'f', [0] )
dEdx_b_minus_6 = array( 'f', [0] )
dEdx_b_minus_7 = array( 'f', [0] )
dEdx_b_minus_8 = array( 'f', [0] )
dEdx_b_minus_9 = array( 'f', [0] )
dEdx_b_minus_10 = array( 'f', [0] )
b_longest_track = array( 'f', [0] )
b_shortest_track = array( 'f', [0] )
b_len_dEdx = array( 'f', [0] )

b_mean_dE_dx = array('f', [0] )
b_median_dE_dx = array('f', [0] )
b_RMS_dE_dx = array('f', [0] )
b_std_dE_dx = array('f', [0] )

b_n_showers = array('f', [0])
b_EM_e = array('f', [0])
b_trk_e = array('f', [0])

background_train_ttree.Branch('dEdx_first', dEdx_b_1, 'dEdx_1/F' )
background_train_ttree.Branch('dEdx_second', dEdx_b_2, 'dEdx_2/F' )
background_train_ttree.Branch('dEdx_third', dEdx_b_3, 'dEdx_3/F' )
background_train_ttree.Branch('dEdx_fourth', dEdx_b_4, 'dEdx_4/F' )
background_train_ttree.Branch('dEdx_fifth', dEdx_b_5, 'dEdx_5/F' )
background_train_ttree.Branch('dEdx_sixth', dEdx_b_6, 'dEdx_6/F' )
background_train_ttree.Branch('dEdx_seventh', dEdx_b_7, 'dEdx_7/F' )
background_train_ttree.Branch('dEdx_eighth', dEdx_b_8, 'dEdx_8/F' )
background_train_ttree.Branch('dEdx_ninth', dEdx_b_9, 'dEdx_9/F' )
background_train_ttree.Branch('dEdx_tenth', dEdx_b_10, 'dEdx_10/F' )
background_train_ttree.Branch('dEdx_last', dEdx_b_minus_1, 'dEdx_-1/F' )
background_train_ttree.Branch('dEdx_second_to_last', dEdx_b_minus_2, 'dEdx_-2/F' )
background_train_ttree.Branch('dEdx_third_to_last', dEdx_b_minus_3, 'dEdx_-3/F' )
background_train_ttree.Branch('dEdx_fourth_to_last', dEdx_b_minus_4, 'dEdx_-4/F' )
background_train_ttree.Branch('dEdx_fifth_to_last', dEdx_b_minus_5, 'dEdx_-5/F' )
background_train_ttree.Branch('dEdx_sixth_to_last', dEdx_b_minus_6, 'dEdx_-6/F' )
background_train_ttree.Branch('dEdx_seventh_to_last', dEdx_b_minus_7, 'dEdx_-7/F' )
background_train_ttree.Branch('dEdx_eighth_to_last', dEdx_b_minus_8, 'dEdx_-8/F' )
background_train_ttree.Branch('dEdx_ninth_to_last', dEdx_b_minus_9, 'dEdx_-9/F' )
background_train_ttree.Branch('dEdx_tenth_to_last', dEdx_b_minus_10, 'dEdx_-10/F' )
background_train_ttree.Branch('suspected_muon', b_longest_track, 'suspected_muon/F' )
background_train_ttree.Branch('shortest_track', b_shortest_track, 'shortest_track/F' )
background_train_ttree.Branch('len_dEdx', b_len_dEdx, 'len_dEdx/F' )

background_train_ttree.Branch('mean', b_mean_dE_dx, 'mean/F')
background_train_ttree.Branch('median', b_median_dE_dx, 'median/F')
background_train_ttree.Branch('RMS', b_RMS_dE_dx, 'RMS/F')
background_train_ttree.Branch('std', b_std_dE_dx, 'std/F')

background_train_ttree.Branch('n_showers', b_n_showers, 'n_showers/F')
background_train_ttree.Branch('EM_e', b_EM_e, 'EM_e/F')
background_train_ttree.Branch('trk_e', b_trk_e, 'trk_e/F')

background_test_ttree.Branch('dEdx_first', dEdx_b_1, 'dEdx_1/F' )
background_test_ttree.Branch('dEdx_second', dEdx_b_2, 'dEdx_2/F' )
background_test_ttree.Branch('dEdx_third', dEdx_b_3, 'dEdx_3/F' )
background_test_ttree.Branch('dEdx_fourth', dEdx_b_4, 'dEdx_4/F' )
background_test_ttree.Branch('dEdx_fifth', dEdx_b_5, 'dEdx_5/F' )
background_test_ttree.Branch('dEdx_sixth', dEdx_b_6, 'dEdx_6/F' )
background_test_ttree.Branch('dEdx_seventh', dEdx_b_7, 'dEdx_7/F' )
background_test_ttree.Branch('dEdx_eighth', dEdx_b_8, 'dEdx_8/F' )
background_test_ttree.Branch('dEdx_ninth', dEdx_b_9, 'dEdx_9/F' )
background_test_ttree.Branch('dEdx_tenth', dEdx_b_10, 'dEdx_10/F' )
background_test_ttree.Branch('dEdx_last', dEdx_b_minus_1, 'dEdx_-1/F' )
background_test_ttree.Branch('dEdx_second_to_last', dEdx_b_minus_2, 'dEdx_-2/F' )
background_test_ttree.Branch('dEdx_third_to_last', dEdx_b_minus_3, 'dEdx_-3/F' )
background_test_ttree.Branch('dEdx_fourth_to_last', dEdx_b_minus_4, 'dEdx_-4/F' )
background_test_ttree.Branch('dEdx_fifth_to_last', dEdx_b_minus_5, 'dEdx_-5/F' )
background_test_ttree.Branch('dEdx_sixth_to_last', dEdx_b_minus_6, 'dEdx_-6/F' )
background_test_ttree.Branch('dEdx_seventh_to_last', dEdx_b_minus_7, 'dEdx_-7/F' )
background_test_ttree.Branch('dEdx_eighth_to_last', dEdx_b_minus_8, 'dEdx_-8/F' )
background_test_ttree.Branch('dEdx_ninth_to_last', dEdx_b_minus_9, 'dEdx_-9/F' )
background_test_ttree.Branch('dEdx_tenth_to_last', dEdx_b_minus_10, 'dEdx_-10/F' )
background_test_ttree.Branch('suspected_muon', b_longest_track, 'suspected_muon/F' )
background_test_ttree.Branch('shortest_track', b_shortest_track, 'shortest_track/F' )
background_test_ttree.Branch('len_dEdx', b_len_dEdx, 'len_dEdx/F' )

background_test_ttree.Branch('mean', b_mean_dE_dx, 'mean/F')
background_test_ttree.Branch('median', b_median_dE_dx, 'median/F')
background_test_ttree.Branch('RMS', b_RMS_dE_dx, 'RMS/F')
background_test_ttree.Branch('std', b_std_dE_dx, 'std/F')

background_test_ttree.Branch('n_showers', b_n_showers, 'n_showers/F')
background_test_ttree.Branch('EM_e', b_EM_e, 'EM_e/F')
background_test_ttree.Branch('trk_e', b_trk_e, 'trk_e/F')

for entry in backgroundtree:
	cut = False
	#for deposit in entry.track_dE_dx:
		#if deposit > 200: #cut on unreasonably high energy deposits
			#cut = True
	if entry.n_reco_tracks != 2: #if the number of reconstructed tracks isn't 2, skip
		cut = True
	if cut == True:
		continue
	
	longest = 0.
	longestidx = -1 # last by default
	for i in xrange(entry.n_reco_tracks): #determines the longest track and its length, along with beginning/ending information
		if entry.track_length[i] > longest:
			longestidx = i
			longest = entry.track_length[i]
			mu_start = ROOT.TVector3( entry.track_startX[i], entry.track_startY[i], entry.track_startZ[i] )
			mu_end = ROOT.TVector3( entry.track_endX[i], entry.track_endY[i], entry.track_endZ[i] ) #vector defining the longest and therefore the muon track
	
	b_longest_track[0] = longest

	shortest = longest #initialization
	shortestidx = 0 #by default
	for i in xrange(entry.n_reco_tracks): #determines the shortest track and its length
		if entry.track_length[i] < shortest:
			shortestidx = i
			shortest = entry.track_length[i]
			
	b_shortest_track[0] = shortest

	if entry.idx_cal_end[shortestidx] - entry.idx_cal_start[shortestidx] < 10: #cut on track length
		cut = True
	if cut == True:
		continue

	list_dE_dx = []
	for x in xrange(entry.idx_cal_start[shortestidx],entry.idx_cal_end[shortestidx]):
		list_dE_dx.append(entry.track_dE_dx[x]) #only appends the proton/kaon dEdx hits to our list

	length = len(list_dE_dx)

	p_start = ROOT.TVector3( entry.track_startX[shortestidx], entry.track_startY[shortestidx], entry.track_startZ[shortestidx] )
	p_end = ROOT.TVector3( entry.track_endX[shortestidx], entry.track_endY[shortestidx], entry.track_endZ[shortestidx] )

	min_start = min( (p_start-mu_start).Mag(), (p_end-mu_start).Mag() )
	min_end = min( (p_start-mu_end).Mag(), (p_end-mu_end).Mag() )

	if min_start < min_end: # muon direction is correct, which we don't directly care about but is relevant to deciding if proton/kaon direction is correct
		if (p_start-mu_start).Mag() > (p_end-mu_start).Mag(): # proton is backwards
			list_dE_dx.reverse()
	else: # track is near muon endpoint, so muon must be backwards
		if (p_start-mu_end).Mag() > (p_end-mu_end).Mag(): # proton is backwards
			list_dE_dx.reverse()

	b_len_dEdx[0] = float(length)

	b_n_showers[0] = entry.n_showers
	b_EM_e[0] = entry.Em_e
	b_trk_e = entry.trk_e

	dEdx_b_1[0] = list_dE_dx[0]
	dEdx_b_2[0] = list_dE_dx[1]
	dEdx_b_3[0] = list_dE_dx[2]
	dEdx_b_4[0] = list_dE_dx[3]
	dEdx_b_5[0] = list_dE_dx[4]
	dEdx_b_6[0] = list_dE_dx[5]
	dEdx_b_7[0] = list_dE_dx[6]
	dEdx_b_8[0] = list_dE_dx[7]
	dEdx_b_9[0] = list_dE_dx[8]
	dEdx_b_10[0] = list_dE_dx[9]
	dEdx_b_minus_1[0] = list_dE_dx[length-1]
	dEdx_b_minus_2[0] = list_dE_dx[length-2]
	dEdx_b_minus_3[0] = list_dE_dx[length-3]
	dEdx_b_minus_4[0] = list_dE_dx[length-4]
	dEdx_b_minus_5[0] = list_dE_dx[length-5]
	dEdx_b_minus_6[0] = list_dE_dx[length-6]
	dEdx_b_minus_7[0] = list_dE_dx[length-7]
	dEdx_b_minus_8[0] = list_dE_dx[length-8]
	dEdx_b_minus_9[0] = list_dE_dx[length-9]
	dEdx_b_minus_10[0] = list_dE_dx[length-10]

	
	del list_dE_dx[length-10:length]
	del list_dE_dx[0:10] #remove end nodes from list to condense middle nodes into the data

	if len(list_dE_dx) > 0:
		b_mean_dE_dx[0] = mean(list_dE_dx)
		b_median_dE_dx[0] = median(list_dE_dx)
		b_RMS_dE_dx[0] = rms(list_dE_dx)
		b_std_dE_dx[0] = std(list_dE_dx)

	else:
		b_mean_dE_dx[0] = 0
		b_median_dE_dx[0] = 0
		b_RMS_dE_dx[0] = 0
		b_std_dE_dx[0] = 0

	if random.random() < frac_train:
		background_train_ttree.Fill()
	else:
		background_test_ttree.Fill()

train_tfile.cd()
signal_train_ttree.Write()
background_train_ttree.Write()

test_tfile.cd()
signal_test_ttree.Write()
background_test_ttree.Write()

print "%d out of %d events included in Signal Training Tree" % (signal_train_ttree.GetEntries(), signaltree.GetEntries())
print "%d out of %d events included in Signal Training Tree" % (background_train_ttree.GetEntries(), backgroundtree.GetEntries())