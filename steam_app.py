import streamlit
import pandas
import snowflake.connector
import requests
from urllib.error import URLError

streamlit.title('🥣 Perfect Omelette Recipe')
streamlit.header('Ingredients Required')
streamlit.text('🐔 2 Eggs')
streamlit.text('🍞 1 Tsp Butter')
streamlit.text('Salt to taste')
streamlit.text('🥗 Preferred spices and chillis')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# streamlit.dataframe(my_fruit_list)

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]


# Display the table on the page.
streamlit.dataframe(fruits_to_show)

#create a function
def get_fruityvice_data (this_fruit_choice):
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
        fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
        return fruityvice_normalized

#start of a new section
streamlit.header("Fruityvice Fruit Advice!")
try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?')
    if not fruit_choice:
        streamlit.error("Please select a fruit to get information")
    else:
        back_from_function = get_fruityvice_data(fruit_choice)
        streamlit.dataframe(back_from_function)

except URLError as e:
    streamlit.error()

streamlit.header("View out Fruit List - Add your Favorites!")
#snowflake-related functions
def get_fruit_load_list():
        with my_cnx.cursor() as my_cur:
                my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
                return my_cur.fetchall()
        
#add a button to load the fruit
if streamlit.button('Get Fruit List'):
        my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
        my_data_rows = get_fruit_load_list()
        my_cnx.close()
        streamlit.dataframe(my_data_rows)
        


#Allow user to add more fruits
def insert_row_snowflake(new_fruit):
        with my_cnx.cursor() as my_cur:
                my_cur.execute("insert into PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST values ('" + new_fruit + "')");
                return 'Thanks for adding ' + new_fruit
                
add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a Fruit to the List'):
        my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
        back_from_function = insert_row_snowflake(add_my_fruit)
        my_cnx.close()
        streamlit.text(back_from_function)
        
