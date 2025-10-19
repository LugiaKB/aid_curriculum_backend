import os
import json
from google import genai
from google.genai import types
from google.genai.errors import APIError


class GeminiClient:
    def __init__(self, model: str = "gemini-2.5-flash"):

        try:
            api_key = os.getenv("GOOGLE_API_KEY")
            if not api_key:
                raise ValueError(
                    "GOOGLE_API_KEY não encontrada nas variáveis de ambiente."
                )
            if not api_key:
                raise ValueError(
                    "GEMINI_API_KEY não encontrado nas variáveis de ambiente."
                )
            self.client = genai.Client(api_key=api_key)
            self.model = model

        except Exception as e:

            print(f"Erro ao inicializar o Gemini Client: {e}")
            self.client = None
            raise

    def _clean_schema(self, schema: dict) -> dict:
        """Remove additionalProperties from the schema recursively"""
        if not isinstance(schema, dict):
            return schema

        cleaned = {}
        for key, value in schema.items():
            if key == "additionalProperties":
                continue
            elif isinstance(value, dict):
                cleaned[key] = self._clean_schema(value)
            elif isinstance(value, list):
                cleaned[key] = [
                    self._clean_schema(item) if isinstance(item, dict) else item
                    for item in value
                ]
            else:
                cleaned[key] = value
        return cleaned

    def generate_json_response(
        self, prompt: str, system_instruction: str, json_schema: dict
    ) -> dict:
        if not self.client:
            return {"status": "error", "message": "Client não está inicializado."}

        # Clean the schema before sending to Gemini
        clean_schema = self._clean_schema(json_schema)

        config = types.GenerateContentConfig(
            system_instruction=system_instruction,
            response_mime_type="application/json",
            response_schema=json_schema,
        )

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    response_mime_type="application/json",
                    response_schema=clean_schema,
                ),
            )

            if response.text:
                return json.loads(response.text)
            else:
                return {
                    "status": "error",
                    "message": "Resposta vazia da API do Gemini.",
                }

        except APIError as e:

            return {"status": "error", "message": f"Erro na API do Gemini: {e}"}

        except json.JSONDecodeError:

            return {
                "status": "error",
                "message": "Falha ao processar o JSON retornado pela LLM.",
            }

        except Exception as e:

            return {
                "status": "error",
                "message": f"Erro inesperado no cliente Gemini: {e}",
            }
