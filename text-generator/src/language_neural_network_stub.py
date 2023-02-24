from language_neural_network_abstract import LanguageNeuralNetworkAbstract


class LanguageNeuralNetworkStub(LanguageNeuralNetworkAbstract):
    def __init__(self, path: str, use_cpu: bool = False):
        # Stub
        pass

    def seed(self, seed: int):
        # Stub
        pass

    def generate(
            self,
            prompt: str,
            count: int = 1,
            max_new_tokens: int = 50,
            num_beams: int = 5,
            no_repeat_ngram_size: int = 5,
            repetition_penalty: float = None,
            early_stopping: bool = True,
            seed: int = 42,
            top_k: int = 50,
            top_p: float = 0.95,
            temperature: float = 1.0,
            bad_words: list[str] = None) -> list[str]:
        return ['some generated text']