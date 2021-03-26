"""
@author: mks
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import streamlit as st
from PIL import Image
import os

os.chdir('C:\\Users\\fgo\\OneDrive - UEFA\\Python\\Streamlit\\Domestic rankings')

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"}

# %% Streamlit titles and sidebar
st.set_page_config(page_title="UEFA Club Competitions Analytics") # use all the width of the page

# Sidebar
# #011839;
# get sidebar texts moved up and background color (#66B2FF => light blue):
st.markdown("""
    <style>
    .css-1aumxhk {
        padding: 0em 1em;
        background-color: #66B2FF;
        background-image: none;
        color: black
    }
    </style>
""", unsafe_allow_html=True)

image = Image.open('UEFA_logo_fullcol.png')
st.sidebar.image(image, width=75, caption='UEFA Club Competitions', use_column_width=False)

st.sidebar.header('55 National Associations')
st.sidebar.header('Domestic Rankings')
st.sidebar.write('')

season = st.sidebar.number_input('Season', min_value=1950, value=2021, step=1)

# %%
df_urls = [
            'https://www.transfermarkt.com/kategoria-superiore/tabelle/wettbewerb/ALB1/saison_id/'+str(season-1), 
            'https://www.transfermarkt.com/primera-divisio/tabelle/wettbewerb/AND1/saison_id/'+str(season-1), 
            'https://www.transfermarkt.com/bardsragujn-chumb/tabelle/wettbewerb/ARM1/saison_id/'+str(season-1), 
            'https://www.transfermarkt.com/bundesliga/tabelle/wettbewerb/A1/saison_id/'+str(season-1), 
            'https://www.transfermarkt.com/premyer-liqasi/tabelle/wettbewerb/AZ1/saison_id/'+str(season-1), 
            'https://www.transfermarkt.com/jupiler-pro-league/tabelle/wettbewerb/BE1/saison_id/'+str(season-1), 
            'https://www.transfermarkt.com/premijer-liga/tabelle/wettbewerb/BOS1/saison_id/'+str(season-1), 
            'https://www.transfermarkt.com/vysheyshaya-liga/tabelle/wettbewerb/WER1/saison_id/'+str(season-2), 
            'https://www.transfermarkt.com/parva-liga/tabelle/wettbewerb/BU1/saison_id/'+str(season-1), 
            'https://www.transfermarkt.com/1-hnl/tabelle/wettbewerb/KR1/saison_id/'+str(season-1), 
            'https://www.transfermarkt.com/first-division/tabelle/wettbewerb/ZYP1/saison_id/'+str(season-1), 
            'https://www.transfermarkt.com/fortuna-liga/tabelle/wettbewerb/TS1/saison_id/'+str(season-1), 
            'https://www.transfermarkt.com/alka-superligaen/tabelle/wettbewerb/DK1/saison_id/'+str(season-1), 
            'https://www.transfermarkt.com/premier-league/tabelle/wettbewerb/GB1/saison_id/'+str(season-1), 
            'https://www.transfermarkt.com/laliga/tabelle/wettbewerb/ES1/saison_id/'+str(season-1), 
            'https://www.transfermarkt.com/premium-liiga/tabelle/wettbewerb/EST1/saison_id/'+str(season-2), 
            'https://www.transfermarkt.com/veikkausliiga/tabelle/wettbewerb/FI1/saison_id/'+str(season-2), 
            'https://www.transfermarkt.com/ligue-1/tabelle/wettbewerb/FR1/saison_id/'+str(season-1), 
            'https://www.transfermarkt.com/betri-deildin/tabelle/wettbewerb/FARO/saison_id/'+str(season-2), 
            'https://www.transfermarkt.com/crystalbet-erovnuli-liga/tabelle/wettbewerb/GE1N/saison_id/'+str(season-2), 
            'https://www.transfermarkt.com/bundesliga/tabelle/wettbewerb/L1/saison_id/'+str(season-1), 
            'https://www.transfermarkt.com/gibraltar-premier-division/tabelle/wettbewerb/GI1/saison_id/'+str(season-1), 
            'https://www.transfermarkt.com/super-league/tabelle/wettbewerb/GR1/saison_id/'+str(season-1), 
            'https://www.transfermarkt.com/nemzeti-bajnoksag/tabelle/wettbewerb/UNG1/saison_id/'+str(season-1), 
            'https://www.transfermarkt.com/league-of-ireland/tabelle/wettbewerb/IR1/saison_id/'+str(season-2), 
            'https://www.transfermarkt.com/pepsi-max-deild/tabelle/wettbewerb/IS1/saison_id/'+str(season-2), 
            'https://www.transfermarkt.com/ligat-haal/tabelle/wettbewerb/ISR1/saison_id/'+str(season-1), 
            'https://www.transfermarkt.com/serie-a/tabelle/wettbewerb/IT1/saison_id/'+str(season-1), 
            'https://www.transfermarkt.com/premier-liga/tabelle/wettbewerb/KAS1/saison_id/'+str(season-2), 
            'https://www.transfermarkt.com/ipko-superliga/tabelle/wettbewerb/KO1/saison_id/'+str(season-1), 
            'n.a.', 
            'https://www.transfermarkt.com/a-lyga/tabelle/wettbewerb/LI1/saison_id/'+str(season-2), 
            'https://www.transfermarkt.com/bgl-ligue/tabelle/wettbewerb/LUX1/saison_id/'+str(season-1), 
            'https://www.transfermarkt.com/virsliga/tabelle/wettbewerb/LET1/saison_id/'+str(season-2), 
            'https://www.transfermarkt.com/divizia-nationala/tabelle/wettbewerb/MO1N/saison_id/'+str(season-2), 
            'https://www.transfermarkt.com/prva-makedonska-fudbalska-liga/tabelle/wettbewerb/MAZ1/saison_id/'+str(season-1), 
            'https://www.transfermarkt.com/premier-league/tabelle/wettbewerb/MAL1/saison_id/'+str(season-1), 
            'https://www.transfermarkt.com/telekom-1-cfl/tabelle/wettbewerb/MNE1/saison_id/'+str(season-1), 
            'https://www.transfermarkt.com/eredivisie/tabelle/wettbewerb/NL1/saison_id/'+str(season-1), 
            'https://www.transfermarkt.com/danske-bank-premiership/tabelle/wettbewerb/NIR1/saison_id/'+str(season-1), 
            'https://www.transfermarkt.com/eliteserien/tabelle/wettbewerb/NO1/saison_id/'+str(season-2), 
            'https://www.transfermarkt.com/ekstraklasa/tabelle/wettbewerb/PL1/saison_id/'+str(season-1), 
            'https://www.transfermarkt.com/liga-nos/tabelle/wettbewerb/PO1/saison_id/'+str(season-1), 
            'https://www.transfermarkt.com/liga-1-betano/tabelle/wettbewerb/RO1/saison_id/'+str(season-1), 
            'https://www.transfermarkt.com/premier-liga/tabelle/wettbewerb/RU1/saison_id/'+str(season-1), 
            'https://www.transfermarkt.com/scottish-premiership/tabelle/wettbewerb/SC1/saison_id/'+str(season-1), 
            'n.a.', 
            'https://www.transfermarkt.com/superliga/tabelle/wettbewerb/SER1/saison_id/'+str(season-1), 
            'https://www.transfermarkt.com/super-league/tabelle/wettbewerb/C1/saison_id/'+str(season-1), 
            'https://www.transfermarkt.com/fortuna-liga/tabelle/wettbewerb/SLO1/saison_id/'+str(season-1), 
            'https://www.transfermarkt.com/prva-liga/tabelle/wettbewerb/SL1/saison_id/'+str(season-1), 
            'https://www.transfermarkt.com/allsvenskan/tabelle/wettbewerb/SE1/saison_id/'+str(season-2), 
            'https://www.transfermarkt.com/super-lig/tabelle/wettbewerb/TR1/saison_id/'+str(season-1), 
            'https://www.transfermarkt.com/premier-liga/tabelle/wettbewerb/UKR1/saison_id/'+str(season-1), 
            'https://www.transfermarkt.com/welsh-premier-league/tabelle/wettbewerb/WAL1/saison_id/'+str(season-1)
        ]

countries = [
            'Albania', 
            'Andorra', 
            'Armenia', 
            'Austria', 
            'Azerbaijan', 
            'Belgium', 
            'Bosnia-Herzegovina', 
            'Belarus', 
            'Bulgaria', 
            'Croatia', 
            'Cyprus', 
            'Czech Republic', 
            'Denmark', 
            'England', 
            'Spain', 
            'Estonia', 
            'Finland', 
            'France', 
            'Faroe Islands', 
            'Georgia', 
            'Germany', 
            'Gibraltar', 
            'Greece', 
            'Hungary', 
            'Republic of Ireland', 
            'Iceland', 
            'Israel', 
            'Italy', 
            'Kazakhstan', 
            'Kosovo', 
            'Liechtenstein', 
            'Lithuania', 
            'Luxembourg', 
            'Latvia', 
            'Moldova', 
            'FYR Macedonia', 
            'Malta', 
            'Montenegro', 
            'Netherlands', 
            'Northern Ireland', 
            'Norway', 
            'Poland', 
            'Portugal', 
            'Romania', 
            'Russia', 
            'Scotland', 
            'San Marino', 
            'Serbia', 
            'Switzerland', 
            'Slovakia', 
            'Slovenia', 
            'Sweden', 
            'Turkey', 
            'Ukraine', 
            'Wales'
        ]

df_countries = pd.DataFrame(
    {'urls': df_urls,
     'countries': countries,
    }).sort_values(by=['countries'])
    
# %%
Title_html = """
            <style>
                .title h1{
                  font-size: 16px;
                  color: black;
                }
            </style> 
            
            <div class="title">
                <h1>-----------------------------------------------</h1>
            </div>
            """
st.sidebar.markdown(Title_html, unsafe_allow_html=True) #Title rendering

st.header('Domestic Rankings for season '+str(season-1)+'/'+str(season))
#st.info("### Domestic Rankings")    
st.write('')

country = st.selectbox("Select Country", df_countries['countries'])
#index_country = [index for index in range(len(df_countries)) if df_countries[index] == country][0]
index_country = df_countries.index[df_countries['countries'] == country].tolist()[0]

st.write('')
st.write('')


# %% Webcrawler
res = requests.get(df_countries.iloc[index_country,0], headers=headers)

if res.status_code == 200 and country != 'Liechtenstein' and country != 'San Marino':
    soup = BeautifulSoup(res.content, 'html.parser')
    soup = soup.find("div",{"class":"responsive-table"})
    soup = soup.find("tbody")
    soup = soup.findAll("tr")

    results = []
    for ele in soup:
        temp = []
        ele = ele.findAll("td")

        sr = ele[0].text.replace("\xa0","")
        club = ele[2].text.replace("\xa0","").strip()
        link = "https://www.transfermarkt.com" + ele[2].find("a")["href"]		

        temp = [sr,club,ele[3].text,ele[4].text,ele[5].text,ele[6].text,ele[7].text,ele[8].text,ele[9].text]

        results.append(temp)

    df_table = pd.DataFrame(results,columns=["#","Club","Matches","W","D","L","Goals","+/-","Pts"])
    df_table.index = [""] * len(df_table) # hide index
    st.dataframe(df_table, height=2000)    
    #st.table(df_table)
    
    '##### Source: https://www.transfermarkt.com'                                    
     
else:                                    
    st.error('No ranking for this country')



                                       