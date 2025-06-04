from mido import MidiFile, MidiTrack, Message
import os
from tqdm import tqdm
print("--Made By Soft Midi Player--")
print("Usage: input <midi path> | output <path with .mid>")
def remove_low_velocity_notes(input_file, output_file, velocity_threshold=50):
    midi = MidiFile(input_file)
    new_midi = MidiFile()

    total_messages = sum(len(track) for track in midi.tracks)
    processed_messages = 0

    with tqdm(total=total_messages, desc="Progress", unit="message") as pbar:
        for track in midi.tracks:
            new_track = MidiTrack()
            accumulated_time = 0

            for msg in track:
                if msg.type == 'note_on' and msg.velocity <= velocity_threshold:
                    accumulated_time += msg.time
                else:
                    msg.time += accumulated_time
                    accumulated_time = 0
                    new_track.append(msg)

                processed_messages += 1
                pbar.update(1)

            new_midi.tracks.append(new_track)

    new_midi.save(output_file)
    print(f"\nSaving Complete: {output_file}")

def main():
    input_midi_path = input("Enter the path to the MIDI file: ")
    if not os.path.exists(input_midi_path):
        print("The MIDI file path you entered does not exist.")
        return
    try:
        velocity_threshold = int(input("Enter the Velocity threshold (default: 50): ") or 50)
    except ValueError:
        print("Please enter a valid number.")
        return

    output_midi_path = input("Enter the file path you want to save after conversion: ")

    print("Start converting...")
    remove_low_velocity_notes(input_midi_path, output_midi_path, velocity_threshold)

if __name__ == "__main__":
    main()
