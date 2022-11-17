import streamlit
import pandas
import snowflake.connector
import requests
from urllib.error import URLError

streamlit.title("My parents new healthy diner")

streamlit.header('Breakfast Menu')
streamlit.text('Omega 3 & Blueberry Oatmeal')
streamlit.text('Kale, Spinach & Rocket Smoothie')
streamlit.text('Hard-Boiled Free-Range Egg')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
my_fruits_selected = streamlit.multiselect("My fruit list:",list(my_fruit_list.index),['Avocado', 'Strawberries'])
my_fruits_to_show = my_fruit_list.loc[my_fruits_selected]
streamlit.dataframe(my_fruits_to_show)

def get_fruityvice_data(my_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.write("Please select a fruit to get information.")
  else:
    streamlit.dataframe(get_fruityvice_data(fruit_choice))
except URLerror as e:
  streamlit.error()

#dont run anything from here
streamlit.stop()
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * from fruit_load_list")
my_data_row = my_cur.fetchall()
streamlit.text("The Fruit load lists contains:")
streamlit.dataframe(my_data_row)

new_fruit = streamlit.text_input('What fruit would you like to add?','Kiwi')
streamlit.write("Thanks for adding "+new_fruit)

my_cur.execute("insert into pc_rivery_db.public.fruit_load_list values('from_streamlit')")
