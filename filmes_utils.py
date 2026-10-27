OPCAO_QUALQUER = "Qualquer"

def listar_generos(filmes):
    return [OPCAO_QUALQUER] + sorted(filmes['Genre'].unique().tolist())

def filtrar_por_genero(filmes, genero):
    if genero == OPCAO_QUALQUER:
        return filmes
    return filmes[filmes['Genre'] == genero]