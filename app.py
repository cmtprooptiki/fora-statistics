import streamlit as st
import pandas as pd
import mysql.connector
import datetime
from streamlit import session_state
import plotly.express as px
import plotly.graph_objects as go
from datetime import timedelta
import numpy as np
import matplotlib.pyplot as plt
import altair as alt
from html_shortcuts import *
from streamlit.components.v1 import html


def init_connection():
    return mysql.connector.connect(**st.secrets["mysql"])

def run_query(conn,query):
    with conn.cursor() as cur:
        cur.execute(query)
        columnsnames=cur.column_names
        return cur.fetchall(),columnsnames
    
def update():
    st.session_state.submitted = True
    
# def highlight_age(index):
 
#     result = ''
#     for i in range(0, len(index), 50):
#         result += index[i:i+50] + '/n'
#     return result
    
def main():

    #hello

    conn = init_connection()
   
  
    st.set_page_config(page_title="Fora Survey Visualization",layout="wide")



    with open( "style.css" ) as css:
        st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

    # col1, col2, col3 = st.columns(3)

    # with col1:
    #     pass

    # with col2:
    #     st.image("https://health-survey.gr/tmp/assets/44f91fe6/Logo_new%20-2-.png", width=600)


    # with col3:
    #     pass

    # st.markdown("<h1 style='text-align:center;background: #f7f7f7;border-radius: 9px;padding: 25px;'>Οπτικοποίηση αποτελεσμάτων για την έρευνα που αφορά τις Προκλήσεις στην Οργάνωση & Διοίκηση των Νοσοκομειακών Μονάδων</h1>", unsafe_allow_html=True)
    # Add the HTML and CSS for the header
    st.markdown(
        """
        <style>
        .header {
            background-image: url('https://healthcare-management.gr/wp-content/uploads/2023/10/Header.png');
            background-size: contain;
            background-position: center;
            height: 453px;
            width: -webkit-fill-available;
            position: revert-layer;
            color: white;
            text-align: center;
        }

  
        .header-text {
            padding: 100px 0;
            font-size: 24px;
        }
        </style>
        <div class="header">
            <div class="header-text">
                Your Header Text Goes Here
            </div>
        </div>
        """
    ,unsafe_allow_html=True)

    # The content of your Streamlit app goes below the header
                # Load the JavaScript function code
    with open("animated_counter.js", "r") as file:
            js_code = file.read()

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
    # st.write("All Data from Query",dfdata)
# Create a container with custom CSS to increase the height


    with st.container():
            col0, col01 = st.columns(2)
            with col0:
                st.image('https://healthcare-management.gr/wp-content/uploads/2023/10/Group-29-1.png',width=400)
            with col01:
                st.markdown("<h3>Έρευνα που αφορά τις Προκλήσεις στην Οργάνωση & Διοίκηση των Νοσοκομειακών Μονάδων</h3>",unsafe_allow_html=True)



    #Create three columns
    with st.container():
        col1,col2 = st.columns(2)



        with col1:

            # st.metric(label="Αριθμός Ολοκληρωμένων Ερωτηματολογίων",value=dfdata["submitdate"].count())
            html_content1 = html_button1(js_code, dfdata["submitdate"].count())
            html(html_content1,height=250)

        with col2:
            st.markdown("<h3 style='text-align: center; font-size:32px;'><strong>Ιδιότητα Ερωτηθέντων<strong></h3>", unsafe_allow_html=True)

            idiotita_counts=dfdata["idiotita"].value_counts()
            fig = px.pie(dfdata,values=idiotita_counts.values, names=idiotita_counts.index, hole=0.6)
            # Customize the layout if needed
            fig.update_traces(textposition='auto', marker=dict(colors=['#7ec4cf','#6881b4','#d1cfe2','#d4afb9','#fcf5c7']), textinfo='percent')
            # Set the legend position to be below the chart
            fig.update_layout(legend=dict(orientation="h"))
            # Adjust the width and height of the chart
            fig.update_layout(width=800, height=500)

            # Change background color to red
            # fig.update_layout(paper_bgcolor='red')

            # Set the border radius to 16px
            #fig.update_layout(autosize=False, margin=dict(l=0, r=0, b=0, t=0), hovermode='closest', showlegend=False, xaxis=dict(showgrid=False, zeroline=False), yaxis=dict(showgrid=False, zeroline=False), yaxis_zeroline=False)
            # Display the chart in your Streamlit app
            st.plotly_chart(fig,use_container_width=True)
            st.markdown("</div>",unsafe_allow_html=True)

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
        #st.write("ilias filtered:",filtered_data)
    else:
        filtered_data = dfdata[dfdata['idiotita'] == selected_idiotita]

    #Create a "Likert Df":
    # Create a dictionary to map Likert scale values to columns (1, 2, 3, 4, 5)
    likert_mapping = {1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}
    # Initialize a new DataFrame to store the reshaped data
    reshaped_data = pd.DataFrame()
    # Loop through the Likert scale questions (e.g., 'q2' and 'q3')
    for question in ['l1', 'l2','l3', 'l4','l5', 'l6']:
        # Melt the DataFrame to stack the Likert scale values into rows
        melted = filtered_data.melt(id_vars='idiotita', value_vars=[question], var_name='question')

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
    #reshaped_data.set_index('question', inplace=True)
    # Print the reshaped DataFrame
    #st.write("ilias reshaped_data",reshaped_data)
    # reshaped_data=reshaped_data.rename(columns={"": "NAN"})
    # reshaped_data=reshaped_data.drop(columns=["NAN"])
    reshaped_data["question"] = reshaped_data["question"].replace({'l1':"Η ΕΚΑΠΥ θα βελτιώσει τη διαδικασία προμηθειών φαρμάκου στα νοσοκομεία.","l2":"Η προμήθεια φαρμάκων μέσω της ΕΚΑΠΥ θα συμβάλει στη μείωση των δαπανών.","l3":"Η διεξαγωγή κλινικών μελετών στα νοσοκομεία βελτιώνει την ποιότητα των παρεχόμενων υπηρεσιών.","l4":"Η εφαρμογή του πλαισίου διασφάλισης Ποιότητας του ΟΔΙΠΥ στα νοσοκομεία θα βελτιώσει την ποιότητα των παρεχόμενων υπηρεσιών.","l5":"Η εφαρμογή του συστήματος DRGs θα βελτιώσει τη διαδικασία αποζημίωσης περιστατικών στα νοσοκομεία.","l6":"Η εφαρμογή του συστήματος DRGs θα βελτιώσει τη διαδικασία κατάρτισης και ελέγχου νοσοκομειακού προϋπολογισμού."})
    reshaped_data=reshaped_data.fillna(0)
    reshaped_data.set_index('question', inplace=True)
    # #Creation of percentage df(every cell is the %of total of the row)
    # Set the 'question' column as the index
    reshaped_data = reshaped_data.reindex(index = ["Η εφαρμογή του συστήματος DRGs θα βελτιώσει τη διαδικασία κατάρτισης και ελέγχου νοσοκομειακού προϋπολογισμού.", "Η εφαρμογή του συστήματος DRGs θα βελτιώσει τη διαδικασία αποζημίωσης περιστατικών στα νοσοκομεία.","Η εφαρμογή του πλαισίου διασφάλισης Ποιότητας του ΟΔΙΠΥ στα νοσοκομεία θα βελτιώσει την ποιότητα των παρεχόμενων υπηρεσιών.", "Η διεξαγωγή κλινικών μελετών στα νοσοκομεία βελτιώνει την ποιότητα των παρεχόμενων υπηρεσιών.", "Η προμήθεια φαρμάκων μέσω της ΕΚΑΠΥ θα συμβάλει στη μείωση των δαπανών.", "Η ΕΚΑΠΥ θα βελτιώσει τη διαδικασία προμηθειών φαρμάκου στα νοσοκομεία."])
    reshaped_data.reset_index(drop=False,inplace=True)
    #st.write(reshaped_data)
    # Get the column names dynamically
    column_names = reshaped_data.columns.tolist()
    # Name of the column to check and potentially remove
    columns_to_remove = ["","question"]
    # Check if each column name exists in the list and remove it
    for column_to_check in columns_to_remove:
        if column_to_check in column_names:
            column_names.remove(column_to_check)
    #st.write(column_names)
    row_sums= reshaped_data.loc[:,column_names].sum(axis=1)
    #st.write(row_sums)
    # row_sums= reshaped_data.iloc[:,1:6].sum(axis=1)
    percentage_data= round(reshaped_data[column_names].divide(row_sums,axis=0) *100,1)
#DEBUGGING TABLES
    # st.write("This is the filtered data",filtered_data)
    # st.write("This is the reshaped data where every row is a likert question:",reshaped_data)
    # st.write("This is the percentage data where every cell is the percentage(%) of total for every row",percentage_data)


    # tbl=np.asanyarray(percentage_data.loc[:,column_names])
    # st.write("This is the numpy array table thta i use for the charts",tbl)
    likert_question_mapping= {0: 'Η εφαρμογή του συστήματος DRGs θα βελτιώσει τη διαδικασία κατάρτισης και ελέγχου νοσοκομειακού προϋπολογισμού.', 
                        1: 'Η εφαρμογή του συστήματος DRGs θα βελτιώσει τη διαδικασία αποζημίωσης περιστατικών στα νοσοκομεία.', 
                        2: 'Η εφαρμογή του πλαισίου διασφάλισης Ποιότητας του ΟΔΙΠΥ στα νοσοκομεία θα βελτιώσει την ποιότητα των παρεχόμενων υπηρεσιών.', 
                        3: 'Η διεξαγωγή κλινικών μελετών στα νοσοκομεία βελτιώνει την ποιότητα των παρεχόμενων υπηρεσιών.', 
                        4: 'Η προμήθεια φαρμάκων μέσω της ΕΚΑΠΥ θα συμβάλει στη μείωση των δαπανών.',
                        5: 'Η ΕΚΑΠΥ θα βελτιώσει τη διαδικασία προμηθειών φαρμάκου στα νοσοκομεία.'
                        }

    likert_colors = {
        'Διαφωνώ απόλυτα': '#d4afb9',
        'Διαφωνώ': '#d1cfe2',
        'Ούτε συμφωνώ ούτε διαφωνώ': '#6881b4',
        'Συμφωνώ': '#7ec4cf',
        'Συμφωνώ απόλυτα': '#fcf5c7'
    }

#################################################################
  


    with st.container():
        col4, col5 = st.columns(2)



    # col4, col5 = st.columns(2)

        # Inside the first column
        with col4:
            #st.subheader("Προμήθειες φαρμάκων: Διερεύνηση του ρόλου της ΕΚΑΠΥ")
            st.markdown("<h3 ><strong>Προμήθειες φαρμάκων:</strong> Διερεύνηση του ρόλου της ΕΚΑΠΥ</h3>", unsafe_allow_html=True)
            chart_data1=percentage_data.iloc[4:6,:]
            # # chart_data1 = pd.DataFrame(
            # #     tbl[4:6,:],
            # #     index=["l2","l1"]#,"l3","l4","l5","l6"],
            # # )

            # st.write(chart_data1)
            #st.bar_chart(chart_datat)
            chart_data11 = pd.melt(chart_data1.reset_index(),var_name="variable", value_name="value",id_vars="index")
            # st.write(chart_data11)
            likert_mapping = {'1': 'Διαφωνώ απόλυτα', '2': 'Διαφωνώ', '3': 'Ούτε συμφωνώ ούτε διαφωνώ', '4': 'Συμφωνώ', '5': 'Συμφωνώ απόλυτα'}
            # Horizontal stacked bar chart
            chart_data11['variable']=chart_data11['variable'].map(likert_mapping)
            chart_data11['index']=chart_data11['index'].map(likert_question_mapping)

            # Create the color scale using the likert_colors mapping
            color_scale = alt.Scale(domain=list(likert_colors.keys()), range=list(likert_colors.values()))
            # Horizontal stacked bar chart
            chart = (
                alt.Chart(chart_data11)
                .mark_bar()
                .encode(
                    x=alt.X("value:O", type="quantitative", title=""),
                    y=alt.Y("index:N", type="nominal", title=""),
                    color=alt.Color("variable", type="nominal", title="",scale=color_scale),
                    order=alt.Order("variable", sort="ascending"),
                )
                .properties(
    width=200,
    height=100
)
.configure_axis(
    labelFontSize=10,
    titleFontSize=10
)

            )

            
            st.altair_chart(chart, theme='streamlit', use_container_width=True)
            

        # Inside the second column
        with col5:
           # st.subheader("Κλινικές μελέτες: Προκλήσεις στην υλοποίηση κλινικών μελετών στην Ελλάδα")
            st.markdown("<h3 ><strong>Κλινικές μελέτες:</strong> Προκλήσεις στην υλοποίηση κλινικών μελετών στην Ελλάδα</h3>", unsafe_allow_html=True)

            chart_data2=percentage_data.iloc[3:4,:]
            # chart_data2 = pd.DataFrame(
            #     tbl[3:4,:],
            #     index=["l3"]#,"l2","l3","l4","l5","l6"],
            # )
            # st.write(chart_data2)
            #st.bar_chart(chart_data2)
            chart_data22 = pd.melt(chart_data2.reset_index(),var_name="variable", value_name="value",id_vars="index")
            # st.write(chart_data22)
            likert_mapping = {'1': 'Διαφωνώ απόλυτα', '2': 'Διαφωνώ', '3': 'Ούτε συμφωνώ ούτε διαφωνώ', '4': 'Συμφωνώ', '5': 'Συμφωνώ απόλυτα'}
            # Horizontal stacked bar chart
            chart_data22['variable']=chart_data22['variable'].map(likert_mapping)
            # Horizontal stacked bar chart
            chart_data22['index']=chart_data22['index'].map(likert_question_mapping)
            color_scale = alt.Scale(domain=list(likert_colors.keys()), range=list(likert_colors.values()))

            chart = (
                alt.Chart(chart_data22)
                .mark_bar()
                .encode(
                    x=alt.X("value", type="quantitative", title=""),
                    y=alt.Y("index", type="nominal", title=""),
                    color=alt.Color("variable", type="nominal", title="",scale=color_scale),
                    order=alt.Order("variable", sort="ascending"),
                )
                .properties(
    width=200,
    height=100
)
            
            )
            st.altair_chart(chart, theme='streamlit', use_container_width=True)


    with st.container():
        col6, col7 = st.columns(2)
    # # Create of another two columns
    # col6, col7 = st.columns(2)

        # Inside the third column
        with col6:
            #st.subheader("Ποιότητα υπηρεσιών υγείας: Η εφαρμογή του πλαισίου διασφάλισης Ποιότητας του ΟΔΙΠΥ")
            st.markdown("<h3 ><strong>Ποιότητα υπηρεσιών υγείας:</strong> Η εφαρμογή του πλαισίου διασφάλισης Ποιότητας του ΟΔΙΠΥ</h3>", unsafe_allow_html=True)

            chart_data3=percentage_data.iloc[2:3,:]
            # chart_data3 = pd.DataFrame(
            #     tbl[2:3,:],
            #     index=["l4"]#,"l2","l3","l4","l5","l6"],
            # )
            # st.write(chart_data3)
            #st.bar_chart(chart_data3)
            chart_data33 = pd.melt(chart_data3.reset_index(),var_name="variable", value_name="value",id_vars="index")
            # st.write(chart_data33)
            # likert_question_mapping= {0: 'Η εφαρμογή του συστήματος DRGs θα βελτιώσει τη διαδικασία κατάρτισης και ελέγχου νοσοκομειακού προϋπολογισμού.', 
            #                 1: 'Η εφαρμογή του συστήματος DRGs θα βελτιώσει τη διαδικασία αποζημίωσης περιστατικών στα νοσοκομεία.', 
            #                 2: 'Η εφαρμογή του πλαισίου διασφάλισης Ποιότητας του ΟΔΙΠΥ στα νοσοκομεία θα βελτιώσει την ποιότητα των παρεχόμενων υπηρεσιών.', 
            #                 3: 'Η διεξαγωγή κλινικών μελετών στα νοσοκομεία βελτιώνει την ποιότητα των παρεχόμενων υπηρεσιών.', 
            #                 4: 'Η προμήθεια φαρμάκων μέσω της ΕΚΑΠΥ θα συμβάλει στη μείωση των δαπανών.',
            #                 5: 'Η ΕΚΑΠΥ θα βελτιώσει τη διαδικασία προμηθειών φαρμάκου στα νοσοκομεία.'
            #                 }
            likert_mapping = {'1': 'Διαφωνώ απόλυτα', '2': 'Διαφωνώ', '3': 'Ούτε συμφωνώ ούτε διαφωνώ', '4': 'Συμφωνώ', '5': 'Συμφωνώ απόλυτα'}
            # Horizontal stacked bar chart
            chart_data33['variable']=chart_data33['variable'].map(likert_mapping)
            chart_data33['index']=chart_data33['index'].map(likert_question_mapping)
            color_scale = alt.Scale(domain=list(likert_colors.keys()), range=list(likert_colors.values()))

            # Horizontal stacked bar chart
            chart = (
                alt.Chart(chart_data33)
                .mark_bar()
                .encode(
                    x=alt.X("value", type="quantitative", title=""),
                    y=alt.Y("index", type="nominal", title=""),
                    color=alt.Color("variable", type="nominal", title="",scale=color_scale),
                    order=alt.Order("variable", sort="ascending"),
                )
                .properties(
    width=200,
    height=100
)
            )
            st.altair_chart(chart,theme='streamlit', use_container_width=True)


        # Inside the forth column
        with col7:
            #st.subheader("Εφαρμογή του συστήματος DRGs: Προκλήσεις εφαρμογής & πρώτα αποτελέσματα")
            st.markdown("<h3 ><strong>Εφαρμογή του συστήματος DRGs:</strong> Προκλήσεις εφαρμογής & πρώτα αποτελέσματα</h3>", unsafe_allow_html=True)

            chart_data4=percentage_data.iloc[0:2,:]
            # chart_data4 = pd.DataFrame(
            #     tbl[0:2,:],
            #     index=["l6","l5"]#,"l2","l3","l4","l5","l6"],
            # )
            # st.write(chart_data4)
            #st.bar_chart(chart_data4)
            chart_data44 = pd.melt(chart_data4.reset_index(),var_name="variable", value_name="value",id_vars="index")
            # st.write(chart_data44)
            likert_question_mapping= {0: 'Η εφαρμογή του συστήματος DRGs θα βελτιώσει τη διαδικασία κατάρτισης και ελέγχου νοσοκομειακού προϋπολογισμού.', 
                                    1: 'Η εφαρμογή του συστήματος DRGs θα βελτιώσει τη διαδικασία αποζημίωσης περιστατικών στα νοσοκομεία.', 
                                    2: 'Η εφαρμογή του πλαισίου διασφάλισης Ποιότητας του ΟΔΙΠΥ στα νοσοκομεία θα βελτιώσει την ποιότητα των παρεχόμενων υπηρεσιών.', 
                                    3: 'Η διεξαγωγή κλινικών μελετών στα νοσοκομεία βελτιώνει την ποιότητα των παρεχόμενων υπηρεσιών.', 
                                    4: 'Η προμήθεια φαρμάκων μέσω της ΕΚΑΠΥ θα συμβάλει στη μείωση των δαπανών.',
                                    5: 'Η ΕΚΑΠΥ θα βελτιώσει τη διαδικασία προμηθειών φαρμάκου στα νοσοκομεία.'
                                    }

            likert_mapping = {'1': 'Διαφωνώ απόλυτα', '2': 'Διαφωνώ', '3': 'Ούτε συμφωνώ ούτε διαφωνώ', '4': 'Συμφωνώ', '5': 'Συμφωνώ απόλυτα'}
            # Horizontal stacked bar chart
            chart_data44['variable']=chart_data44['variable'].map(likert_mapping)
            
            chart_data44['index']=chart_data44['index'].map(likert_question_mapping)
            color_scale = alt.Scale(domain=list(likert_colors.keys()), range=list(likert_colors.values()))

            # chart_data44['index'] = chart_data44['index'].apply(highlight_age)
            # st.write(chart_data44)
            # scale = alt.Scale(
            #     # domain=["Διαφωνώ απόλυτα", "Διαφωνώ", "Ούτε συμφωνώ ούτε διαφωνώ", "Συμφωνώ", "Συμφωνώ απόλυτα"],
            #     range=["#e7ba52", "#a7a7a7", "#aec7e8", "#1f77b4", "#9467bd"],
            # )
            chart = (
                alt.Chart(chart_data44)
                .mark_bar()
                .encode(
                    x=alt.X("value", type="quantitative", title=""),
                    y=alt.Y("index", type="nominal", title="",axis=alt.Axis(labelLimit=200, tickCount=500,labelFontSize=9)),
                    # color=alt.Color("variable",scale=scale, type="nominal", title=""),
                    color=alt.Color("variable", type="nominal", title="",scale=color_scale),

                    order=alt.Order("variable", sort="ascending"),
    
                    )
        #             .configure_axis(
        # labelFontSize=10,
        # titleFontSize=15) 
        .properties(
    width=200,
    height=100
)


            )
            
            st.altair_chart(chart,theme='streamlit', use_container_width=True)




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