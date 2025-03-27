# note generator in one minute, plays bpm notes. each note plays for bpm/60 seconds * 1000 milliseconds
# 500ms required for padding after a note.
# time of note = 500 + hit_time of last note 

from note_class import Note, hardNote, holdNote, holdNote
import pygame

# track_time measured in seconds

def generate_notes(track_time, bpm, start_time):

    # needs (bpm * track_time) number of notes
    
    notes = []

    for x in range (0, int(bpm*track_time/60)):

        hit_time = start_time + (60 * 1000)/bpm - 500

        notes.append(Note(start_time, hit_time))

        start_time = hit_time + 500

    return notes

def generate_notes_hold(track_time, bpm, start_time, hold_time):

    # needs (bpm * track_time) number of notes

    notes = []

    hold_time = hold_time * 1000

    for x in range (0, int(bpm*track_time/60)):

        hit_time = start_time + (60 * 1000)/bpm - 500

        notes.append(holdNote(start_time, hit_time, hold_time))
        print('start:', start_time, 'expected start:', hit_time + hold_time + 500)

        start_time = hit_time + hold_time + 500

    return notes
