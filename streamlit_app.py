# Import python packages
#from snowflake.snowpark.context import get_active_session
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
streamlit.title(f":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom Smoothie!.
  """
)

name_on_order = st.text_input("Name on Smoothie", 'Mohan')
st.write("The name on Smoothie is", name_on_order)

#session = get_active_session()
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select (col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

options = st.multiselect(
    "Choose upto 5 fruits:",
   my_dataframe, max_selections=5
)
if options:
    #st.write("You selected:", options)
    #st.text (options)
    options_string = ''
    for fruit_choosen in options:
        options_string += fruit_choosen + ','
    #st.write( options_string )
    my_sql = " insert into smoothies.public.orders (ingredients, name_on_order) values ('" +options_string+ "','"+name_on_order+"')" 
    st.write( my_sql )
    time_to_submit = st.button ('submit order')
    if  time_to_submit:
        session.sql(my_sql).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
