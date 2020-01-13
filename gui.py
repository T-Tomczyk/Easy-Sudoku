# Modules
import PySimpleGUI as sg
import copy

# File
import easy_sudoku as es

# Theme, only for esthetics.
sg.theme('Light Blue 3')

# Enforces continuos operation of the program until user exits.
running = True
while running:

    # Generate a puzzle and a solution to it.
    puzzle = []
    puzzle_list = []
    solution_list = []
    def generate_puzzle_and_solution():
        global puzzle
        global puzzle_list
        global solution_list
        puzzle = es.generate_grid()
        puzzle_list = es.to_list(puzzle)
        solution_list = es.to_list(es.solve_grid(puzzle))

    # Initial call.
    generate_puzzle_and_solution()

    # Create a list of square IDs with changable values (not pre-determined clues).
    changable_square_IDs = []
    for square_id in range(len(puzzle_list)):
        if puzzle_list[square_id] == 0:
            changable_square_IDs.append(square_id)

    # Displays a new small pop-up window with a keypad for entering values into squares.
    # Returns clicked value or ' ' if 'clear' or current_value if 'cancel'.
    def pop_numpad(current_value, square_id):
        def create_button(number):
            return sg.Button(str(number), size=(4,2), pad=(1,1), button_color=('white','#202020'))

        layout = [
            [create_button(1), create_button(2), create_button(3)],
            [create_button(4), create_button(5), create_button(6)],
            [create_button(7), create_button(8), create_button(9)],
            [
                sg.Button('Clear', size=(6,2), pad=(1,1), button_color=('white','#202020')),
                sg.Button('Cancel', size=(7,2), pad=(1,1), button_color=('white','#202020'))
            ],
        ]

        window = sg.Window('',layout)

        while True:
            event, value = window.read()
            if event in (None, 'Cancel'):
                if current_value != 0:
                    clicked = current_value
                else:
                    clicked = ' '
                break
            elif event == 'Clear':
                puzzle_list[square_id] = 0
                clicked = ' '
                break
            elif event in ('1','2','3','4','5','6','7','8','9'):
                puzzle_list[square_id] = int(event)
                clicked = int(event)
                break
        window.close()

        return clicked

    # Returns lists of buttons representing one row. Used to create the grid layout with.
    # Formats the buttons with color to make each of the 3x3 regions distinguishable.
    # Also differentiates between clickable (playable) buttons and pre-determined ones (clues).
    def button_row_layout(row_index):
        global puzzle_list

        # Creates a new button with given characteristics.
        # i: button id from 0 to 80
        # color: 0 for main color and 1 for secondary color
        # clickable: True (playable by user) or False (pre-determined clue)
        def new_button(i, color, clickable):
            value_to_insert = puzzle_list[i]
            if value_to_insert == 0:
                value_to_insert = ' '

            if color == 0:
                if clickable:
                    return sg.Button(value_to_insert, key=i, size=(4,2), pad=(1,1),
                        button_color=('#22bdff','#202020'))
                else:
                    return sg.Button(value_to_insert, key=i, size=(4,2), pad=(1,1),
                        button_color=('#ffffff','#202020'))
            else:
                if clickable:
                    return sg.Button(value_to_insert, key=i, size=(4,2), pad=(1,1),
                        button_color=('#22bdff','#050505'))
                else:
                    return sg.Button(value_to_insert, key=i, size=(4,2), pad=(1,1),
                        button_color=('#ffffff','#050505'))

        # Empty list which will be later appended and at the end returned.
        result = []

        # Iterates through all square indexes iwithin given row (eg. 0-8 for row 0 or 18-26 for row 2).
        for i in range(row_index*9, row_index*9+9):

            # Decide if given button should be clickable (playable) or not (clue).
            if puzzle_list[i] == 0:
                clickable = True
            else:
                clickable = False

            # Decide if given button should be main or secondary color (based on location).
            if row_index in range(0,3) or row_index in range(6,9):
                if i in range(row_index*9+3, row_index*9+6):
                    color = 0
                else:
                    color = 1
            else:
                if i in range(row_index*9, row_index*9+3) or i in range(row_index*9+6, row_index*9+9):
                    color = 0
                else:
                    color = 1

            result.append(new_button(i, color, clickable))

        return result

    # Main layout.
    layout = [
        [sg.Button('New Game'), sg.Button('Submit'), sg.Text('', key='user_message', size=(24,2))],
    ]

    # Initial insetion of a puzzle into the main window.
    for row_index in range(9):
        layout.append(button_row_layout(row_index))

    # Insert new puzzle into window.
    def new_game():
        generate_puzzle_and_solution()
        global puzzle_list
        for square_id in range(81):
            if puzzle_list[square_id] == 0:
                window[square_id].update(' ')
            else:
                window[square_id].update(puzzle_list[square_id])

    # Show the main window to the user.
    window = sg.Window('Easy Sudoku', layout)

    # Main single game window loop.
    while True:
        # Continous reading of window events.
        event, value = window.read()

        # Top bar menu buttons.
        if event in ('Quit', None):
            running = False
            break
        elif event == 'Submit':
            if puzzle_list == solution_list:
                window['user_message'].update('Congratulations! You solved it.')
            else:
                window['user_message'].update('Incorrect.')
        elif event == 'New Game':
            window['user_message'].update('')
            running = True
            break

        # Grid buttons.
        for square_id in changable_square_IDs:
            if event == square_id:
                window[square_id].update(pop_numpad(puzzle_list[square_id], event))

    window.close()