from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class NLUFeature:
    """NLU feature configuration"""
    id: str              # API identifier
    display_name: str    # UI display name
    description: str     # Help text
    default_params: Dict[str, Any] = None  # Default API parameters

class NLUConfig:
    """NLU service configuration"""
    
    FEATURES = {
        'sentiment': NLUFeature(
            id='sentiment',
            display_name='Sentiment',
            description='Analyze the overall sentiment (positive/negative) of the text',
            default_params={'document': True}
        ),
        'emotion': NLUFeature(
            id='emotion',
            display_name='Emotion',
            description='Detect emotions (joy, sadness, anger, etc.) in the text',
            default_params={'document': True}
        ),
        'entities': NLUFeature(
            id='entities',
            display_name='Entities',
            description='Identify people, companies, organizations, and other entities',
            default_params={
                'sentiment': True,
                'emotion': False,
                'limit': 50
            }
        ),
        'keywords': NLUFeature(
            id='keywords',
            display_name='Keywords',
            description='Extract important keywords from the text',
            default_params={
                'sentiment': True,
                'emotion': False,
                'limit': 50
            }
        ),
        'categories': NLUFeature(
            id='categories',
            display_name='Categories',
            description='Categorize the text into predefined categories',
            default_params={
                'explanation': False,
                'limit': 10
            }
        ),
        'concepts': NLUFeature(
            id='concepts',
            display_name='Concepts',
            description='Identify high-level concepts and related concepts',
            default_params={
                'limit': 50
            }
        ),
        'relations': NLUFeature(
            id='relations',
            display_name='Relations',
            description='Find relationships between entities in the text',
            default_params={
                'model': 'en-news'
            }
        ),
        'semantic_roles': NLUFeature(
            id='semantic_roles',
            display_name='Semantic Roles',
            description='Identify subject, action, and object in sentences',
            default_params={
                'limit': 50,
                'keywords': True,
                'entities': True
            }
        )
    }

    @classmethod
    def get_feature_ids(cls) -> list:
        """Get list of feature IDs for API"""
        return list(cls.FEATURES.keys())

    @classmethod
    def get_ui_features(cls) -> list:
        """Get feature tuples for UI (display_name, id) for UI components"""
        return [
            (f.display_name, f.id) 
            for f in cls.FEATURES.values()
        ]

    @classmethod
    def get_feature_params(cls, feature_id: str) -> dict:
        """Get default parameters for feature"""
        return cls.FEATURES[feature_id].default_params.copy()

    @classmethod
    def get_feature_description(cls, feature_id: str) -> str:
        """Get feature description for tooltips/help"""
        return cls.FEATURES[feature_id].description

    @classmethod
    def validate_feature_id(cls, feature_id: str) -> bool:
        """Check if feature ID is valid"""
        return feature_id in cls.FEATURES

    @classmethod
    def get_all_features(cls) -> Dict[str, dict]:
        """Get all features with default parameters for 'all' option"""
        return {
            f_id: cls.get_feature_params(f_id)
            for f_id in cls.get_feature_ids()
        } 