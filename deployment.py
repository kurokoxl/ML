import streamlit as st
import requests
from streamlit_lottie import st_lottie
import joblib
import numpy as np

st.set_page_config(page_title='Job Placement', page_icon='::star::')

def load_lottie(url): # test url if you want to use your own lottie file 'valid url' or 'invalid url'
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def prepare_input_data_for_model(gender,ssc_p,ssc_b , hsc_p,hsc_b,hsc_subject,degree_p,undergrad_degree,workex,employability_test,specialisation,mba_p):
    #sex = gender.map(gen)
    if gender == 'M':
        sex = 0
    else:
        sex = 1
    #s_b = ssc_b.map(sb)
    if ssc_b == 'Central':
        s_b = 0
    else:
        s_b = 1
    #h_b = hsc_b.map(hb)
    if hsc_b == 'Central':
        h_b = 0
    else:
        h_b = 1
    #h_s = hsc_subject.map(h_sub)
    if hsc_subject == 'Commerce':
        h_s = 0
    elif hsc_subject == 'Science':
        h_s = 1
    else:
        h_s = 2
    #g_d = undergrad_degree.map(grad_degree)
    if undergrad_degree == 'Comm&Mgmt':
        g_d = 0 
    elif undergrad_degree == 'Sci&Tech':
        g_d = 1
    else:
        g_d = 2
    #wexp = workex.map(w_exp)
    if workex == 'Yes':
        wexp = 0
    else:
        wexp = 1
    #specia = specialisation.map(spec)
    if specialisation == 'Mkt&Fin':
        specia = 0
    else:
        specia = 1
    
    A = [sex,ssc_p,s_b,hsc_p,h_b,h_s,degree_p,g_d,wexp,employability_test,specia,mba_p]
    sample = np.array(A).reshape(-1,len(A))
    
    return sample



loaded_model = joblib.load(open("job_placement_model", 'rb'))



st.write('# Job Placement Deployment')
#st.header('Placement')

lottie_link = "https://assets8.lottiefiles.com/packages/lf20_ax5yuc0o.json"
animation = load_lottie(lottie_link)

st.write('---')
st.subheader('Enter your details to predict your job placement status')

with st.container():
    
    right_column, left_column = st.columns(2)
    
    with right_column:
        name = st.text_input('Name:')
        
        gender = st.radio('Gender : ', ['F', 'M'])
        
        ssc_p = st.number_input('SSC Percentage : ', min_value=0.0, max_value=100.0, value=0.0, step=0.1)
        
        ssc_b = st.radio('SSC Board : ', ['Central', 'Others'])
        
        hsc_p = st.number_input('HSC Percentage : ', min_value=0.0, max_value=100.0, value=0.0, step=0.1)
        
        hsc_b = st.radio('HSC Board : ', ['Central', 'Others'])
        
        hsc_subject = st.selectbox('HSC Subject : ', ('Commerce', 'Science', 'Arts'))
        
        degree_p = st.number_input('Degree Percentage : ', min_value=0.0, max_value=100.0, value=0.0, step=0.1)
        
        undergrad_degree = st.selectbox('Undergraduate Degree : ', ('comm&Mgmt', 'Sci&Tech', 'Others'))
        
        workex = st.radio('Work Experience : ', ['Yes', 'No'])
        
        employability_test = st.number_input('Employability Test Percentage : ', min_value=0.0, max_value=100.0, value=0.0, step=0.1)
        
        specialisation = st.selectbox('Specialisation : ', ('Mkt&Fin', 'Mkt&HR'))
        
        mba_p = st.number_input('MBA Percentage : ', min_value=0.0, max_value=100.0, value=0.0, step=0.1)
        
        sample = prepare_input_data_for_model(gender,ssc_p,ssc_b , hsc_p,hsc_b,hsc_subject,degree_p,undergrad_degree,workex,employability_test,specialisation,mba_p)
        

    with left_column:
        st_lottie(animation, speed=1, height=400, key="initial")
        

    if st.button('Predict'):
            pred_Y = loaded_model.predict(sample)
            
            if pred_Y == 0:
                #st.write("## Predicted Status : ", result)
                st.write('### Congratulations ', name, '!! You are placed.')
                st.balloons()
            else:
                st.write('### Sorry ', name, '!! You are not placed.')
    
