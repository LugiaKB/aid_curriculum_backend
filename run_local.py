from app.integrations.gemini.service import GeminiService
from app.schemas.cv import CVRequest


def main():
    # Perguntar qual exemplo executar
    print("Escolha o exemplo para executar:")
    print("1 - CV sem vaga específica")
    print("2 - CV com análise de compatibilidade para vaga")
    choice = input("Digite 1 ou 2: ")

    # Example input data
    example_cv = CVRequest(
        full_name="Maria Silva Santos",
        desired_role="Desenvolvedora Full Stack",
        email="mariasilva@email.com",
        phone="11987654321",
        professional_experience="""
        Tô trabalhando como dev fullstack faz uns 3 anos já. Comecei na área como estagiária
        numa empresa chamada WebSolutions, fiquei 6 meses lá mexendo só com frontend. Foi bem legal
        porque aprendi bastante sobre React e como fazer interfaces bonitas e funcionais.
        
        Depois fui pra uma startup, a InovaTech, já como júnior. Lá eu fazia de tudo um pouco,
        sabe como é startup né? Acabei aprendendo muito de backend também, principalmente Node e
        MongoDB. Fiquei um ano lá, a gente tinha uma equipe pequena mas bem unida.
        
        Agora tô na TechBR desde 2022, é meu emprego atual. Aqui é mais estruturado, trabalho
        principalmente com Python e React. Tenho ajudado bastante o time com a parte de AI também,
        já que tô estudando isso na pós. Ah, e comecei a liderar alguns projetos menores
        recentemente, tá sendo uma experiência bem bacana!
        """,
        education="""
        Fiz Ciência da Computação na UFMG, me formei em 2021. Antes disso tinha feito 
        técnico em informática no CEFET, que foi onde me apaixonei por programação na verdade.
        
        Agora tô fazendo uma pós em Inteligência Artificial na USP EAD, comecei esse ano
        e tô curtindo muito! Já fiz alguns projetos legais com machine learning.
        """,
        skills="""
        De tecnologia eu mando bem em Python e JavaScript, são minhas principais linguagens.
        Trabalho bastante com React no frontend e tenho uma boa experiência com Node.
        Banco de dados eu já mexi com vários, mas uso mais SQL e MongoDB mesmo.
        
        Ultimamente tô estudando muito a parte de IA e machine learning, já fiz alguns 
        projetos legais na pós e até implementei umas coisas no trabalho.
        
        Sei me virar bem com Git, sempre organizo direito meus commits e tal.
        Gosto de trabalhar com método ágil, acho que ajuda muito na organização.
        
        Ah, e meu inglês é fluente! Leio documentação, assisto conferência e até faço 
        umas calls com cliente gringo de vez em quando.
        """,
        projects="""
        Desenvolvi um app de lista de tarefas para Android usando React Native e Firebase (link no GitHub).
        Criei um modelo de classificação de imagens em Python usando TensorFlow e Keras como projeto de pós-graduação.
        """,
        target_job_description=(
            """
        Empresa busca Desenvolvedor(a) Full Stack Sênior para atuar em projetos inovadores
        na área de IA e desenvolvimento web.

        Requisitos:
        - Sólida experiência com Python e JavaScript
        - Conhecimento em frameworks React e Node.js
        - Experiência com bancos de dados SQL e NoSQL
        - Conhecimento em Machine Learning e IA
        - Experiência com metodologias ágeis
        - Inglês avançado para comunicação com equipe internacional
        - Desejável experiência com AWS e Docker
        
        Diferencias:
        - Experiência em liderança de equipes
        - Conhecimento em arquitetura de microsserviços
        - Familiaridade com Kubernetes
        """
            if choice == "2"
            else None
        ),
    )

    # Initialize the Gemini service
    gemini_service = GeminiService()

    # Generate the CV
    result = gemini_service.generate_cv(example_cv)

    # Print the generated CV
    print("\n=== Generated CV ===\n")
    import json

    content = result.get("cv_content", result.get("error", "Unknown error occurred"))
    print(json.dumps(content, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
