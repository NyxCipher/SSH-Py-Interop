from simple_term_menu import TerminalMenu

# Define submenus
submenu1 = TerminalMenu(["Submenu 1 Option 1", "Submenu 1 Option 2", "Submenu 1 Option 3"])
submenu2 = TerminalMenu(["Submenu 2 Option 1", "Submenu 2 Option 2", "Submenu 2 Option 3"])

# Define the main menu with submenus
main_menu = TerminalMenu(["Serverz", "Processez", "Controlz", "Exit"])

while True:
    # Show the main menu and get the selected option index
    main_menu_entry_index = main_menu.show()

    if main_menu_entry_index is None or main_menu_entry_index == 3:
        # Exit the program
        break
    elif main_menu_entry_index == 0:
        # User selected Option 1, show submenu 1
        submenu1_entry_index = submenu1.show()
        if submenu1_entry_index is not None:
            print(f"Selected submenu 1 option: {submenu1_entry_index + 1}")
    elif main_menu_entry_index == 1:
        # User selected Option 2, show submenu 2
        submenu2_entry_index = submenu2.show()
        if submenu2_entry_index is not None:
            print(f"Selected submenu 2 option: {submenu2_entry_index + 1}")
