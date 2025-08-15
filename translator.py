from deep_translator import (GoogleTranslator,
                             ChatGptTranslator,
                             MicrosoftTranslator,
                             PonsTranslator,
                             LingueeTranslator,
                             MyMemoryTranslator,
                             YandexTranslator,
                             PapagoTranslator,
                             DeeplTranslator,
                             QcriTranslator,
                             single_detection,
                             batch_detection)

langs_list = MicrosoftTranslator().get_supported_languages()  # output: [arabic, french, english etc...]

texts = [
  """
  ​""", "How are you, Bopha?"]
translated = GoogleTranslator('en', 'km').translate_batch(texts)

print(langs_list)