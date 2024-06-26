import time
import socket
import threading
import os
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, WebDriverException, TimeoutException
from selenium.webdriver import Chrome, ChromeOptions
import threading

class Twitter:
    class TwitterLocator:
        SIGN_IN_BTN = """
                        return Array.from(document.querySelectorAll('span')).find(span => span.textContent.trim() === 'Sign in');
                      """
        SIGN_IN_USERNAME_INPUT = (By.XPATH, '//input[@autocomplete="username"]')
        SIGN_IN_PASSWORD_INPUT = (By.XPATH, '//input[@autocomplete="current-password"]')
        POST_SUBMIT_BUTTON = (By.XPATH, '//button[@data-testid="tweetButtonInline"]')
    

    def __init__(self,username: str =None, password: str= None, chrome_path = None, chrome_driver_path = None, chrome_profile_path: str = None):
        self.chrome_profile_path = chrome_profile_path
        self.url = r"https://x.com/"
        free_port = self.find_available_port()
        self.driver = self.setup_chrome(free_port)
        self.driver.get(self.url)
        self.username = username
        self.lock = threading.Lock()
        self.password = password
        self.wait_for_human_verification()

    def wait_for_human_verification(self):
        """
        Pauses the automation process and waits for the user to manually complete tasks such as log-in
        or human verification, which are not automatable. The function repeatedly prompts the user until
        they confirm the completion of the manual task.

        Returns:
            None

        Raises:
            SystemExit: If an unrecoverable input error occurs, indicating a problem with the system or environment.
        """
        with self.lock:
            print("You need to manually complete the log-in or the human verification if required.")

            while True:
                try:
                    user_input = input(
                        "Enter 'y' if you have completed the log-in or the human verification, or 'n' to check again: ").lower()
                except EOFError:
                    # Print error message and exit the program in case of an End-Of-File condition on input
                    print("Error reading input. Exiting the program.")
                    raise SystemExit("Failed to read user input.")  # Exiting the program due to input error

                # Check the user's input and act accordingly
                if user_input == 'y':
                    print("Continuing with the automation process...")
                    break  # Break the loop to continue with automation
                elif user_input == 'n':
                    print("Waiting for you to complete the human verification...")
                    time.sleep(5)  # Waiting for a specified time before asking again
                else:
                    print("Invalid input. Please enter 'y' or 'n'.")  # Handle invalid input

    def click_on_sign_in_btn(self):
        self.driver.execute_script(self.TwitterLocator.SIGN_IN_BTN).click()

    def fill_username_input(self, username: str = None):
        if username is None:
            username = self.username
        self.driver.find_element(*self.TwitterLocator.SIGN_IN_USERNAME_INPUT).send_keys(username)
    
    def fill_password_input(self, password: str = None):
        if password is None:
            password = self.password
        self.driver.find_element(*self.TwitterLocator.SIGN_IN_PASSWORD_INPUT).send_keys(password)

    def click_on_post_section(self):
        t.driver.execute_script("""
                        return Array.from(document.querySelectorAll('div')).find(span => span.textContent.trim() === 'What is happening?!');
                      """).click()

    def type_in_post_section(self, text):
        editor = self.driver.find_element(By.CSS_SELECTOR, '[data-contents="true"]')
        editor.click()

        for char in text:
            if char == '\n':
                editor.send_keys(Keys.ENTER)
            else:
                editor.send_keys(char)


    def setup_chrome(self, port: int) -> Chrome:
        options = ChromeOptions()
        options.add_argument(f"--remote-debugging-port={port}")
        if self.chrome_profile_path:
            options.add_argument(f"--user-data-dir={self.chrome_profile_path}")
        return Chrome(options=options)
    
    def post_send_submit(self):
        self.driver.find_element(*self.TwitterLocator.POST_SUBMIT_BUTTON).click()
    
    def find_available_port(self):
        """
        Finds and returns an available port number on the local machine.
        It does this by creating a temporary socket, binding it to an ephemeral port,
        and then closing the socket to free the port for use.

        Returns:
            available_port (int): The available port number found.

        Raises:
            Exception: If the function fails to find an available port due to a socket error.
        """
        try:
            # Create a socket object using IPv4 addressing and TCP
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                # Bind the socket to any available address on the machine ('') and port 0
                # The OS will then automatically assign an available ephemeral port
                s.bind(('', 0))

                # Set socket options - SO_REUSEADDR allows the socket to be bound to an address
                # that is already in use, which is useful for avoiding socket errors
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

                # Retrieve the port number assigned by the OS
                available_port = s.getsockname()[1]

                # Return the found port
                return available_port

        except socket.error as e:
            # Raise a new exception for the calling code to handle
            raise Exception("Failed to find an available port") from e
    

    def send_post(self, text):
        self.click_on_post_section()
        self.type_in_post_section(text)
        self.post_send_submit()
    


