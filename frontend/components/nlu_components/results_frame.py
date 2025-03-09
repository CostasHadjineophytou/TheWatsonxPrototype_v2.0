import tkinter as tk
from tkinter import ttk

class ResultsFrame(ttk.LabelFrame):
    """Frame for displaying NLU analysis results"""
    
    def __init__(self, parent):
        super().__init__(parent, text="Analysis Results")
        self._init_ui()
        
    def _init_ui(self):
        """Initialize UI components"""
        # Results text area
        self.results_text = tk.Text(
            self, 
            height=15,
            width=50, 
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.results_text.pack(padx=5, pady=5, fill='both', expand=True)
        
    def display_results(self, results: dict):
        """Format and display analysis results"""
        if not results:
            self._show_result("No analysis results available")
            return

        output = []
        
        # Format sentiment
        if 'sentiment' in results:
            if isinstance(results['sentiment'], dict) and 'error' in results['sentiment']:
                output.append(f"Sentiment: {results['sentiment']['error']}")
            else:
                sentiment = results['sentiment']
                output.append(f"Sentiment: {sentiment['label']} ({sentiment['score']:.2f})")
            
        # Format emotion
        if 'emotion' in results:
            if isinstance(results['emotion'], dict) and 'error' in results['emotion']:
                output.append(f"Emotions: {results['emotion']['error']}")
            else:
                emotion_text = ", ".join(f"{k}: {v:.2f}" for k, v in results['emotion'].items())
                output.append(f"Emotions:\n{emotion_text}")
            
        # Format entities
        if 'entities' in results:
            if isinstance(results['entities'], dict) and 'error' in results['entities']:
                output.append(f"Entities: {results['entities']['error']}")
            else:
                entities = results['entities']
                if entities:
                    entity_text = "\n• ".join(
                        f"{e['text']} ({e['type']}) - {e['confidence']:.2f}"
                        for e in entities
                    )
                    output.append(f"Entities:\n• {entity_text}")
                else:
                    output.append("Entities: None found")
            
        # Format keywords
        if 'keywords' in results:
            if isinstance(results['keywords'], dict) and 'error' in results['keywords']:
                output.append(f"Keywords: {results['keywords']['error']}")
            else:
                keywords = results['keywords']
                if keywords:
                    keyword_text = "\n• ".join(
                        f"{k['text']} (relevance: {k['relevance']:.2f})"
                        for k in keywords
                    )
                    output.append(f"Keywords:\n• {keyword_text}")
                else:
                    output.append("Keywords: None found")
            
        # Format categories
        if 'categories' in results:
            if isinstance(results['categories'], dict) and 'error' in results['categories']:
                output.append(f"Categories: {results['categories']['error']}")
            else:
                categories = results['categories']
                if categories:
                    category_text = "\n• ".join(
                        f"{c['label']} (score: {c['score']:.2f})"
                        for c in categories
                    )
                    output.append(f"Categories:\n• {category_text}")
                else:
                    output.append("Categories: None found")
            
        # Format concepts
        if 'concepts' in results:
            if isinstance(results['concepts'], dict) and 'error' in results['concepts']:
                output.append(f"Concepts: {results['concepts']['error']}")
            else:
                concepts = results['concepts']
                if concepts:
                    concept_text = "\n• ".join(
                        f"{c['text']} (relevance: {c['relevance']:.2f})"
                        for c in concepts
                    )
                    output.append(f"Concepts:\n• {concept_text}")
                else:
                    output.append("Concepts: None found")

        # Format relations
        if 'relations' in results:
            if isinstance(results['relations'], dict) and 'error' in results['relations']:
                output.append(f"Relations: {results['relations']['error']}")
            else:
                relations = results['relations']
                if relations:
                    relation_text = "\n• ".join(
                        f"{r['type']}: {r['sentence']}"
                        for r in relations
                    )
                    output.append(f"Relations:\n• {relation_text}")
                else:
                    output.append("Relations: None found")

        # Format semantic roles
        if 'semantic_roles' in results:
            if isinstance(results['semantic_roles'], dict) and 'error' in results['semantic_roles']:
                output.append(f"Semantic Roles: {results['semantic_roles']['error']}")
            else:
                roles = results['semantic_roles']
                if roles:
                    role_text = "\n• ".join(
                        f"{r.get('subject', '')} {r.get('action', '')} {r.get('object', '')}"
                        for r in roles
                    )
                    output.append(f"Semantic Roles:\n• {role_text}")
                else:
                    output.append("Semantic Roles: None found")

        # If no results were processed
        if not output:
            output.append("No analysis results available")

        self._show_result("\n\n".join(output))
        
    def _show_result(self, text: str):
        """Update results text widget"""
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete("1.0", tk.END)
        self.results_text.insert("1.0", text)
        self.results_text.config(state=tk.DISABLED)
        
    def clear(self):
        """Clear the results display"""
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete("1.0", tk.END)
        self.results_text.config(state=tk.DISABLED) 