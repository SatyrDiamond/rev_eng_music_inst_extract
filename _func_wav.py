import wave, numpy

def to_wav(outfile, data, revpol):
	with wave.open(outfile, "w") as f:
		f.setnchannels(revpol.wav_channels)
		f.setsampwidth(revpol.wav_sampwidth)
		f.setframerate(revpol.wav_hz)
		f.writeframes(data.tobytes())

def outcomb(revpol):
	outhash = {}
	outdata = {}

	fixedbar = revpol.totalbars_fixed().__floor__()

	totald = []

	for x in range(fixedbar):
		for y in range(fixedbar):
			if [y, x] in totald or y==x:
				pass
			else:
				data = revpol.get_revpol_fixed(x, y)
				ohash = data.tobytes().__hash__().to_bytes(8, 'big', signed=True).hex()
				if ohash not in outhash: 
					outdata[ohash] = data
					outhash[ohash] = []
				outhash[ohash].append([x, y])
				totald.append([x, y])

	return outdata, outhash


class samplereverpol:
	def __init__(self, filename, tempo):
		wavfile = wave.open(filename, mode='rb')
		self.tempo = tempo
		self.wav_hz = wavfile.getframerate()
		self.wav_channels = wavfile.getnchannels()
		self.wav_sampwidth = wavfile.getsampwidth()
		self.wav_data = wavfile.readframes(wavfile.getnframes())
		self.wav_data = numpy.frombuffer(self.wav_data, numpy.int16 if self.wav_sampwidth==2 else numpy.int8)
		self.wav_data = self.wav_data.reshape([-1, self.wav_channels])
		self.fixedbar = 8
		self.tempmul = self.tempo/120

	def get_bar(self, pos, size):
		start = (pos/self.tempmul)*self.wav_hz
		end = ((pos+size)/self.tempmul)*self.wav_hz
		bar = ((size/self.tempmul)*self.wav_hz).__ceil__()
		return self.wav_data[int(start):(int(start)+bar)]

	def get_fixedbar(self, pos):
		return self.get_bar(self.fixedbar*pos, self.fixedbar)

	def get_revpol_fixed(self, pos, target):
		firstd = self.get_fixedbar(pos)
		secondd = self.get_fixedbar(target)
		return firstd-secondd

	def totalbars(self):
		return (len(self.wav_data)/self.wav_hz)*self.tempmul

	def totalbars_fixed(self):
		return ((len(self.wav_data)/self.wav_hz)/self.fixedbar)*self.tempmul
