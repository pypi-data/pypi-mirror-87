from os import name as osname
import json
import version


class YACT:

    title = """
    $$\\     $$\\  $$$$$$\\   $$$$$$\\ $$$$$$$$\\ 
    \\$$\\   $$  |$$  __$$\\ $$  __$$\\__$$  __|
     \\$$\\ $$  / $$ /  $$ |$$ /  \\__|  $$ |    
      \\$$$$  /  $$$$$$$$ |$$ |        $$ |    
       \\$$  /   $$  __$$ |$$ |        $$ |    
        $$ |    $$ |  $$ |$$ |  $$\\   $$ |    
        $$ |    $$ |  $$ |\\$$$$$$  |  $$ |    Yet Another CTF Tool v{version}
        \\__|    \\__|  \\__| \\______/   \\__|    by Fabien "BioTheWolff" Z.
    """
    config = None

    #
    # UTILS
    #
    def get_config(self):
        try:
            with open('/etc/starct/config.json') as f:
                self.config = json.loads(f.read())
        except OSError:
            self.config = False
        except json.JSONDecodeError:
            self.config = []

    #
    # DUNDERS
    #
    def __init__(self):
        # Checking compatibility
        if osname != 'posix':
            print("YACT only supports POSIX systems for now!")
            exit(1)

        self.get_config()
        self.title = self.title.replace("{version}", version.version)

        self.__call__()

    def __call__(self):
        print(self.title)


if __name__ == '__main__':
    YACT()
