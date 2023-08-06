from setuptools import setup

name = "docdump"

setup(
	name=name,
	version='1.0.4',
	author = "Grant Holtes",
	author_email = "gwholes@gmail.com",
	url = "https://github.com/Gholtes/docdump",
	keywords = ["nlp", "text processing", "document", "pdf", "Microsoft office", "text"],
	packages=[name],
	install_requires=[
		"PyPDF2",
		"openpyxl",
		"python-docx",
		"python-pptx"
	],
	license="MIT",
	description='A package to extract text from common document types.',
	long_description_content_type='text/markdown',
	long_description=open('README.md', 'r').read()
)