import httpx
import ijson
import llm
import os
import urllib.parse


SAFETY_SETTINGS = [
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
]


@llm.hookimpl
def register_models(register):
    register(VertexAI("gemini-1.5-flash-preview-0514"))
    register(VertexAI("gemini-1.5-pro-preview-0514"))
    register(VertexAI("gemini-1.0-pro"))


class VertexAI(llm.Model):
    can_stream = True

    def __init__(self, model_id):
        self.model_id = model_id
        self.location = os.environ.get("LLM_VERTEX_LOCATION", "us-central1")
        self.project_id = os.environ.get("LLM_VERTEX_PROJECT_ID")

    def build_messages(self, prompt, conversation):
        if not conversation:
            return [{"role": "user", "parts": [{"text": prompt.prompt}]}]
        messages = []
        for response in conversation.responses:
            messages.append(
                {"role": "user", "parts": [{"text": response.prompt.prompt}]}
            )
            messages.append({"role": "model", "parts": [{"text": response.text()}]})
        messages.append({"role": "user", "parts": [{"text": prompt.prompt}]})
        return messages

    def execute(self, prompt, stream, response, conversation):
        access_token = llm.get_key("", "vertex", "VERTEX_ACCESS_TOKEN")
        url = "https://{LOCATION}-aiplatform.googleapis.com/v1/projects/{PROJECT_ID}/locations/{LOCATION}/publishers/google/models/{MODEL_ID}:streamGenerateContent".format(
            MODEL_ID=self.model_id,
            LOCATION=self.location,
            PROJECT_ID=self.project_id
        )
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        gathered = []
        body = {
            "contents": self.build_messages(prompt, conversation),
            "safetySettings": SAFETY_SETTINGS,
        }
        if prompt.system:
            body["system_instructions"] = {"parts": [{"text": prompt.system}]}
        with httpx.stream(
            "POST",
            url,
            headers=headers,
            timeout=None,
            json=body,
        ) as http_response:
            events = ijson.sendable_list()
            coro = ijson.items_coro(events, "item")
            for chunk in http_response.iter_bytes():
                coro.send(chunk)
                if events:
                    event = events[0]
                    if isinstance(event, dict) and "error" in event:
                        raise llm.ModelError(event["error"]["message"])
                    try:
                        yield event["candidates"][0]["content"]["parts"][0]["text"]
                    except KeyError:
                        yield ""
                    gathered.append(event)
                    events.clear()
        response.response_json = gathered
