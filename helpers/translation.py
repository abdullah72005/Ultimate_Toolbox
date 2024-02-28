import googletrans
from googletrans import Translator

def translatetxt(input_txt, input_lang, output_lang, langs):
    translator = Translator()

    if input_lang == 'detect':
        g = translator.detect(input_txt)
        input_lang = g.lang
        output = translator.translate(input_txt, src=input_lang, dest=langs[output_lang])
    else:
        output = translator.translate(input_txt, src=langs[input_lang], dest=langs[output_lang])
    
    return output.text