#INSTALL REQUIRED PACKAGE
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import mysql.connector
import plotly.express as px

#CREATE CONEECTION WITH MYSQL
mydb=mysql.connector.connect(host='localhost',user='root',password='12345',database='phonepe')
mycursor=mydb.cursor()

#STREAMLIT
st.set_page_config(layout= "wide")


with st.sidebar:
    select= option_menu("DATA EXPLORATION AND VISUALIZATION",["Home","Explore Data", "Insights"], styles={"nav-link-selected": {"background-color": "#6F36AD"}})

#HOME PAGE
if select=="Home":
    st.markdown("<h1 style='font-size:35px; color:purple'>PHONEPE PULSE AND DATA VISUALIZATION</h1>", unsafe_allow_html=True)
    st.markdown("<h1 style='font-size:25px; color:purple'>PHONEPE </h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='font-size:23px;'>A PAYMENT APP IN INDIA </h2>", unsafe_allow_html=True)
    st.markdown("<h3 style='font-size:20px;'> PhonePe is an Indian digital payments and financial services company based out of Bangalore, India. The PhonePe app, based on the Unified Payments Interface, went live in August 2016. PhonePe offers a wide range of services for the common people as well as for businesses enhancing their payment experiences. They also have additional features which will help people handle their finances by helping them in investing, paying for services. etc. PhonePe was acquired by Flipkart in 2016 and is India's one of the fastest-growing fintech companies </h3>", unsafe_allow_html=True)
    st.markdown("<h1 style='font-size:25px; color:purple'>TECHNOLOGY USED</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='font-size:20px;'>Github Cloning, Python, Pandas, MySQL,mysql-connector-python, Streamlit, and Plotly.</h3>", unsafe_allow_html=True)
    st.markdown("<h1 style='font-size:25px; color:purple'>OVERVIEW </h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='font-size:20px; '>User-friendly solution for visualizing data from the Phonepe pulse repository. Live geo visualization dashboard that displays information and insights from the Phonepe pulse Github repository in an interactiveand visually appealing manner. The dashboard will have at least 10 different dropdown options for users to select different facts and figures to display.</h3>", unsafe_allow_html=True)

#EXPLOREDATA:INSURANCE, PAYMENTS
if select == "Explore Data":
    insurance, payments= st.tabs(["Insurance", "Payments"])

    #INSURANCE ANALYSIS
    with insurance:
        colum1,colum2= st.columns([1,1],gap="large")
        with colum1:
            i_year = st.slider("Year", min_value=2020, max_value=2023)
        with colum2:
            i_Quarter = st.slider("Quarter", min_value=1, max_value=4)

        #GEO_VISUALISATION
        mycursor.execute(f"select state, sum(transactioncount),sum(transactionamount) from aggregated_insurance where year={i_year} and quarter={i_Quarter} group by state")
        df1 = pd.DataFrame(mycursor.fetchall(),columns= ['State', 'transactioncount', 'transactionamount'])
        df2 = pd.read_csv(r'C:\Users\Monisha User\Desktop\guvi-project\states_india.csv')
        df1.State = df2.st_nm

        fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey='properties.ST_NM',
                locations='State',
                color='transactioncount',
                color_continuous_scale='sunset')

        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig,use_container_width=True)
        
    


        #TSTATE,DISTRICT,PINCODE INSURANCE REPOR  
        state, district, pincode = st.tabs(["State", "District", "Pincode"])
        with state:
             query = f"SELECT state, Transactioncount, transactionamount FROM aggregated_insurance WHERE year={i_year} AND quarter={i_Quarter} ORDER BY transactionamount DESC LIMIT 10"
             mycursor.execute(query)
             df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Transactioncount', 'Transactionamount'])
             st.write(df)
        with district:
            query = f"SELECT districts, Transactioncount, transactionamount FROM map_insurance WHERE year={i_year} AND quarter={i_Quarter} ORDER BY transactionamount DESC LIMIT 10"
            mycursor.execute(query)
            df = pd.DataFrame(mycursor.fetchall(), columns=['districts', 'Transactioncount', 'Transactionamount'])
            st.write(df)
        with pincode:
            query = f"SELECT pincode, Transactioncount, transactionamount FROM top_insurance WHERE year={i_year} AND quarter={i_Quarter} ORDER BY transactionamount DESC LIMIT 10"
            mycursor.execute(query)
            df = pd.DataFrame(mycursor.fetchall(), columns=['pincode', 'Transactioncount', 'Transactionamount'])
            st.write(df)
    
    
    #PAYMENT ANALYSIS:TRANSACTION, PAYMENTS
    with payments:
        Type = st.selectbox("Type", ("Transactions", "Users"))
        colum1,colum2= st.columns([1,1],gap="large")
        with colum1:
            t_year = st.slider("*Year*", min_value=2018, max_value=2023)
        with colum2:
            t_Quarter = st.slider("*Quarter*", min_value=1, max_value=4)
        
        #TRANSACTION ANALYSIS
        if Type=="Transactions":
             
            #GEO_VISUALIZATION
             mycursor.execute(f"select state, sum(transactioncount),sum(transactionamount) from aggregated_transaction where year={t_year} and quarter={t_Quarter} group by state")
             df1 = pd.DataFrame(mycursor.fetchall(),columns= ['State', 'transactioncount', 'transactionamount'])
             df2 = pd.read_csv(r'C:\Users\Monisha User\Desktop\guvi-project\states_india.csv')
             df1.State = df2.st_nm

             fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                      featureidkey='properties.ST_NM',
                      locations='State',
                      color='transactioncount',
                      color_continuous_scale='sunset')

             fig.update_geos(fitbounds="locations", visible=False)
             st.plotly_chart(fig,use_container_width=True)
             



             #TRANSACTION TYPE
             query = f"select  TransactionType as Categories, sum(TransactionCount) as Total_Transaction_Count, sum(TransactionAmount) as Total_Transaction_Amount from aggregated_transaction where year={t_year} and Quarter={t_Quarter} group by TransactionType"
             mycursor.execute(query)
             df = pd.DataFrame(mycursor.fetchall(), columns=['Categories','Total_Transaction_Count', 'Total_Transaction_Amount'])
             st.write(df)  

           
             #DISTRICT, PINCODE REPORT OF TRANSACTION
             district,pincode=st.tabs(["District","Pincode"])
             with district:
                 query = f"SELECT district, count as Transactioncount, amount as transactionamount FROM map_transaction WHERE year={t_year} AND quarter={t_Quarter} ORDER BY transactionamount DESC LIMIT 10"
                 mycursor.execute(query)
                 df = pd.DataFrame(mycursor.fetchall(), columns=['districts', 'Transactioncount', 'Transactionamount'])
                 st.write(df)
             with pincode:
                 query = f"SELECT pincode, Transactioncount, transactionamount FROM top_transaction WHERE year={t_year} AND quarter={t_Quarter} ORDER BY transactionamount DESC LIMIT 10"
                 mycursor.execute(query)
                 df = pd.DataFrame(mycursor.fetchall(), columns=['Pincode', 'Transactioncount', 'Transactionamount'])
                 st.write(df)
  
        #USER ANALYSIS
        if Type=="Users":

            #GEO VISUALIZATION
            mycursor.execute(f"select state, sum(registereduser),sum(appopens) from map_user where year={t_year} and quarter={t_Quarter} group by state;")
            df1 = pd.DataFrame(mycursor.fetchall(),columns= ['State', 'registereduser', 'appopens'])
            df2 = pd.read_csv(r'C:\Users\Monisha User\Desktop\guvi-project\states_india.csv')
            df1.State = df2.st_nm

            fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                      featureidkey='properties.ST_NM',
                      locations='State',
                      color='registereduser',
                      color_continuous_scale='sunset')

            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig,use_container_width=True)
             


            #TOP BRAND, PINCODE, DISTRICT REPORT OF USER
            top_brand,district,pincode=st.tabs(["Top_Brand","District","Pincode"])
            with top_brand:
                 query = f"select brands, sum(count),sum(Percentage) from aggregated_user where year={t_year} and Quarter={t_Quarter} group by Brands order by sum(count) desc limit 10;"
                 mycursor.execute(query)
                 df = pd.DataFrame(mycursor.fetchall(), columns=['BRANDS', 'TOTAL_COUNT', 'TOTAL_PERCENTAGE'])
                 st.write(df)

            with district:
                 query = f"SELECT district, RegisteredUser, appopens FROM map_user WHERE year={t_year} AND quarter={t_Quarter} ORDER BY RegisteredUser DESC LIMIT 10"
                 mycursor.execute(query)
                 df = pd.DataFrame(mycursor.fetchall(), columns=['districts', 'RegisteredUser', 'AppOpens'])
                 st.write(df)
            with pincode:
                 query = f"SELECT pincode, RegisteredUser FROM top_user WHERE year={t_year} AND quarter={t_Quarter} ORDER BY RegisteredUser DESC LIMIT 10"
                 mycursor.execute(query)
                 df = pd.DataFrame(mycursor.fetchall(), columns=['Pincode', 'RegisteredUser'])
                 st.write(df)

#GET VARIOUS YEAR WISE INSIGHT WITH DATA VISUALIZATION                 
if select=="Insights":
    
    s_year = st.slider("*Year*", min_value=2018, max_value=2023)
    questions = st.selectbox('Select Questions',
    ['1.List the most used transaction type based on transaction count',
     '2.List the most used transaction type based on the transaction amount',
     '3.List the top 10 used mobile brand',
     '4.List the district which had least app opens',
     '5.List the state which has more registered user',
     '6.List the district which had more app opens',
     '7.List the state with least insurance transaction count',
     '8.List the state with more user transaction count',
     '9.List the district with more insurance transaction count',
     '10.List the top 10 district with least insurance transaction count'
     ])
    
    if questions == '1.List the most used transaction type based on transaction count':
        query = f"select transactiontype, avg(transactioncount) as average_transaction from aggregated_transaction where year={s_year} group by TransactionType"
        mycursor.execute(query)
        df = pd.DataFrame(mycursor.fetchall(), columns=['Transactiontype', 'Average_transaction'])
        st.write(df)
        fig = px.bar(df,title='TRANSACTION TYPE BASED ON TRANSACTION COUNT',
                            x="Transactiontype",
                            y="Average_transaction",
                            color='Transactiontype',
                            color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig)  
            
    elif questions == '2.List the most used transaction type based on the transaction amount':
        query = f"select transactiontype, avg(transactionamount) as average_transaction from aggregated_transaction where year={s_year} group by TransactionType"
        mycursor.execute(query)
        df = pd.DataFrame(mycursor.fetchall(), columns=['Transactiontype', 'TransactionAmount'])
        st.write(df)
        fig = px.bar(df,title='TRANSACTION TYPE BASED ON TRANSACTION AMOUNT',
                            x="Transactiontype",
                            y="TransactionAmount",
                            color='Transactiontype',
                            color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig)
       
    elif questions == '3.List the top 10 used mobile brand':
        query = f"select brands, count(*) from aggregated_user where year={s_year} group by brands limit 10 "
        mycursor.execute(query)
        df = pd.DataFrame(mycursor.fetchall(), columns=['Brands', 'Count'])
        st.write(df)
        fig = px.pie(df, values='Count',
                         names='Brands',
                         title='TOP USED MOBILE BRANDS',
                         color_discrete_sequence=px.colors.sequential.Agsunset,
                         hover_data=['Count'])

        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig,use_container_width=True)

    elif questions == '4.List the district which had least app opens':
        query = f"select district,avg(appopens) from map_user where year={s_year} group by District order  by avg(AppOpens)  limit 10"
        mycursor.execute(query)
        df = pd.DataFrame(mycursor.fetchall(), columns=['District', 'AppOpens'])
        st.write(df)
        fig = px.bar(df,title='DISTRICT:APPOPENS',
                            x="District",
                            y="AppOpens",
                            color='AppOpens',
                            color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig)

    elif questions == '5.List the state which has more registered user':
        query = f"select state,round(avg(registereduser)) from map_user where year={s_year} group by state order by round(avg(RegisteredUser)) desc limit 10"
        mycursor.execute(query)
        df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'RegisteredUser'])
        st.write(df)
        fig = px.bar(df,title='STATE WHICH HAS MORE REGISTERED  USER',
                            x="RegisteredUser",
                            y="State",
                            color='RegisteredUser',
                            orientation='h',
                            color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig)
  
    elif questions == '6.List the district which had more app opens':
        query = f"select district,avg(appopens) from map_user where year={s_year} group by District order  by avg(AppOpens) desc limit 10"
        mycursor.execute(query)
        df = pd.DataFrame(mycursor.fetchall(), columns=['District', 'AppOpens'])
        st.write(df)
        fig = px.bar(df,title='DISTRICT:APPOPENS',
                            x="District",
                            y="AppOpens",
                            color='AppOpens',
                            color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig)

    elif questions == '7.List the state with least insurance transaction count':
        query = f"select state,sum(transactioncount) as total_transaction_count from aggregated_insurance where year={s_year} group by state order by total_transaction_count limit 10 "
        mycursor.execute(query)
        df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Insurance_TransactionCount'])
        st.write(df)
        fig = px.pie(df, values='Insurance_TransactionCount',
                         names='State',
                         title='TOP USED MOBILE BRANDS',
                         color_discrete_sequence=px.colors.sequential.Agsunset,
                         hover_data=['Insurance_TransactionCount'])

        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig,use_container_width=True)
    
    elif questions == '8.List the state with more user transaction count':
        query = f"select state, sum(transactioncount) from aggregated_transaction where year={s_year} group by state order by sum(TransactionCount) desc limit 10; "
        mycursor.execute(query)
        df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'User_Transaction_Count'])
        st.write(df)
        fig = px.bar(df,title='STATE:TRANSACTION COUNT',
                            x="State",
                            y="User_Transaction_Count",
                            color='User_Transaction_Count',
                            color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig)
    
    elif questions == '9.List the district with more insurance transaction count':
        query = f"select districts, sum(transactioncount) from map_insurance where year={s_year} group by districts order by sum(TransactionCount) desc limit 10; "
        mycursor.execute(query)
        df = pd.DataFrame(mycursor.fetchall(), columns=['District','Insurance_TransactionCount'])
        st.write(df)
        fig = px.bar(df,title='DISTRICT:INSURANCE TRANSACTION COUNT',
                            y="District",
                            x="Insurance_TransactionCount",
                            color='Insurance_TransactionCount',
                            color_continuous_scale=px.colors.sequential.Agsunset,
                            orientation='h')
        st.plotly_chart(fig)
   
    elif questions == '10.List the top 10 district with least insurance transaction count':
        query = f"select districts, sum(transactioncount) from map_insurance where year={s_year} group by districts order by sum(TransactionCount) limit 10; "
        mycursor.execute(query)
        df = pd.DataFrame(mycursor.fetchall(), columns=['District','Insurance_TransactionCount'])
        st.write(df)
        fig = px.bar(df,title='DISTRICT:INSURANCE TRANSACTION COUNT',
                            y="District",
                            x="Insurance_TransactionCount",
                            color='Insurance_TransactionCount',
                            color_continuous_scale=px.colors.sequential.Agsunset,
                            orientation='h')
        st.plotly_chart(fig)

    