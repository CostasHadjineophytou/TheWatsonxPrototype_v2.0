"""Sample responses for logic layer tests"""

# Sample text processing result
TTS_RESULT = {
    'original': 'Sample input text',
    'processed': 'Processed sample text',
    'metadata': {
        'word_count': 3,
        'language': 'en',
        'processing_time': 0.15
    }
}

# Sample NLU analysis result
NLU_ANALYSIS_RESULT = {
    'text': 'Sample text for analysis',
    'sentiment': {
        'document': {
            'label': 'positive',
            'score': 0.8
        }
    },
    'entities': [
        {
            'text': 'John',
            'type': 'PERSON',
            'confidence': 0.95,
            'relevance': 0.8
        }
    ],
    'keywords': [
        {
            'text': 'sample',
            'relevance': 0.8,
            'count': 1
        }
    ]
}

# Sample project data
PROJECT_DATA = {
    'id': 'test_project_123',
    'name': 'Test Project',
    'description': 'A test project for unit tests',
    'created_at': '2024-02-26T00:00:00Z',
    'settings': {
        'language': 'en',
        'model': 'default'
    }
}

# Sample model configuration
MODEL_CONFIG = {
    'name': 'test_model',
    'type': 'text-generation',
    'parameters': {
        'temperature': 0.7,
        'max_tokens': 100
    }
} 