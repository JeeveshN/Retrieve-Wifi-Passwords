
from PassRetrievalTool import PassRetrievalTool # Import the class

class PassRetrievalTool_test:

    def __init__(self):
        wifi_password_dictionary = PassRetrievalTool.get_all_wifi_password_dictionary() # Call the static method get_wifi_password_dictionary() and save it

        PassRetrievalTool.print_passwords(wifi_password_dictionary) # Print them or do whatever you want.

if __name__ == "__main__":
    test = PassRetrievalTool_test()
