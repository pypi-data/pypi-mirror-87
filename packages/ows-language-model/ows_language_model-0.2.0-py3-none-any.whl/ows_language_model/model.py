from ows_language_model.config import config

# TODO: define model here

# defines all callbacks, scheduling and builds model here

from transformers import GPT2Tokenizer, GPT2LMHeadModel

tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
model = GPT2LMHeadModel.from_pretrained('gpt2')


if __name__ == '__main__':
    # could print summary
    pass
