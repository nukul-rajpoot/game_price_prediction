from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import re
import numpy as np

class FinBERTSentimentAnalyzer:
    def __init__(self):
        # Initialize tokenizer and model
        self.tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
        self.model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")
        
        # Move model to GPU if available
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = self.model.to(self.device)
        
        # Labels for FinBERT
        self.labels = ['negative', 'neutral', 'positive']

    def preprocess_reddit_text(self, text):
        """
        Preprocess Reddit text data
        """
        # Convert to lowercase
        text = text.lower()
        
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text)
        
        # Remove Reddit-style references like u/ and r/
        text = re.sub(r'[ru]/[A-Za-z0-9_-]+', '', text)
        
        # Remove special characters and extra whitespace
        text = re.sub(r'[^\w\s]', ' ', text)
        text = ' '.join(text.split())
        
        # Remove numbers (optional, comment out if you want to keep numbers)
        # text = re.sub(r'\d+', '', text)
        
        return text

    def get_sentiment(self, text, batch_size=32):
        """
        Get sentiment scores for preprocessed text
        """
        # Preprocess the text
        processed_text = self.preprocess_reddit_text(text)
        
        # Tokenize with explicit clean_up_tokenization_spaces parameter
        inputs = self.tokenizer(processed_text, 
                              return_tensors="pt",
                              truncation=True,
                              max_length=512,
                              padding=True,
                              clean_up_tokenization_spaces=True)
        
        # Move inputs to GPU
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        # Get model outputs
        with torch.no_grad():
            outputs = self.model(**inputs)
            scores = torch.nn.functional.softmax(outputs.logits, dim=1)
            
        # Convert to numpy for easier handling
        scores = scores.cpu().numpy()[0]
        
        # Create dictionary with sentiment scores
        sentiment_dict = {
            label: float(score) 
            for label, score in zip(self.labels, scores)
        }
        
        # Get predicted sentiment
        predicted_sentiment = self.labels[np.argmax(scores)]
        
        return {
            'sentiment': predicted_sentiment,
            'scores': sentiment_dict,
            'processed_text': processed_text
        }

# Example usage
if __name__ == "__main__":
    # Initialize analyzer
    analyzer = FinBERTSentimentAnalyzer()
    
    # Example Reddit text
    reddit_text = """
    golden coil is a steal right now!
    """
    
    # Get sentiment
    result = analyzer.get_sentiment(reddit_text)
    
    # Print results
    print(f"Original text: {reddit_text}")
    print(f"Processed text: {result['processed_text']}")
    print(f"Predicted sentiment: {result['sentiment']}")
    print(f"Sentiment scores: {result['scores']}")
