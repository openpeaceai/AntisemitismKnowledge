#!/usr/bin/env python
# coding: utf-8

# In[50]:


import streamlit as st
import pandas as pd
pd.set_option('display.max_colwidth', None)
from sqlalchemy import create_engine

import numpy as np 
import mysql.connector
import pycountry
from datetime import datetime, date, timedelta

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

# Survey information
degree_of_difficulty = 1
survey_id = 2


# In[51]:


st.set_page_config(
    page_title="Antisemitism Knowledge Assessment",
    page_icon="☮️",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "https://openpeace.ai/about-us"
    }
)


# In[52]:


# Add css to make text bigger
st.markdown(
    """
    <style>
    
    label 
    {
    font-size:115% !important;
    color: #800000;
    }
    
    div[class*="stSelect"] label {
    font-size:115% !important;
    color: #800000;
    }


    div[class*="stTextArea"] label {
    font-size:115% !important;
    color: #800000;
    }

    div[class*="stTextInput"] label {
    font-size:115% !important;
    color: #800000;
    }
    
    div[class*="stDateInput"] label {
    font-size:115% !important;
    color: #800000;
    }

    div[class*="stNumberInput"] label {
    font-size:115% !important;
    color: #800000;
    }
    
    div[data-testid="column"]:nth-of-type(1)
    {
        border:0px solid blue;
        color: #c0c0c0;
    }
    div[data-testid="column"]:nth-of-type(2)
    {
        border:0px solid blue;
        color: #c0c0c0;
        text-align: end;
    }
    .stTextInput > label 
    {
    font-size:115%; font-weight:bold; color:#800000;
    }    
    .stMultiSelect > label 
    {
    font-size:115%; font-weight:bold; color:#800000;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# In[53]:


def send_email(email, score, num_correct_answers, num_incorrect_answers, num_answered_questions, num_unanswered_questions):
    # Create HTML message
    message = MIMEMultipart()
    message["From"] = "Surveys And Quizzes<SurveysAndQuizzes@openpeace.ai>"
    message["To"] = email
    message["Subject"] = "Antisemitism Knowledge Assessment Results"

    # Add image to the email
    #with open("https://img1.wsimg.com/isteam/ip/f8df9fda-2223-42be-a383-5d7d72e7c082/Openpeace%20Logo_Layout%201A.png/:/rs=w:230,h:38,cg:true,m/cr=w:230,h:38/qt=q:100/ll", "rb") as f:
    #    img_data = f.read()
    #image = MIMEImage(img_data)
    #message.attach(image)

    # Create HTML table to show the survey results
    html_table = f"""
        
        
        <img src='https://img1.wsimg.com/isteam/ip/f8df9fda-2223-42be-a383-5d7d72e7c082/Openpeace%20Logo_Layout%201A.png/:/rs=w:230,h:38,cg:true,m/cr=w:230,h:38/qt=q:100/ll'>
        <hr />
        <p>
        Dear {email},
        <br/><br/>
        Thank you for participating in the Antisemitism Knowledge Assessment with degree of difficulty 1.<br/><br/>
        We appreciate your interest in improving your knowledge and understanding of antisemitism.
        <br/><br/>
        Your assessment results are as follows:
        </p>
        <ul>
        <li>Number of correct answers: {num_correct_answers}</li>
        <li>Number of incorrect answers: {num_incorrect_answers}</li>
        <li>Number of unanswered questions: {num_unanswered_questions}</li>
        <li><b>Score: {score:.2f}%</b></li>
        </ul>
        <p>
        We invite you to <a href='https://openpeace.ai/m/create-account'>create an account</a> on our website, <a href='https://openpeace.ai'>openpeace.ai</a>, \
        to access additional resources and to stay up-to-date with our initiatives.<br>
        You can also <a href='https://openpeace.ai/your-voice-matters'>sign up for our newsletter</a> to receive updates on our work.
        </p>
        <p>
        Thank you again for your participation.
        </p>
        <p>
        Best regards,<br/><br/>
        The openpeace.ai Team
        </p>
        <hr />
        <p style='font-size:11px; color:#ccc;'>
        Please note that this email address is not monitored.<br/>
        Please do not reply to this message.<br/>
        If you have any questions or concerns, please <a href='https://openpeace.ai/your-voice-matters'>contact us</a>.
        </p>
        
        
        
        
        <table style="border-collapse: collapse; display:none;">
            <tr>
                <th style="padding: 8px; border: 1px solid black;">Score</th>
                <th style="padding: 8px; border: 1px solid black;">Correct Answers</th>
                <th style="padding: 8px; border: 1px solid black;">Incorrect Answers</th>
                <th style="padding: 8px; border: 1px solid black;">Answered Questions</th>
                <th style="padding: 8px; border: 1px solid black;">Unanswered Questions</th>
            </tr>
            <tr>
                <td style="padding: 8px; border: 1px solid black;">{score:.2f}%</td>
                <td style="padding: 8px; border: 1px solid black;">{num_correct_answers}</td>
                <td style="padding: 8px; border: 1px solid black;">{num_incorrect_answers}</td>
                <td style="padding: 8px; border: 1px solid black;">{num_answered_questions}</td>
                <td style="padding: 8px; border: 1px solid black;">{num_unanswered_questions}</td>
            </tr>
        </table>
    """
    message.attach(MIMEText(html_table, "html"))

    # Send email using SMTP
    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login("father@openpeace.ai", "ulscgjxslrbzpjlj")

        smtp.send_message(message)


# In[54]:


#with st.sidebar:
st.image("https://img1.wsimg.com/isteam/ip/f8df9fda-2223-42be-a383-5d7d72e7c082/Openpeace%20Logo_Layout%201A.png/:/rs=w:230,h:38,cg:true,m/cr=w:230,h:38/qt=q:100/ll", width=230)  # Adjust the width as needed
st.header("Antisemitism Knowledge Assessment")
st.image("https://img1.wsimg.com/isteam/ip/f8df9fda-2223-42be-a383-5d7d72e7c082/antisemiticconspiracies960-min.jpg/:/rs=w:1440,h:1440")

st.markdown('###### Welcome to the Antisemitism Knowledge Assessment, \
            an interactive tool designed to help individuals deepen their \
            understanding of antisemitism and its various manifestations. \
            Our goal is to promote awareness, foster empathy, and facilitate \
            constructive dialogue around this complex and sensitive subject.')
#st.markdown('##') 
st.info('###### Read each scenario carefully: For each scenario, take your \
            time to read and understand the situation presented. \
            Consider the context and the potential implications of the scenario \
            in terms of antisemitism. After analyzing the scenario, select the \
            option that best represents your judgment: "Is Antisemitic" \
            or "Is not Antisemitic." After submission check your email for your \
            Antisemitism Knowledge score.')
st.markdown('---')     
st.markdown('##### Please enter your email address, age and country.')

#st.write("Please enter your email, birthday and country:")    
# Input fields for email, birthday and country
email = st.text_input("Email:", "")

#min_birthday = date.today() - timedelta(days=365*110)
#max_birthday = date.today() - timedelta(days=365*14)
#birthday = st.date_input("Birthday (MM/DD/YYYY):", value=datetime(2000, 1, 1), min_value=min_birthday, max_value=max_birthday)

# Create a list of age options between 14 and 100
age_options = ["Select Your Age"] + list(range(14, 101))

# Create a selectbox for the age option
selected_age = st.selectbox("Select your age:", age_options)

# Output the selected age
#st.write("Selected age:", selected_age)

countries = ["Select Country"] + ["United States"] + sorted([country.name for country in pycountry.countries])
country = st.selectbox("Country:", countries)

st.error('Your information will remain anonymous, as we prioritize your privacy and security.')


st.markdown('---')     
#st.markdown('##### The following section explores a range of topics, \
#            including beliefs, practices, interconnectedness, transcendent experiences, \
#            and personal development.', unsafe_allow_html=False)


# In[55]:


server = '184.168.194.64'
database = 'op_mssql_mama'
username = 'op_papa'
password = 's3x9&B7t'

# Create the connection string
connection_str = f'mssql+pymssql://{username}:{password}@{server}/{database}'

# Create the database engine
engine = create_engine(connection_str)


# In[56]:


# Read scenarios with the specified degree_of_difficulty

scenarios_df = pd.read_sql(f"SELECT * FROM op_papa.antisemitism_knowledge_scenario WHERE degree_of_difficulty = {degree_of_difficulty}", engine)

#scenarios_df = pd.read_sql(f"SELECT TOP 10 * FROM op_papa.antisemitism_knowledge_scenario ORDER BY NEWID()", engine)

# Get the scenario_ids of the filtered scenarios
scenario_ids = scenarios_df['scenario_id'].tolist()

# Read only the responses relevant to the filtered scenarios
responses_df = pd.read_sql(f"SELECT * FROM op_papa.antisemitism_knowledge_response WHERE scenario_id IN ({','.join(map(str, scenario_ids))})", engine)


# In[57]:


# Create the survey
st.markdown("##### Assessment (degree of difficulty: 1)")
#st.markdown("##### Assessment")


# In[58]:


# Initialize user responses
user_responses = {}


# In[59]:


for index, scenario in scenarios_df.iterrows():
    st.write(f"Scenario {index + 1}: {scenario['scenario']}")
    
    # Filter responses for the current scenario
    scenario_responses = responses_df[responses_df['scenario_id'] == scenario['scenario_id']]
    
    # Convert response options to list of strings
    response_options = [row['response_option'].replace("(", "").replace(")", "").replace("'", "").replace(",", "") for _, row in scenario_responses.iterrows() if row['response_option'] != ""]
    response_options.insert(2, "I don't know")
    
    # Display radio buttons for response options
    default_option_index = response_options.index("I don't know") if user_responses.get(scenario['scenario_id']) is None else None
    user_response = st.radio("Choose your response:", response_options, index=default_option_index, key=str(scenario['scenario_id']))
    
    # Store the user's response as a string or None if not selected
    user_responses[scenario['scenario_id']] = user_response if user_response != "I don't know" else None


# In[61]:


# Add a submit button to trigger the calculation of the results
if st.button("Submit"):
    
    with st.spinner('Wait for it...'):
        
        if email:
            if selected_age == 'Select Your Age':
                selected_age = 0

            if all(response is None for response in user_responses.values()):
                st.error("No response selected. Please select at least one response.")
            else:
                # Calculate the number of correct and incorrect responses, and the score as a percentage of correct answers
                total_questions = len(user_responses)
                correct_answers = 0
                incorrect_answers = 0
                for scenario_id, user_response in user_responses.items():
                    response = responses_df[responses_df['scenario_id'] == scenario_id]
                    is_correct = response[response['is_correct'] == True]['response_option'].iloc[0]
                    if user_response is None:
                        total_questions -= 1
                    elif user_response == is_correct:
                        correct_answers += 1
                    else:
                        incorrect_answers += 1

                score = correct_answers / total_questions * 100

                # Check if user already exists in the op_survey_users table
                query = f"SELECT * FROM op_survey_users WHERE email = '{email}'"
                existing_user = pd.read_sql(query, engine)

                if existing_user.empty:
                    # Insert the new user into the op_survey_users table
                    query = f"INSERT INTO op_survey_users (email, age, country) VALUES ('{email}', '{selected_age}', '{country}')"
                    engine.execute(query)

                    # Get the user_id for the newly created user
                    query = f"SELECT id FROM op_survey_users WHERE email = '{email}'"
                    user_id = pd.read_sql(query, engine).iloc[0]['id']
                else:
                    # Use the existing user_id
                    user_id = existing_user.iloc[0]['id']

                # Check if the user has already submitted this survey
                query = f"SELECT * FROM antisemitism_knowledge_user_scores WHERE user_id = {user_id} AND survey_id = 2"
                existing_response = pd.read_sql(query, engine)

                if existing_response.empty:
                    # Calculate the final score and insert it into the antisemitism_knowledge_user_scores table
                    query = f"INSERT INTO antisemitism_knowledge_user_scores (user_id, survey_id, score, correct_answers, incorrect_answers, total_questions) VALUES ({user_id}, 2, {score}, {correct_answers}, {incorrect_answers}, {total_questions})"
                    engine.execute(query)

                    # Send the user an email with their score
                    #subject = "Your Antisemitism Knowledge Assessment Results"
                    #body = f"Hello,\n\nThank you for taking the Antisemitism Knowledge Assessment. Your score is {score:.2f}%.\n\nBest regards,\nThe Assessment Team"
                    #send_email(email, subject, body)


                    send_email(email, score, correct_answers, incorrect_answers, total_questions, len(user_responses) - total_questions)

                    st.success("Thsank you. Check your email for the results.")
                    #col1, col2 = st.columns(2) 
                    #with col1:
                    #    st.success("Results: "f"Score: {score:.2f}%")

                    #with col2:
                    #    st.success(f"Number of correct answers: [{correct_answers}].")
                    #    st.error(f"Number of incorrect answers: [{incorrect_answers}].")
                    #    st.info(f"Number of answered questions: [{total_questions}].")
                    #    st.warning(f"Number of unanswered questions: [{len(user_responses) - total_questions}].")

                else:
                    st.warning("You have already submitted this survey. You cannot submit it more than once.")
        else:
            st.error("Please provide all required information.")


# In[ ]:




