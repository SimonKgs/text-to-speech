import pyttsx3
from pypdf import PdfReader

# init the pyttsx3 engine
engine = pyttsx3.init()

voice_options = {}


# this function will get the voices id for the user
def list_voices():
    voices = engine.getProperty('voices')

    for voice in voices:
        # print(voice.name)
        # print(f"ID: {voice.id}, Name: {voice.name}, Lang: {voice.languages}")
        if "spanish" in voice.name.lower():
            voice_options['spanish'] = voice.id
        elif "english" in voice.name.lower():
            voice_options['english'] = voice.id


def save_pdf_to_speech(document_path, language='s', read_now='n'):
    # get the voices
    list_voices()

    # select language, default english
    doc_language = 'english'
    if language == 's':
        doc_language = 'spanish'

    # read the pdf
    reader = PdfReader(f"{document_path}.pdf")
    number_of_pages = len(reader.pages)

    # apply language selected
    engine.setProperty('voice',
                       fr'{voice_options[doc_language]}')

    # first get each page, then extract the text (it comes in a separate words)
    # finally I create an array with the words of each page
    full_file = [reader.pages[page].extract_text().split() for page in range(number_of_pages)]
    # This will join the words of each page
    full_text = [" ".join(text) for text in full_file]
    # and finally I need to join the pages to have the full document
    final_text = " ".join(full_text)

    # Having all set, save the file into a .mp3
    engine.save_to_file(final_text, f'{document_path}.mp3')

    print(final_text)

    # If the user wants read it at the end
    if read_now.lower() == 'y':
        engine.say(final_text)
        engine.runAndWait()


# getting user options
document = input('write the name of the document:\n').lower()
which_language = input('Select the language of the file. E for English / S for Spanish\n').lower()
read_it = input('do you want to read it now? y/n\n').lower()

save_pdf_to_speech(document, language=which_language, read_now=read_it)
