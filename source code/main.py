import streamlit as st
import time
import psycopg2
import random
import string
import datetime
from datetime import timedelta

st.title('Real Estate Agency')

todays_date=datetime.date.today()
def query_execution(query,variables=None):
    connection=psycopg2.connect(database='real_estate_db',user='tirumaleshn2000',password='',host='localhost',port='5431')
    cursor=connection.cursor()
    cursor.execute(query,variables)
    record=cursor.fetchall()
    connection.commit()
    connection.close()
    return record

def entry_execution(query,variables=None):
    connection=psycopg2.connect(database='real_estate_db',user='tirumaleshn2000',password='',host='localhost',port='5431')
    cursor=connection.cursor()
    cursor.execute(query,variables)
    connection.commit()
    connection.close()


#user status
user_status=None

#creating form
@st.cache_resource
class login:
    user_status_list=[]
ob_login=login()

class proceed:

    def property_status(self,user_id):
        record=ob_login.user_status_list[-1]
        user_id=record[0]
        agents_id='a'+user_id
        booked_proeperties_query='''select * from property_booking inner join property on property_booking.property_id=property.property_id inner join credit_card on property_booking.creditcard_id=credit_card.creditcard_id where property.agents_id=%s'''
        values=(agents_id,)
        booked_properties_records=query_execution(booked_proeperties_query,values)

        st.subheader('List of properties booked')
        #st.write(booked_properties_records)
        if len(booked_properties_records)==0:
            st.info('No bookings made by renters')
        for pro in booked_properties_records:
            booking_id=pro[0]
            property_id=pro[1]
            renters_id=pro[2]
            booking_date=pro[3]
            creditcard_id=pro[4]
            property_id=pro[5]
            agents_id=pro[6]
            type=pro[7]
            city=pro[8]
            state=pro[9]
            location=pro[10]
            description=pro[11]
            availability=pro[12]
            date_posted=pro[13]
            price=pro[14]
            start_date=pro[15]
            end_date=pro[16]
            creditcard_id=pro[17]
            card_number=pro[18]
            renters_id=pro[19]
            address=pro[20]
            card_expiry_date=pro[21]
            col1,col2=st.columns(2)
            #includes the details of the renter, the property, the rental period, and the payment method used.
            with col1:
                st.write('Property ID: ')
                st.write('Property type: ')
                st.write('Location: ')
                st.write('City: ')
                st.write('State: ')
                st.write('Price: ')
                st.write('Start date: ')
                st.write('End date: ')
                st.write('Renter ID: ')
                st.write('Booking date: ')
                st.write('Payment card: ')
                st.write('Billing Address: ')
            with col2:
                st.write(property_id)
                st.write(type)
                st.write(location)
                st.write(city)
                st.write(state)
                st.write(str(price))
                st.write(str(start_date))
                st.write(str(end_date))
                st.write(renters_id)
                st.write(str(booking_date))
                st.write(card_number)
                st.write(address)
            if st.button('Cancel this booking',key=booking_id+'cancel'):
                cancel_booking_query='delete from property_booking where property_id = %s'
                cancel_booking_query_values=(property_id,)
                entry_execution(cancel_booking_query,cancel_booking_query_values,)
                update_property_avail='update property set availability=%s'
                update_property_values=('Yes',)
                entry_execution(update_property_avail,update_property_values)
                st.success('Booking cancelled successfully')
                time.sleep(1)
                st.experimental_rerun()
            st.write('---------')




    def add_property(self,user_id):
        st.header('Add a new property')
        initial_value=None
        #add property type, city, state, location, description, availability, price
        #with st.form('Add new property',clear_on_submit=True):
        st.write('Please enter the details of the property')
        property_type_empty=st.empty()

        property_type=property_type_empty.selectbox('Property type',['House','Apartment','Commercial Building','Vacation Home','Land'])
        sale_or_rent=st.selectbox('Rent or Sale?',['Rental','Sale'])
        if property_type=='House':
            with st.form('house',clear_on_submit=True):
                house_rooms=st.number_input('Number of rooms',step=1,value=0)
                house_sft=st.number_input('Square footage')
                property_location=st.text_input('Property location',value='')
                property_city=st.text_input('City',value='')
                property_state=st.text_input('State',value='')
                nearby_schools=st.text_input('Enter nearby school names(if exists) using commas',value='')
                if len(nearby_schools)!=0:
                    nearby_schools_list=nearby_schools.split(',')

                else:
                    nearby_schools_list='None'
                crime_rate=st.number_input('Crime Rate',min_value=0.0,max_value=100.0,step=0.1)
                property_desc=st.text_input('Description',value='')
                if sale_or_rent=='Rental':
                    todays_date=datetime.date.today()
                    property_sd=st.date_input('Lease start date',min_value=todays_date)
                    property_ed=st.date_input('Lease end date',value=property_sd,min_value=property_sd)
                    property_price=st.number_input('Rental price per month',value=0.0,step=0.1)
                elif sale_or_rent=='Sale':
                    todays_date=datetime.date.today()
                    property_sd=None
                    property_ed=None
                    property_price=st.number_input('Sale price',value=0.0,step=0.1)

                property_availability=st.radio('Is it available? ',['Yes','No'],index=0)

                if st.form_submit_button('Submit'):
                    property_id='pr'+get_random_string(5)
                    agents_id='a'+user_id
                    date_posted=todays_date
                    add_property_query='''insert into property(property_id,agents_id,type,city,state,location,description,availability,price,date_posted,start_date,end_date,sale_or_rent,crime_rate)
                    values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
                    add_property_values=(property_id,agents_id,property_type,property_city,property_state,property_location,property_desc,
                    property_availability,property_price,date_posted,property_sd,property_ed,sale_or_rent,crime_rate)
                    entry_execution(add_property_query,add_property_values)
                    #if property_type=='House':
                    house_id='h'+property_id
                    query='''insert into house(house_id,property_id,rooms,sqt_area) values (%s,%s,%s,%s)'''
                    values=(house_id,property_id,house_rooms,house_sft)
                    entry_execution(query,values)
                    #inserting the near by schools
                    if nearby_schools_list!='None':
                        for school in nearby_schools_list:
                            entry_execution('insert into nearby_schools(property_id,school_name) values (%s,%s)',(property_id,school,))
                    success_empty=st.empty()
                    success_empty.success('New property added')
                    time.sleep(2)
                    success_empty.empty()
                    st.experimental_rerun()



        elif property_type=='Vacation Home':
            with st.form('vacation_home',clear_on_submit=True):
                vacation_home_rooms=st.number_input('Number of rooms',step=1,value=0)
                vacation_home_sft=st.number_input('Square footage')
                property_location=st.text_input('Property location',value='')
                property_city=st.text_input('City',value='')
                property_state=st.text_input('State',value='')
                nearby_schools=st.text_input('Enter nearby school names(if exists) using commas',value='')
                if len(nearby_schools)!=0:
                    nearby_schools_list=nearby_schools.split(',')

                else:
                    nearby_schools_list='None'
                crime_rate=st.number_input('Crime Rate',min_value=0.0,max_value=100.0,step=0.1)
                property_desc=st.text_input('Description',value='')
                if sale_or_rent=='Rental':
                    todays_date=datetime.date.today()
                    property_sd=st.date_input('Lease start date',min_value=todays_date)
                    property_ed=st.date_input('Lease end date',value=property_sd,min_value=property_sd)
                    property_price=st.number_input('Rental price per month',value=0.0,step=0.1)
                elif sale_or_rent=='Sale':
                    todays_date=datetime.date.today()
                    property_sd=None
                    property_ed=None
                    property_price=st.number_input('Sale price',value=0.0,step=0.1)

                property_availability=st.radio('Is it available? ',['Yes','No'],index=0)

                if st.form_submit_button('Submit'):
                    property_id='pr'+get_random_string(5)
                    agents_id='a'+user_id
                    date_posted=todays_date
                    add_property_query='''insert into property(property_id,agents_id,type,city,state,location,description,availability,price,date_posted,start_date,end_date,sale_or_rent,crime_rate)
                    values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
                    add_property_values=(property_id,agents_id,property_type,property_city,property_state,property_location,property_desc,
                    property_availability,property_price,date_posted,property_sd,property_ed,sale_or_rent,crime_rate)
                    entry_execution(add_property_query,add_property_values)
                    #if property_type=='vacation_home':
                    vacation_home_id='v'+property_id
                    query='''insert into vacation_home(vacation_home_id,property_id,rooms,sqt_area) values (%s,%s,%s,%s)'''
                    values=(vacation_home_id,property_id,vacation_home_rooms,vacation_home_sft)
                    entry_execution(query,values)
                    #inserting the near by schools
                    if nearby_schools_list!='None':
                        for school in nearby_schools_list:
                            entry_execution('insert into nearby_schools(property_id,school_name) values (%s,%s)',(property_id,school,))
                    success_empty=st.empty()
                    success_empty.success('New property added')
                    time.sleep(2)
                    success_empty.empty()
                    st.experimental_rerun()


        elif property_type=='Land':
            with st.form('land',clear_on_submit=True):

                land_sft=st.number_input('Square footage')
                property_location=st.text_input('Property location',value='')
                property_city=st.text_input('City',value='')
                property_state=st.text_input('State',value='')
                nearby_schools=st.text_input('Enter nearby school names(if exists) using commas',value='')
                if len(nearby_schools)!=0:
                    nearby_schools_list=nearby_schools.split(',')

                else:
                    nearby_schools_list='None'
                crime_rate=st.number_input('Crime Rate',min_value=0.0,max_value=100.0,step=0.1)
                property_desc=st.text_input('Description',value='')
                if sale_or_rent=='Rental':
                    todays_date=datetime.date.today()
                    property_sd=st.date_input('Lease start date',min_value=todays_date)
                    property_ed=st.date_input('Lease end date',value=property_sd,min_value=property_sd)
                    property_price=st.number_input('Rental price per month',value=0.0,step=0.1)
                elif sale_or_rent=='Sale':
                    todays_date=datetime.date.today()
                    property_sd=None
                    property_ed=None
                    property_price=st.number_input('Sale price',value=0.0,step=0.1)

                property_availability=st.radio('Is it available? ',['Yes','No'],index=0)

                if st.form_submit_button('Submit'):
                    property_id='pr'+get_random_string(5)
                    agents_id='a'+user_id
                    todays_date=datetime.date.today()
                    date_posted=todays_date
                    add_property_query='''insert into property(property_id,agents_id,type,city,state,location,description,availability,price,date_posted,start_date,end_date,sale_or_rent,crime_rate)
                    values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
                    add_property_values=(property_id,agents_id,property_type,property_city,property_state,property_location,property_desc,
                    property_availability,property_price,date_posted,property_sd,property_ed,sale_or_rent,crime_rate)
                    entry_execution(add_property_query,add_property_values)
                    #if property_type=='land':
                    land_id='l'+property_id
                    query='''insert into land(land_id,property_id,sqt_area) values (%s,%s,%s)'''
                    values=(land_id,property_id,land_sft)
                    entry_execution(query,values)
                    #inserting the near by schools
                    if nearby_schools_list!='None':
                        for school in nearby_schools_list:
                            entry_execution('insert into nearby_schools(property_id,school_name) values (%s,%s)',(property_id,school,))
                    success_empty=st.empty()
                    success_empty.success('New property added')
                    time.sleep(2)
                    success_empty.empty()
                    st.experimental_rerun()

        elif property_type=='Apartment':
            with st.form('apartment',clear_on_submit=True):
                apartment_rooms=st.number_input('Number of rooms',step=1)
                apartment_sft=st.number_input('Square footage')
                apartment_sft=float(apartment_sft)
                building_type=st.text_input('Building Type')
                property_location=st.text_input('Property location',value='')
                property_city=st.text_input('City',value='')
                property_state=st.text_input('State',value='')
                nearby_schools=st.text_input('Enter nearby school names(if exists) using commas',value='')
                if len(nearby_schools)!=0:
                    nearby_schools_list=nearby_schools.split(',')
                crime_rate=st.number_input('Crime Rate',min_value=0.0,max_value=100.0,step=0.1)
                property_desc=st.text_input('Description',value='')
                if sale_or_rent=='Rental':
                    todays_date=datetime.date.today()
                    property_sd=st.date_input('Lease start date',min_value=todays_date)
                    st.write(property_sd)
                    property_ed=st.date_input('Lease end date',value=property_sd,min_value=property_sd)
                    property_price=st.number_input('Rental price per month',value=0.0,step=0.1)
                elif sale_or_rent=='Sale':
                    todays_date=datetime.date.today()
                    property_sd=None
                    property_ed=None
                    property_price=st.number_input('Sale price',value=0.0,step=0.1)

                property_availability=st.radio('Is it available? ',['Yes','No'],index=0)

                if st.form_submit_button('Submit'):
                    property_id='pr'+get_random_string(5)
                    agents_id='a'+user_id
                    st.write(user_id)
                    st.write(agents_id)
                    date_posted_empty=st.empty()
                    date_posted=date_posted_empty.date_input('')
                    date_posted_empty.empty()
                    add_property_query='''insert into property(property_id,agents_id,type,city,state,location,description,availability,price,date_posted,start_date,end_date,sale_or_rent,crime_rate)
                    values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
                    add_property_values=(property_id,agents_id,property_type,property_city,property_state,property_location,property_desc,
                    property_availability,property_price,date_posted,property_sd,property_ed,sale_or_rent,crime_rate)
                    entry_execution(add_property_query,add_property_values)
                    apts_id='a'+property_id
                    query='''insert into apartment(apts_id,property_id,rooms,sqt_area) values (%s,%s,%s,%s)'''
                    values=(apts_id,property_id,apartment_rooms,apartment_sft)
                    entry_execution(query,values)
                    #inserting the near by schools
                    if nearby_schools_list!='None':
                        for school in nearby_schools_list:
                            entry_execution('insert into nearby_schools(property_id,school_name) values (%s,%s)',(property_id,school,))
                    success_empty=st.empty()
                    success_empty.success('New property added')
                    time.sleep(2)
                    success_empty.empty()

                    st.experimental_rerun()


        elif property_type=='Commercial Building':
            with st.form('commercial building',clear_on_submit=True):
                cb_sft=st.number_input('Square footage')
                business_type=st.text_input('Business Type')
                cb_sft=float(cb_sft)

                property_location=st.text_input('Property location',value='')
                property_city=st.text_input('City',value='')
                property_state=st.text_input('State',value='')
                nearby_schools=st.text_input('Enter nearby school names(if exists) using commas',value='')
                if len(nearby_schools)!=0:
                    nearby_schools_list=nearby_schools.split(',')

                else:
                    nearby_schools_list='None'
                crime_rate=st.number_input('Crime Rate',min_value=0.0,max_value=100.0,step=0.1)
                property_desc=st.text_input('Description',value='')
                if sale_or_rent=='Rental':
                    todays_date=datetime.date.today()
                    property_sd=st.date_input('Lease start date',min_value=todays_date)
                    st.write(property_sd)
                    property_ed=st.date_input('Lease end date',value=property_sd,min_value=property_sd)
                    property_price=st.number_input('Rental price per month')
                elif sale_or_rent=='Sale':
                    todays_date=datetime.date.today()
                    property_sd=None
                    property_ed=None
                    property_price=st.number_input('Sale price',value=0.0,step=0.1)

                property_availability=st.radio('Is it available? ',['Yes','No'],index=0)

                if st.form_submit_button('Submit'):
                    property_id='pr'+get_random_string(5)
                    agents_id='a'+user_id

                    date_posted_empty=st.empty()
                    date_posted=date_posted_empty.date_input('')
                    date_posted_empty.empty()
                    add_property_query='''insert into property(property_id,agents_id,type,city,state,location,description,availability,price,date_posted,start_date,end_date,sale_or_rent,crime_rate)
                    values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
                    add_property_values=(property_id,agents_id,property_type,property_city,property_state,property_location,property_desc,
                    property_availability,property_price,date_posted,property_sd,property_ed,sale_or_rent,crime_rate)
                    entry_execution(add_property_query,add_property_values)
                    cb_id='c'+property_id
                    query='''insert into commercial_building(building_id,property_id,business_type,sqf_area) values (%s,%s,%s,%s)'''
                    values=(cb_id,property_id,business_type,cb_sft)
                    entry_execution(query,values)
                    #inserting the near by schools
                    if nearby_schools_list!='None':
                        for school in nearby_schools_list:
                            entry_execution('insert into nearby_schools(property_id,school_name) values (%s,%s)',(property_id,school,))
                    success_empty=st.empty()
                    success_empty.success('New property added')
                    time.sleep(2)
                    success_empty.empty()
                    #intial_value=None
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
                '  \n',pro[6],'  \n',pro[7],'  \n',str(pro[9]))
            if st.button('Delete'):
                property_id=pro[0]
                if pro[2]=='House':
                    house_id='h'+property_id
                    delete_query_house = 'delete from house where property_id = %s'
                    delete_house_values = (property_id,)
                    delete_schools='delete from nearby_schools where property_id=%s'
                    delete_school_values=(property_id,)
                    entry_execution(delete_schools,delete_school_values)
                    entry_execution(delete_query_house,delete_house_values)
                elif pro[2]=='Apartment':
                    house_id='h'+property_id
                    delete_query_house = 'delete from apartment where property_id = %s'
                    delete_house_values = (property_id,)
                    entry_execution(delete_query_house,delete_house_values)
                    delete_schools='delete from nearby_schools where property_id=%s'
                    delete_school_values=(property_id,)
                    entry_execution(delete_schools,delete_school_values)
                    entry_execution(delete_query_house,delete_house_values)
                elif pro[2]=='Commercial Building':
                    house_id='h'+property_id
                    delete_query_house = 'delete from commercial_building where property_id = %s'
                    delete_house_values = (property_id,)
                    entry_execution(delete_query_house,delete_house_values)
                    delete_schools='delete from nearby_schools where property_id=%s'
                    delete_school_values=(property_id,)
                    entry_execution(delete_schools,delete_school_values)
                    entry_execution(delete_query_house,delete_house_values)
                elif pro[2]=='Vacation Home':
                    vacation_home='v'+property_id
                    delete_query_house = 'delete from vacation_home where property_id = %s'
                    delete_house_values = (property_id,)
                    entry_execution(delete_query_house,delete_house_values)
                    delete_schools='delete from nearby_schools where property_id=%s'
                    delete_school_values=(property_id,)
                    entry_execution(delete_schools,delete_school_values)
                    entry_execution(delete_query_house,delete_house_values)
                elif pro[2]=='Land':
                    house_id='h'+property_id
                    delete_query_house = 'delete from land where property_id = %s'
                    delete_house_values = (property_id,)
                    entry_execution(delete_query_house,delete_house_values)
                    delete_schools='delete from nearby_schools where property_id=%s'
                    delete_school_values=(property_id,)
                    entry_execution(delete_schools,delete_school_values)
                    entry_execution(delete_query_house,delete_house_values)
                delete_property_booking='delete from property_booking where property_id = %s'
                delete_property_booking_values=(property_id,)
                entry_execution(delete_property_booking,delete_property_booking_values)
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
        st.write('Select the properties below to modify')
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
                st.write('**Rental or Sale:**','  \n**Type:**','  \n**City:** ','  \n**State:** ','  \n**Location:** ',
                '  \n**Description:** ','  \n**Availability:** ','  \n**Price:** ')
            with col2:
                st.write(pro[12],'  \n',pro[2],'  \n',pro[3],'  \n',pro[4],'  \n',pro[5],
                '  \n',pro[6],'  \n',pro[7],'  \n',str(pro[9]))

            #
            agent_id='a'+user_id
            property_id=pro[0]
            agent_id=pro[1]
            type=pro[2]
            city=pro[3]
            state=pro[4]
            location=pro[5]
            description=pro[6]
            availability=pro[7]
            date=pro[8]
            price=pro[9]
            sale_or_rent=pro[12]

            rental_or_sale_index=['Rental','Sale'].index(pro[12])
            rental_or_sale=st.selectbox('Rental or Sale',options=['Rental','Sale'],index=rental_or_sale_index)
            property_type_index=['House','Apartment','Commercial Building','Vacation Home','Land'].index(pro[2])
            property_type=st.selectbox('Property type',['House','Apartment','Commercial Building','Vacation Home','Land'],index=property_type_index)
            availability_index=['Yes','No'].index(availability)
            property_location=st.text_input('Property location',value=location)
            property_city=st.text_input('City',value=city)
            property_state=st.text_input('State',value=state)
            property_desc=st.text_input('Description',value=description)
            property_price=st.number_input('Price',value=price,step=0.1)

            property_availability=st.radio('Is it available? ',options=['Yes','No'],index=availability_index)
            condition=(sale_or_rent==rental_or_sale)&(property_type==type)&(property_city==city)&(property_state==state)&(property_location==location)&(property_desc==description)&(property_availability==availability)&(property_price==price)

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
        st.header('Agent page')
        st.write('Welcome!')
        select_action=st.radio('Please select to perform: ',['Add a new property',
        'Delete the existing property','Modify the existing property','Show property status'])
        if select_action=='Add a new property':
            ob_pro.add_property(user_id)
        if select_action=='Delete the existing property':
            ob_pro.delete_property(user_id)
        if select_action=='Modify the existing property':
            ob_pro.modify_property(user_id)
        if select_action=='Show property status':
            ob_pro.property_status(user_id)

    def booked_properties(self):
        record=ob_login.user_status_list[-1]
        user_id=record[0]
        renters_id='r'+user_id
        booked_proeperties_query='''select * from property_booking inner join property on property_booking.property_id=property.property_id inner join credit_card on property_booking.creditcard_id=credit_card.creditcard_id where property_booking.renters_id=%s'''
        values=(renters_id,)
        booked_properties_records=query_execution(booked_proeperties_query,values)

        st.subheader('List of properties booked')
        for pro in booked_properties_records:
            booking_id=pro[0]
            property_id=pro[1]
            renters_id=pro[2]
            booking_date=pro[3]
            creditcard_id=pro[4]
            property_id=pro[5]
            agents_id=pro[6]
            type=pro[7]
            city=pro[8]
            state=pro[9]
            location=pro[10]
            description=pro[11]
            availability=pro[12]
            date_posted=pro[13]
            price=pro[14]
            start_date=pro[15]
            end_date=pro[16]
            creditcard_id=pro[17]
            card_number=pro[18]
            renters_id=pro[19]
            address=pro[20]
            card_expiry_date=pro[21]
            col1,col2=st.columns(2)
            with col1:
                st.write('Property ID: ')
                st.write('Property type: ')
                st.write('Location: ')
                st.write('City: ')
                st.write('State: ')
                st.write('Price: ')
                st.write('Start date: ')
                st.write('End date: ')
                st.write('Payment card: ')
                st.write('Billing Address: ')
            with col2:
                st.write(property_id)
                st.write(type)
                st.write(location)
                st.write(city)
                st.write(state)
                st.write(str(price))
                st.write(str(start_date))
                st.write(str(end_date))
                st.write(card_number)
                st.write(address)
            if st.button('Cancel booking',key=booking_id+'cancel'):
                cancel_booking_query='delete from property_booking where property_id = %s'
                cancel_booking_query_values=(property_id,)
                entry_execution(cancel_booking_query,cancel_booking_query_values,)
                update_property_avail='update property set availability=%s where property_id=%s'
                update_property_values=('Yes',property_id,)
                entry_execution(update_property_avail,update_property_values)
                st.success('Booking cancelled successfully, amount will be refunded within 7 days.')
                time.sleep(1)
                st.experimental_rerun()
            st.write('---------')




    def search(self):
        st.subheader('Search for properties')
        properties=''
        filter_choice=st.radio('',['Show all results','Apply filter'])
        if filter_choice=='Show all results':
            sort_by=st.radio('Order price by',['Low to high','High to Low'])
            if sort_by=='Low to high':
                properties_query='''select * from property'''+''' order by price asc'''
            else:
                properties_query='''select * from property order by price desc'''

            properties=query_execution(properties_query)
            record=ob_login.user_status_list[-1]
            user_id=record[0]

        else:
            property_type=st.selectbox('Property type',['House','Apartment','Commercial Building','Vacation Home','Land'])
            if property_type=='House':
                properties_query='''select location from property inner join house on house.property_id=property.property_id'''
                properties_=query_execution(properties_query)
                properties_location=[]
                for i in properties_:
                    properties_location.append(i[0])
                bedrooms_num=st.number_input('Number of bedrooms',step=1)
                location=st.selectbox('Location',options=properties_location)
                sale_or_rent_choice=st.radio('Show',['Sale','Rental'])
                min_price=st.number_input('Minimum price')
                max_price=st.number_input('Maximum price')
                sort_by=st.radio('Order price by',['Low to high','High to Low'])
                if sort_by=='Low to high':
                    query_ext=''' order by price desc'''
                else:
                    query_ext=''' order by price asc'''
                properties_house_query='''select * from property inner join house on house.property_id=property.property_id where house.rooms=%s
                and location=%s and sale_or_rent=%s and price>=%s and price<=%s'''+query_ext
                properties_house_query_values=(bedrooms_num,location,sale_or_rent_choice,min_price,max_price)
                if st.button('Apply filter',key='house filter'):
                    properties=query_execution(properties_house_query,properties_house_query_values)
            elif property_type=='Apartment':
                properties_query='''select location from property inner join apartment on apartment.property_id=property.property_id'''
                properties_=query_execution(properties_query)
                properties_location=[]
                for i in properties_:
                    properties_location.append(i[0])
                bedrooms_num=st.number_input('Number of bedrooms')
                location=st.selectbox('Location',options=properties_location)
                sale_or_rent_choice=st.radio('Show',['Sale','Rental'])
                min_price=st.number_input('Minimum price')
                max_price=st.number_input('Maximum price')
                sort_by=st.radio('Order price by',['Low to high','High to Low'])
                if sort_by=='Low to high':
                    query_ext=''' order by price desc'''
                else:
                    query_ext=''' order by price asc'''
                properties_apartment_query='''select * from property inner join apartment on apartment.property_id=property.property_id where apartment.rooms=%s
                and location=%s and sale_or_rent=%s and price>=%s and price<=%s'''+query_ext
                properties_apartment_query_values=(bedrooms_num,location,sale_or_rent_choice,min_price,max_price)
                if st.button('Apply filter',key='apartment filter'):
                    properties=query_execution(properties_apartment_query,properties_apartment_query_values)

            elif property_type=='Vacation Home':
                properties_query='''select location from property inner join vacation_home on vacation_home.property_id=property.property_id'''
                properties_=query_execution(properties_query)
                properties_location=[]
                for i in properties_:
                    properties_location.append(i[0])
                bedrooms_num=st.number_input('Number of bedrooms',step=1)
                location=st.selectbox('Location',options=properties_location)
                sale_or_rent_choice=st.radio('Show',['Sale','Rental'])
                min_price=st.number_input('Minimum price')
                max_price=st.number_input('Maximum price')
                sort_by=st.radio('Order price by',['Low to high','High to Low'])
                if sort_by=='Low to high':
                    query_ext=''' order by price desc'''
                else:
                    query_ext=''' order by price asc'''
                properties_vc_query='''select * from property inner join vacation_home on vacation_home.property_id=property.property_id where vacation_home.rooms=%s
                and location=%s and sale_or_rent=%s and price>=%s and price<=%s'''+query_ext
                properties_vc_query_values=(bedrooms_num,location,sale_or_rent_choice,min_price,max_price)
                if st.button('Apply filter',key='house filter'):
                    properties=query_execution(properties_vc_query,properties_vc_query_values)

            elif property_type=='Land':
                properties_query='''select location from property inner join land on land.property_id=property.property_id'''
                properties_=query_execution(properties_query)
                properties_location=[]
                for i in properties_:
                    properties_location.append(i[0])

                location=st.selectbox('Location',options=properties_location)
                sale_or_rent_choice=st.radio('Show',['Sale','Rental'])
                min_price=st.number_input('Minimum price')
                max_price=st.number_input('Maximum price')
                sort_by=st.radio('Order price by',['Low to high','High to Low'])
                if sort_by=='Low to high':
                    query_ext=''' order by price desc'''
                else:
                    query_ext=''' order by price asc'''
                properties_land_query='''select * from property inner join land on land.property_id=property.property_id where
                location=%s and sale_or_rent=%s and price>=%s and price<=%s'''+query_ext
                properties_land_query_values=(location,sale_or_rent_choice,min_price,max_price)
                if st.button('Apply filter',key='house filter'):
                    properties=query_execution(properties_land_query,properties_land_query_values)

            else:
                properties_query='''select location from property inner join commercial_building on commercial_building.property_id=property.property_id'''
                properties_=query_execution(properties_query)
                properties_location=[]
                for i in properties_:
                    properties_location.append(i[0])
                location=st.selectbox('Location',options=properties_location)
                sale_or_rent_choice=st.radio('Show',['Sale','Rental'])
                min_price=st.number_input('Minimum price')
                max_price=st.number_input('Maximum price')
                sort_by=st.radio('Order price by',['Low to high','High to Low'])
                if sort_by=='Low to high':
                    query_ext=''' order by price desc'''
                else:
                    query_ext=''' order by price asc'''
                properties_cb_query='''select * from property inner join commercial_building on commercial_building.property_id=property.property_id where
                location=%s and price>=%s and price<=%s and sale_or_rent=%s'''+query_ext
                properties_cb_query_values=(location,min_price,max_price,sale_or_rent_choice)
                if st.button('Apply filter',key='commercial building filter'):
                    properties=query_execution(properties_cb_query,properties_cb_query_values)






#- Show the price, number of bedrooms, property type, and property description for each property.
#Furthermore, the users can specify whether the results should be ordered by: price or number of bedrooms.

        if len(properties)!=0:
            record=ob_login.user_status_list[-1]
            user_id=record[0]
        else:
            st.info('There are no properties with the given filters')

        for pro in properties:
            property_id=pro[0]
            agents_id=pro[1]
            type=pro[2]
            city=pro[3]
            state=pro[4]
            location=pro[5]
            description=pro[6]
            availability=pro[7]
            booking_date=pro[8]
            price=pro[9]
            property_sd=pro[10]
            property_ed=pro[11]
            sale_or_rent=pro[12]
            crime_rate=pro[13]
            schools_query='''select school_name from nearby_schools where property_id=%s'''
            schools_query_values=(property_id,)
            schools=query_execution(schools_query,schools_query_values)
            button_empty=st.empty()
            col1,col2=st.columns(2)
            with col1:
                st.write('Property type: ')
                if (type=='House'):
                    st.write('Number of bedrooms:')
                elif (type=='Apartment'):
                    st.write('Number of bedrooms:')
                else:
                    pass
                st.write('Location: ')
                st.write('City: ')
                st.write('State: ')
                st.write('Price: ')
                st.write('Near By Schools: ')
                st.write('Crime rate: ')
                st.write('Description: ')


            with col2:
                st.write(type)
                if (type=='House'):
                    bedrooms_count='''select house.rooms from house inner join property on property.property_id=house.property_id where property.property_id=%s'''
                    bedrooms_count_values=(property_id,)
                    bedroom_records=query_execution(bedrooms_count,bedrooms_count_values)
                    st.write(str(bedroom_records[0][0]))
                elif (type=='Apartment'):
                    bedrooms_count='''select apartment.rooms from apartment inner join property on property.property_id=apartment.property_id where property.property_id=%s'''
                    bedrooms_count_values=(property_id,)
                    bedroom_records=query_execution(bedrooms_count,bedrooms_count_values)
                    if len(bedroom_records)!=0:
                        st.write(str(bedroom_records[0][0]))
                    else:
                        st.write('Not provided')
                else:
                    pass
                st.write(location)
                st.write(city)
                st.write(state)
                st.write(str(price))
                school_name=''
                if len(schools)!=0:
                    for school in schools:
                        school_name=school_name+school[0]+', '
                else:
                    st.write('None')
                st.write(school_name)
                st.write(str(crime_rate))
                st.write(description)




            if availability=='No':
                st.info('Not available')
            if availability=='Yes':
                search_options=st.selectbox('Select the action',['View','Book'],key=pro[0])
                if search_options=='View':
                    pass
                elif search_options=='Book':
                    renter_id='r'+user_id
                    query='''select * from credit_card where renters_id = %s'''
                    values=(renter_id,)
                    credit_card_records=query_execution(query,values)
                    #st.write(credit_card_records)
                    if len(credit_card_records)==0:
                        todays_date=datetime.date.today()
                        lease_start_date=st.date_input('Lease start date',min_value=todays_date,max_value=property_ed,key=property_id+'start_date')
                        lease_end_date=st.date_input('Lease end date',min_value=todays_date,max_value=property_ed,key=property_id+'end_date')
                        creditcard_number=st.text_input('Card Number',key=property_id+'card_number')
                        billing_address=st.text_input('Billing Address',key=property_id+'billing_address')
                        expiry_date=st.text_input('Expiry date',key=property_id+'expiry_date')


                        if st.button('Add card and book',key=property_id+'button'):
                            creditcard_id=get_random_string(7)
                            booking_id='b'+get_random_string(5)
                            card_num_exists='''select card_number from credit_card where renters_id = %s and card_number = %s'''
                            values=(renter_id,creditcard_number,)
                            records=query_execution(card_num_exists,values)
                            if len(records)==0:
                                add_cc_query='''insert into credit_card(creditcard_id,card_number,renters_id,address,card_expiry_date) values (%s,%s,%s,%s,%s)'''
                                add_cc_values=(creditcard_id,creditcard_number,renter_id,billing_address,expiry_date)
                                entry_execution(add_cc_query,add_cc_values)
                                add_property_query='''insert into property_booking (booking_id,property_id,renters_id,booking_date,creditcard_id) values (%s,%s,%s,%s,%s)'''
                                add_property_values=(booking_id,property_id,renter_id,todays_date,creditcard_id)
                                entry_execution(add_property_query,add_property_values)
                                #update availability in the property table
                                update_property_query='''update property set availability=%s where property_id = %s'''
                                updated_availability='No'
                                update_property_values=(updated_availability,property_id,)
                                entry_execution(update_property_query,update_property_values)
                                #update reward prgram.
                                reward_execution=query_execution('select reward_points from reward_program where renter_id=%s',(renter_id,))
                                if len(reward_execution)!=0:
                                    points=int(reward_execution[0][0])+int(price)
                                    entry_execution('update reward_program set reward_points = %s where renter_id = %s',(points,renter_id,))

                                st.success('Success')

                                st.experimental_rerun()
                            else:
                                st.info('Card already exists')

                    else:
                        card_numbers=[]
                        for record in credit_card_records:
                            card_numbers.append(record[1])
                        todays_date=datetime.date.today()
                        lease_start_date=st.date_input('Lease start date',min_value=todays_date,max_value=property_ed,key=property_id+'start_date')
                        lease_end_date=st.date_input('Lease end date',min_value=todays_date,max_value=property_ed,key=property_id+'end_date')
                        select_cc=st.selectbox('Select card',options=['Select from below']+card_numbers,key=property_id+'select card')
                        if select_cc!='Select from below':
                            card_number_index=card_numbers.index(select_cc)
                            current_card=credit_card_records[card_number_index]
                            creditcard_id=current_card[0]
                            st.write('Card Number: ',current_card[1])
                            st.write('Expiry date: ',current_card[4])
                            st.write('Billing address: ',current_card[3])
                            if st.button('Book',key=property_id+'book without new card'):
                                booking_id='b'+get_random_string(5)
                                add_property_query='''insert into property_booking (booking_id,property_id,renters_id,booking_date,creditcard_id) values (%s,%s,%s,%s,%s)'''
                                add_property_values=(booking_id,property_id,renter_id,todays_date,creditcard_id)
                                entry_execution(add_property_query,add_property_values)
                                update_property_query='''update property set availability=%s where property_id = %s'''
                                updated_availability='No'
                                update_property_values=(updated_availability,property_id,)
                                entry_execution(update_property_query,update_property_values)
                                #update reward prgram.
                                reward_execution=query_execution('select reward_points from reward_program where renter_id=%s',(renter_id,))
                                if len(reward_execution)!=0:
                                    points=int(reward_execution[0][0])+int(price)
                                    entry_execution('update reward_program set reward_points = %s where renter_id = %s',(points,renter_id,))
                                st.success('Property booked')
                                time.sleep(1)

                                st.experimental_rerun()

            st.write('--------------')






    def manage_payments(self):
        record=ob_login.user_status_list[-1]
        user_id=record[0]
        select_op=st.radio('',['Add new card','Modify card','Delete card'])
        if select_op=='Add new card':
            st.write('Credit card operations')
            #
            query='''select * from credit_card where renters_id = %s'''
            renter_id='r'+user_id
            values=(renter_id,)
            credit_card_records=query_execution(query,values)
            #st.write(credit_card_records)
            cc_num=[]
            for cc in credit_card_records:
                cc_num.append(cc[1])
            #
            card_number=st.text_input('Card Number')
            expiry_date=st.text_input('Expiry')
            billing_address=st.text_input('Address')
            if st.button('Add'):
                creditcard_id=get_random_string(7)
                card_num_exists='''select card_number from credit_card where renters_id = %s and card_number = %s'''
                values=(renter_id,card_number,)
                records=query_execution(card_num_exists,values)
                if len(records)!=0:
                    st.error('Card already exists')
                else:
                    while True:
                        creditcard_id=get_random_string(7)
                        cc_id_exists='''select * from credit_card where creditcard_id = %s'''
                        values=(creditcard_id,)
                        records=query_execution(cc_id_exists,values)
                        if len(records)==0:
                            cc_insert='''insert into credit_card (creditcard_id,card_number,renters_id,address,card_expiry_date) values (%s,%s,%s,%s,%s)'''
                            cc_values=(creditcard_id,card_number,renter_id,billing_address,expiry_date)
                            entry_execution(cc_insert,cc_values)
                            break
                        else:
                            pass
                    st.success('Card added successfully')

        if select_op=='Delete card':
            st.write('Delete card')
            query='''select * from credit_card where renters_id = %s'''
            renter_id='r'+user_id
            values=(renter_id,)
            credit_card_records=query_execution(query,values)
            cc_num=[]
            for cc in credit_card_records:
                cc_num.append(cc[1])
            #st.write(cc_num)
            if len(cc_num)==0:
                st.write('No cards found')
            if len(cc_num)!=0:
                cc_select=st.selectbox('',cc_num)
                if cc_select!='Select':
                    #st.write(credit_card_records)
                    cc_index=cc_num.index(cc_select)
                    current_card=credit_card_records[cc_index]
                    card_id=current_card[0]
                    card_number=current_card[1]
                    renters_id=current_card[2]
                    address=current_card[3]
                    expiry_date=current_card[4]
                    #st.write(current_card)
                    col1,col2=st.columns(2)
                    with col1:
                        st.write('Card Number: ')
                        st.write('Expiry: ')
                        st.write('Address: ')
                    with col2:
                        st.write(card_number)
                        st.write(expiry_date)
                        st.write(address)
                    if st.button('Delete'):
                        delete_card_query='''delete from credit_card where card_number = %s'''
                        values=(card_number,)
                        entry_execution(delete_card_query,values)
                        st.success('Card removed successfully')
                        time.sleep(1)
                        cc_select='Select'
                        st.experimental_rerun()


        if select_op=='Modify card':
            st.write('Modify card')
            query='''select * from credit_card where renters_id = %s'''
            renter_id='r'+user_id
            values=(renter_id,)
            credit_card_records=query_execution(query,values)
            cc_num=[]
            for cc in credit_card_records:
                cc_num.append(cc[1])
            if len(cc_num)==0:
                st.info('No cards found')
            else:
                cc_select=st.selectbox('',cc_num)
                if cc_select!='Select':

                    cc_index=cc_num.index(cc_select)
                    current_card=credit_card_records[cc_index]
                    card_id=current_card[0]
                    card_number=current_card[1]
                    renters_id=current_card[2]
                    address=current_card[3]
                    expiry_date=current_card[4]
                    new_card_number=st.text_input('Card Number: ',value=card_number)
                    new_expiry_date=st.text_input('Expiry: ',value=expiry_date)
                    new_address=st.text_input('Address: ',value=address)
                    if (new_card_number==card_number)&(new_expiry_date==expiry_date)&(address==new_address):
                        pass
                    else:
                        if st.button('Modify'):
                            update_query='''UPDATE credit_card SET card_number = %s, card_expiry_date = %s, address = %s where creditcard_id = %s'''
                            values=(new_card_number,new_expiry_date,new_address,card_id)
                            entry_execution(update_query,values)
                            st.success('Modified successfully')




    def renter(self):
        record=ob_login.user_status_list[-1]
        user_id=record[0]
        st.header('Renter page')
        st.subheader('Welcome')
        renter_id='r'+user_id
        reward_program_query='''select reward_points from reward_program where renter_id = %s'''
        query_execution_values=(renter_id,)
        rewards=query_execution(reward_program_query,query_execution_values)
        if len(rewards)!=0:
            st.write('Reward points: ',rewards[0][0])
        renter_options=st.selectbox('Please select the options',['Search for the properties','Manage payments','Booked Properties'])
        if renter_options=='Manage payments':
            ob_pro.manage_payments()
        if renter_options=='Search for the properties':
            ob_pro.search()
        if renter_options=='Booked Properties':
            ob_pro.booked_properties()

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
    reward_or_not_empty=st.empty()
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
        move_in_date=move_in_date_empty.date_input('Move-In Date',min_value=todays_date)
        preferedlocation=preferedlocation_empty.text_input('Prefered Location')
        budget=budget_empty.number_input('Budget',step=0.1)
        reward_or_not=reward_or_not_empty.radio('Want to join reward program?',options=['Yes','No'])

    address=ad_empty.text_input('Address')
    password=pass_empty.text_input('Enter password',type='password')
    repassword=repass_empty.text_input('Re Enter the password',type='password')
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
                        if reward_or_not=='Yes':
                            entry_execution('insert into reward_program(renter_id,reward_points) values (%s,%s)',(renters_id,0))
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
