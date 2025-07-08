import streamlit as st
import pandas as pd
import plotly.express as px

# Chargement des données
df = pd.read_csv("df_total_final.csv")

st.title("Analyse de la Popularité - Statistiques FFA")

# Préparation des filtres
annees = sorted(df['année'].dropna().unique())
disciplines = sorted(df['discipline'].dropna().unique())
clubs = sorted(df['club'].dropna().unique())

# -------------------------------------------
# 1. PARTICIPATION PAR ANNÉE ET DISCIPLINE
# -------------------------------------------
st.header("1. Participation par année et discipline")

selected_disciplines = st.multiselect("Choisir une ou plusieurs disciplines", disciplines, default=disciplines[:3])

df_filtered = df[df['discipline'].isin(selected_disciplines)]
df_grouped = df_filtered.groupby(['année', 'discipline'])['licenciés'].sum().reset_index()

fig1 = px.line(df_grouped, x="année", y="licenciés", color="discipline", markers=True,
               title="Participation par année et discipline")
st.plotly_chart(fig1, use_container_width=True)

# -------------------------------------------
# 2. COMPARAISON POST-COVID ET CYCLES JO
# -------------------------------------------
st.header("2. Impact du COVID et des Jeux Olympiques")

st.markdown("""
Les années de référence sont :
- **2020** : COVID
- **2021** : JO Tokyo (reportés)
- **2024** : JO Paris
""")

df_agg = df.groupby("année")["licenciés"].sum().reset_index()
fig2 = px.bar(df_agg, x="année", y="licenciés", title="Évolution globale du nombre de licenciés")

# Ajout de repères COVID / JO
fig2.add_vline(x=2020, line_dash="dash", line_color="red", annotation_text="COVID", annotation_position="top left")
fig2.add_vline(x=2021, line_dash="dot", line_color="blue", annotation_text="JO Tokyo")
fig2.add_vline(x=2024, line_dash="dot", line_color="green", annotation_text="JO Paris")

st.plotly_chart(fig2, use_container_width=True)

# -------------------------------------------
# 3. TOP 20 CLUBS EN PARTICIPATION
# -------------------------------------------
st.header("3. Top 20 clubs moteurs")

df_clubs = df.groupby("club")["licenciés"].sum().reset_index().sort_values(by="licenciés", ascending=False).head(20)
fig3 = px.bar(df_clubs, x="licenciés", y="club", orientation="h",
              title="Top 20 des clubs en nombre de licenciés", height=600)
st.plotly_chart(fig3, use_container_width=True)

# -------------------------------------------
# 4. FOCUS CLUBS ÉLITE A
# -------------------------------------------
st.header("4. Clubs Élite A")

# Filtrer les clubs Élite A (tu peux ajuster selon ta colonne exacte)
df_elite = df[df['label'] == "Élite A"]

if df_elite.empty:
    st.warning("Aucun club 'Élite A' trouvé dans les données.")
else:
    df_elite_agg = df_elite.groupby("club")["licenciés"].sum().reset_index().sort_values(by="licenciés", ascending=False)

    fig4 = px.bar(df_elite_agg, x="licenciés", y="club", orientation="h",
                  title="Clubs Élite A - Nombre total de licenciés", height=600)
    st.plotly_chart(fig4, use_container_width=True)

    # Lien externe vers classement FFA (à modifier selon besoin réel)
    st.markdown("[Voir classement FFA](https://www.athle.fr/asp.net/main.html/html.aspx?htmlid=2935)")

