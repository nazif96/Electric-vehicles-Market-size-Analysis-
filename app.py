import streamlit as st
import pandas as pd
import plotly.express as px
from fpdf import FPDF
import plotly.io as pio
import os
from streamlit_option_menu import option_menu
from streamlit_extras.metric_cards import style_metric_cards

# 🔽 Place la fonction ici
def generate_pdf_report(df_filtered, fig_box, fig_prix=None, fig_hist=None):
    
    fig_box.write_image("boxplot.png")
    if fig_prix:
        fig_prix.write_image("prix.png")
    if fig_hist:
        fig_hist.write_image("hist.png")

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, "Rapport Profil Véhicules Électriques", ln=True, align="C")

    pdf.set_font("Arial", "", 12)
    pdf.ln(10)
    pdf.cell(0, 10, f"Nombre de véhicules sélectionnés : {len(df_filtered)}", ln=True)

    pdf.ln(5)
    pdf.cell(0, 10, "Autonomie par Marque :", ln=True)
    pdf.image("boxplot.png", w=180)

    if fig_prix:
        pdf.add_page()
        pdf.cell(0, 10, "Prix moyen par modèle :", ln=True)
        pdf.image("prix.png", w=180)

    if fig_hist:
        pdf.add_page()
        pdf.cell(0, 10, "Répartition des autonomies :", ln=True)
        pdf.image("hist.png", w=180)

    pdf.output("rapport_ve.pdf")

    os.remove("boxplot.png")
    if fig_prix: os.remove("prix.png")
    if fig_hist: os.remove("hist.png")


st.set_page_config(page_title="Analyse Marché des Véhicules Électriques", page_icon="🚘", layout="wide")

st.title("🚗 Analyse du Marché des Véhicules Électriques - 2025")
 

# Menu latéral
with st.sidebar:
    selected = option_menu("Menu",
                           options=["Accueil", "Analyses",'Profils VéhiculesVE', 'Recommandation'],
                           icons=['house', 'bar-chart', 'car-front', 'check-square'], 
                           menu_icon="cast",
                           default_index=0, 
                           orientation="vertical") 




# Chargement des données
@st.cache_data
def load_data(filepath):
    try:
        df = pd.read_csv(filepath, compression='infer')
        df = df.dropna()
        df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_").str.replace(r"[()]", "", regex=True)
        if 'model_year' in df.columns:
            df['model_year'] = df['model_year'].astype("Int64")
        else:
            st.warning("⚠️ La colonne 'model_year' est absente.")
        return df
    except FileNotFoundError:
        st.error(f"❌ Fichier non trouvé : {filepath}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement : {e}")
        return pd.DataFrame()

df = load_data("Electric_Vehicle_Data_2025.csv.gz")

# Fonction table
def table():
    theme_plotly = None  # st.theme_set(theme_plotly)

    with st.expander("Tableau des données", expanded=True):
        all_columns = df.columns.tolist()
        default_cols = ['make', 'model_year', 'electric_range', 'base_msrp']
        default_cols = [col for col in default_cols if col in all_columns]

        shwdata = st.multiselect("Filtrer les données", all_columns, default=default_cols)

        if shwdata:
            filtered_df = df[shwdata]
            st.dataframe(filtered_df, use_container_width=True)
            st.write("### Description des données")
            st.write(filtered_df.describe())

            # Bouton de téléchargement
            csv = filtered_df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Télécharger les données filtrées", data=csv, file_name="donnees_vehicules_electriques.csv", mime='text/csv')
        else:
            st.warning("Veuillez sélectionner au moins une colonne à afficher.")

# Page d'accueil
if selected == "Accueil":
    st.markdown("Cette application permet d'analyser les données sur les véhicules électriques en fonction de différents critères.")
    st.markdown("Les données proviennent de [EV-Database](https://catalog.data.gov/dataset/electric-vehicle-population-data).") 
    st.subheader("Bienvenue dans l'application d'analyse du marché des véhicules électriques !")
    st.write("### Données sur les véhicules électriques")
    st.write("Cette section présente un tableau contenant des informations sur différents modèles de véhicules électriques.")
    table()
    
# Page d'analyse
if selected == "Analyses":
    st.subheader("Analyse du marché des véhicules électriques")
    #st.write("### Analyse du marché des véhicules électriques")
    #st.write("Cette section vous permet d'analyser les données sur les véhicules électriques en fonction de différents critères.")
    
    # Filtre par année
    years = sorted(df['model_year'].dropna().unique())
    selected_year = st.sidebar.selectbox("Choisir une année modèle", years)
    df_filtered = df[df['model_year'] == selected_year]

    st.subheader(f"Données pour l’année modèle {selected_year}")

    # KPI's
    def metrics():
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Nombre de véhicules", df_filtered['model'].count(), delta=None, delta_color="normal") 
        col2.metric("Nombre de modèles", df_filtered['model'].nunique(), delta=None, delta_color="normal")
        col3.metric("Nombre de marques", df_filtered['make'].nunique(), delta=None, delta_color="normal")
        
        style_metric_cards(background_color="#121270", border_left_color= "#f20045",  box_shadow="3px")

    metrics()

    # Top 10 Marques
    top_marques = df_filtered['make'].value_counts().nlargest(10).reset_index()
    top_marques.columns = ['marque', 'count']  # Renomme les colonnes pour plus de clarté

    fig_marques = px.bar(
        top_marques,
        x='marque',
        y='count',
        labels={'marque': 'Marque', 'count': 'Nombre'},
        title='Top 10 Marques de VE'
    )
    st.plotly_chart(fig_marques)
    
    # Type de VE
    type_counts = df_filtered['electric_vehicle_type'].value_counts().reset_index()
    type_counts.columns = ['type', 'count']

    fig_types = px.pie(
        type_counts,
        names='type',
        values='count',
        title='Répartition par Type de Véhicule'
    )
    st.plotly_chart(fig_types)
    
    
#profils véhicules 

if selected == "Profils VéhiculesVE":
    st.markdown("🔎 Profil des Véhicules Électriques")

    # -- Filtres dynamiques
    st.sidebar.header("🎛️ Filtres")
    marques = st.sidebar.multiselect("Marque", sorted(df['make'].dropna().unique()), default=None)
    modeles = st.sidebar.multiselect("Modèle", sorted(df['model'].dropna().unique()), default=None)
    annees = st.sidebar.multiselect("Année modèle", sorted(df['model_year'].dropna().unique()), default=None)
    types = st.sidebar.multiselect("Type de VE", df['electric_vehicle_type'].dropna().unique(), default=None)

    # -- Application des filtres
    df_filtered = df.copy()
    if marques:
        df_filtered = df_filtered[df_filtered['make'].isin(marques)]
    if modeles:
        df_filtered = df_filtered[df_filtered['model'].isin(modeles)]
    if annees:
        df_filtered = df_filtered[df_filtered['model_year'].isin(annees)]
    if types:
        df_filtered = df_filtered[df_filtered['electric_vehicle_type'].isin(types)]

    st.subheader(f"Résultats pour {len(df_filtered)} véhicules")

    # -- Boxplot de l'autonomie
    if not df_filtered.empty:
        fig_box = px.box(df_filtered, x="make", y="electric_range", points="all", title="Autonomie par Marque")
        st.plotly_chart(fig_box)

        # -- Prix moyen par modèle (si dispo)
        if 'base_msrp' in df_filtered.columns and df_filtered['base_msrp'].notna().sum() > 0:
            prix_par_modele = df_filtered[df_filtered['base_msrp'] > 0].groupby('model')['base_msrp'].mean().reset_index()
            fig_prix = px.bar(prix_par_modele.sort_values(by="base_msrp", ascending=False),
                            x='model', y='base_msrp',
                            title="Prix moyen par modèle",
                            labels={"base_msrp": "Prix moyen (USD)", "model": "Modèle"})
            st.plotly_chart(fig_prix)

        # -- Histogramme de l'autonomie
        fig_hist = px.histogram(df_filtered, x='electric_range', nbins=30,
                                title="Répartition des autonomies",
                                labels={"electric_range": "Autonomie (km)"})
        st.plotly_chart(fig_hist)
        
        # -- Bouton de génération de rapport PDF
        if st.button("📄 Générer le rapport PDF"):
            with st.spinner("Génération du rapport..."):
                generate_pdf_report(df_filtered, fig_box,
                                    fig_prix if 'fig_prix' in locals() else None,
                                    fig_hist if 'fig_hist' in locals() else None)
                with open("rapport_ve.pdf", "rb") as f:
                    st.download_button("📥 Télécharger le rapport PDF",
                                       data=f,
                                       file_name="rapport_ve.pdf",
                                       mime="application/pdf")


    else:
        st.warning("Aucun véhicule ne correspond à ces filtres.")

# Page de recommandation
if selected == "Recommandation":
    st.subheader("🎯 Recommandations de modèles selon l’usage")

    usage = st.selectbox("Quel est votre besoin principal ?", [
        "Usage urbain (courts trajets, budget modéré)",
        "Longs trajets (grande autonomie)",
        "Usage polyvalent (bon compromis)",
        "Budget très limité"
    ])

    df_reco = df[df['electric_range'].notna() & (df['electric_range'] > 0)]
    reco = pd.DataFrame()  # pour éviter erreur

    if usage == "Usage urbain (courts trajets, budget modéré)":
        reco = df_reco[df_reco['electric_range'] < 200].sort_values(by='electric_range').head(5)

    elif usage == "Longs trajets (grande autonomie)":
        reco = df_reco[df_reco['electric_range'] > 350].sort_values(by='electric_range', ascending=False).head(5)

    elif usage == "Usage polyvalent (bon compromis)":
        reco = df_reco[df_reco['electric_range'].between(250, 350)].sort_values(by='electric_range', ascending=False).head(5)

    elif usage == "Budget très limité":
        df_prix = df[df['base_msrp'].notna() & (df['base_msrp'] > 0)]
        reco = df_prix.sort_values(by='base_msrp').head(5)

    # affichage des résultats
    if not reco.empty:
        colonnes_affichage = ['make', 'model', 'model_year', 'electric_range']
        if 'base_msrp' in reco.columns and reco['base_msrp'].notna().sum() > 0:
            colonnes_affichage.append('base_msrp')

        st.markdown("### 🔍 Modèles recommandés :")
        st.dataframe(reco[colonnes_affichage])
    else:
        st.warning("Aucun modèle ne correspond aux critères.")

## Auteur
if selected == "Accueil":
    ...
    st.markdown("---")
    st.markdown("**👤 Auteur :** Nazifou AFOLABI")
    st.markdown("Profil : [LinkedIn](https://www.linkedin.com/in/nazifou-afolabi-10544729b/)")
    st.markdown("📧 Pour toute remarque ou suggestion : [me contacter](mailto:nazif@exemple.com)")


# Footer
st.markdown("---")
st.markdown(" Analyse du Marché des Véhicules Électriques - 2025")




