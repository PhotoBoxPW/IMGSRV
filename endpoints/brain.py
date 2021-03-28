from utils.endpoint import Endpoint, setup


@setup
class Brain(Endpoint):
    def generate(self, kwargs):
        texts = kwargs['texts']

        if len(texts) < 2:
            texts = ['using one quote', 'using two quotes or more']

        # set limit
        texts = texts[:18]

        base = self.create_text_ladder(texts)
        return self.send_file(base, format='jpeg')