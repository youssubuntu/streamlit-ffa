import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Statistiques FFA", layout="wide")

# Chargement du fichier parquet
df = pd.read_parquet("df_total_final.parquet")

# Sidebar - Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Aller à :", [
    "🏃 Participation par année et discipline",
    "📊 Impact COVID / JO",
    "🏅 Top 20 clubs",
    "⭐ Clubs Élite A"
])

# Filtres dans la sidebar
st.sidebar.markdown("---")
st.sidebar.subheader("Filtres")

annees = sorted(df['annee'].dropna().unique())
disciplines = sorted(df['discipline'].dropna().unique())
clubs = sorted(df['club'].dropna().unique())

selected_years = st.sidebar.multiselect("Années", annees, default=annees)
selected_disciplines = st.sidebar.multiselect("Disciplines", disciplines, default=disciplines)
selected_clubs = st.sidebar.multiselect("Clubs", clubs, default=clubs)

# Filtrage
df_filtered = df[
    df['annee'].isin(selected_years) &
    df['discipline'].isin(selected_disciplines) &
    df['club'].isin(selected_clubs)
]

# Page 1 : Participation
if page == "🏃 Participation par année et discipline":
    st.title("Participation par année et discipline")
    df_grouped = df_filtered.groupby(['annee', 'discipline']).size().reset_index(name="participations")
    fig1 = px.line(df_grouped, x="annee", y="participations", color="discipline", markers=True)
    st.plotly_chart(fig1, use_container_width=True)

# Page 2 : COVID et JO
elif page == "📊 Impact COVID / JO":
    st.title("Impact du COVID et des Jeux Olympiques")
    st.markdown("""
    Années clés :
    - **2020** : COVID
    - **2021** : JO Tokyo
    - **2024** : JO Paris
    """)
    df_total = df.groupby("annee").size().reset_index(name="participations")
    fig2 = px.bar(df_total, x="annee", y="participations", title="Évolution du nombre de performances")
    fig2.add_vline(x=2020, line_dash="dash", line_color="red", annotation_text="COVID")
    fig2.add_vline(x=2021, line_dash="dot", line_color="blue", annotation_text="JO Tokyo")
    fig2.add_vline(x=2024, line_dash="dot", line_color="green", annotation_text="JO Paris")
    st.plotly_chart(fig2, use_container_width=True)

# Page 3 : Top clubs
elif page == "🏅 Top 20 clubs":
    st.title("Top 20 des clubs moteurs")
    df_clubs = df_filtered.groupby("club").size().reset_index(name="participations")
    df_top20 = df_clubs.sort_values(by="participations", ascending=False).head(20)
    fig3 = px.bar(df_top20, x="participations", y="club", orientation="h", height=600)
    st.plotly_chart(fig3, use_container_width=True)

# Page 4 : Clubs Élite A (s'il y en a)
elif page == "⭐ Clubs Élite A":
    st.title("Clubs labellisés Élite A")
    if 'label' not in df.columns:
        st.warning("Aucune colonne 'label' dans les données.")
    else:
        df_elite = df_filtered[df_filtered['label'] == "Élite A"]
        if df_elite.empty:
            st.warning("Aucun club 'Élite A' trouvé avec les filtres actuels.")
        else:
            df_elite_count = df_elite.groupby("club").size().reset_index(name="participations")
            fig4 = px.bar(df_elite_count.sort_values(by="participations", ascending=False),
                          x="participations", y="club", orientation="h", height=600)
            st.plotly_chart(fig4, use_container_width=True)
