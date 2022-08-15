import re
import pandas as pd

cuision_pd = pd.read_excel('infobox_data_cleared.xlsx')
for a in range(len(cuision_pd)):
    if len(cuision_pd['country'][a]) > 40 :
        cuision_pd = cuision_pd.drop(index = a)

cuision_pd = cuision_pd.reset_index(drop = True)


def country_split():                       # Segmentation of the country column for cuision data
    clear_list = [",","also"]
    country_clist = cuision_pd['country']  # the column of data clear dataset
    for t in range(len(country_clist)):
        try:
            country_clist[t] = country_clist[t].replace("|",",").replace("*",",").replace("<br>",",")
            country_clist[t] = country_clist[t].replace((re.findall(r'\(.+?\)',country_clist[t]))[0],'')
        except:
            pass

    for i in range(len(country_clist)):
        for n in range(len(clear_list)):
            try:
                if clear_list[n] in country_clist[i]:
                    country_clist[i] = country_clist[i].split(clear_list[n])
            except:
                pass

    return country_clist


def continent_identify(country_list_path, data_source):       # country_list_path is the path of the country list Excel table data
    data_total = pd.read_excel(country_list_path)           # data_source is the data source of the recipe to be processed, note that it is a list or dataframe sequence
    itct_list_df = pd.read_excel(country_list_path, usecols=['Region Name'])
    sub_region_list_df = pd.read_excel(country_list_path, usecols=['Sub-region Name'])
    inter_list_df = pd.read_excel(country_list_path, usecols=['Intermediate Region Name'])
    ct_list_df = data_total['Country or Area']
    b = list(enumerate(ct_list_df))
    a = {}
    for i, j in b:
        a[j] = i
    c_ct_df = data_source
    c_ct = c_ct_df.values.tolist()
    itct_list = itct_list_df.values.tolist()
    sub_region_list = sub_region_list_df.values.tolist()
    inter_list = inter_list_df.values.tolist()
    c_continent_list = []
    c_sub_region_list = []
    c_inter_region_list = []
    for i in range(len(c_ct)):
        if type(c_ct[i]) == str:
            country_name = c_ct[i]
        # country_name = str(c_ct[i]).replace("'", "").replace("[", '').replace("]", '')
            if country_name in a:
                c_continent_list.append(str(itct_list[a.get(country_name)]).replace("'", "").replace("[", '').replace("]", ''))
                c_sub_region_list.append(str(sub_region_list[a.get(country_name)]).replace("'", "").replace("[", '').replace("]", ''))
                c_inter_region_list.append(str(inter_list[a.get(country_name)]).replace("'", "").replace("[", '').replace("]", ''))
            else:
                c_continent_list.append('')
                c_sub_region_list.append('')
                c_inter_region_list.append('')

        if type(c_ct[i]) == list:
            list_continent_temp = []            # Three temporary lists to hold recipes corresponding to lists corresponding to multiple countries
            list_sub_region_temp = []
            list_inter_region_temp = []
            for p in range(len(c_ct[i])):
                if c_ct[i][p] in a:
                    list_continent_temp.append(str(itct_list[a.get(c_ct[i][p])]).replace("'", "").replace("[", '').replace("]", ''))
                    list_sub_region_temp.append(str(sub_region_list[a.get(c_ct[i][p])]).replace("'", "").replace("[", '').replace("]", ''))
                    list_inter_region_temp.append(str(inter_list[a.get(c_ct[i][p])]).replace("'", "").replace("[", '').replace("]", ''))
                else:
                    list_continent_temp.append('')
                    list_sub_region_temp.append('')
                    list_inter_region_temp.append('')

            c_continent_list.append(list_continent_temp)
            c_sub_region_list.append(list_sub_region_temp)
            c_inter_region_list.append(list_inter_region_temp)

    return c_continent_list, c_sub_region_list, c_inter_region_list


def country_name_rewrite(country_clist):           # country_clist is the list of country names that need to be rewritten
    country_all = pd.read_csv('all_countries_with_aliases.csv')
    aliases_list = country_all['Aliases']
    name_list = country_all['Name']
    for i in range(len(aliases_list)):
        try:
            aliases_list[i] = aliases_list[i].split(" # ")
        except:
            pass

    for j in range(len(country_clist)):
        if type(country_clist[j]) == str:           # rename if country has only one case
            for n in range(len(aliases_list)):
                try:
                    if country_clist[j] in aliases_list[n]:
                        country_clist[j] = name_list[n]
                except:
                    pass

        if type(country_clist[j]) == list:          # The query country is rename in multiple cases
            for t in range(len(country_clist[j])):
                for g in range(len(aliases_list)):
                    try:
                        if country_clist[j][t] in aliases_list[g]:
                            country_clist[j][t] = name_list[g]
                    except:
                        pass
    return country_clist


def ingredients_split(ingredients_data):            #Input component data, which can be a list or a sequence of dataframes
    # clear_list = [' ,','']
    ingredients_list = []
    for n in range(len(ingredients_data)):
        for g in re.findall(r'\(.+?\)',ingredients_data[n]):
            ingredients_data[n] = ingredients_data[n].replace(g,'')
        ingredients_data[n] = ingredients_data[n].replace('|',' or ')
        ingredients_data[n] = ingredients_data[n].replace(' or ', ',').replace(' ; ',',').replace(' and ',',').replace('.','')
        ingredients_data[n] = ingredients_data[n].replace(',,',',').replace(' ,',',').replace(', ',',').replace('#',',').replace('"','').replace("'","")
        ingredients_data[n] = ingredients_data[n].split(',')
        ingredients_list.append(ingredients_data[n])

    return ingredients_list

def get_ingredients_list(region_name,place_switch = 3):     # Enter the country/region name to get the dish name and ingredients of the corresponding country/region,
    ingredients_place = []                                  # region_name can be any alias country name, but it must be changed to a list
    cuision_name = []                                       # 0 is the input place name is continent, 1 is the input place name sub-region, 2 is the input inter-region
    ingredients_list = ingredients_split(cuision_pd['main_ingredient'].values.tolist())
    cuision_list = ingredients_split(cuision_pd['name'].values.tolist())
    if place_switch != 3:
        place = region_name
        geo_info = (continent_identify(country_list_path = 'country_list.xlsx',
                          data_source = country_name_rewrite(country_split())))[place_switch]
        cuision_country = geo_info                          # The region list corresponding to the recipe (continent, sub-region, etc.)

    if place_switch == 3:
        place = country_name_rewrite(region_name)
        cuision_country = country_name_rewrite(country_split())

    for i in range(len(cuision_country)):
        if type(cuision_country[i]) == str:
            if place in cuision_country[i]:
                ingredients_place.append(ingredients_list[i])
                cuision_name.append(cuision_list[i])

        if type(cuision_country[i]) == list:
            # ingr_place_temp = []
            # cuision_name_temp = []
            for g in range(len(cuision_country[i])):
                if place in cuision_country[i][g]:
                    ingredients_place.append(ingredients_list[i])
                    cuision_name.append(cuision_list[i])
            # ingredients_place.append(ingr_place_temp)                     # After getting the input place name and corresponding to the county of the recipe,
            # cuision_name.append(cuision_name_temp)                        # ingredients list for the corresponding row
    for c in range(len(ingredients_place)):
        if type(ingredients_place[c]) == list:
            for o in range(len(ingredients_place[c])):
                ingredients_place[c][o] = ingredients_place[c][o].lower()
                ingredients_place[c][o] = ingredients_place[c][o].replace('eggs', 'egg')
        else:
            ingredients_place[c] = ingredients_place[c].lower()
            ingredients_place[c] = ingredients_place[c].replace('eggs', 'egg')

    return ingredients_place, cuision_name                                  # Returns the list of ingredients of the dish corresponding to the name of the region, and the name of the dish


def similarity_calculater(list_1,list_2):                             #list_1_2 are the two lists that need to calculate the similarity
    list_reset_1 = []
    list_reset_2 = []
    for i in list_1:
        if type(i) == list:
            for n in i:
                list_reset_1.append(n)
        else:
            list_reset_1.append(i)

    for j in list_2:
        if type(j) == list:
            for p in j:
                list_reset_2.append(p)
        else:
            list_reset_2.append(j)

    same_counter = 0
    for x in list_reset_1:
        if x in list_reset_2:
            same_counter = same_counter + 1
    for y in list_reset_2:
        if y in list_reset_1:
            same_counter = same_counter + 1

    similarity = same_counter / (len(list_reset_1)+len(list_reset_2))

    return similarity                       # Returns the similarity between two lists

def ingredients_counter(list_data):         # list is the list data for which frequency of occurrence needs to be counted
    from collections import Counter
    list_reset = []
    for i in list_data:
        if type(i) == list:
            for n in i:
                list_reset.append(n)
        else:
            list_reset.append(i)

    list_frequency = Counter(list_reset).most_common(10)
    return list_frequency



# print(get_ingredients_list('Europe', place_switch=0)[1])
# print(continent_identify(country_list_path='/Users/chrisx/Desktop/country_list.xlsx',
#                          data_source = country_name_rewrite(country_split()))[0][8])
# print(similarity_calculater(get_ingredients_list('Western Asia', place_switch=0)[0],get_ingredients_list('Eastern Europe',place_switch=1)[0]))

list_continent = ['Africa','Americas','Asia','Europe','Oceania']            # Enter the country/region name to get the dish name and ingredients of the corresponding country/region,
for t in list_continent:                                                    # region_name can be any alias country name, but it must be changed to a list
    print(ingredients_counter(get_ingredients_list(t,place_switch=0)[0]))   # 0 is the input place name is continent, 1 is the input place name sub-region, 2 is the input inter-region
                                                                            #Output the top ten ingredients with the highest frequency

for i in list_continent:                                                    #output the ingredients similarity between each continent
    for b in list_continent:
        simi = similarity_calculater(get_ingredients_list(i, place_switch=0)[0]   # Enter the country/region name to get the dish name and ingredients of the corresponding country/region,
                                     ,get_ingredients_list(b, place_switch=0)[0]) # region_name can be any alias country name, but it must be changed to a list
        print(i +' and '+ b +' similarity: '+ str(simi))                          # 0 is the input place name is continent, 1 is the input place name sub-region, 2 is the input inter-region

# print(ingredients_split(cuision_pd['main_ingredient'].values.tolist()))       # Separate ingredients as a list

# country_name_rewrite(country_split()).to_excel('/Users/chrisx/Desktop/cuision_country_test.xlsx')

# country_list = pd.read_excel('/Users/chrisx/Desktop/country_list.xlsx')     # start here
# country_list_1 = country_name_rewrite(pd.read_excel('/Users/chrisx/Desktop/country_list.xlsx')['Country or Area'])
# country_list['Country or Area'] = country_list_1
# country_list.to_excel('/Users/chrisx/Desktop/country_list.xlsx')            # Output after processing country or area data of country_list

# cuision_pd['country'] = country_split()                                     # start here
# cuision_pd.to_excel('/Users/chrisx/Desktop/infobox_data_cleared.xlsx')      # Rewrite the country to the recipe data and output it


# if __name__ == '__main__':                                                    # start here
#     (a,b,c) = continent_identify(country_list_path = '/Users/chrisx/Desktop/country_list.xlsx',
#                          data_source = country_name_rewrite(country_split()))
#     cuision_pd['continent'] = a
#     cuision_pd['sub-region'] = b
#     cuision_pd['inter-region'] = c                                            # Output multiple lists returned by the continent recognition program
# cuision_pd.to_excel('/Users/chrisx/Desktop/infobox_data_cleared.xlsx')
# print((continent_identify(country_list_path = '/Users/chrisx/Desktop/country_list.xlsx',
#                           data_source = country_name_rewrite(country_split())))[2])