from transformers import pipeline

model = None


def question_answering(question, context):
    return model(question, context)
