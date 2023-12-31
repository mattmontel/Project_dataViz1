__author__='Matthieu MONTEL'
__copyright__='Copyright 2023'
__credits__=['Matthieu Montel']
__version__='0.0.1'
__maintainer__='Matthieu Montel'
__email__='matthieu.montel@efrei.net'
__status__='Final Code'

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import geopandas as gpd
import matplotlib.patches as mpatches
import pydeck as pdk
import plotly.graph_objects as go
import matplotlib.patches as mpatches

@st.cache_resource
def load_info():
    st.sidebar.text("Nom : MONTEL")
    st.sidebar.text("Prénom : Matthieu")
    st.sidebar.text("École : EFREI PARIS")
    st.sidebar.text("Promo : 2025")
    st.sidebar.text("Classe : BIA2")

load_info()

st.title("Analyse des Résultats des Élections Présidentielles")
st.write("""Bienvenue sur cette analyse interactive des résultats des élections présidentielles. Utilisez les widgets pour explorer les données et obtenir des insights sur les performances des candidats par département.""")

dataT1 = pd.read_csv('resultats-par-niveau-burvot-t1-france-entiere.csv')
dataT2 = pd.read_csv('resultats-par-niveau-burvot-t2-france-entiere.csv')


#Traitement des données
dataT2 = dataT2.drop(['Code de la circonscription', 'Libellé de la circonscription','Code du b.vote','Libellé de la commune','Code de la commune'], axis=1)


def custom_aggregationT2(column):
    result = {
        'Inscrits': column['Inscrits'].sum(),
        'Abstentions': column['Abstentions'].sum(),
        '% Abs/Ins': column['% Abs/Ins'].mean(),
        'Votants': column['Votants'].sum(),
        '% Vot/Ins': column['% Vot/Ins'].mean(),
        'Blancs': column['Blancs'].sum(),
        '% Blancs/Ins': column['% Blancs/Ins'].mean(),
        '% Blancs/Vot': column['% Blancs/Vot'].mean(),
        'Nuls': column['Nuls'].sum(),
        '% Nuls/Ins': column['% Nuls/Ins'].mean(),
        '% Nuls/Vot': column['% Nuls/Vot'].mean(),
        'Exprimés': column['Exprimés'].sum(),
        '% Exp/Ins': column['% Exp/Ins'].mean(),
        '% Exp/Vot': column['% Exp/Vot'].mean(),
        'N°Panneau':'1',
        'Sexe':'M',
        'Nom':'MACRON',
        'Prénom':'Emmanuel',
        'Voix1':column['Voix'].sum(),
        '% Voix/Ins': column['% Voix/Ins'].mean(),
        '% Voix/Exp': column['% Voix/Exp'].mean(),
        'N°Panneau2':'2',
        'Sexe2':'F',
        'Nom2':'LE PEN',
        'Prénom2':'Marine',
        'Voix2': column['Voix2'].sum(),
        '% Voix/Ins2': column['% Voix/Ins2'].mean(),
        '% Voix/Exp2': column['% Voix/Exp2'].mean(),
    }
    return pd.Series(result)

grouped_data = dataT2.groupby(['Code du département', 'Libellé du département']).apply(custom_aggregationT2).reset_index()



#création de toutes les fonctions pour les visualisations futurs
@st.cache_resource
def interactive_bar_candidate(data, candidate='Macron'):
    column = 'Voix1' if candidate == 'Macron' else 'Voix2'
    fig = px.bar(data, x='Libellé du département', y=column, title=f'Votes pour {candidate} par département')
    return fig


@st.cache_resource
def interactive_bar_candidateT1(data, candidate='Macron'):
    candidats = ['Arthaud','Roussel','Macron','Lassalle','Le Pen','Zemmour','Melenchon','Hidalgo','Jadot','Pecresse','Poutou','Dupont-Aignan']
    
    index = candidats.index(candidate) + 1
    column = f'Voix{index}'

    fig = px.bar(data, x='Libellé du département', y=column, title=f'Votes pour {candidate} par département')
    return fig


@st.cache_resource
def load_geojson():
    return gpd.read_file('departements.geojson')


@st.cache_resource
def create_map(_merged):
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    merged.plot(color=merged['color'], ax=ax)
    macron_patch = mpatches.Patch(color='blue', label='Macron')
    lepen_patch = mpatches.Patch(color='red', label='Le Pen')
    plt.legend(handles=[macron_patch, lepen_patch])
    plt.title("Résultats des élections présidentielles par département")
    return fig


@st.cache_resource
def abstention_chart(data, threshold):
    filtered_data = data[data['Abstentions'] > threshold]
    return filtered_data.set_index('Libellé du département')['Abstentions']


@st.cache_resource
def pie_chart(departement_data):
    labels = ['Votants', 'Abstentions', 'Blancs']
    sizes = [departement_data['Votants'].values[0], departement_data['Abstentions'].values[0], departement_data['Blancs'].values[0]]
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    return fig


@st.cache_resource
def determine_winner_color(row):
    candidats = ['Arthaud','Roussel','Macron','Lassalle','Le Pen','Zemmour','Melenchon','Hidalgo','Jadot','Pecresse','Poutou','Dupont-Aignan']
    colors = ['gray', 'gold', 'blue', 'cyan', 'red', 'black', 'purple', 'orange', 'green', 'pink', 'brown', 'navy']

    max_votes = 0
    max_candidate = None
    for i, candidate in enumerate(candidats):
        if row[f'Voix{i+1}'] > max_votes:
            max_votes = row[f'Voix{i+1}']
            max_candidate = candidate

    return colors[candidats.index(max_candidate)]


@st.cache_resource
def create_mapT1(_merged):
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    _merged.plot(color=_merged['color'], ax=ax)

    candidats = ['Arthaud','Roussel','Macron','Lassalle','Le Pen','Zemmour','Melenchon','Hidalgo','Jadot','Pecresse','Poutou','Dupont-Aignan']
    colors = ['gray', 'gold', 'blue', 'cyan', 'red', 'black', 'purple', 'orange', 'green', 'pink', 'brown', 'navy']

    # Création de la légende
    patches = [mpatches.Patch(color=colors[i], label=candidats[i]) for i in range(len(candidats))]
    plt.legend(handles=patches, bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.title("Résultats des élections présidentielles par département")
    return fig


@st.cache_resource
def compare_total_votes(dataT1, grouped_data):
    total_votes_T1 = {
        "Macron": dataT1["Voix3"].sum(),
        "Le Pen": dataT1["Voix5"].sum()
    }
    
    total_votes_T2 = {
        "Macron": grouped_data["Voix1"].sum(),
        "Le Pen": grouped_data["Voix2"].sum()
    }
    
    fig = px.bar(
        x=["Macron T1", "Le Pen T1", "Macron T2", "Le Pen T2"],
        y=[total_votes_T1["Macron"], total_votes_T1["Le Pen"], total_votes_T2["Macron"], total_votes_T2["Le Pen"]],
        title="Comparaison des voix totales entre le premier et le second tour"
    )
    
    return fig


@st.cache_resource
def compare_voting_patterns(dataT1,grouped_data):

    votants_T1 = dataT1["Votants"].sum()
    blancs_T1 = dataT1["Blancs"].sum()
    abstentions_T1 = dataT1["Abstentions"].sum()

    votants_T2 = grouped_data["Votants"].sum()
    blancs_T2 = grouped_data["Blancs"].sum()
    abstentions_T2 = grouped_data["Abstentions"].sum()  


    categories = ["Votants", "Blancs", "Abstentions"]
    values_T1 = [votants_T1, blancs_T1, abstentions_T1]
    values_T2 = [votants_T2, blancs_T2, abstentions_T2]

    fig = go.Figure(data=[
        go.Bar(name='Tour 1', x=categories, y=values_T1),
        go.Bar(name='Tour 2', x=categories, y=values_T2)
    ])

    fig.update_layout(title="Comparaison des votants, votes blancs et abstentions entre le Tour 1 et le Tour 2", xaxis_title="Catégories", yaxis_title="Nombre", barmode='group')

    return fig


option = st.selectbox(
    'Choisissez une option:',
    ('Premier tour', 'Deuxième tour', 'Comparaison des deux')
)

if option == 'Premier tour':
    st.write('Résultats du premier tour...')
    

    st.subheader("Aperçu des Données")
    st.write(dataT1.head())

    st.subheader("Analyse des Votes par Candidat")
    st.write("Sélectionnez un candidat pour visualiser le nombre de votes qu'il a reçu dans chaque département.")
    candidate = st.selectbox('Choisissez un candidat:', ['Arthaud','Roussel','Macron','Lassalle','Le Pen','Zemmour','Melenchon','Hidalgo','Jadot','Pecresse','Poutou','Dupont-Aignan'])
    fig = interactive_bar_candidateT1(dataT1, candidate)
    st.plotly_chart(fig)

    st.subheader("Cartographie des Résultats par Département")
    france_departments = load_geojson()
    merged = france_departments.set_index('nom').join(dataT1.set_index('Libellé du département'))
    merged['color'] = merged.apply(determine_winner_color, axis=1)
    fig = create_mapT1(merged)
    st.pyplot(fig)      

    st.subheader("Détails des Votes par Département")
    departement = st.selectbox("Choisissez un département:", dataT1['Libellé du département'].unique())
    departement_data = dataT1[dataT1['Libellé du département'] == departement]
    fig = pie_chart(departement_data)
    st.pyplot(fig)


elif option == 'Deuxième tour':
    st.write('Résultats du deuxième tour...')


    st.subheader("Aperçu des Données")
    st.write(grouped_data.head())

    st.subheader("Analyse des Votes par Candidat")
    st.write("Sélectionnez un candidat pour visualiser le nombre de votes qu'il a reçu dans chaque département.")
    candidate = st.selectbox('Choisissez un candidat:', ['Macron', 'Le Pen'])
    fig = interactive_bar_candidate(grouped_data, candidate)
    st.plotly_chart(fig)

    st.subheader("Cartographie des Résultats par Département")
    france_departments = load_geojson()
    merged = france_departments.set_index('nom').join(grouped_data.set_index('Libellé du département'))
    merged['color'] = merged.apply(lambda row: 'blue' if row['Voix1'] > row['Voix2'] else 'red', axis=1)
    fig = create_map(merged)
    st.pyplot(fig)

    st.subheader("Analyse des Abstentions")
    threshold = st.slider("Filtrer les départements par abstentions supérieures à:", 0, grouped_data['Abstentions'].max(), value=1000, step=100)
    chart_data = abstention_chart(grouped_data, threshold)
    st.bar_chart(chart_data)

    st.subheader("Détails des Votes par Département")
    departement = st.selectbox("Choisissez un département:", grouped_data['Libellé du département'].unique())
    departement_data = grouped_data[grouped_data['Libellé du département'] == departement]
    fig = pie_chart(departement_data)
    st.pyplot(fig)


elif option == 'Comparaison des deux':
    st.write('Comparaison des deux tours...')


    st.plotly_chart(compare_total_votes(dataT1, grouped_data))
    st.plotly_chart(compare_voting_patterns(dataT1,grouped_data))


