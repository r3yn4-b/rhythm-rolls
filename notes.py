from note_generator import generate_notes, generate_notes_hold

def level1(start_time):
    notes = generate_notes(30, 30, 600)
    print('level', 1)
    return notes

def level2(start_time):
    notes = generate_notes(30, 50, 600)
    print('level', 2)
    return notes

def level3(start_time):
    notes = []
    for i in range(0, 3):
        new_notes = generate_notes(10, 20*i, 10500*i)
        for x in range(0, len(new_notes)):
            notes.append(new_notes[x])
    print('level', 3)
    return notes

def level4(start_time):
    notes = generate_notes_hold(30, 40, start_time, 1)
    print('level', 4)
    return notes

levels_dict = {

    1: level1,
    2: level2,
    3: level3,
    4: level4,

}