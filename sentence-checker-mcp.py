import language_tool_python

class SentenceChecker:
    """MCP for checking sentence completeness, grammar, and structure"""
    
    def __init__(self):
        self.tool = language_tool_python.LanguageTool('en-US')

    def check_completeness(self, sentence):
        """Check if the sentence ends with proper punctuation"""
        if sentence and sentence.strip()[-1] in ['.', '!', '?']:
            return True
        return False

    def check_grammar(self, sentence):
        """Check for grammatical errors using LanguageTool"""
        matches = self.tool.check(sentence)
        return matches

    def check_punctuation(self, sentence):
        """Check for proper punctuation and spacing"""
        errors = []
        sentence = sentence.strip()
        
        if not sentence:
            errors.append('Sentence is empty.')
            return errors
            
        if sentence[-1] not in ['.', '!', '?']:
            errors.append('Sentence should end with a punctuation mark (. ! ?).')
        
        return errors

    def check_capitalization(self, sentence):
        """Check if sentence starts with a capital letter"""
        sentence = sentence.strip()
        if sentence and not sentence[0].isupper():
            return False
        return True

    def provide_suggestions(self, sentence):
        """Provide improvement suggestions for the sentence"""
        matches = self.tool.check(sentence)
        suggestions = []
        for match in matches:
            suggestions.append({
                'message': match.message,
                'offset': match.offset,
                'length': match.length
            })
        return suggestions

    def analyze_sentence(self, sentence):
        """Comprehensive sentence analysis"""
        analysis = {
            'sentence': sentence,
            'is_complete': self.check_completeness(sentence),
            'starts_with_capital': self.check_capitalization(sentence),
            'grammar_errors': [{'message': m.message} for m in self.check_grammar(sentence)],
            'punctuation_errors': self.check_punctuation(sentence),
            'suggestions': self.provide_suggestions(sentence),
            'is_valid': (
                self.check_completeness(sentence) and 
                self.check_capitalization(sentence) and 
                len(self.check_grammar(sentence)) == 0 and 
                len(self.check_punctuation(sentence)) == 0
            )
        }
        return analysis


# Example usage
if __name__ == '__main__':
    checker = SentenceChecker()
    
    test_sentences = [
        "This is a proper sentence.",
        "this starts with lowercase",
        "Missing punctuation",
        "This has multiple errors in it grammar."
    ]
    
    for sentence in test_sentences:
        result = checker.analyze_sentence(sentence)
        print(f"\nSentence: {sentence}")
        print(f"Valid: {result['is_valid']}")
        print(f"Issues: {result['punctuation_errors'] + result['grammar_errors']}")