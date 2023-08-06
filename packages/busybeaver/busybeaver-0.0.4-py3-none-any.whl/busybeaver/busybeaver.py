import configparser
import logging
from .constants import *

logging.basicConfig(filename='bb.log', level=logging.DEBUG)

class Hut:
    """
    Main class for setting up single/batch post processing

    Usage example:
    process_manager = Hut("config.ini")
    """
    def __init__(self, config_file = None):
      
        self.config_file = config_file
        self.models = {}

        if self.config_file != None:
            self.loadConfig(self.config_file)

    # Allows returning model object by indexing the hut by with model name
    #   e.g. model = myhut["modelname"]
    #   (same as doing myhut.models["modelname"])

    def __getitem__(self, indices):
        # caution: no support for integer indices or slicing etc.
        return self.models[indices]


    def loadConfig(self, config_file):
        """
        Loads a configuration .ini file into the hut.
        """

        # Read the config file
        logging.info("Reading config file.")
        config = configparser.ConfigParser()
        config.read(self.config_file)

        # Create empty Model objects for each model
        models = config.sections()[1:]
        for name in models:
            new_model = Model(name)
            self.models[name] = new_model
            logging.info("Created model for {}.".format(new_model.name))
        

class Model:
    """
    A class for holding information related to a single model

    Usage example:
    cool_model = Model("Name of model")

    Note: Model instances are intended to be initialized through the Hut object
    """
    def __init__(self, model_name):

        self.name = model_name
        self.results = {}
        self.pfiles = {}
        self.runstack = []

    def addFile(self, file_type, file_path):

        if (file_type in RESULT_FILE_TYPES):
            self.results[file_type] = file_path
        elif (file_type in PROCESSING_FILE_TYPES):
            self.pfiles[file_type] = file_path
        else:
            logging.error("{} not a valid file type. Check constants.py for valid types.".format(file_type))

    # NOTE: Need to add a way for operations to accept arguments
    def addOperation(self, operation, *args):

        if (operation in OPERATIONS):
            self.runstack.append([operation, args])
        else:
            logging.error("{} not a valid operation type. Check constants.py for valid types.".format(operation))