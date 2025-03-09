"""
Sample response data for testing backend services.
These fixtures provide consistent test data for unit and integration tests.
"""

# Sample model service responses
MODELS_RESPONSE = {
    "resources": [
        {
            "model_id": "ibm/granite-20b-multilingual",
            "name": "Granite 20B Multilingual",
            "type": "foundation_model",
            "description": "IBM Granite 20B Multilingual model"
        },
        {
            "model_id": "ibm/mpt-7b-instruct",
            "name": "MPT 7B Instruct",
            "type": "foundation_model",
            "description": "MPT 7B Instruct model"
        },
        {
            "model_id": "ibm/custom-model",
            "name": "Custom Model",
            "type": "custom_model",
            "description": "Custom fine-tuned model"
        }
    ]
}

MODEL_DETAIL_RESPONSE = {
    "model_id": "ibm/granite-20b-multilingual",
    "name": "Granite 20B Multilingual",
    "type": "foundation_model",
    "description": "IBM Granite 20B Multilingual model",
    "parameters": {
        "max_tokens": 2048,
        "temperature": 0.7,
        "top_p": 1.0,
        "top_k": 50
    }
}

# Sample text service responses
TEXT_GENERATION_RESPONSE = {
    "generated_text": "This is a sample generated text response from the model. It demonstrates the format of text generation API responses.",
    "model_id": "ibm/granite-20b-multilingual",
    "created_at": "2023-07-15T10:30:45Z",
    "metadata": {
        "token_count": 24,
        "processing_time": 0.856
    }
}

# Sample NLU service responses
NLU_ANALYSIS_RESPONSE = {
    "sentiment": {
        "document": {
            "score": 0.8,
            "label": "positive"
        }
    },
    "entities": [
        {
            "type": "Person",
            "text": "John Doe",
            "relevance": 0.9
        },
        {
            "type": "Organization",
            "text": "IBM",
            "relevance": 0.85
        }
    ],
    "keywords": [
        {
            "text": "artificial intelligence",
            "relevance": 0.95
        },
        {
            "text": "machine learning",
            "relevance": 0.9
        }
    ]
}

# Sample project service responses
PROJECTS_RESPONSE = {
    "resources": [
        {
            "project_id": "123e4567-e89b-12d3-a456-426614174000",
            "name": "Test Project 1",
            "description": "A test project for unit testing",
            "created_at": "2023-07-10T08:15:30Z"
        },
        {
            "project_id": "223e4567-e89b-12d3-a456-426614174001",
            "name": "Test Project 2",
            "description": "Another test project",
            "created_at": "2023-07-11T09:20:35Z"
        }
    ]
}

PROJECT_DETAIL_RESPONSE = {
    "project_id": "123e4567-e89b-12d3-a456-426614174000",
    "name": "Test Project 1",
    "description": "A test project for unit testing",
    "created_at": "2023-07-10T08:15:30Z",
    "models": [
        "ibm/granite-20b-multilingual",
        "ibm/mpt-7b-instruct"
    ],
    "settings": {
        "default_model": "ibm/granite-20b-multilingual"
    }
}

# Sample STT service responses
STT_RESPONSE = {
    "results": [
        {
            "alternatives": [
                {
                    "transcript": "This is a sample transcription of speech to text.",
                    "confidence": 0.95
                }
            ],
            "final": True
        }
    ],
    "result_index": 0
}

# Sample TTS service responses
SAMPLE_AUDIO_BINARY = b'mock audio data for testing' 
TTS_RESPONSE = {
    "audio_length": 3.5,
    "characters": 42,
    "warnings": []
}

# Sample IAM token response
IAM_TOKEN_RESPONSE = {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "SPrXw5tBE3kS5...",
    "token_type": "Bearer",
    "expires_in": 3600,
    "expiration": 1625097600
} 