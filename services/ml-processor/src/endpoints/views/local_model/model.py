from transformers import T5ForConditionalGeneration, T5Tokenizer
from endpoints.views.local_model.preprocessing import full_preprocessing
import torch
import numpy as np


class T5Model():
    def __init__(self):
        self.device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")

        self.summarizer = {
            'model': T5ForConditionalGeneration.from_pretrained('utrobinmv/t5_summary_en_ru_zh_large_2048'),
            'tokenizer': T5Tokenizer.from_pretrained('utrobinmv/t5_summary_en_ru_zh_large_2048')
        }

        self.summarizer['model'].eval()
        self.summarizer['model'].to(self.device)
        self.summarizer['model'].generation_config.length_penalty = 0.6
        self.summarizer['model'].generation_config.no_repeat_ngram_size = 2
        self.summarizer['model'].generation_config.num_beams = 10

    def get_embeddings(self, text):
        inputs = self.summarizer['tokenizer'](text, return_tensors="pt", max_length=1024, truncation=True)
        
        with torch.no_grad():
            outputs = self.summarizer['model'].encoder(**inputs.to(self.device))
            last_hidden_states = outputs.last_hidden_state
        
        text_embedding = last_hidden_states.mean(dim=1).squeeze()
        return text_embedding

    def summarize(self, texts, brief = False):
        src_text = 'summary' + (' brief: ' if brief else ': ') + "\n".join(texts)
        
        input_ids = self.summarizer['tokenizer'](src_text, return_tensors="pt")
        with torch.no_grad():
            generated_tokens = self.summarizer['model'].generate(**input_ids.to(self.device))
        
        combined_news = self.summarizer['tokenizer'].batch_decode(generated_tokens, skip_special_tokens=True)[0]
        combined_news += '.' if combined_news[-1] != '.' else ''
        return combined_news

    def news_processing(self, text):
        new_text = self.summarize([full_preprocessing(text)], True)
        embedding = self.get_embeddings(new_text)


