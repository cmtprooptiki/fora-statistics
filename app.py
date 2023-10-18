import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import mysql.connector
import datetime
from streamlit import session_state
import plotly.express as px
import plotly.graph_objects as go
from datetime import timedelta
import numpy as np
#import matplotlib.pyplot as plt

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
        reshaped_data = pd.concat([reshaped_data, pivoted])

    # Reset the index of the final reshaped DataFrame
    reshaped_data.reset_index(drop=True, inplace=True)
    # Set the 'question' column as the index
    reshaped_data.set_index('question', inplace=True)
    # Print the reshaped DataFrame
    reshaped_data=reshaped_data.rename(columns={"": "NAN"})
    reshaped_data=reshaped_data.drop(columns=["NAN"])
    st.write("This is the reshaped data where every row is a likert question:",reshaped_data)
    #gia 1o test diagramma
    # xdata=np.asanyarray(reshaped_data)
    # st.write(xdata)
    # ydata=np.asanyarray(reshaped_data.index)
    # st.write(ydata)


########################################################################################################################################################
############################################################################arxi 1o test diagramma#####################################################
########################################################################################################################################################
    # import plotly.graph_objects as go

    # top_labels = ['Strongly<br>agree', 'Agree', 'Neutral', 'Disagree',
    #             'Strongly<br>disagree']

    # colors = ['rgba(38, 24, 74, 0.8)', 'rgba(71, 58, 131, 0.8)',
    #         'rgba(122, 120, 168, 0.8)', 'rgba(164, 163, 204, 0.85)',
    #         'rgba(190, 192, 213, 1)']

    # x_data = xdata

    # y_data = ydata

    # fig = go.Figure()

    # for i in range(0, len(x_data[0])):
    #     for xd, yd in zip(x_data, y_data):
    #         fig.add_trace(go.Bar(
    #             x=[xd[i]], y=[yd],
    #             orientation='h',
    #             marker=dict(
    #                 color=colors[i],
    #                 line=dict(color='rgb(248, 248, 249)', width=1)
    #             )
    #         ))

    # fig.update_layout(
    #     xaxis=dict(
    #         showgrid=False,
    #         showline=False,
    #         showticklabels=False,
    #         zeroline=False,
    #         domain=[0.15, 1]
    #     ),
    #     yaxis=dict(
    #         showgrid=False,
    #         showline=False,
    #         showticklabels=False,
    #         zeroline=False,
    #     ),
    #     barmode='stack',
    #     paper_bgcolor='rgb(248, 248, 255)',
    #     plot_bgcolor='rgb(248, 248, 255)',
    #     margin=dict(l=120, r=10, t=140, b=80),
    #     showlegend=False,
    # )

    # annotations = []

    # for yd, xd in zip(y_data, x_data):
    #     # labeling the y-axis
    #     annotations.append(dict(xref='paper', yref='y',
    #                             x=0.14, y=yd,
    #                             xanchor='right',
    #                             text=str(yd),
    #                             font=dict(family='Arial', size=14,
    #                                     color='rgb(67, 67, 67)'),
    #                             showarrow=False, align='right'))
    #     # labeling the first percentage of each bar (x_axis)
    #     annotations.append(dict(xref='x', yref='y',
    #                             x=xd[0] / 2, y=yd,
    #                             text=str(xd[0]) + '%',
    #                             font=dict(family='Arial', size=14,
    #                                     color='rgb(248, 248, 255)'),
    #                             showarrow=False))
    #     # labeling the first Likert scale (on the top)
    #     if yd == y_data[-1]:
    #         annotations.append(dict(xref='x', yref='paper',
    #                                 x=xd[0] / 2, y=1.1,
    #                                 text=top_labels[0],
    #                                 font=dict(family='Arial', size=14,
    #                                         color='rgb(67, 67, 67)'),
    #                                 showarrow=False))
    #     space = xd[0]
    #     for i in range(1, len(xd)):
    #             # labeling the rest of percentages for each bar (x_axis)
    #             annotations.append(dict(xref='x', yref='y',
    #                                     x=space + (xd[i]/2), y=yd,
    #                                     text=str(xd[i]) + '%',
    #                                     font=dict(family='Arial', size=14,
    #                                             color='rgb(248, 248, 255)'),
    #                                     showarrow=False))
    #             # labeling the Likert scale
    #             if yd == y_data[-1]:
    #                 annotations.append(dict(xref='x', yref='paper',
    #                                         x=space + (xd[i]/2), y=1.1,
    #                                         text=top_labels[i],
    #                                         font=dict(family='Arial', size=14,
    #                                                 color='rgb(67, 67, 67)'),
    #                                         showarrow=False))
    #             space += xd[i]

    # fig.update_layout(annotations=annotations)

    # st.plotly_chart(fig)
########################################################################################################################################################
############################################################################telos 1o test diagramma#####################################################
########################################################################################################################################################

########################################################################################################################################################
############################################################################arxi 2o test diagramma######################################################
########################################################################################################################################################

    #Creation of percentage df(every cell is the %of total of the row)
    row_sums= reshaped_data.sum(axis=1)
    percentage_data= round(reshaped_data.divide(row_sums,axis=0) *100,1)
    percentage_data = percentage_data.rename({'l1':"Η ΕΚΑΠΥ θα βελτιώσει τη διαδικασία προμηθειών φαρμάκου στα νοσοκομεία.","l2":"Η προμήθεια φαρμάκων μέσω της ΕΚΑΠΥ θα συμβάλει στη μείωση των δαπανών.","l3":"Η διεξαγωγή κλινικών μελετών στα νοσοκομεία βελτιώνει την ποιότητα των παρεχόμενων υπηρεσιών.","l4":"Η εφαρμογή του πλαισίου διασφάλισης Ποιότητας του ΟΔΙΠΥ στα νοσοκομεία θα βελτιώσει την ποιότητα των παρεχόμενων υπηρεσιών.","l5":"Η εφαρμογή του συστήματος DRGs θα βελτιώσει τη διαδικασία αποζημίωσης περιστατικών στα νοσοκομεία.","l6":"Η εφαρμογή του συστήματος DRGs θα βελτιώσει τη διαδικασία κατάρτισης και ελέγχου νοσοκομειακού προϋπολογισμού."})
    percentage_data.reset_index(drop=False, inplace=True)
    st.write("This is the percentage data where every cell is the percentage(%) of total for every row",percentage_data)

    # Populate the variables from the percentage_data DataFrame
    questions = percentage_data.question
    strongdisagree = percentage_data["1"]
    disagree = percentage_data["2"]
    neutral = percentage_data["3"]
    agree = percentage_data["4"]
    strongagree = percentage_data["5"]

    ind = [x for x, _ in enumerate(questions)]

    # Create a Streamlit app and display the bar chart
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot(plt)

    st.bar_chart(strongdisagree, label='SD', color='#c71d1d')
    st.bar_chart(disagree, label='D', color='#e28e8e')
    st.bar_chart(neutral, label='N', color='#e7e7e7')
    st.bar_chart(agree, label='A', color='#879caf')
    st.bar_chart(strongagree, label='SA', color='#1b617b')
    st.pyplot(plt)















########################################################################################################################################################
############################################################################telos 2o test diagramma#####################################################
########################################################################################################################################################









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