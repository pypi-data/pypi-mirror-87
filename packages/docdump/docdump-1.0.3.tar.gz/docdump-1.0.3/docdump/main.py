from docdump.word import word_reader
from docdump.powerpoint import powerpoint_reader
from docdump.excel import excel_reader
from docdump.pdf import pdf_reader
from docdump.text import txt_reader
from docdump.metadata import *

import os

class doc_reader:
	def __init__(self, doc_path):
		self.filename = doc_path
		self.path = os.path.abspath(doc_path)
		self.filetype = self._get_filetype()
		self.text = self._get_text()
		self.metadata = self._get_metadata()

	def _get_text(self):
		type_ = self.filetype
		return self._read(self.path, type_)

	def _get_metadata(self):
		type_ = self.filetype
		return self._read_metadata(self.path, type_)

	def _get_filetype(self):
		ext_to_type = {
			"docx":"word",
			"doc":"word",
			"pptx":"powerpoint",
			"ppt":"powerpoint",
			"xlsx":"excel",
			"xlsm":"excel",
			"xls":"excel",
			"pdf":"pdf",
			"txt":"txt"
		}
		try:
			type_ = ext_to_type[self.path.split(".")[-1]]
		except KeyError:
			raise ValueError("file type not recognised. Please only use file extentions: {0}".format(ext_to_type.keys()))
		return type_

	def _read(self, doc_path, type_):
		if type_ == "word":
			reader = word_reader()
		elif type_ == "powerpoint":
			reader = powerpoint_reader()
		elif type_ == "excel":
			reader = excel_reader()
		elif type_ == "pdf":
			reader = pdf_reader()
		elif type_ == "txt":
			reader = txt_reader()
		else:
			return None

		return reader.read(doc_path)
	
	def _read_metadata(self, doc_path, type_):
		if type_ in ["word", "powerpoint"]:
			metadata_reader = word_ppt_metadata()
		elif type_ == "excel":
			metadata_reader = excel_metadata()
		elif type_ == "pdf":
			metadata_reader = pdf_metadata()
		else:
			return None
		
		return metadata_reader.read(doc_path)

