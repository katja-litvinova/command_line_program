This is a command line program to check the search results for the page: https://yousician.com/songs.
It prints all the found songs in alphabetical order, sorted primarily by the artist name, and then by the song name.

# Instruction for using:

1. Install python 3.9
2. Install pip 21.1.2
3. Create a virtual environment:

    ```bash
    pip install virtualenv
     cd ~/test_automation_assignment
    virtualenv ./venv
    ```

4. Activate a virtual environment:

    ```bash
    cd ~/test_automation_assignment
    source venv/bin/activate
    ```

5. Install the necessary environment requirements (libraries, modules, packages etc.):

    ```bash
    pip install -r requirements.txt
    ```

6. Download [Chromdriver](https://chromedriver.chromium.org/downloads), place it in venv/bin
7. Execute the program from the terminal via the command:

    ```bash
    python search.py --search "song or artist"
    ```
    If your search argument has more than one word then use double quotes, for example:
	
   ```bash
    python search.py --search "the yousicians"
    ```

