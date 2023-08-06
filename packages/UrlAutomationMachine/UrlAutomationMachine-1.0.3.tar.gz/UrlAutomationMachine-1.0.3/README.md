# URLAutomationMachine

The machine we all need but the one we most likely do not deserve. The url checking program we all desire

# Features:

- Uses regex to parse each line for a url
- Processes each request and checks status code for successful attempt
- Any url with a status code around ```200``` will pass automation
- Urls with a status code of ```404``` or ```400``` will fail automation
- Urls with a status code that is unknown ```403``` will fail automation but will be displayed in grey colouring
- Flags are used to pass in filenames and describe the version of the file.
- ```-j``` option allows for program to display the output in a JSON format

# Contributing:

I welcome any and all contributions to this project. Please make sure to follow the instructions in the contributing
file in order to effectively develop on this project.
You can read more [here](CONTRIBUTING)

# Licensing:

This project is distributed under the MIT License which can be found [here](LICENSE)
