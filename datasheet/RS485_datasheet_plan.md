# RS485 Adapter Datasheet – Plan for the Generator

## 1. Goal
The goal is to have a program that automatically creates a polished PDF datasheet for the RS485 adapter. You will run the program, and it will pull in the latest schematic and a standard connection diagram and assemble everything into a nicely formatted document. The first page must now mirror the servomotor datasheet hero layout by including the Gearotons slogan (“Affordable and Simple All-in-One Motion Control” and “From Education to Innovation”) in the exact same color, and by showcasing RS485 adapter photos sourced directly from `../Pictures/adapter/RS485_adapter_20250714153203.jpg` and `../Pictures/adapter/RS485_adapter_20250714153158.jpg` relative to the datasheet repository (referenced in place, not copied or symlinked).

### Hero layout parity – November 2025 requirements
- The hero area must render the two-line Gearotons slogan in the identical green used by the servomotor datasheet (`SERVOMOTOR_SLOGAN_COLOR` in code) so the documents look like a matched family.
- A row of RS485 adapter photos must appear directly under the slogan on page one, using the exact file paths provided above (relative path `../Pictures/adapter`). These assets are loaded from that folder at runtime; no copies, moves, or intermediary symlinks are allowed.
- If either photo is missing, the generator should stop immediately with a clear fatal error explaining which absolute path is absent so the operator can restore the assets before distributing a datasheet.
- Layout, spacing, and typography should mirror the servomotor PDF hero so the adapter datasheet inherits the same visual rhythm (logo, slogan, imagery, then body content).

## 2. How the program will behave (in human terms)
- You run a single command to generate the datasheet.
- The program looks at the RS485 adapter PCB project and figures out which board revision is the latest one based on its version number (for example 1.2 is older than 1.2.5, and 1.3 is newer than both).
- From that latest board revision, it finds the matching schematic PDF and converts the first page into an image suitable for placing in the datasheet.
- It reuses the same style and overall visual layout as your existing servomotor datasheet so the two documents look like they belong to the same product family. The hero area now includes the identical Gearotons slogan (“Affordable and Simple All-in-One Motion Control” / “From Education to Innovation”) rendered in the same green color used on the servomotor datasheet, and it loads the RS485 adapter photos directly from `/Users/tom/Pictures/adapter/RS485_adapter_20250714153203.jpg` and `/Users/tom/Pictures/adapter/RS485_adapter_20250714153158.jpg` without copying or symlinking them.
- It inserts the existing connection diagram drawing in the appropriate section of the datasheet.
- It uses some simple text files or placeholders for things like the introduction and feature list so you can edit the words without touching the code.
- At the end it saves a new PDF and also a “latest” copy that always reflects the newest datasheet version.
- We should keep a vector based representation of the datasheet as opposed to convertiong it to a raster based image, so as to keep high quality test at any resolution.

## 3. How the latest schematic will be chosen
- The program looks at the different PCB revision folders for the RS485 adapter.
- It only considers folders whose names look like version numbers (for example 1.0, 1.2, 1.20.5).
- It compares these version numbers and chooses the highest one as “latest”.
- Inside that latest version, it expects to find a schematic PDF with a name like “1.2-index-schTop.pdf”.
- the name of the schematic diagram file has a version number in it. This must match the directory version number, the directoy being a subdirectory of PCB/
- If the expected file name is missing but there are other similar schematic files with “index-schTop” in the name, it should ignore it and print out an error which includes the name of the file that it specifically is looking for and exit right away. It should advise that the user needs to export the schematic diagram from KiCAD.

## 4. Connection diagram
- The datasheet will include a “Connection Diagram” section that uses the same drawing you already use for the servomotor datasheet.
- We should make a symlink in the current directoy to the real connection diagram file. Make sure you link to the actual file and not to some symlink that may exist already.
- This gives readers a familiar, high-level picture of how the RS485 adapter fits into a system.

## 5. Main headings that will appear in the datasheet
These are the top-level sections the reader will see, in order:
- RS485 Adapter Overview (short introduction)
- Key Features
- Connection Diagram
- Schematic (Latest Revision)
- Electrical Specifications
- Mechanical and Interface Details
- Getting Started
- Feedback and Support
- Company and Open-Source Information
- Datasheet Version and Release Date

## 6. What you will be able to edit easily
You will be able to change the following without touching the program logic:
- The introduction text that describes the RS485 adapter at a high level.
- The list of key features.
- The numbers and text in the specification tables (for example voltage range, current consumption, connector pinout notes).
- The list of datasheet versions and release dates.

