from PyPDF2 import PdfFileReader

class pdf_reader:
	def __init__(self):
		pass

	def read(self, path):
		'''
		Opens a pdf file, extracts text data

		inputs: str, a path to a PDF file
		outputs: str, a string of all the text in the pdf that could be extracted.

		runtime ~= 0.05sec per pdf
		'''
		text_dump = []
		with open(path, "rb") as f:
			reader = PdfFileReader(f, strict=False) #strict = False; suppress warnings as some can be fatal

			for page in reader.pages:
				text_dump.append(page.extractText())

		return " ".join(text_dump)

		
