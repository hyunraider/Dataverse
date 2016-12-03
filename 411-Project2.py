import csv
'''
csv_file = open("wiki_data.csv")

for cur in csv_file:
	list = cur.split(',')
	print list[1]
'''
csv_file = open("wiki_data.category.csv", "ab")
writer = csv.writer(csv_file)

file = open('wiki_data.csv',"r")

for cur in file:
	i = cur.split(',"')
	parse = i[1]
	parse = parse.strip('[')
	parse = parse.strip(']')
	parse = parse.replace(']"','')

	element = parse.split(', ')
	for it in element:
		writer.writerow([i[0], it])



	#writer.writerow([i[0], url, summary, categories, imageurl])
	
