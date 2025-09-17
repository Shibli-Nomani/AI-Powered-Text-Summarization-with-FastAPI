# models/summary_model.py
from langchain_groq import ChatGroq
from services.config import GROQ_API_KEY

summarymodel = ChatGroq(model="openai/gpt-oss-20b", groq_api_key=GROQ_API_KEY)


    #def summarize(self, text: str) -> str:
    #   """Generate summary for the transcript."""
    #   response = self.model.chat([{
    #       "role": "user",
    #       "content": f"Summarize the following text:\n{text}"
    #   }])
    #   return response["message"]["content"]
