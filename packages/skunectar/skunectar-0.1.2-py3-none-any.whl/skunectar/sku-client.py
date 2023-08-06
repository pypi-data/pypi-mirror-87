__author__='njorgensen@skupos.com'

import pandas as pd
import snowflake.connector
from dotenv import load_dotenv
import os, sys

class SkuposSnowSQLClient:
    
    """
    A simple class used to represent a Python connection to Snowflake

    ...

    Attributes
    ----------
    dotenv_path : str
        the location to your configuration environment (e.g. /Users/.../config.env)
    con_kwargs : dict[str, str]
        a keyword mapping of connection arguments parsed from the dotenv_path

    Methods
    -------
    fetch_data(sql, params=None)
        Given string-encased piece of SQL, fetch a Pandas DataFrame representation of the ouput table
    """
    
    def __init__(self, dotenv_path):
        self.dotenv_path = dotenv_path
        self.load_and_confirm_credentials(self.dotenv_path)
        self.con_kwargs = self.retrieve_con_kwargs()
        
    def load_and_confirm_credentials(self):    
        """Parses the .env file and loads the variables into os.
        
        Will raise errors (verbose=True) if file doesn't exist, etc.
        """
        load_dotenv(dotenv_path=self.dotenv_path, verbose=True)
        
    def retrieve_con_kwargs(self):
        """Returns con_kwargs, the args used for the Snowflake connection
        """
        return {'user':      os.getenv("SNOWFLAKE_USER"),
                'password':  os.getenv("SNOWFLAKE_PASSWORD"),
                'account':   os.getenv("SNOWFLAKE_ACCOUNT"),
                'warehouse': os.getenv('SNOWFLAKE_WAREHOUSE'),
                'role':      os.getenv('SNOWFLAKE_ROLE')
               }
    
    def connect(self):
        """Utility function to connect to Snowflake using the con_kwargs
        """
        try:
            conn = snowflake.connector.connect(**self.con_kwargs)
            cur = conn.cursor()
            return conn, cur
        except:
            print("Unexpected Error:", sys.exc_info()[0])
            
            
    def fetch_data(self, sql, params=None):
        """Returns a Pandas DataFrame holding the desired SQL table.

        Parameters
        ----------
        sql : str, required
            The query used to get the desired data
        params : dict, optional
            Optional params to use within the execution, e.g. limits, timeouts, etc. (default is None)
        """
        conn, cur = self.connect()
        try:
            cur.execute(sql, params)
            df = cur.fetch_pandas_all()
            df.columns = [col.lower() for col in df.columns]
        finally:
            cur.close()
        conn.close()
        return df
