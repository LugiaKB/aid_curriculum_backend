# Gerador de Currículos API

Uma aplicação FastAPI que gera currículos profissionais utilizando a IA Gemini do Google.

## Configuração

1. Instale o pipenv se ainda não tiver instalado:
```bash
pip install pipenv
```

2. Copie o arquivo `.env.example` para `.env` e adicione sua chave de API do Google:
```bash
GOOGLE_API_KEY=sua_chave_api_aqui
```

3. Instale as dependências:
```bash
pipenv install
```

4. Execute a aplicação:

Para iniciar o servidor da API:
```bash
pipenv run api
```
A API estará disponível em `http://localhost:8000`

Para testar a geração de currículos localmente com dados de exemplo:
```bash
pipenv run generate
```

## Uso da API

Envie uma requisição POST para `/api/v1/generate-cv` com a seguinte estrutura JSON:

```json
{
  "full_name": "Maria Silva Santos",
  "desired_role": "Desenvolvedora Full Stack",
  "email": "mariasilva@email.com",
  "phone": "11987654321",
  "professional_experience": "Experiência como desenvolvedora...",
  "education": "Formação acadêmica...",
  "skills": "Habilidades técnicas e soft skills...",
  "target_job_description": "Descrição da vaga desejada (opcional)"
}
```

## Documentação da API

Depois que o servidor estiver rodando, você pode acessar:
- Documentação Swagger UI em: `http://localhost:8000/docs`
- Documentação ReDoc em: `http://localhost:8000/redoc`

## Exemplo de Resposta

A API retorna um JSON contendo:
- Currículo gerado em formato estruturado
- Análise de compatibilidade com a vaga (quando fornecida)
- Sugestões de melhorias
- Recursos de aprendizado recomendados

## Testes automatizados do tratamento de erro

1. Swagger UI: http://localhost:8000/docs
2. Rodar pipenv run python test_error_handling.py
