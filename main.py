import sys
import os
import random
import time

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame

def random_distribution(r):
    """
    Generate a random number based on a normal distribution.
    :param r: The randomness factor (0 = no randomness, 1 = maximum randomness).
    :return: A random number between 0 and 1.
    """
    if r <= 0:
        return 1 / 2
    elif r >= 1:
        return random.uniform(0, 1)
    else:
        std_dev = (1 / 2) * r
        val = random.gauss(1 / 2, std_dev)
        return max(0, min(1, val))

def main(file, frequency, r_factor):
    """
    Play a sound from a file with a specified frequency and r_factor.
    :param file: The path to the sound file.
    :param frequency: The frequency at which to play the sound.
    :param
    r_factor: The randomness of the frequency.
    :return: None
    """
    if not os.path.exists(file):
        print(f"File {file} does not exist.")
        sys.exit(1)

    time_between_sounds = 3600 * 2 / frequency

    while True:
        pygame.mixer.music.load(file)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)   
        time.sleep(time_between_sounds * random_distribution(r_factor))

def get_file():
    """
    Get the sound file from the user.
    :return: The path to the sound file.
    """

    soundboard_dir = os.path.join(os.path.dirname(__file__), "soundboard")

    if len(sys.argv) > 1:
        return os.path.join(soundboard_dir, sys.argv[1])

    if not os.path.exists(soundboard_dir):
        os.makedirs(soundboard_dir)
    files = [f for f in os.listdir(soundboard_dir)
             if os.path.isfile(os.path.join(soundboard_dir, f))
             and f.lower().endswith(('.wav', '.mp3', '.ogg'))
            ]
    if not files:
        print("No sound files found in the soundboard directory.")
        sys.exit(1)
    files.sort(key=lambda x: x.lower())
    print("Available sound files:")
    for i, f in enumerate(files):
        print(f"{i + 1}: {f}")
    i = input("Please provide a sound file"+
        (f" (1-{len(files)})" if len(files) > 1 else "") +
        ": ")
    try:
        i = int(i) - 1
        if i < 0 or i >= len(files):
            print("Provided number is out of range.")
            sys.exit(1)
        return os.path.join(soundboard_dir, files[i])
    except ValueError:
        print("Invalid input. Please provide a valid number.")
        sys.exit(1)

def get_double(argn, message, predicate, p_error):
    """
    Get a double from the user.
    :param argn: The argument number to check.
    :param message: The message to display if the argument is not provided.
    :param predicate: A function that takes a float and returns True if it is valid.
    :param p_error: The error message to display if the predicate fails.
    :return: A float.
    """
    if len(sys.argv) > argn:
        v = sys.argv[argn]
    else:
        print(message)
        v = input()
    try:
        v = float(v)
        if not predicate(v):
            print(p_error)
            sys.exit(1)
        return v
    except ValueError:
        print("Invalid input. Please provide a valid number.")
        sys.exit(1)


def get_frequency():
    """
    Get the frequency from the user.
    :return: A positive float.
    """
    return get_double(
        2,
        "Please provide how many times per hour the sound should be played (on average): ",
        lambda x: x > 0,
        "Frequency must be a positive number."
    )

def get_r_factor():
    """
    Get the randomness factor from the user.
    :return: A float between 0 and 1.
    """
    return get_double(
        3,
        "How random should the occurances be? (0 = no randomness, 1 = maximum randomness): ",
        lambda x: 0 <= x <= 1,
        "Randomness factor must be between 0 and 1."
    )


if __name__ == "__main__":
    pygame.mixer.init()
    try:
        file = get_file()
        frequency = get_frequency()
        r_factor = get_r_factor()
        print("Press Ctrl+C to stop.")
        main(file, frequency, r_factor)
    except KeyboardInterrupt:
        print("\nClosing down.")