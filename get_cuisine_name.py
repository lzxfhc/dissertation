import pandas as pd
import wikipediaapi

#/////////Get a list of all cuisines names in wikipedia//////////

wiki_wiki = wikipediaapi.Wikipedia('en')
cuisine_list = []
def print_categorymembers(categorymembers, level=0, max_level=6):
    for c in categorymembers.values():
        if c.ns == 0:
            print("%s: %s (ns: %d)" % ("*" * (level + 1), c.title, c.ns))
            # print("%s: %s" % ("*" * (level + 1), c.title))
            cuisine_list.append(c.title)

        if c.ns == wikipediaapi.Namespace.CATEGORY and level < max_level:
            print_categorymembers(c.categorymembers, level=level + 1, max_level=max_level)


cat = wiki_wiki.page("Category:Foods by cooking technique")
# print("Category members: Cuisine by country")
print_categorymembers(cat.categorymembers)
cuisine_name = pd.DataFrame({'cuisine_name':cuisine_list})
cuisine_name.to_csv('/Users/chrisx/Desktop/cuisine_name.csv')
