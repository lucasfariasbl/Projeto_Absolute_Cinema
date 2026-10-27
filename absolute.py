import streamlit as st
import pandas as pd
import random
from filmes_utils import listar_generos, filtrar_por_genero 

# Configuração da página
st.set_page_config(
    page_title="Top Filmes IMDb",
    page_icon="🎬",
    layout="wide"
)

# Carregar os dados
@st.cache_data
def load_data():
    data = pd.read_csv('filmes.csv')
    return data

# Página principal
def main_page():
    st.title("🎬 Top Filmes IMDb")
    st.markdown("---")
    
    # Carregar dados
    df = load_data()
    
    # Filtros na sidebar
    st.sidebar.header("Filtros")
    
    # Filtro por gênero
    
    selected_genre = st.sidebar.selectbox(
        "Selecione um gênero:",
        listar_generos(df)
    )
    
    # Filtro por ano
    min_year = int(df['Year'].min())
    max_year = int(df['Year'].max())
    year_range = st.sidebar.slider(
        "Selecione o intervalo de anos:",
        min_year, max_year, (min_year, max_year)
    )
    
    # Filtro por nota
    min_rating = float(df['Rating'].min())
    max_rating = float(df['Rating'].max())
    rating_filter = st.sidebar.slider(
        "Nota mínima:",
        min_rating, max_rating, min_rating
    )
    
    # Aplicar filtros
    filtered_df = df.copy()
    
    filtered_df = filtrar_por_genero(filtered_df, selected_genre)
    
    filtered_df = filtered_df[
        (filtered_df['Year'] >= year_range[0]) & 
        (filtered_df['Year'] <= year_range[1]) &
        (filtered_df['Rating'] >= rating_filter)
    ]
    
    # Mostrar estatísticas
    st.sidebar.markdown("---")
    st.sidebar.metric("Filmes encontrados", len(filtered_df))
    st.sidebar.metric("Melhor nota", f"{filtered_df['Rating'].max():.1f}")
    
    # Layout dos filmes
    cols_per_row = 4
    films = filtered_df.to_dict('records')
    
    for i in range(0, len(films), cols_per_row):
        cols = st.columns(cols_per_row)
        
        for j, col in enumerate(cols):
            if i + j < len(films):
                film = films[i + j]
                
                with col:
                    # Card do filme
                    st.markdown(f"### #{film['Rank']} - {film['Title']} ({film['Year']})")
                    
                    # Imagem do filme
                    st.image(film['Image URL'], use_container_width=True)
                    
                    # Nota
                    st.markdown(f"**⭐ Nota: {film['Rating']}**")
                    st.markdown(f"**⏱️ Duração: {film['Duration']}**")
                    st.markdown(f"**🎭 Gênero: {film['Genre']}**")
                    
                    # Botão para mais informações
                    if st.button(f"Ver no IMDb", key=f"imdb_{film['Rank']}"):
                        st.markdown(f"[Abrir no IMDb]({film['IMDb URL']})")
                    
                    st.markdown("---")

# Página de sugestão de filme
def suggestion_page():
    st.title("🎲 Sugestão de Filme Aleatório")
    st.markdown("---")
    
    df = load_data()
    
    # Filtros para sugestão
    st.sidebar.header("Filtros para Sugestão")
    
    selected_genre_suggestion = st.sidebar.selectbox(
        "Selecione um gênero:",
        listar_generos(df),
        key="suggestion_genre"
    )
    
    min_year_suggestion = st.sidebar.number_input(
        "Ano mínimo:",
        min_value=int(df['Year'].min()),
        max_value=int(df['Year'].max()),
        value=1980
    )
    
    min_rating_suggestion = st.sidebar.slider(
        "Nota mínima:",
        min_value=float(df['Rating'].min()),
        max_value=float(df['Rating'].max()),
        value=8.0,
        key="suggestion_rating"
    )
    
    # Botão para gerar sugestão
    if st.button("🎯 Me sugira um filme!"):
        # Aplicar filtros
        filtered_suggestions = df.copy()
        
        filtered_suggestions = filtrar_por_genero(filtered_suggestions, selected_genre_suggestion)
        
        filtered_suggestions = filtered_suggestions[
            (filtered_suggestions['Year'] >= min_year_suggestion) &
            (filtered_suggestions['Rating'] >= min_rating_suggestion)
        ]
        
        if len(filtered_suggestions) > 0:
            # Selecionar filme aleatório
            random_film = filtered_suggestions.sample(1).iloc[0]
            
            # Mostrar sugestão
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.image(random_film['Image URL'], use_container_width=True)
            
            with col2:
                st.markdown(f"# 🎬 {random_film['Title']} ({random_film['Year']})")
                st.markdown(f"### ⭐ **Nota: {random_film['Rating']}**")
                st.markdown(f"### ⏱️ **Duração: {random_film['Duration']}**")
                st.markdown(f"### 🎭 **Gênero: {random_film['Genre']}**")
                st.markdown(f"### 🏆 **Posição no Ranking: #{random_film['Rank']}**")
                
                # Botão para ver no IMDb
                if st.button("🔗 Ver no IMDb", key="suggestion_imdb"):
                    st.markdown(f"[Abrir página do IMDb]({random_film['IMDb URL']})")
                
                st.info("💡 **Dica:** Não gostou da sugestão? Clique no botão novamente para uma nova recomendação!")
        
        else:
            st.warning("❌ Nenhum filme encontrado com os filtros selecionados. Tente ajustar os critérios.")

# Navegação
st.sidebar.title("Navegação")
page = st.sidebar.radio("Ir para:", ["🎬 Catálogo de Filmes", "🎲 Sugestão de Filme"])

if page == "🎬 Catálogo de Filmes":
    main_page()
else:
    suggestion_page()

# Rodapé
st.sidebar.markdown("---")
st.sidebar.markdown("### Sobre")
st.sidebar.info(
    "Este site mostra os top 250 filmes do IMDb. "
    "Os dados são atualizados regularmente."
)