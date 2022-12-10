## Description
A file organizer with GUI and a .exe compilation.\
The compiled app file_organizer_gui.exe is in a dist folder.

### Features:
1. The user can enter input and output paths in the fields or select them using the file explorer. The output path repeats the input one by default.
2. If the user presses the 'Organize' button - the app will check:
    - if the path entered
    - if the folder:
      - exists;
      - readable;
      - writable;
      - is not empty.
3. If there's an issue, the app shows a window with the error message.
4. Creates a root folder named: 'Organized files (DD-MMM-YYYY HH.MM.SS).'
5. Sorts files by their extensions into folders by type.
6. This script can't delete the files, so they're safe.

## Demo
![file_organizer](https://user-images.githubusercontent.com/44866199/167579604-72034ca6-7b93-4751-a1d4-5db215a3d90c.gif)
