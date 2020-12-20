import speech_recognition as sr


r = sr.Recognizer()

ACTIONS = [
    {'command': 'select', 'action': 'select'},
    {'command': 'create', 'action': 'create'},
    {'command': 'change', 'action': 'change'},
    {'command': 'delete', 'action': 'delete'},
]

OUTPUT = [
    '',
    '# random comment here!',
    'array = [1,2,3]',
    '',
    'for num in array:',
    '    print(num)',
]

CURSOR = 0

INPUT_DOTS = '.'

def record_audio():
    with sr.Microphone() as source:
        audio = r.listen(source)
        voice_data = ''

        try:
            text = r.recognize_google(audio, show_all=True)
            voice_data = text
        except sr.UnknownValueError:
            pass
            #  print("Sorry, my computer brain didn't understand :(")
        except sr.RequestError:
            print("Sorry, my language service is down :(")

        return voice_data


def print_output():
    print('---------')
    for i, line in enumerate(OUTPUT):
        if i == CURSOR:
            print(f"| {i}  >>  " + line)
        else:
            print(f"| {i}      " + line)
    print('---------')


def is_action(first_try, voice_data):
    for item in ACTIONS:
        if item['command'] in first_try:
            exec(item['action'] + f'({first_try, voice_data})')
            return True
    return False

def return_first_num_or_false(str):
    return_char = ''
    found_num = False
    for i, char in enumerate(str):
        if char.isdigit():
            found_num = True
            return_char += char
        else:
            if found_num == True:
                break

    if return_char == '':
        return False
    return return_char

def select(voice_data):

    after_line = voice_data[0].partition('line')[2].strip()
    line_selector = return_first_num_or_false(after_line)

    # if no digit in first try, go through other possible interpretations
    if not line_selector:
        for potential_correct_interpretation in voice_data[1]:
            PCI = potential_correct_interpretation['transcript']

            after_line = PCI.partition('line')[2]
            line_selector = return_first_num_or_false(after_line)

            if line_selector:
                break

    if line_selector:
        print('\n')
        print('SELECT LINE: ' + line_selector)
        line_selector = int(line_selector)
        if line_selector < len(OUTPUT):
            global CURSOR
            CURSOR = line_selector
            print_output()
        else:
            print('ERROR: Index out of range!')
            print_output()

    return

def create(voice_data):
    print('CREATE')
def change(voice_data):
    print('CHANGE')
def delete(voice_data):
    print('DELETE')

while True:
    voice_data = record_audio()

    if voice_data and voice_data['alternative']:

        first_try = voice_data['alternative'][0]['transcript'].lower()
        if 'exit' in first_try:
            exit()
        if not is_action(first_try, voice_data['alternative']):
            print('No actions for: "' + first_try + '"')

