from mido import MidiFile, MidiTrack, Message
import os
from tqdm import tqdm
print("--Made By Soft Midi Player.--")
def remove_low_velocity_notes(input_file, output_file, velocity_threshold=50):
    midi = MidiFile(input_file)
    new_midi = MidiFile()

    total_messages = sum(len(track) for track in midi.tracks)
    processed_messages = 0

    with tqdm(total=total_messages, desc="진행 상태", unit="메시지") as pbar:
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
    print(f"\n저장 완료: {output_file}")

def main():
    input_midi_path = input("MIDI 파일 경로를 입력하세요: ")
    if not os.path.exists(input_midi_path):
        print("입력한 MIDI 파일 경로가 존재하지 않습니다.")
        return
    try:
        velocity_threshold = int(input("Velocity threshold를 입력하세요 (기본값: 50): ") or 50)
    except ValueError:
        print("유효한 숫자를 입력해 주세요.")
        return

    output_midi_path = input("변환 후 저장할 파일 경로를 입력하세요: ")  # 저장 경로 입력

    print("변환을 시작합니다...")
    remove_low_velocity_notes(input_midi_path, output_midi_path, velocity_threshold)

if __name__ == "__main__":
    main()
