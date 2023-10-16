import streamlit as st
import pandas as pd
import mysql.connector
import datetime
from streamlit import session_state
import plotly.express as px
import plotly.graph_objects as go
from datetime import timedelta

def init_connection():
    return mysql.connector.connect(**st.secrets["mysql"])

def run_query(conn,query):
    with conn.cursor() as cur:
        cur.execute(query)
        columnsnames=cur.column_names
        return cur.fetchall(),columnsnames
    
def update():
    st.session_state.submitted = True
    

def main():


    conn = init_connection()
   
  
    st.set_page_config(page_title="Sidebar Form Example")
    if 'submitted' not in st.session_state:
        st.session_state.submitted = False


    # Define the sidebar form
    with st.sidebar.form("my_sidebar_form"):
        st.write("## date2222 range Form")
        startdate = st.date_input(
        "Give Start Date",
        datetime.date.today())




        enddate = st.date_input(
        "Give End Date",
        datetime.datetime.now() + datetime.timedelta(days=1))

        st.write('Your birthday is:', enddate)

        



        # name = st.text_input("Enter your name:")
        # email = st.text_input("Enter your email:")
        # age = st.number_input("Enter your age:", min_value=0, max_value=120)
        # color = st.selectbox("Choose your favorite color:", ["Red", "Green", "Blue"])
        #submit_button = st.form_submit_button(label="Submit",on_click=update)
        st.form_submit_button(label="Submit",on_click=update)
    # Display the results


    if st.session_state.submitted:
        st.write("Given startdate and endate",startdate)
        st.write("Given startdate and endate",enddate)

        st.write("## Results")
        sql = """SELECT `kimai2_teams`.name as team_name,`kimai2_users_teams`.`user_id`,`kimai2_users_teams`.`team_id`,`kimai2_users_teams`.`teamlead`,

`kimai2_projects_teams`.`project_id`

,`kimai2_users`.`alias` as username,`kimai2_projects`.`name` as project_name,
`kimai2_projects`.`visible` as active,`kimai2_projects`.`time_budget`,`kimai2_projects`.`start` as start_date, `kimai2_projects`.`end` as end_date,
 (
    SELECT SUM(kimai2_timesheet.duration)
    FROM kimai2_timesheet
    WHERE kimai2_timesheet.project_id = kimai2_projects.id
  ) AS duration
FROM `kimai2_teams`
INNER JOIN kimai2_users_teams ON kimai2_teams.id=kimai2_users_teams.team_id
INNER JOIN kimai2_projects_teams ON kimai2_projects_teams.team_id=kimai2_teams.id
INNER JOIN kimai2_users ON kimai2_users_teams.user_id=kimai2_users.id
INNER JOIN kimai2_projects ON kimai2_projects_teams.project_id=kimai2_projects.id
WHERE kimai2_users_teams.teamlead=1;
        """

        
    
        rows,columnames = run_query(conn,sql)

    # st.write(columnames)
        dfdata=pd.DataFrame(rows,columns=columnames)
        st.write("All Data from Query",dfdata)
   
        # Load the tips dataset from Plotly

if __name__ == '__main__':
    main()