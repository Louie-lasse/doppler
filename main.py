import sys
import os

def main(file, frequency, r_factor):
    """
    Play a sound from a file with a specified frequency and r_factor.
    :param file: The path to the sound file.
    :param frequency: The frequency at which to play the sound.
    :param
    r_factor: The randomness of the frequency.
    :return: None
    """
    pass

def get_file():
    """
    Get the sound file from the user.
    :return: The path to the sound file.
    """
    if len(sys.argv) > 1:
        return sys.argv[1]

    soundboard_dir = os.path.join(os.path.dirname(__file__), "soundboard")
    if not os.path.exists(soundboard_dir):
        os.makedirs(soundboard_dir)
    files = [f for f in os.listdir(soundboard_dir)
             if os.path.isfile(os.path.join(soundboard_dir, f))
             and f.lower().endswith(('.wav', '.mp3', '.ogg'))]
    if not files:
        print("No sound files found in the soundboard directory.")
        sys.exit(1)
    files.sort(lambda x: x.lower())
    print("Available sound files:")
    for i, f in enumerate(files):
        print(f"{i + 1}: {f}")
    i = input("Please provide a sound file: ")
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
    file = get_file()
    frequency = get_frequency()
    r_factor = get_r_factor()
    main(file, frequency, r_factor)
