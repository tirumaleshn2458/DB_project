import streamlit as st
import time
st.title('Real Estate Agency')

#user status
user_status=None

#creating form
@st.cache
class login:
    user_status_list=[]

class proceed:

    def add_property(self):
        st.header('Add a new property')
        #add property type, city, state, location, description, availability, price
        st.write('Please enter the details of the property')
        property_type_empty=st.empty()
        property_location_empty=st.empty()
        property_city_empty=st.empty()
        property_state_empty=st.empty()
        property_desc_empty=st.empty()
        property_availability_empty=st.empty()
        add_property_button_empty=st.empty()
        property_type=property_type_empty.text_input('Property type')
        property_location=property_location_empty.text_input('Property location')
        property_city=property_city_empty.text_input('City')
        property_state=property_state_empty.text_input('State')
        property_desc=property_desc_empty.text_input('Description')
        property_availability=property_availability_empty.radio('Is it available? ',['Yes','No'])
        if add_property_button_empty.button('Submit'):
            success_empty=st.empty()
            success_empty.success('New property added')
            property_type_empty.empty()
            property_location_empty.empty()
            property_city_empty.empty()
            property_state_empty.empty()
            property_desc_empty.empty()
            property_availability_empty.empty()
            add_property_button_empty.empty()
            time.sleep(2)
            success_empty.empty()
            st.experimental_rerun()



    def agent(self):
        st.header('Agent page')
        st.write('Welcome!')
        select_action=st.selectbox('Please select to perform: ',['Add a new property',
        'Delete the existing property','Modify the existing property'])
        if select_action=='Add a new property':
            ob_pro.add_property()
    def renter(self):
        st.header('Renter page')

ob_pro=proceed()

ob_login=login()

user_type_empty=st.empty()
username_empty=st.empty()
password_empty=st.empty()
login_button_empty=st.empty()
if len(ob_login.user_status_list)==0:
    user_type=user_type_empty.radio('',options=['Agent','Renter'])
    username=username_empty.text_input('Username: ')
    password=password_empty.text_input('Password: ',type='password')
    if login_button_empty.button('Login'):
        ob_login.user_status_list.append('proceed')
        ob_login.user_status_list.append(username)
        ob_login.user_status_list.append(password)
        ob_login.user_status_list.append(user_type)
        username_empty.empty()
        password_empty.empty()
        login_button_empty.empty()
        user_type_empty.empty()


if 'proceed' in ob_login.user_status_list:
    if st.button('Log out'):
        ob_login.user_status_list.clear()
        st.experimental_rerun()
    st.write('Success')
    if ob_login.user_status_list[-1]=='Agent':
        ob_pro.agent()
    elif ob_login.user_status_list[-1]=='Renter':
        ob_pro.renter()
