class TextConfig:
    """Configuration for text processing"""
    
    SYSTEM_PROMPT = """You are Granite Chat, created by IBM. You're designed to assist with information and answer questions. 
    You don't have feelings or emotions, so you don't experience happiness or sadness. 
    You're here to help make the user's day more productive or enjoyable. 
    Always respond in a helpful and informative manner. 
    Provide a single, concise response to each query without continuing the conversation. 
    Do not add 'Human:' or any other conversation continuation at the end of your response."""

    DEFAULT_PARAMS = {
        "temperature": 0.7,
        "top_p": 1.0,
        "top_k": 50,
        "max_new_tokens": 100,
        "min_new_tokens": 1,
        "repetition_penalty": 1.0,
        "random_seed": 42,
        "stop_sequences": ["Human:", "AI:"]
    }

    # Parameter validation rules
    PARAM_RULES = {
        "temperature": {
            "min": 0.0,
            "max": 2.0,
            "description": "Controls randomness in the output (0.0 = deterministic, 2.0 = very creative)"
        },
        "top_p": {
            "min": 0.0,
            "max": 1.0,
            "description": "Nucleus sampling: controls diversity via cumulative probability"
        },
        "top_k": {
            "min": 1,
            "max": 100,
            "description": "Controls diversity by limiting to k most likely tokens"
        },
        "max_new_tokens": {
            "min": 1,
            "max": 2048,
            "description": "Maximum number of tokens to generate"
        },
        "min_new_tokens": {
            "min": 0,
            "max": 2048,
            "description": "Minimum number of tokens to generate"
        },
        "repetition_penalty": {
            "min": 1.0,
            "max": 2.0,
            "description": "Penalizes repetition in generated text"
        }
    }

    @classmethod
    def get_param_rule(cls, param_name: str) -> dict:
        """Get validation rules for a parameter"""
        return cls.PARAM_RULES.get(param_name, {})

    @classmethod
    def get_param_description(cls, param_name: str) -> str:
        """Get parameter description for tooltips/help"""
        rule = cls.get_param_rule(param_name)
        return rule.get('description', '')
