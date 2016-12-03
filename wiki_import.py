import wikipedia
import csv

months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

def det_exc(category):
  if "Articles" in category:
    return True
  elif "articles" in category:
    return True
  elif "introduction" in category:
    return True
  elif "Introduction" in category:
    return True
  elif "NPOV" in category:
    return True
  elif "Webarchive" in category:
    return True
  elif "pages" in category:
    return True
  elif "Pages" in category:
    return True
  elif "EngvarB" in category:
    return True
  elif "EngvarA" in category:
    return True
  elif "Wikipedia" in category:
    return True
  elif "Wikidata" in category:
    return True
  elif "Accuracy" in category:
    return True
  elif "accuracy" in category:
    return True
  elif "Interlanguage" in category:
    return True
  elif any(x in category for x in months):
    return True
  elif category[0:4] == "Use ":
    return True
  elif category[0:3] == "CS1":
    return True
  elif category[0:8] == "Commons ":
    return True
  elif category[0:6] == "Vague ":
    return True
  else:
    return False

csv_file = open("wiki_data.csv", "w", newline='')
writer = csv.writer(csv_file)

csv_cat = open("wiki_cat.csv", "w", newline='')
writer_cat = csv.writer(csv_cat)

input_file = open("wiki_input.txt", "r")

#cat_dict = {}

for line in input_file:
  #the_input = input("Keyword: ")

  the_input = line.rstrip()
  
  wiki_page = wikipedia.page(the_input)
  
  title = wiki_page.title
  url = wiki_page.url
  summary = wiki_page.content
  categories = wiki_page.categories
  images = wiki_page.images
  if (images):
    imageurl = images[0]
  else:
    imageurl = ''

  exclude_these = []
  for category in categories:
    if (det_exc(category) == True):
      exclude_these.append(category)
      continue
#    if category in cat_dict:
#      cat_dict[category] += 1
#    else:
#      cat_dict[category] = 1
    
  categories = [cat for cat in categories if cat not in exclude_these]
  
  summary = summary.split('\n')
  summary = summary[0].encode('ascii','replace')

  writer.writerow([title, url, summary, imageurl])
  
  for category in categories:
    writer_cat.writerow([title, category])

csv_file.close()
csv_cat.close()
#cat_file = open("wiki_categories.txt", "w")

#for k, v in cat_dict.items():
#  cat_file.write("{}\n".format(k))
