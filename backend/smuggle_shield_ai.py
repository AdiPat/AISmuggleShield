from llm import LLM, LLMOptions, GenerateOptions
from pydantic import BaseModel
import json


class DetectedPatterns(BaseModel):
    pattern: str
    confidence: float


class AnalyzePageRequest(BaseModel):
    detected_patterns: list[DetectedPatterns]


class AnalyzeHeadersRequest(BaseModel):
    detected_patterns: list[DetectedPatterns]
    headers: dict


class SmuggleShieldAI(LLM):

    def __init__(self, options: LLMOptions = None):
        super().__init__(options=options)

    def get_page_chunks(self, page_source: str, chunk_size=1024) -> list[str]:
        if not page_source:
            return []

        if len(page_source) < chunk_size:
            return [page_source]

        return [
            page_source[i : i + chunk_size]
            for i in range(0, len(page_source), chunk_size)
        ]

    def analyze_page(self, page_source: str) -> dict:
        chunks = self.get_page_chunks(page_source)

        all_detected_patterns = []

        for chunk in chunks:
            result = self.generate_object(
                options=GenerateOptions(
                    system_prompt="You are an AI security agent that detects if HTML smuggling is active on a page. You have to detect patterns and report them. ",
                    prompt=f"Page Source: {chunk}",
                    response_schema=AnalyzePageRequest,
                    verbose=False,
                )
            )
            all_detected_patterns.extend(result.detected_patterns)

        return {"detected_patterns": all_detected_patterns, "page_source": page_source}

    def analyze_headers(self, headers: dict) -> dict:
        headers_json = json.dumps(headers)
        result = self.generate_object(
            options=GenerateOptions(
                system_prompt="You are an AI security agent that detects if HTML smuggling is active in headers. You have to detect patterns and report them. ",
                prompt=f"Headers: {headers_json}",
                response_schema=AnalyzeHeadersRequest,
                verbose=False,
            )
        )
        return {"result": result, "headers": headers}
