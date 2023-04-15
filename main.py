import streamlit as st
import time
import psycopg2
import random
import string


st.title('Real Estate Agency')


def query_execution(query,variables):
    connection=psycopg2.connect(database='real_estate_db',user='tirumaleshn2000',password='',host='localhost',port='5431')
    cursor=connection.cursor()
    cursor.execute(query,variables)
    record=cursor.fetchall()
    connection.commit()
    connection.close()
    return record

def entry_execution(query,variables):
    connection=psycopg2.connect(database='real_estate_db',user='tirumaleshn2000',password='',host='localhost',port='5431')
    cursor=connection.cursor()
    cursor.execute(query,variables)
    connection.commit()
    connection.close()




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

sign_or_login_empty=st.empty()
user_type_empty=st.empty()
email_id_empty=st.empty()
password_empty=st.empty()
login_button_empty=st.empty()


def get_random_string(length):
    letters = string.ascii_lowercase+string.digits
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def login_page():
    user_type=user_type_empty.radio('',options=['Agent','Renter'])
    email_id=email_id_empty.text_input('Email: ')
    password=password_empty.text_input('Password: ',type='password')
    if login_button_empty.button('Login'):
        if len(email_id)!=0:
            if len(password)!=0:
                login_query='select * from users where email_id = %s and password = %s and user_type = %s'
                login_variables=(email_id,password,user_type)
                records=query_execution(login_query,login_variables)
                if len(records)!=0:
                    ob_login.user_status_list.append('proceed')
                    ob_login.user_status_list.append(email_id)
                    ob_login.user_status_list.append(password)
                    ob_login.user_status_list.append(user_type)
                    email_id_empty.empty()
                    password_empty.empty()
                    login_button_empty.empty()
                    user_type_empty.empty()
                else:
                    st.error('Invalid login details')
            else:
                st.error('Please enter the password')
        else:
            st.error('Please enter the username')

def register():
    st.write('Please fill the details to register')
    fn_empty=st.empty()
    mn_empty=st.empty()
    ln_empty=st.empty()
    email_empty=st.empty()
    ut_empty=st.empty()
    agency_empty=st.empty()
    contact_empty=st.empty()
    ad_empty=st.empty()
    pass_empty=st.empty()
    repass_empty=st.empty()
    register_button_empty=st.empty()
    first_name=fn_empty.text_input('First Name')
    middle_name=mn_empty.text_input('Middle Name')
    last_name=ln_empty.text_input('Last Name')
    email_id=email_empty.text_input('Email ID')
    user_type=ut_empty.selectbox('User Type',options=['Agent','Renter'])
    if user_type=='Agent':
        real_estate_agency=
    address=ad_empty.text_input('Address')
    password=pass_empty.text_input('Enter password')
    repassword=repass_empty.text_input('Re Enter the password')
    if register_button_empty.button('Register'):
        while True:
            user_id=get_random_string(7)
            query='select * from users where user_id = %s'
            values=(user_id,)
            result=query_execution(query,values)
            if len(result)==0:
                register_query='''insert into users (first_name,middle_name,last_name,user_type,address,email_id,password,user_id)
                values (%s,%s,%s,%s,%s,%s,%s,%s)'''
                values=(first_name,middle_name,last_name,user_type,address,email_id,password,user_id)
                entry_execution(register_query,values)
                st.success('Registered successfully')
                fn_empty.empty()
                mn_empty.empty()
                ln_empty.empty()
                email_empty.empty()
                ut_empty.empty()
                ad_empty.empty()
                pass_empty.empty()
                repass_empty.empty()
                register_button_empty.empty()
                break
            else:
                pass





if len(ob_login.user_status_list)==0:
    sign_or_login=sign_or_login_empty.radio('',options=['Login','Register'])
    if sign_or_login=='Login':
        login_page()
    elif sign_or_login=='Register':
        register()





if 'proceed' in ob_login.user_status_list:
    if st.button('Log out'):
        ob_login.user_status_list.clear()
        st.experimental_rerun()
    st.write('Success')
    if ob_login.user_status_list[-1]=='Agent':
        ob_pro.agent()
    elif ob_login.user_status_list[-1]=='Renter':
        ob_pro.renter()
