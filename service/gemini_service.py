import gemini.gemini as gemini

access_token = None


async def get_polarity(text):
    text += ". Do a sentiment analysis on this text"
    text += " use a 1 to 5 scale (considering 2 decimal positions) where 1 is"
    text += " too bad and 5 is too good and then return only a number."
    text += " dont give me the sentiment or extra information, just the polarity."
    text += " if the text is neutral, return 3."
    text += " if the text is not understandable return 0."
    text += " return any number as a plain text without any MD format."

    return await gemini.send_message(text, access_token)


async def consult_from(context: str, query: str):
    text = context + ". "

    text += "based on this text, I you respond to this following text:"
    text += query + ". "

    text += "only use information that is in the first text, "
    text += "don't use any external information about any concept on the text. "

    return await gemini.send_message(text, access_token)


async def resume_from(context: str):
    text = context + ". "

    text += "summarize the text above. "
    text += "return the summary as MD text for MD post. "
    text += "the summary should be concise and clear. "
    text += "do not include any information that is not in the text. "
    text += "only return the MD format as plain text."

    return await gemini.send_message(text, access_token)
