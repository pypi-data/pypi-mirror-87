import os
import time
from io import BytesIO
from zipfile import ZipFile

import requests
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


__version__ = "0.0.1"


CSV='csv'
JSON='json'
XLSX='xlsx'
PNG='png'
JPG='jpg'
PDF='pdf'


class MetbaseUtils:
    """
    This class is used to export 'question' and 'dashboard' in Metabase business intelligence tool (see https://www.metabase.com)
    ...

    Attributes
    ----------
    chrome_driver_path : str
        The absolute file path the Chrome driver
    metabase_host : str
        The host IP address or host name where Metabase service is running
    metabase_port : int
        The port number where Metabase service is running on
    metabase_user : str
        The username used to login into Metabase
    metabase_password: str
        The password used to login into Metabase
    output_dir: str, optional
        The output directory for the downloaded files, default is current working directory
    Methods
    -------
    export_question(id, output_dir, with_data=True, with_visualization=True, data_format=XLSX,
        visualization_format=PDF, package_as_zip=True, single_pdf=False)
        Optionally packages and exports the specified question by its id into a zip file or separate data and visualization files
    export_dashboard()
        TODO
    """
    def __init__(self, chrome_driver_path, metabase_host, metabase_port, metabase_user, metabase_password, output_dir=None):
        """
        Parameters
        ----------
        name : str
            The name of the animal
        sound : str
            The sound the animal makes
        num_legs : int, optional
            The number of legs the animal (default is 4)
        """
        self.chrome_driver_path = chrome_driver_path
        self.metabase_host = metabase_host
        self.metabase_port = metabase_port
        self.metabase_user = metabase_user
        self.metabase_password = metabase_password
        self.output_dir = os.getcwd() if output_dir is None else output_dir
    
    def _get_data(self, data_format):
        pass

    def _get_visualization(self):
        pass
    
    def _package_files(self):
        pass
    
    def export_question(self,
                        id,
                        with_data=True,
                        with_visualization=True,
                        data_format=XLSX,
                        visualization_format=PDF,
                        package_as_zip=True,
                        single_pdf=False,
                        output_dir=None):
        """TODO

        Parameters
        ----------
        id : int, optional
            The sound the animal makes (default is None)

        Raises
        ------
        NotImplementedError
            If no sound is set for the animal or passed in as a
            parameter.
        """
        if with_data:
            self._get_data(data_format, output_dir)
    
    def export_dashboard(self, id, output_dir=None):
        """Prints what the animals name is and what sound it makes.

        If the argument `sound` isn't passed in, the default Animal
        sound is used.

        Parameters
        ----------
        sound : str, optional
            The sound the animal makes (default is None)

        Raises
        ------
        NotImplementedError
            If no sound is set for the animal or passed in as a
            parameter.
        """
        pass
