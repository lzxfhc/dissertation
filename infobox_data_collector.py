import pandas as pd
import wptools

#//////////Download the data in the info box according to the list of entities.///////////

cuision_data = pd.read_csv('/Users/chrisx/Desktop/cuisine_name.csv', usecols=[1])

test_list = ['Bisquick', 'Matzah ball', 'Bollo', 'Medu vada']

infobox_total = {'name': '', 'image': '', 'Alternative names': '',
                 'caption': '', 'alternate_name': '',
                 'Place of origin': '', 'Region or state': '', 'Serving temperature': '',
                 'Course': '', 'Similar dishes': '', 'type': '', 'main_ingredient': ''}

cuision_list = cuision_data['cuisine_name'].tolist()
cuision_list
infobox_total = pd.DataFrame(columns=['name', 'image', 'Alternative names',
                                      'caption', 'alternate_name', 'country', 'region',
                                      'served', 'course', 'similar_dish', 'type', 'serving_size', 'main_ingredient'])
for i in range(len(cuision_list)):
    so = wptools.page(cuision_list[i]).get_parse()
    infobox = so.data['infobox']
    if infobox != None:
        infobox_df = pd.DataFrame(infobox, index=[0])
        infobox_total = pd.concat([infobox_total, infobox_df])

infobox_total