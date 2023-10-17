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

    #hello

    conn = init_connection()
   
  
    st.set_page_config(page_title="Sidebar Form Example",layout="wide")
    if 'submitted' not in st.session_state:
        st.session_state.submitted = False

    sql = """
    select * from hs_survey_411958 where submitdate IS NOT NULL
        """

        
    
    rows,columnames = run_query(conn,sql)
    columns_headers=[
        'id',
        'token',
        'submitdate',
        'lastpage',
        'startlanguage',
        'seed',
        'startdate',
        'datestamp',
        'idiotita',	
        'idiotita_other',	
        'text1',	
        'yn1',
        'l1',	
        'l2',
        'stl_yn1',
        'stl_l1',
        'text2'	,
        'yn2',
        'l3',
        'stl_yn2',
        'stl_l2',
        'text3',
        'yn3',
        'l4',
        'stl_yn3',
        'stl_l3',
        'text4',
        'yn4',
        'l5',
        'l6',
        'stl_yn4',
        'stl_l4'

    ]
    # st.write(columnames)
    dfdata=pd.DataFrame(rows,columns=columns_headers)
    dfdata["idiotita"] = dfdata["idiotita"].replace({'A1': "Στέλεχος νοσοκομείου (διοικητικό στέλεχος, υπεύθυνος/η ποιότητας, φαρμακείου & προμηθειών)","A2": "Στέλεχος Υπουργείου Υγείας ή άλλου οργανισμού χάραξης πολιτικής","A3":"Στέλεχος φαρμακευτικής, ή άλλης εταιρείας/ φορέα, που δραστηριοποιείται στο χώρο της υγείας","A4":"Φοιτητής","-oth-":"Άλλο"})
    st.write("All Data from Query",dfdata)

    #Create a "Likert Df":
    # Create a dictionary to map Likert scale values to columns (1, 2, 3, 4, 5)
    likert_mapping = {1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}
    # Initialize a new DataFrame to store the reshaped data
    reshaped_data = pd.DataFrame()
    # Loop through the Likert scale questions (e.g., 'q2' and 'q3')
    for question in ['l1', 'l2','l3', 'l4','l5', 'l6']:
        # Melt the DataFrame to stack the Likert scale values into rows
        melted = dfdata.melt(id_vars='idiotita', value_vars=[question], var_name='question')

        # Pivot the melted DataFrame to count the occurrences of each Likert scale value
        pivoted = melted.pivot_table(index='question', columns='value', values='idiotita', aggfunc='count', fill_value=0)

        # Reset the index and rename the columns
        pivoted.reset_index(inplace=True)
        pivoted.rename(columns=likert_mapping, inplace=True)

        # Add the reshaped data to the final DataFrame
        Likert_data = pd.concat([reshaped_data, pivoted])

    # Reset the index of the final reshaped DataFrame
    Likert_data.reset_index(drop=True, inplace=True)
    # Set the 'question' column as the index
    Likert_data.set_index('question', inplace=True)
    # Print the reshaped DataFrame
    st.write(Likert_data)
    
    ###################################################################################################################
    ###############################################START VAGGELIS######################################################
    ###################################################################################################################


    #Create three columns
    col1,col2 = st.columns(2)

    with col1:
        st.metric(label="Αριθμός Ολοκληρωμένων Ερωτηματολογίων",value=dfdata["submitdate"].count())

    with col2:
        idiotita_counts=dfdata["idiotita"].value_counts()
        fig = px.pie(dfdata,values=idiotita_counts.values, names=idiotita_counts.index, title="Ιδιότητα Ερωτηθέντων:", hole=0.6)
        # Customize the layout if needed
        fig.update_traces(textposition='auto', textinfo='percent')
        # Set the legend position to be below the chart
        fig.update_layout(legend=dict(orientation="h"))
        # Adjust the width and height of the chart
        fig.update_layout(width=800, height=500)
        # Display the chart in your Streamlit app
        st.plotly_chart(fig)

    #FILTRO GIA IDIOTHTA
    # Set the default selection to "Total"
    selected_idiotita = "Όλες οι Ιδιότητες"
    # Create a filter for "idiotita"
    idiotita_options = list(dfdata['idiotita'].unique())
    idiotita_options.append("Όλες οι Ιδιότητες")
    selected_idiotita = st.selectbox("Επιλέξτε ιδιότητα:", idiotita_options, index=idiotita_options.index(selected_idiotita))
    # Filter the data based on the selected "idiotita"
    if selected_idiotita == "Όλες οι Ιδιότητες":
        filtered_data = dfdata
        selected_idiotita = "Όλες οι ιδιότητες"
    else:
        filtered_data = dfdata[dfdata['idiotita'] == selected_idiotita]

    # Create two columns
    col4, col5 = st.columns(2)

    # Inside the first column
    with col4:
        st.title("Προμήθειες φαρμάκων: Διερεύνηση του ρόλου της ΕΚΑΠΥ")

    # Inside the second column
    with col5:
        st.title("Κλινικές μελέτες: Προκλήσεις στην υλοποίηση κλινικών μελετών στην Ελλάδα")

    # Create of another two columns
    col6, col7 = st.columns(2)

    # Inside the third column
    with col6:
        st.title("Ποιότητα υπηρεσιών υγείας: Η εφαρμογή του πλαισίου διασφάλισης Ποιότητας του ΟΔΙΠΥ")

    # Inside the forth column
    with col7:
        st.title("Εφαρμογή του συστήματος DRGs: Προκλήσεις εφαρμογής & πρώτα αποτελέσματα")





    ###################################################################################################################
    ###############################################END VAGGELIS######################################################
    ###################################################################################################################



    # Define the sidebar form
#     with st.sidebar.form("my_sidebar_form"):
#         st.write("## date2222 range Form")
#         startdate = st.date_input(
#         "Give Start Date",
#         datetime.date.today())




#         enddate = st.date_input(
#         "Give End Date",
#         datetime.datetime.now() + datetime.timedelta(days=1))

#         st.write('Your birthday is:', enddate)

        



#         # name = st.text_input("Enter your name:")
#         # email = st.text_input("Enter your email:")
#         # age = st.number_input("Enter your age:", min_value=0, max_value=120)
#         # color = st.selectbox("Choose your favorite color:", ["Red", "Green", "Blue"])
#         #submit_button = st.form_submit_button(label="Submit",on_click=update)
#         st.form_submit_button(label="Submit",on_click=update)
#     # Display the results


#     if st.session_state.submitted:
#         st.write("Given startdate and endate",startdate)
#         st.write("Given startdate and endate",enddate)

#         st.write("## Results")
#         sql = """SELECT `kimai2_teams`.name as team_name,`kimai2_users_teams`.`user_id`,`kimai2_users_teams`.`team_id`,`kimai2_users_teams`.`teamlead`,

# `kimai2_projects_teams`.`project_id`

# ,`kimai2_users`.`alias` as username,`kimai2_projects`.`name` as project_name,
# `kimai2_projects`.`visible` as active,`kimai2_projects`.`time_budget`,`kimai2_projects`.`start` as start_date, `kimai2_projects`.`end` as end_date,
#  (
#     SELECT SUM(kimai2_timesheet.duration)
#     FROM kimai2_timesheet
#     WHERE kimai2_timesheet.project_id = kimai2_projects.id
#   ) AS duration
# FROM `kimai2_teams`
# INNER JOIN kimai2_users_teams ON kimai2_teams.id=kimai2_users_teams.team_id
# INNER JOIN kimai2_projects_teams ON kimai2_projects_teams.team_id=kimai2_teams.id
# INNER JOIN kimai2_users ON kimai2_users_teams.user_id=kimai2_users.id
# INNER JOIN kimai2_projects ON kimai2_projects_teams.project_id=kimai2_projects.id
# WHERE kimai2_users_teams.teamlead=1;
#         """

        
    
#         rows,columnames = run_query(conn,sql)

#     # st.write(columnames)
#         dfdata=pd.DataFrame(rows,columns=columnames)
#         st.write("All Data from Query",dfdata)
   
        # Load the tips dataset from Plotly

if __name__ == '__main__':
    main()