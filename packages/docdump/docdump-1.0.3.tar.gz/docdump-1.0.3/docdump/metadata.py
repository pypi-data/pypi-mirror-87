from argparse import ArgumentParser
from datetime import datetime as dt
from xml.etree import ElementTree as etree

import zipfile

from openpyxl import load_workbook

from PyPDF2 import PdfFileReader

class pdf_metadata:
	def __init__(self):
		pass

	def read(self, path):
		pdf = PdfFileReader(open(path, "rb"), strict=False)
		pdf_info = pdf.getDocumentInfo()
		return str(pdf_info)

class excel_metadata:
	def __init__(self):
		pass

	def read(self, path):
		try:
			workbook = load_workbook(filename=path, data_only=True) 
			#data only ensure that the value of the formula is imported not the formula itself
		except ValueError:
			raise ValueError("Workbook could not be loaded: {0}".format(path))

		metadata_raw = workbook.properties

		metadata = {}

		for attribute in str(metadata_raw).split(","):
			if "=" in attribute and not ("openpyxl" in attribute):
				split_attribute = attribute.split("=")
				if split_attribute[1] != "None":
					metadata[split_attribute[0]] = split_attribute[1]
		
		return metadata

class word_ppt_metadata:
	def __init__(self):
		pass

	def read(self, path):
		if not zipfile.is_zipfile(path):
			return None

		zfile = zipfile.ZipFile(path)
		print(zfile.namelist())
		core_xml = etree.fromstring(zfile.read('docProps/core.xml'))
		app_xml = etree.fromstring(zfile.read('docProps/app.xml'))

		metadata = {}

		core_mapping = {
			'title': 'Title',
			'subject': 'Subject',
			'creator': 'Author(s)',
			'keywords': 'Keywords',
			'description': 'Description',
			'lastModifiedBy': 'Last Modified By',
			'modified': 'Modified Date',
			'created': 'Created Date',
			'category': 'Category',
			'contentStatus': 'Status',
			'revision': 'Revision'
		}

		for element in list(core_xml):
			for key, title in core_mapping.items():
				if key in element.tag:
					if 'date' in title.lower():
						text = dt.strptime(element.text, "%Y-%m-%dT%H:%M:%SZ")
					else:
						text = element.text
					
					metadata[title] = text

		app_mapping = {
			'TotalTime': 'Edit Time (minutes)',
			'Pages': 'Page Count',
			'Words': 'Word Count',
			'Characters': 'Character Count',
			'Lines': 'Line Count',
			'Paragraphs': 'Paragraph Count',
			'Company': 'Company',
			'HyperlinkBase': 'Hyperlink Base',
			'Slides': 'Slide count',
			'Notes': 'Note Count',
			'HiddenSlides': 'Hidden Slide Count',
		}
		for element in list(app_xml):
			for key, title in app_mapping.items():
				if key in element.tag:
					if 'date' in title.lower():
						text = dt.strptime(element.text, "%Y-%m-%dT%H:%M:%SZ")
					else:
						text = element.text
					
					metadata[title] = text
	
		return metadata

