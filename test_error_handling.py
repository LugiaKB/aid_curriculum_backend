#!/usr/bin/env python3
"""
Script para testar o tratamento de erros da API de geração de currículos
"""

import requests
import json
from typing import Dict, Any

API_BASE_URL = "http://localhost:8000/api/v1"

def test_api_request(test_name: str, data: Dict[str, Any]) -> None:
    """
    Testa uma requisição na API e exibe o resultado
    """
    print(f"\n{'='*50}")
    print(f"TESTE: {test_name}")
    print(f"{'='*50}")
    
    try:
        response = requests.post(f"{API_BASE_URL}/generate-cv", json=data)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ SUCESSO - Currículo gerado!")
            result = response.json()
            print(f"Nome gerado: {result['generated_cv']['personal_info']['name']}")
        else:
            print("❌ ERRO - Problemas na validação:")
            error_data = response.json()
            print(f"Erro: {error_data.get('error', 'N/A')}")
            print(f"Mensagem: {error_data.get('message', 'N/A')}")
            
            if 'details' in error_data:
                print("Detalhes dos erros:")
                for i, detail in enumerate(error_data['details'], 1):
                    print(f"  {i}. {detail}")
    
    except requests.exceptions.ConnectionError:
        print("❌ ERRO: Não foi possível conectar à API. Certifique-se de que o servidor está rodando.")
    except Exception as e:
        print(f"❌ ERRO INESPERADO: {str(e)}")

def run_error_tests():
    """
    Executa uma série de testes para diferentes tipos de erro
    """
    print("🔍 INICIANDO TESTES DE TRATAMENTO DE ERROS")
    
    # Teste 1: Dados válidos (deve funcionar)
    test_api_request(
        "Dados válidos",
        {
            "full_name": "João Silva Santos",
            "desired_role": "Desenvolvedor Python",
            "email": "joao@gmail.com",
            "phone": "11987654321",
            "professional_experience": "Trabalho há 3 anos como desenvolvedor Python em uma startup de tecnologia, onde desenvolvo APIs RESTful e sistemas web.",
            "education": "Bacharel em Ciência da Computação pela USP, formado em 2021.",
            "skills": "Python, Django, PostgreSQL, Git, Docker, conhecimentos em AWS e metodologias ágeis."
        }
    )
    
    # Teste 2: Nome inválido (muito curto)
    test_api_request(
        "Nome muito curto",
        {
            "full_name": "João",
            "desired_role": "Desenvolvedor Python",
            "email": "joao@gmail.com",
            "phone": "11987654321",
            "professional_experience": "Trabalho há 3 anos como desenvolvedor Python em uma startup de tecnologia.",
            "education": "Bacharel em Ciência da Computação pela USP.",
            "skills": "Python, Django, PostgreSQL, Git."
        }
    )
    
    # Teste 3: Email inválido
    test_api_request(
        "Email inválido",
        {
            "full_name": "Maria Silva Santos",
            "desired_role": "Desenvolvedora Frontend",
            "email": "email_invalido",
            "phone": "11987654321",
            "professional_experience": "Experiência de 2 anos em desenvolvimento frontend com React e TypeScript.",
            "education": "Técnico em Informática pelo SENAI.",
            "skills": "React, TypeScript, HTML, CSS, JavaScript."
        }
    )
    
    # Teste 4: Telefone inválido
    test_api_request(
        "Telefone inválido",
        {
            "full_name": "Pedro Costa Lima",
            "desired_role": "Analista de Dados",
            "email": "pedro@yahoo.com",
            "phone": "123",
            "professional_experience": "Trabalho com análise de dados e business intelligence há 2 anos.",
            "education": "Graduação em Estatística pela UFMG.",
            "skills": "Python, SQL, Power BI, Excel, estatística."
        }
    )
    
    # Teste 5: Sem contato (sem email e sem telefone)
    test_api_request(
        "Sem informações de contato",
        {
            "full_name": "Ana Paula Souza",
            "desired_role": "Designer UX/UI",
            "professional_experience": "Experiência em design de interfaces e experiência do usuário.",
            "education": "Curso superior em Design Digital.",
            "skills": "Figma, Adobe XD, Photoshop, prototipagem."
        }
    )
    
    # Teste 6: Campos obrigatórios vazios
    test_api_request(
        "Campos obrigatórios vazios",
        {
            "full_name": "",
            "desired_role": "",
            "email": "teste@gmail.com",
            "professional_experience": "",
            "education": "",
            "skills": ""
        }
    )
    
    # Teste 7: Nome com números
    test_api_request(
        "Nome com números",
        {
            "full_name": "João123 Silva",
            "desired_role": "Desenvolvedor",
            "email": "joao@gmail.com",
            "phone": "11987654321",
            "professional_experience": "Experiência em desenvolvimento de software.",
            "education": "Formação em tecnologia.",
            "skills": "Programming languages and tools."
        }
    )

if __name__ == "__main__":
    run_error_tests()
    print(f"\n{'='*50}")
    print("🏁 TESTES CONCLUÍDOS")
    print("💡 Para testar interativamente, acesse: http://localhost:8000/docs")
    print(f"{'='*50}")
