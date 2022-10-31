#streamlit.stop()

import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError 

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

streamlit.title('My First Streamlit App')
streamlit.header('Breakfast Favourites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado on Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)

streamlit.header("Fruityvice Fruit Advice!")
fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)

# normalise the json response
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# put it into a dataframe
streamlit.dataframe(fruityvice_normalized)

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * FROM fruit_load_list")
my_data_rows = my_cur.fetchall()
my_fruit_data_frame = pandas.DataFrame(my_data_rows)
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_fruit_data_frame)
add_fruit = streamlit.text_input('What fruit would you like to add?','Jackfruit')
#my_cur.execute("INSERT INTO fruit_load_list VALUES ('%s')", (add_fruit))
new_fruit_df = pandas.DataFrame([add_fruit])
my_fruit_data_frame = my_fruit_data_frame.append(new_fruit_df)
streamlit.write('Thank you for adding ', add_fruit)

#test adding test_value
my_cur.execute("INSERT INTO fruit_load_list values 'test_value'")

