#
#     Kwola is an AI algorithm that learns how to use other programs
#     automatically so that it can find bugs in them.
#
#     Copyright (C) 2020 Kwola Software Testing Inc.
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU Affero General Public License as
#     published by the Free Software Foundation, either version 3 of the
#     License, or (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU Affero General Public License for more details.
#
#     You should have received a copy of the GNU Affero General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.
#


from ..config.config import KwolaCoreConfiguration
from ..tasks import TrainAgentLoop
from ..diagnostics.test_installation import testInstallation
import os.path
import questionary
import sys
from ..config.logger import getLogger, setupLocalLogging
import logging


def getConfigurationDirFromCommandLineArgs(askTuneQuestion=True):
    """
        This function is responsible for parsing the command line arguments and returning a directory containing a
        Kwola configuration. If none exists, a new Kwola configuration will be created.

        :return: A string containing the directory name with the configuration.
    """

    commandArgs = sys.argv[1:]

    cantStartMessage = """
    Error! Can not start .. You must provide either a web URL or the directory name of an existing Kwola run. 
    The URL must be a valid url including the http:// part. If a directory name, the directory must be accessible
    from the current working folder, and must have the ..json configuration file contained within it.
    Please try again.
        """

    configDir = None

    if len(commandArgs) == 0:
        configDir = KwolaCoreConfiguration.findLocalKwolaConfigDirectory()
        if configDir is None:
            print(cantStartMessage)
            exit(1)
        else:
            print(f"Loading the Kwola run in directory {configDir}")

    elif len(commandArgs) >= 1:
        secondArg = commandArgs[0]

        configName = None

        if len(commandArgs) >= 2:
            configName = commandArgs[1]

        if os.path.exists(secondArg) and KwolaCoreConfiguration.checkDirectoryContainsKwolaConfig(secondArg):
            configDir = secondArg
            print(f"Loading the Kwola run in directory {configDir}")
        elif KwolaCoreConfiguration.isValidURL(secondArg):
            # Create a new config directory for this URL
            url = secondArg

            if configName is None:
                configName = questionary.select(
                    "Which configuration do you want to load for your model?",
                    choices=[
                        'small',
                        'medium',
                        'large',
                        'testing',
                        'standard_experiment',
                        'pure_random'
                    ]).ask()  # returns value of selection

            if configName is None:
                exit(0)

            email = questionary.text("What is the email/username you want to use (blank disables this action)?").ask()
            if email is None:
                exit(0)

            password = questionary.text("What is the password you want to use (blank disables this action)?").ask()
            if password is None:
                exit(0)

            name = questionary.text("What is the human name / short text you want to use (blank disables this action)?").ask()
            if name is None:
                exit(0)

            paragraph = questionary.text("What is the paragraph / long text you want to use (blank disables this action)?").ask()
            if paragraph is None:
                exit(0)

            commandChoices = [
                "Enable random number command?",
                "Enable random bracket command?",
                "Enable random math symbol command?",
                "Enable random other symbol command?",
                "Enable double click command?",
                "Enable right click command?",
                "Enable scrolling command?",
                "Enable type random letters command?",
                "Enable type random address command?",
                "Enable type random email command?",
                "Enable type random phone command?",
                "Enable type random paragraph command?",
                "Enable type random date time command?",
                "Enable type random credit card command?",
                "Enable type random url command?"
            ]

            results = questionary.checkbox("Please select which commands you want to enable", choices=commandChoices).ask()
            if results is None:
                exit(0)

            enableRandomNumberCommand = bool(commandChoices[0] in results)
            enableRandomBracketCommand = bool(commandChoices[1] in results)
            enableRandomMathCommand = bool(commandChoices[2] in results)
            enableRandomOtherSymbolCommand = bool(commandChoices[3] in results)
            enableDoubleClickCommand = bool(commandChoices[4] in results)
            enableRightClickCommand = bool(commandChoices[5] in results)
            enableScrolling = bool(commandChoices[6] in results)
            enableRandomLettersCommand = bool(commandChoices[7] in results)
            enableRandomAddressCommand = bool(commandChoices[8] in results)
            enableRandomEmailCommand = bool(commandChoices[9] in results)
            enableRandomPhoneNumberCommand = bool(commandChoices[10] in results)
            enableRandomParagraphCommand = bool(commandChoices[11] in results)
            enableRandomDateTimeCommand = bool(commandChoices[12] in results)
            enableRandomCreditCardCommand = bool(commandChoices[13] in results)
            enableRandomURLCommand = bool(commandChoices[14] in results)

            autologin = False

            if email and password:
                autologin = questionary.select(
                    "Do you want Kwola to attempt automatic heuristic email/password login upon landing at the given URL?",
                    choices=[
                        'yes',
                        'no'
                    ]).ask()  # returns value of selection
                if autologin is None:
                    exit(0)

            autologin = bool(autologin == 'yes')

            prevent_offsite_links = questionary.select(
                "Do you want Kwola to stay on the website it starts on (prevent offsite links)?",
                choices=[
                    'yes',
                    'no'
                ]).ask()  # returns value of selection
            if prevent_offsite_links is None:
                exit(0)

            prevent_offsite_links = bool(prevent_offsite_links == 'yes')

            configDir = KwolaCoreConfiguration.createNewLocalKwolaConfigDir(configName,
                                                                            url=url,
                                                                            email=email,
                                                                            password=password,
                                                                            name=name,
                                                                            paragraph=paragraph,
                                                                            enableTypeEmail=True,
                                                                            enableTypePassword=True,
                                                                            enableRandomNumberCommand=enableRandomNumberCommand,
                                                                            enableRandomBracketCommand=enableRandomBracketCommand,
                                                                            enableRandomMathCommand=enableRandomMathCommand,
                                                                            enableRandomOtherSymbolCommand=enableRandomOtherSymbolCommand,
                                                                            enableDoubleClickCommand=enableDoubleClickCommand,
                                                                            enableRightClickCommand=enableRightClickCommand,
                                                                            enableRandomLettersCommand=enableRandomLettersCommand,
                                                                            enableRandomAddressCommand=enableRandomAddressCommand,
                                                                            enableRandomEmailCommand=enableRandomEmailCommand,
                                                                            enableRandomPhoneNumberCommand=enableRandomPhoneNumberCommand,
                                                                            enableRandomParagraphCommand=enableRandomParagraphCommand,
                                                                            enableRandomDateTimeCommand=enableRandomDateTimeCommand,
                                                                            enableRandomCreditCardCommand=enableRandomCreditCardCommand,
                                                                            enableRandomURLCommand=enableRandomURLCommand,
                                                                            enableScrolling=enableScrolling,
                                                                            autologin=autologin,
                                                                            prevent_offsite_links=prevent_offsite_links
                                                                            )
            if askTuneQuestion:
                needToChange = questionary.select(
                    "Do you want to tune any configuration settings in your Kwola run before proceeding?",
                    choices=[
                        'no',
                        'yes'
                    ]).ask()  # returns value of selection

                if needToChange == "yes":
                    print(f"Please see the configuration file {os.path.join(configDir, 'kwola.json')} for all of the settings that you can tune in this Kwola run.")
                    print(f"When you are ready, simply run the following command to restart Kwola with your updating settings:")
                    print(f"kwola {configDir}")
                    exit(0)

            ready = questionary.select(
                "Are you ready to unleash the Kwolas?",
                choices=[
                    'yes',
                    'no'
                ]).ask()  # returns value of selection

            if ready == "no":
                exit(0)

            print(f"")
            print(f"Starting a fresh Kwola run in directory {configDir} targeting URL {url}")
            print(f"", flush=True)
        else:
            print(cantStartMessage)
            exit(2)

    return configDir


def main():
    """
        This is the entry point for the main Kwola application, the console command "kwola".
        All it does is start a training loop.
    """
    setupLocalLogging()
    success = testInstallation(verbose=True)
    if not success:
        print(
            "Unable to start the training loop. There appears to be a problem "
            "with your Kwola installation or environment. Exiting.")
        exit(1)

    configDir = getConfigurationDirFromCommandLineArgs()
    TrainAgentLoop.trainAgent(configDir)
