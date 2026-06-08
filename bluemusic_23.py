import wave, numpy, os
from _func_wav import *

def do_blue_23(filename):
	revpol = samplereverpol('Blue (23).wav', 122)
	#outdata, outhash = outcomb(revpol)

	#for x, y in outhash.items():
	#	oy = y[0]
	#	outfile = 'blue_23/%i_%i.wav' % (oy[0], oy[1])
	#	data = revpol.get_revpol_fixed(oy[0], oy[1])
	#	to_wav(outfile, data, revpol)

	inst_slaps = revpol.get_revpol_fixed(11, 15)
	to_wav('blue_23_inst/inst_slaps.wav', inst_slaps, revpol)

	inst_wao = revpol.get_revpol_fixed(11, 27)
	to_wav('blue_23_inst/inst_wao.wav', inst_wao, revpol)

	comb_bassslaps = revpol.get_revpol_fixed(11, 16)
	inst_bass = comb_bassslaps-inst_slaps
	to_wav('blue_23_inst/inst_bass.wav', inst_bass, revpol)

	comb_high_predrum = revpol.get_revpol_fixed(7, 8)
	comb_high_predrum_revcrash = revpol.get_revpol_fixed(7, 9)
	inst_revcrash = comb_high_predrum-comb_high_predrum_revcrash
	to_wav('blue_23_inst/inst_revcrash.wav', inst_revcrash, revpol)
	
	comb_high_revcrash = revpol.get_revpol_fixed(2, 14)
	inst_high = -(comb_high_revcrash+inst_revcrash)
	to_wav('blue_23_inst/inst_high.wav', inst_high, revpol)

	comb_saw_bass = revpol.get_revpol_fixed(10, 21)
	inst_saw = -(comb_saw_bass-inst_bass)
	to_wav('blue_23_inst/inst_saw.wav', inst_saw, revpol)

	comb_hicrash_bass = revpol.get_revpol_fixed(4, 17)
	inst_hicrash = (comb_hicrash_bass+inst_bass)
	to_wav('blue_23_inst/inst_hicrash.wav', inst_hicrash, revpol)

	wip = revpol.get_fixedbar(29).copy()
	val75 = int(len(wip)*0.75)
	wip -= inst_wao
	wip -= inst_bass
	wip -= inst_slaps
	inst_crash = wip[:val75]
	to_wav('blue_23_inst/inst_crash.wav', inst_crash, revpol)

	wip = revpol.get_fixedbar(35).copy()
	val75 = int(len(wip)*0.75)
	wip -= inst_wao
	wip -= inst_saw
	wip -= inst_hicrash
	wip[:val75] -= inst_slaps[:val75]
	wip[:val75] -= inst_bass[:val75]
	inst_predrum = wip[val75:]
	to_wav('blue_23_inst/inst_predrum.wav', inst_predrum, revpol)

	wip = revpol.get_fixedbar(24).copy()
	wip -= inst_high
	wip[:val75] -= inst_crash[:val75]
	wip[val75:] -= inst_predrum
	comb_hiloop = wip
	to_wav('blue_23_inst/comb_hiloop.wav', comb_hiloop, revpol)

	wip = revpol.get_fixedbar(3).copy()
	wip -= comb_hiloop
	wip -= inst_revcrash
	inst_locrash = wip
	to_wav('blue_23_inst/inst_locrash.wav', inst_locrash, revpol)



os.makedirs('blue_23_inst', exist_ok=True)
do_blue_23('Blue (23).wav')


#to_wav('outwav.wav', data)
