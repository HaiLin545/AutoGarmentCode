import os
import base64
import openai


class Agent:
    """Lightweight GPT-4o wrapper with image support."""

    def __init__(self):
        self.max_tokens = 4096
        self.model = "gpt-4o-2024-11-20"
        self.client = openai.OpenAI(
            api_key='sk-FJOtSwQcHzTLVLUqEf181cF66b264cBd84C092625702247d',
            base_url='https://api.laozhang.ai/v1',
        )

    @staticmethod
    def _encode_image(path: str) -> str:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")

    @staticmethod
    def _mime_type(path: str) -> str:
        ext = os.path.splitext(path)[1].lower().lstrip(".")
        mapping = {"jpg": "jpeg", "jpeg": "jpeg", "png": "png", "gif": "gif", "webp": "webp"}
        return mapping.get(ext, "jpeg")

    def call(
        self,
        system_prompt: str,
        user_content: str,
        image_path: str = None,
        temperature: float = 0.2,
    ) -> str:
        messages = [{"role": "system", "content": system_prompt}]

        if image_path:
            b64 = self._encode_image(image_path)
            mime = self._mime_type(image_path)
            messages.append({
                "role": "user",
                "content": [
                    {"type": "text", "text": user_content},
                    {"type": "image_url", "image_url": {
                        "url": f"data:image/{mime};base64,{b64}"
                    }},
                ],
            })
        else:
            messages.append({"role": "user", "content": user_content})

        resp = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=self.max_tokens,
            temperature=temperature,
        )
        return resp.choices[0].message.content
