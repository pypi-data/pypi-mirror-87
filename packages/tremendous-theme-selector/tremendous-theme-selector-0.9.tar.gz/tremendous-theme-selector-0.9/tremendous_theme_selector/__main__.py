import os
import random

import click
import pygame

from tremendous_theme_selector.utils import get_all_files, get_binary_label, stringify_annotations, write_lines, parse_annotations, play_file


@click.group()
def main():
    pass


@main.command()
@click.argument('input-folder-path', type=str)
@click.option('-i', '--input-labels-file-path', default=None, type=str)
@click.option('-o', '--output-labels-file-path', default='assets/output-labels.txt', type=str)
@click.option('-n', '--n-files-to-annotate', default=None, type=int)
def annotate_with_binary_labels(input_folder_path, input_labels_file_path, output_labels_file_path, n_files_to_annotate):
    assert input_labels_file_path != output_labels_file_path
    pygame.mixer.init()
    files = list(get_all_files(input_folder_path))
    if input_labels_file_path is not None:
        parsed_labels = parse_annotations(input_labels_file_path)
        files = [
            file
            for file in files
            if file not in parsed_labels
        ]
    annotations = {}
    counter = 0
    while len(files) > 0:
        chosen_file = random.choice(files)
        print(f'Annotating file {chosen_file}' + (f' {counter + 1}/{n_files_to_annotate}' if n_files_to_annotate is not None else ''))
        play_file(chosen_file)
        annotations[chosen_file] = get_binary_label()
        counter += 1
        files.remove(chosen_file)
        if n_files_to_annotate is not None and counter >= n_files_to_annotate:
            print(f'Good job! You have annotated {n_files_to_annotate} files!')
            break
    else:
        print('Good job! You have annotated all the files!')
    os.makedirs(os.path.dirname(os.path.realpath(output_labels_file_path)), exist_ok=True)
    write_lines(
        output_labels_file_path,
        stringify_annotations(annotations)
    )


if __name__ == '__main__':
    main()
