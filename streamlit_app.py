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
    fruit_data = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(fruit_data)
except URLerror as e:
  streamlit.error()

streamlit.text("The Fruit load lists contains:")
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("SELECT * from fruit_load_list")
    return my_cur.fetchall()

if streamlit.button("Get load list"):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_fruit_rows = get_fruit_load_list()
  streamlit.dataframe(my_fruit_rows)
  
streamlit.stop()

def insert_snowlflake_row(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("insert into pc_rivery_db.public.fruit_load_list values('from streamlit')")
    return "thanks for adding :"+ new_fruit
    
new_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button("Add a fruit to the list"):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    fruit_added = insert_snowflake_row(new_fruit)
    streamlit.write(fruit_added)                

