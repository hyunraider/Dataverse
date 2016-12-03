import wikipedia
my_list = open("wiki_input.txt").read().split('\n')

wiki_input = open("wiki_input.txt", "a")
while(True):
    usr_input = input("Input new keyword ('Quit' to quit): ")
    if (usr_input == "Quit"):
        break
    if (usr_input in my_list):
        print("{} is already in the database".format(usr_input))
        continue
    try:
        wiki_page = wikipedia.page(usr_input)
    except:
        print("{} does not exist in Wikipedia".format(usr_input))
        continue
    
    wiki_input.write("{}\n".format(usr_input))

wiki_input.close()
