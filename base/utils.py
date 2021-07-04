import mutagen



def get_duration(file):
	source = mutagen.File(file)
	return source.info.length

