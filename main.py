from PyPDF2 import PdfReader
import os
import csv
import re

phone_number_regex = "((\+\d{1,3})?\s?\(?\d{1,4}\)?[\s.-]?\d{3}[\s.-]?\d{4})"
rows = [["NAME", "EMAIL", "PHONE"]]

for filename in os.listdir('./resumes'):
	name = filename.split('.')[0]
	email = ''
	phone = ''
	reader = PdfReader(f'./resumes/{filename}')
	for page in reader.pages:
		text = page.extract_text()
		for line in text.splitlines():
			if line.startswith('Contact Email: '):
				email = line.split(' ')[2]
			if line.startswith('Mobile: '):
				phone = line[8:]
			if line.startswith('Home: ') and phone == '':
				phone = line[6:]
			if line.startswith(': ') and (num := re.search(phone_number_regex, line)) and phone == '':
				phone = line[2:]
	phone = phone.strip()
	email = email.strip()
	name = name.strip()
	if email == '':
		print(f"Warning: No email found for {name}")
	if phone == '':
		print(f"Warning: No phone found for {name}")
	rows.append([name,email,phone])

outfile = open('output.csv','w+', newline='')
writer = csv.writer(outfile)
writer.writerows(rows)
outfile.close()
