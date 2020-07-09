import genanki
import re

outputfile = 'output.apkg'
cloze_regexp = re.compile(r""".*\{\{c\d{1,2}::.+\}\}.*""")

def is_cloze(front):
    return cloze_regexp.search(front)

def generate_model(id, name, fields, templates):
    return genanki.Model(
        id,
        name,
        fields=[{'name' : field} for field in fields],
        templates=templates,
    )

cloze_model = generate_model(
    1374501812,
    'Cloze Deletion',
    fields=['Text'],
    templates=[
        {
            'name' : 'Card 1',
            'qfmt' : '{{cloze:Text}}<br><br>{{type:cloze:Text}}',
            'afmt' : '{{cloze:Text}}<br><br>{{type:cloze:Text}}',
        }
    ])

answer_model = generate_model(
    1586655081,
    'Free Response',
    fields=['Question', 'Answer'],
    templates=[
        {
            'name' : 'Card 1',
            'qfmt' : '{{Question}}<br><br>{{type:Answer}}',
            'afmt' : '{{Question}}<br><br><hr id=answer><br>{{Answer}}',
        }
    ])
    
default_deck = genanki.Deck(1, 'Default')

def make_deck():
    write_deck = default_deck
    with open('anki.txt', 'r') as readfile:
        cloze_card = False
        lines = []
        
        for line in readfile:
            clean_line = line.strip()
            if clean_line:
                if is_cloze(clean_line):
                    cloze_card = True
                lines.append(clean_line)
            else:
                if not lines:
                    continue
                else:
                    add_note = None
                    
                    if cloze_card:
                        add_note = genanki.Note(
                            model=cloze_model, fields=['\n'.join(lines)]
                        )
                    else:
                        add_note = genanki.Note(
                            model=answer_model,
                            fields=['\n'.join(lines[:-1]), lines[-1]]
                        )
                    
                    write_deck.add_note(add_note)
                    cloze_card = False
                    lines = []
                    

    genanki.Package(write_deck).write_to_file("output.apkg")

make_deck()
