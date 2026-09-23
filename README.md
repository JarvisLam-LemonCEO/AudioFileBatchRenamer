# Audio File Batch Renamer (From Downie4)

A simple Python desktop application for batch renaming audio files with a graphical user interface.

This tool is designed for downloaded audio files that follow a naming format such as:

```text
Album - ARASHI NO.1〜嵐は嵐を呼ぶ〜 - 001 - 台風ジェネレーション -Typhoon Generation-.mp3
```

The program removes everything before the third `" - "` separator and keeps the actual song title.

After renaming:

```text
台風ジェネレーション -Typhoon Generation-.mp3
```

---

## Features

* Simple graphical user interface using Tkinter
* Select an entire folder at once
* Preview filenames before making any changes
* Rename multiple files with one click
* Automatically detects the third `" - "` separator
* Keeps the original file extension
* Preserves hyphens that are part of the song title
* Skips files that do not match the expected filename structure
* Detects filename conflicts before renaming
* Prevents accidental overwriting of existing files

---

## Example

### Before

```text
Album - ARASHI NO.1〜嵐は嵐を呼ぶ〜 - 001 - 台風ジェネレーション -Typhoon Generation-.mp3
Album - ARASHI NO.1〜嵐は嵐を呼ぶ〜 - 002 - SUNRISE日本.mp3
Album - ARASHI NO.1〜嵐は嵐を呼ぶ〜 - 003 - HORIZON.mp3
```

### After

```text
台風ジェネレーション -Typhoon Generation-.mp3
SUNRISE日本.mp3
HORIZON.mp3
```

The program specifically looks for:

```text
 - 
```

which is a hyphen surrounded by spaces.

This means a title such as:

```text
台風ジェネレーション -Typhoon Generation-
```

will not be accidentally removed because `-Typhoon Generation-` does not use the same `" - "` separator format.

---

## How It Works

The main filename processing logic uses:

```python
filename.split(" - ", 3)
```

Python splits the filename at the first three occurrences of `" - "`.

For example:

```text
Album - Album Name - 001 - Song Name.mp3
```

becomes:

```text
Album
Album Name
001
Song Name.mp3
```

The application keeps only the final part:

```text
Song Name.mp3
```

---

## Requirements

* Python 3
* Tkinter

Tkinter is included with most standard Python installations.

No additional Python packages are required.

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
```

### 2. Enter the project folder

```bash
cd YOUR-REPOSITORY
```

### 3. Run the program

```bash
python batch_renamer.py
```

Depending on your system, you may need to use:

```bash
python3 batch_renamer.py
```

---

## Usage

1. Launch the Python application.
2. Click **Choose Folder**.
3. Select the folder containing your audio files.
4. Review the filenames in the preview table.
5. Check that the new filenames are correct.
6. Click **Rename All**.
7. Confirm the rename operation.
8. The files will be renamed automatically.

---

## Filename Format

The application expects filenames with at least three `" - "` separators.

For example:

```text
Category - Album - Track Number - Song Title.mp3
```

It removes:

```text
Category - Album - Track Number - 
```

and keeps:

```text
Song Title.mp3
```

The text before the third separator does not need to be the same for every album.

For example, all of these are supported:

```text
Album - Album A - 001 - Song One.mp3
Album - Album B - 015 - Song Two.mp3
Music - Japanese Album - 023 - Song Three.flac
Download - Another Album - 108 - Song Four.m4a
```

They will become:

```text
Song One.mp3
Song Two.mp3
Song Three.flac
Song Four.m4a
```

---

## Supported File Types

The program does not limit renaming to a specific audio format.

It can work with files such as:

```text
.mp3
.m4a
.flac
.wav
.aac
.ogg
```

Other file types can also be renamed if their filenames match the expected format.

---

## Safety

The application includes several protections before changing files.

### Preview

All filename changes can be reviewed before clicking **Rename All**.

### Conflict Detection

If the new filename already exists in the folder, the program stops the rename operation instead of overwriting the file.

For example, if:

```text
Song Name.mp3
```

already exists, the application will display a filename conflict warning.

### Non-Matching Files

Files that do not contain at least three `" - "` separators are ignored.

---

## Project Structure

```text
audio-file-batch-renamer/
│
├── batch_renamer.py
├── README.md
└── LICENSE
```

---

## Why I Made This

Some downloaded music collections include long metadata prefixes inside the filename, such as:

```text
Album - Album Name - Track Number - Song Title
```

Renaming hundreds of files manually can take a lot of time.

This tool provides a quick way to clean those filenames while still allowing the user to preview every change before modifying the files.

---

## Future Improvements

Possible future features include:

* Undo last rename
* Custom separator selection
* Choose how many filename sections to remove
* Drag-and-drop folder support
* Rename individual selected files
* Recursive folder scanning
* Audio-file-only filtering
* Dark mode
* Custom filename patterns
* Save rename history
* Standalone Windows and macOS applications

---

## Contributing

Contributions, suggestions, and bug reports are welcome.

If you find a problem or have an idea for an improvement, feel free to open an issue or submit a pull request.

---

## License

This project is open source.

You may add a license such as the MIT License if you want others to freely use, modify, and distribute the project.

See the `LICENSE` file for more information.

---

## Disclaimer

Always review the preview list before renaming important files.

Although the application includes filename conflict protection, it is recommended to keep a backup of important files before performing large batch rename operations.
