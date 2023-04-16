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
ob_login=login()

class proceed:

    def add_property(self,user_id):
        st.header('Add a new property')
        #add property type, city, state, location, description, availability, price
        st.write('Please enter the details of the property')
        property_type_empty=st.empty()
        property_location_empty=st.empty()
        property_city_empty=st.empty()
        property_state_empty=st.empty()
        property_desc_empty=st.empty()
        price_empty=st.empty()
        property_availability_empty=st.empty()
        add_property_button_empty=st.empty()
        property_type=property_type_empty.selectbox('Property type',['House','Apartment','Commercial Building'])
        property_location=property_location_empty.text_input('Property location')
        property_city=property_city_empty.text_input('City')
        property_state=property_state_empty.text_input('State')
        property_desc=property_desc_empty.text_input('Description')
        property_price=price_empty.text_input('Price')
        if len(property_price)!=0:
            try:
                property_price=float(property_price)
            except:
                st.error('Please enter the numeric value for price')
        property_availability=property_availability_empty.radio('Is it available? ',['Yes','No'])
        if add_property_button_empty.button('Submit'):
            property_id='pr'+get_random_string(5)
            agents_id='a'+user_id
            st.write(user_id)
            st.write(agents_id)
            date_posted_empty=st.empty()
            date_posted=date_posted_empty.date_input('')
            date_posted_empty.empty()
            add_property_query='''insert into property(property_id,agents_id,type,city,state,location,description,availability,price,date_posted)
            values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
            add_property_values=(property_id,agents_id,property_type,property_city,property_state,property_location,property_desc,
            property_availability,property_price,date_posted)
            entry_execution(add_property_query,add_property_values)
            success_empty=st.empty()
            success_empty.success('New property added')
            property_type_empty.empty()
            property_location_empty.empty()
            property_city_empty.empty()
            property_state_empty.empty()
            property_desc_empty.empty()
            property_availability_empty.empty()
            price_empty.empty()
            add_property_button_empty.empty()
            time.sleep(2)
            success_empty.empty()
            st.experimental_rerun()

    #delete the property
    def delete_property(self,user_id):
        st.write('Select the properties below to delete')
        st.write('----------------------------------------------')
        agents_id='a'+user_id
        properties_query='''select * from property where agents_id = %s'''
        properties_value=(agents_id,)
        properties=query_execution(properties_query,properties_value)
        property_ids=[]
        for prop in properties:
            property_ids.append(prop[0])
        select_properties=st.selectbox('',['Select here']+property_ids)
        if select_properties!='Select here':
            pro_id_index=property_ids.index(select_properties)
            pro=properties[pro_id_index]
            success_empty=st.empty()
            st.subheader('Property ID: {}'.format(pro[0]))
            col1, col2 = st.columns(2)
            with col1:
                st.write('**Type:**','  \n**City:** ','  \n**State:** ','  \n**Location:** ',
                '  \n**Description:** ','  \n**Availability:** ','  \n**Price:** ')
            with col2:
                st.write(pro[2],'  \n',pro[3],'  \n',pro[4],'  \n',pro[5],
                '  \n',pro[6],'  \n',pro[7],'  \n',pro[8])
            if st.button('Delete'):
                property_id=pro[0]
                delete_query='delete from property where property_id = %s'
                delete_values=(property_id,)
                entry_execution(delete_query,delete_values)
                property_ids.remove(select_properties)
                success_empty.success('Property deleted successfully')
                time.sleep(2)
                success_empty.empty()
                st.experimental_rerun()
                select_properties='Select here'



    def modify_property(self,user_id):
        st.write('Modify the properties')
        st.write('Select the properties below to delete')
        st.write('----------------------------------------------')
        agents_id='a'+user_id
        properties_query='''select * from property where agents_id = %s'''
        properties_value=(agents_id,)
        properties=query_execution(properties_query,properties_value)
        property_ids=[]
        for prop in properties:
            property_ids.append(prop[0])
        select_properties=st.selectbox('',['Select here']+property_ids)
        if select_properties!='Select here':
            pro_id_index=property_ids.index(select_properties)
            pro=properties[pro_id_index]
            success_empty=st.empty()
            st.subheader('Property ID: {}'.format(pro[0]))
            col1, col2 = st.columns(2)
            with col1:
                st.write('**Type:**','  \n**City:** ','  \n**State:** ','  \n**Location:** ',
                '  \n**Description:** ','  \n**Availability:** ','  \n**Price:** ')
            with col2:
                st.write(pro[2],'  \n',pro[3],'  \n',pro[4],'  \n',pro[5],
                '  \n',pro[6],'  \n',pro[7],'  \n',str(pro[8]))

            #
            agent_id='a'+user_id
            property_id=pro[0]
            type=pro[2]
            city=pro[3]
            state=pro[4]
            location=pro[5]
            description=pro[6]
            availability=pro[7]
            price=pro[8]

            property_type_index=['House','Apartment','Commercial Building'].index(pro[2])
            property_type=st.selectbox('Property type',['House','Apartment','Commercial Building'],index=property_type_index)
            availability_index=['Yes','No'].index(pro[7])
            property_location=st.text_input('Property location',value=pro[5])
            property_city=st.text_input('City',value=pro[3])
            property_state=st.text_input('State',value=pro[4])
            property_desc=st.text_input('Description',value=pro[6])
            property_price=st.text_input('Price',value=pro[8])
            if len(property_price)!=0:
                try:
                    property_price=float(property_price)
                except:
                    st.error('Please enter the numerical value')
            property_availability=st.radio('Is it available? ',options=['Yes','No'],index=availability_index)
            condition=(property_type==type)&(property_city==city)&(property_state==state)&(property_location==location)&(property_desc==description)&(property_availability==availability)&(property_price==price)

            if condition:
                pass
            else:
                if st.button('Modify'):

                    modify_query = '''UPDATE property SET type = %s, city = %s, state = %s, location = %s,
                    description = %s, availability = %s, price = %s WHERE property_id = %s'''
                    modified_values = (property_type,property_city,property_state,property_location,property_desc,property_availability,property_price,property_id)
                    entry_execution(modify_query,modified_values)
                    st.success('Modified')
                    time.sleep(2)
                    st.experimental_rerun()


    def agent(self):
        record=ob_login.user_status_list[-1]
        user_id=record[0]
        first_name=record[1]
        middle_name=record[2]
        last_name=record[3]
        user_type=record[4]
        address=record[5]
        email_id=record[6]
        password=record[7]
        st.write(record)
        st.header('Agent page')
        st.write('Welcome!')
        select_action=st.radio('Please select to perform: ',['Add a new property',
        'Delete the existing property','Modify the existing property'])
        if select_action=='Add a new property':
            ob_pro.add_property(user_id)
        if select_action=='Delete the existing property':
            ob_pro.delete_property(user_id)
        if select_action=='Modify the existing property':
            ob_pro.modify_property(user_id)

    def search(self):
        st.write('Search options')
    def renter(self):
        st.header('Renter page')
        renter_options=st.selectbox('Please select the options',['Search for the properties','Add credit card for property booking'])
        if renter_options=='Add credit card for property booking':
            st.write('Add or delete credit cards')
        if renter_options=='Search for the properties':
            ob_pro.search()

ob_pro=proceed()



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
                    record=records[0]
                    user_id=record[0]
                    first_name=record[1]
                    middle_name=record[2]
                    last_name=record[3]
                    user_type=record[4]
                    address=record[5]
                    email_id=record[6]
                    password=record[7]
                    ob_login.user_status_list.append('user_type'+'-'+user_type)
                    ob_login.user_status_list.append(record)
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
    job_empty=st.empty()
    contact_empty=st.empty()
    agency_empty=st.empty()
    contact_empty=st.empty()
    move_in_date_empty=st.empty()
    preferedlocation_empty=st.empty()
    budget_empty=st.empty()
    ad_empty=st.empty()
    pass_empty=st.empty()
    repass_empty=st.empty()
    register_button_empty=st.empty()
    first_name=fn_empty.text_input('First Name')
    middle_name=mn_empty.text_input('Middle Name')
    last_name=ln_empty.text_input('Last Name')
    email_id=email_empty.text_input('Email ID')
    user_type=ut_empty.radio('User Type',options=['Agent','Renter'])
    if user_type=='Agent':
        real_estate_agency=agency_empty.text_input('Agency name')
        job_title=job_empty.text_input('Job Title')
        contact=contact_empty.text_input('Contact')
    if user_type=='Renter':
        date_empty=st.empty()
        todays_date=date_empty.date_input('')
        date_empty.empty()
        move_in_date=move_in_date_empty.date_input('Move-In Date')
        preferedlocation=preferedlocation_empty.text_input('Prefered Location')
        budget=budget_empty.text_input('Budget')

    address=ad_empty.text_input('Address')
    password=pass_empty.text_input('Enter password')
    repassword=repass_empty.text_input('Re Enter the password')
    if register_button_empty.button('Register'):
        user_existed_query='''select * from users where email_id = %s and user_type = %s'''
        user_existed_value=(email_id,user_type,)
        existed_records=query_execution(user_existed_query,user_existed_value)
        if len(existed_records)==0:
            while True:
                user_id=get_random_string(7)
                query='select * from users where user_id = %s'
                values=(user_id,)
                result=query_execution(query,values)
                if len(result)==0:
                    register_query='''insert into users (first_name,middle_name,last_name,user_type,address,email_id,password,user_id)
                    values (%s,%s,%s,%s,%s,%s,%s,%s)'''
                    register_values=(first_name,middle_name,last_name,user_type,address,email_id,password,user_id)
                    entry_execution(register_query,register_values)
                    if user_type=='Agent':
                        agents_id='a'+user_id
                        agent_register_q='''insert into agents(agents_id,user_id,realestate_agency,contact,job_title) values (%s,%s,%s,%s,%s)'''
                        agent_register_values=(agents_id,user_id,real_estate_agency,contact,job_title)
                        entry_execution(agent_register_q,agent_register_values)
                        agency_empty.empty()
                        job_empty.empty()
                        contact_empty.empty()
                    elif user_type=='Renter':
                        renters_id='r'+user_id
                        renter_register_q='''insert into renter(renters_id,user_id,move_in_date,preferedlocation,budget) values (%s,%s,%s,%s,%s)'''
                        renter_register_values=(renters_id,user_id,move_in_date,preferedlocation,budget)
                        entry_execution(renter_register_q,renter_register_values)
                        move_in_date_empty.empty()
                        preferedlocation_empty.empty()
                        budget_empty.empty()
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
        else:
            st.error('This mail id already exists')





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
    if 'user_type-Agent' in ob_login.user_status_list:
        ob_pro.agent()
    elif 'user_type-Renter' in ob_login.user_status_list:
        ob_pro.renter()
