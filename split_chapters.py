import re, os

with open('data/art_of_war.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Remove Gutenberg header
start_marker = '*** START OF THE PROJECT GUTENBERG EBOOK'
if start_marker in text:
    text = text.split(start_marker)[1]

# Find the actual chapter start - after contents page
first_chapter = text.find('Chapter I.')
if first_chapter > 0:
    text = text[first_chapter:]

# Split by "Chapter X." pattern
chapters = re.split(r'(Chapter [IVX]+\.)', text)

names = ['','laying_plans','waging_war','attack_by_stratagem','tactical_dispositions',
         'energy','weak_points_and_strong','maneuvering','variation_in_tactics',
         'the_army_on_the_march','terrain','the_nine_situations','attack_by_fire','use_of_spies']

roman_map = {'I':1,'II':2,'III':3,'IV':4,'V':5,'VI':6,'VII':7,'VIII':8,'IX':9,'X':10,'XI':11,'XII':12,'XIII':13}

os.makedirs('data/chapters', exist_ok=True)

for i in range(1, len(chapters)-1, 2):
    header = chapters[i].strip()
    content = chapters[i+1].strip()
    
    # Extract roman numeral
    roman = header.replace('Chapter','').replace('.','').strip()
    num = roman_map.get(roman)
    
    if num and 1 <= num <= 13:
        title = names[num].replace('_', ' ').upper()
        filename = f'data/chapters/chapter_{num:02d}_{names[num]}.txt'
        with open(filename, 'w', encoding='utf-8') as out:
            out.write(f'CHAPTER {num}: {title}\n\n{content}')
        print(f'Created Chapter {num} ({title}): {len(content)} chars')

print('Done.')