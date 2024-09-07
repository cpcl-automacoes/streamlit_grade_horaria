import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

st.set_page_config(page_title="Aulas por professor", page_icon="🕒",layout="wide")
sheet_url = st.secrets["SPREADSHEET"]

conn = st.connection("gsheets", type=GSheetsConnection)
df_lelia = conn.read(worksheet="Turma - LÉLIA GONZÁLEZ",spreadsheet=sheet_url)
df_eliane = conn.read(worksheet="Turma - ELIANE POTIGUARA",spreadsheet=sheet_url)

df = pd.concat([df_lelia,df_eliane])

df['Data'] = pd.to_datetime(df['Data'],format="%d/%m/%Y")

# Get today's date
today = pd.to_datetime(datetime.today().strftime('%d/%m/%Y'), format='%d/%m/%Y')

# Filter rows where the date is equal or greater than today
filtered_df = df[df['Data'] >= today]

filtered_df['Data'] = filtered_df['Data'].dt.strftime('%d/%m/%Y')

# Melt the dataframe to reshape it
df_melted = pd.melt(filtered_df, id_vars=['Data'], var_name='Horário da Aula', value_name='Aula')

# Extract the professor names from the 'Aula' column
df_melted['Professor'] = df_melted['Aula'].str.extract(r'\((.*?)\)')
df_melted['Aula'] = df_melted['Aula'].str.split(' ').str[0]

# Renaming columns for clarity
df_melted.rename(columns={'Data': 'Data da Aula'}, inplace=True)

# Selecting the relevant columns
df_final = df_melted[['Professor', 'Data da Aula', 'Horário da Aula']]

professores = df_final["Professor"].unique()

professor_select = st.selectbox(
    label="Selecione o professor",
    options = professores,
    placeholder = "Selecione o professor"
)

selected_df = filtered_df.loc[filtered_df["Professor"] == professor_select]
st.dataframe(selected_df,use_container_width=True,hide_index=True)
