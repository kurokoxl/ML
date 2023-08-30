import streamlit as st
import requests
from streamlit_lottie import st_lottie
import joblib
import numpy as np
import time

st.set_page_config(page_title='Loan prediction', page_icon='::star::') #PAGE NAME

             

def load_lottie(url): # test url if you want to use your own lottie file 'valid url' or 'invalid url'
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def prepare_input_data_for_model(CD_Account,Mortgage,Education , CCAvg,Family,Income):
    
    #s_b = ssc_b.map(sb)
    if CD_Account == 'Yes':
        cd = 1
    else:
        cd = 0
    
    A = [Income,Family, CCAvg,Education,Mortgage ,cd]
    sample = np.array(A).reshape(-1,len(A))
    
    return sample



loaded_model = joblib.load(open("loan_model", 'rb'))#MODEL FILE NAME# 




st.write('# Loan prediction deployment :dollar:')
#st.header('Placement')

lottie_link = "https://lottie.host/1578ed6f-efac-4e1d-904e-fc83d39bcb38/pzCq6uJ38M.json"
animation = load_lottie(lottie_link)

st.write('---')
st.subheader('Enter your details to predict your loan')

with st.container():
    with st.spinner(text="Loading model..."):
        time.sleep(1.5)
    
    right_column, left_column = st.columns(2)
    
    with right_column:
        name = st.text_input('Name:')
        Mortgage = st.number_input('Mortgage : ', min_value=0.0, value=0.0, step=0.1)
        Income = st.number_input('Income : ', min_value=0.0, max_value=200.0, value=0.0, step=0.1)
        CCAvg  = st.number_input('CCAvg: ', min_value=0.0, max_value=100.0, value=0.0, step=0.1)
        Family =   st.number_input('Family number: ', min_value=0.0, max_value=100.0, value=0.0, step=1.0)
        Education=st.number_input('Education: ', min_value=0.0, max_value=3.0, value=0.0, step=1.00)
        CD_Account=st.radio('CD Account :',['Yes','No'])

        
       # ID = st.number_input('ID : ',  min_value=0.0, max_value=100.0, value=0.0, step=0.1)
       # Age = st.number_input('Age : ',  min_value=0.0, max_value=100.0, value=0.0, step=0.1)
     #   Experience= st.number_input('Experience : ', min_value=0.0, max_value=100.0, value=0.0, step=0.1)
      #  ZIP_Code = st.number_input('ZIP Code: ', min_value=0.0, max_value=99999.0, value=0.0, step=0.1)
      #  Personal_Loan = st.radio('Personal Loan : ', ['Yes', 'No'])
       # Securities_Account = st.radio('Securities Account : ', ['Yes', 'No'])
       # Online = st.radio('Online : ', ['Yes', 'No'])
      #  CreditCard = st.radio('CreditCard : ', ['Yes', 'No'])
       
        sample = prepare_input_data_for_model(CD_Account,Mortgage,Education , CCAvg,Family,Income)
        #CHANGE DATA TO 0 1

    with left_column:
        st_lottie(animation, speed=1, height=400, key="initial")
        

    if st.button('Predict'):
            pred_Y = loaded_model.predict(sample)###'SEND DATA TO MODEL'
            with st.spinner(text="Predicting..."):
                    time.sleep(1.5)
                    
            #change
            if pred_Y == 1:
                #st.write("## Predicted Status : ", result)
                st.success('### Congratulations!! You will take the loan. :white_check_mark:')
                st.balloons()
            else:
               st.error('### Sorry!! You will not take the loan.:x:')
    
