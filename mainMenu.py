import menuUi

class Menu:


    exit_funct = None

    def set_functions_by_name(self, name, funct):
        print(name)
        if name == "exit":
            self.exit_funct = funct
            print("jjjjjj")


    # button functions
    def test_button_function(self):
        print("Buttons Pressed")


    def initialize_menu(self):
        # define buttons
        menu_ui = menuUi.UiMenu()
        menu_ui.add_button_type("default", None, None, None, (450, 50))
        menu_ui.add_button_type("back", None, None, None, (200, 50))


        menu_ui.add_menu("Main Menu")
        menu_ui.add_button("Main Menu", "default", "Start Game", (150, 250), self.test_button_function)
        menu_ui.add_button("Main Menu", "default", "Options", (150, 350), self.test_button_function)
        menu_ui.add_button("Main Menu", "default", "Quit", (150, 450), self.exit_funct)

        menu_ui.add_menu("Options")
        menu_ui.add_button("Options", "back", "Back", (75, 500), self.test_button_function)

        # set the menu to the default menu
        menu_ui.set_current_menu("Main Menu")

        return menu_ui
