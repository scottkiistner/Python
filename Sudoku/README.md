# Python
A simple Sudoku app that generates a solvable sudoku puzzle for the user to solve
Each puzzle is random, unique and procedurally generated
The App's display/input functionality runs on Pygame

=CONTROLS=
[Tab] - Switches input mode
  -> If the highlights are yellow, inputs will be full box numbers
  -> If the highlights are blue, inputs will be pencil marks
[1-9] - Inputs the respective number of the keyboard
  -> If the highlights are yellow, the input overwrites editable cells
  -> If the highlights are blue, the input toggles for all selected cells
[LMB] - Highlights a cell to be edited, can be held to select multiple cells
[RMB] - Highlights all cells of the same number (Only filled Cells)
[BACKSPACE] - Clears a filled Cell
