from docx import Document

class word_reader:
	def __init__(self):
		pass

	def read(self, path):
		'''
		Opens a word file, extracts text data

		inputs: str, a path to a PDF file
		outputs: str, a string of all the text in the pdf that could be extracted.
		'''
		document = Document(path)
		return '\n'.join(paragraph.text for paragraph in document.paragraphs)