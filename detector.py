# Import necessary library
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sns
import numpy as np

# Title 
st.sidebar.title(':green[Credit Fraud Detection]')

# Provide options to the user to select the type of file
type_options = ['PDF','EXCEL','CSV']
type = st.sidebar.selectbox('Select Your File Type',type_options)

# Get file from user to create dataframe based on user selection
def df_type(type):
   if type == 'CSV':
      uploader = st.sidebar.file_uploader('Upload Your File Below',type=['CSV'])
      upload = pd.read_csv(uploader)
      return upload

   elif type == 'EXCEL':
       uploader = st.sidebar.file_uploader('Upload Your File Below',type=['EXCEL'])
       upload = pd.read_excel(uploader)
       return upload

   else:
       uploader = st.sidebar.file_uploader('Upload Your File Below',type=['PDF'])
       #upload = pd.read_
       #st.dataframe(upload)
       #return upload

# Call the function for uploading the file
frame = df_type(type)

if frame is not None:
   
   # To ignore globle warning message by streamlit
   st.set_option('deprecation.showPyplotGlobalUse', False)
   
   # Create dataframe
   df = pd.DataFrame(frame)
    
   df_copy = df.copy()
   
   # Drop all the none value columns from the dataframe & sorting it by the loan amount
   df_new = df_copy.dropna(axis=1,how='all')
   df_new = df_new.sort_values('loan_amnt')

   
   if df_new is not None:
      
      # Find total number of loan sanctioned
      st.subheader(':blue[Total Number Of Loan Sanctioned]')
      x=np.shape(df_new)
      st.subheader(x[0])
      
      # Seperate the numbers from the % symbol at the intrest rate column and store it as folat data type 
      df_new['int_rate'] = df_new['int_rate'].str.rstrip('%').astype('float')
      
      # Analysis
      # To understand the loan amount range
      st.write(':red[Loan amount distribution and mostly borrowed loan amount range]')

      # Plot the distribution of loan amounts
      plt.figure(figsize=(8,5))
      sns.histplot(data=df_new, x='loan_amnt')
      plt.title('Distribution of Loan Amounts')
      plt.xlabel('Loan Amount')
      plt.ylabel('Count')
      st.pyplot()

      # Hypothisis
      st.write(':green[The loan amount ranges from 500 to 35,000, with most loans between 5,000 and 15,000.]')
      
      
      # Create columns to show the loan status distribution
      co1,co2 = st.columns(2)

      with co1:

      # Analysis
          st.write(':red[Percentage of loan repayment status]') 

      # Calculate loan status distribution
          loan_status_dist = df_new['loan_status'].value_counts(normalize=True) * 100

      # Print the distribution
          st.subheader('Loan status distribution:')
          st.table(loan_status_dist)

      # Hypothesis
          st.write(':green[The majority of loans are fully paid (82.96%), followed by current loans (14.16%). A small percentage of loans are either charged off or late in payment. This indicates that most borrowers are able to repay their loans.]')

      with co2:

      # Visualize the distribution by using a pie plot
          plt.figure(figsize=(5,5))
          plt.pie(loan_status_dist, labels=loan_status_dist.index, autopct='%1.1f%%', startangle=90)
          #plt.title("Loan Status Distribution")
          st.pyplot()
      
      # Create tabs for various analysis on the data
      st.subheader(':blue[Loan Status Based On :]')
      tab1,tab2,tab3,tab4,tab5 = st.tabs(['Intrest Rate','Loan Amount','Home Ownership','Anual Income','Purpose'],)

      with tab1:
         # Analysis
         st.write(':red[How the intrest rate affect the repayment]')

         # Create boxplot to show the analysis between intrest rate and loan repayment status
         sns.set(style="whitegrid")
         plt.figure(figsize=(10,8))
         sns.boxplot(x="loan_status", y="int_rate", data=df_new)
         plt.title('Interest Rate by Loan Status')
         plt.xlabel('Loan Status')
         plt.ylabel('Interest Rate (%)')
         st.pyplot()

         # Hypothesis
         st.write(':green[Charged-off have a higher interest rate compared to fully paid and current loans. This indicates that higher interest rates can lead to loan defaults]')

      with tab2:
         # Analysis
         st.write(':red[How the loan amount affect the repayment]')

         # Create boxplot to show the analysis between loan amount and loan repayment status
         plt.figure(figsize=(10,8))
         sns.boxplot(x='loan_status', y='loan_amnt', data=df_new)
         plt.title('Loan amount by Loan Status')
         plt.xlabel('Loan Status')
         plt.ylabel('Loan amount')
         st.pyplot()

         # Hypothesis
         st.write(':green[Fully paid loans have a higher loan amount compared to charged-off and late loans. This suggests that borrowers who take out higher loans are more likely to fully repay them.]')

      with tab3:
         # Analysis
         st.write(':red[How the home ownership affect the repayment]')

         # Create countplot to show the analysis between home ownership and loan repayment status.
         sns.countplot(x="home_ownership", hue="loan_status", data=df_new)
         plt.title('Home Ownership by Loan Status')
         st.pyplot()

         # Hypothesis
         st.write(':green[Borrowers who own a home have a lower default rate compared to those who rent. This suggests that homeowners are more financially stable and have a higher likelihood of repaying their loans.]')

      with tab4:
         # Analysis
         st.write(':red[How the annual income affect the repayment]')
         # Create boxplot to show the analysis between intrest rate and loan repayment status
         # Filter fully paid loans and charged off loans
         fully_paid = df_new[df_new['loan_status'] == 'Fully Paid'] 
         charged_off = df_new[df_new['loan_status'] == 'Charged Off'] 

         fully_paid1 = fully_paid[fully_paid['annual_inc'] <= 400000]
         charged_off1 = charged_off[charged_off['annual_inc'] <= 400000]
                           
         # Plot histograms of annual income for fully paid and charged off loans
         sns.histplot(fully_paid1['annual_inc'], color='green', alpha=1, label='Fully Paid')
         sns.histplot(charged_off1['annual_inc'], color='red', alpha=1, label='Charged Off')


         # Set plot title and labels
         plt.title('Distribution of Annual Income for Fully Paid and Charged Off Loans')
         plt.xlabel('Annual Income')
         plt.ylabel('Count')
         plt.legend()
         st.pyplot()

         # Hypothesis
         st.write(':green[Borrowers with higher annual incomes are more likely to fully repay their loans.The distribution of annual income for fully paid loans is skewed towards higher income levels compared to charged-off loans, it would support the hypothesis.]')

      with tab5:
         # Analysis
         st.write(':red[How the purpose of the loan affect the repayment]')
         # Create boxplot to show the analysis between purpose of the loan and loan repayment status
         plt.figure(figsize=(10,6))
         sns.countplot(data=df_new, x='purpose', hue='loan_status')
         plt.xticks(rotation=90)
         plt.title('Loan Status by Purpose')
         st.pyplot()

         # Hypothisis
         st.write(':green[The resulting plot shows that debt consolidation is the most common purpose for taking out a loan, followed by credit cards and home improvement. Fully paid loans are the majority for all purposes. Charged-off loans are the minority for all purposes. This suggests that the purpose of the loan is not a significant factor in determining loan status.]')

      # Analysis on each loan amount sanctioned
      # Provide slider to select the loan amount 
      amount = df_new['loan_amnt'].unique()
      loan_amount = st.select_slider('Select Loan Amount',options=amount)
      
      amount_df=df_new[df_new['loan_amnt'] == loan_amount]

      # plot the count plot to show the loan status of selected amount
      plt.figure(figsize=(8,5))
      sns.countplot(x='loan_amnt',hue='loan_status',data=amount_df,palette = 'PuRd' ,orient='h',width=0.2)
      st.set_option('deprecation.showPyplotGlobalUse', False)
      st.pyplot()
      
      # Calculate number of debtors for the selected loan amount
      num_loan = np.shape(amount_df[amount_df['loan_amnt'] == loan_amount])
      st.header(':blue[Number of Debtors :]')
      st.header(num_loan[0])
      
      # Function for calculate the minimum,maximum & average intrest rate of selected loan amount
      def intrest_rate(inst_ptr):
          
          intrs = np.array(df_new['int_rate'])
          min = round(intrs.min())
          max = round(intrs.max())
          avg = round(intrs.mean())
          st.write(':orange[Minimun Intrest Rate (%) :]')
          st.subheader(min)
          st.write(':orange[Maximim Intrest Rate (%) :]')
          st.subheader(max)
          st.write(':orange[average Intrest Rate (%) :]')
          st.subheader(avg)
      
      # Function for calculate the minimum,maximum & average installment amount of selected loan amount
      def installment_amount(inst_amnt):
          
          intst = []

          for i in inst_amnt['installment']:
              intst.append(i)

          intrs = np.array(intst)
          min = round(intrs.min())
          max = round(intrs.max())
          avg = round(intrs.mean())
          st.write(':orange[Minimun Intrest amount (INR) :]')
          st.subheader(min)
          st.write(':orange[Maximum Intrest amount (INR) :]')
          st.subheader(max)
          st.write(':orange[Average Intrest amount (INR) :]')
          st.subheader(avg)

      # Provide user to select the repayment status type to analyse 
      choice = st.selectbox(':violet[Which type of debtor you want to analyze?]',options=['Fully Paid','Current','Charged Off'])

      if choice == 'Fully Paid':
             
             # Show the number of fully repayed debtors for the selected amount
             full_paid =  amount_df[amount_df['loan_status'] == 'Fully Paid']
             st.dataframe(full_paid)
             y = full_paid.shape
             st.subheader(':green[Number Of Fully Paid Debtors :]')
             st.subheader(y[0])
             
             # Provide a selectbox to the user for the various type of analysis options
             anly_base = st.selectbox(':blue[On which criteria base you want to analyse?]',options=['Intrest Rate','Installment Amount','Grade','Employment Duration','Resident type','Anual Income','Purpose'])
             if anly_base == 'Intrest Rate':
                
                 intrest_rate(full_paid)

             elif anly_base == 'Installment Amount':
           
                 installment_amount(full_paid)
                 
      # Show the number of currently repaying debtors for the selected amount
      elif choice == 'Current':
             current_payee =  amount_df[amount_df['loan_status'] == 'Current']
             st.dataframe(current_payee)
             y = current_payee.shape
             st.subheader(':violet[Number Of Current Debtors :]')
             st.subheader(y[0]) 
            
             # Provide a selectbox to the user for the various type of analysis options
             anly_base = st.selectbox(':blue[Analyze Based On :]',options=['Intrest Rate','Installment Amount'])

             if anly_base == 'Intrest Rate':
 
                intrest_rate(current_payee)

             elif anly_base == 'Installment Amount':
 
                installment_amount(current_payee)
      
      # Show the number of charged off debtors for the selected amount
      else:
             chargedoff =  amount_df[amount_df['loan_status'] == 'Charged Off']
             st.dataframe(chargedoff)
             y = chargedoff.shape
             st.subheader(':red[Number Of Charged Off Debtors :]')
             st.subheader(y[0])
             
             # Provide a selectbox to the user for the various type of analysis options
             anly_base = st.selectbox(':blue[Analyze Based On :]',options=['Intrest Rate','Installment Amount'])
             if anly_base == 'Intrest Rate':
                 
                intrest_rate(chargedoff)

             elif anly_base == 'Installment Amount':

                installment_amount(chargedoff)


      
      
      
                