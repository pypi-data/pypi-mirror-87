import os
from os import walk

import pygame


def get_all_files(path: str, extension: str = 'wav'):
    for (dirpath, dirnames, filenames) in walk(path):
        for file in filenames:
            splitted_filename = file.split('.')
            if len(splitted_filename) > 1 and splitted_filename[-1] == extension:
                yield os.path.join(dirpath, file)


def get_binary_label():
    user_input = input('Enter your score: ')
    if user_input == '-':
        return 0
    elif user_input == '+':
        return 1
    else:
        print('Cannot recognize the label, please, try again.')


def write(filename, content):
    with open(filename, 'w') as f:
        f.write(content)
        f.flush()


def write_lines(filename, lines):
    write(filename, '\n'.join(lines))


def read_lines(filename):
    with open(filename) as f:
        return [line.replace('\n', '') for line in f.readlines()]


def stringify_annotations(annotations: dict):
    return sorted(
        tuple(
            map(
                lambda path_and_label: f'{path_and_label[0]}\t{str(path_and_label[1])}',
                annotations.items()
            )
        )
    )


def parse_annotations(path: str):
    def get_entry(line):
        annotated_file_path, label = line.split('\t')
        return annotated_file_path, int(label)

    return {
        key: value
        for key, value in
        map(
            get_entry,
            read_lines(path)
        )
    }


def play_file(path: str):
    my_sound = pygame.mixer.Sound(path)
    my_sound.play()
    pygame.time.wait(int(my_sound.get_length() * 1000))
