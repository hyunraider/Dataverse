import wikipedia
import csv

csv_file = open("wiki_data.csv", "ab")
writer = csv.writer(csv_file)

while(True):
  the_input = raw_input("Keyword: ")
  
  if (the_input == "kek"):
    break
  wiki_page = wikipedia.page(the_input)
  
  title = wiki_page.title
  url = wiki_page.url
  summary = wiki_page.content
  categories = wiki_page.categories
  imageurl = wiki_page.images[0]

  summary = summary.split('\n')
  summary = summary[0].encode('ascii','replace')

  writer.writerow([title, url, summary, categories, imageurl])

