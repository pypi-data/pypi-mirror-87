class txt_reader:
	def __init__(self):
		pass

	def read(self, path):
		'''
		Opens a .txt file, extracts text data

		inputs: str, a path to a PDF file
		outputs: str, a string of all the text in the pdf that could be extracted.
		'''
		return open(path).read()
