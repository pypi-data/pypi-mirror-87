import json
import os

import requests
import pandas as pd

class SubstancesClient(object):

    def __init__(self,service_url='',api_key=''):
        """Client initializer.

        Default credentials are read in from a file,
        $HOME/.aionics_substances_key, if available.
        This file should have the service URL on line 1,
        and the API key on line 2.
        Initialization arguments take precedence over key file entries. 

        Parameters
        ----------
        service_url : str
            Web URL pointing to an Aionics substances application
        api_key : str
            API authorization key for the application 
        """
        super(SubstancesClient,self).__init__()

        if not service_url or not api_key:
            if service_url:
                raise RuntimeError('An api_key is required')
            if api_key:
                raise RuntimeError('A service_url is required')
            homedir = os.path.expanduser('~')
            hostfile = os.path.join(homedir,'.aionics_substances_key')
            with open(hostfile,'r') as f:
                service_url = str(f.readline().strip())
                api_key = str(f.readline().strip())
        if not service_url[-1] == '/': service_url = service_url + '/'

        connect_url = service_url+'connect_client'
        sess = requests.Session()
        resp = sess.post(connect_url,headers={'x-api-key':api_key})
        if resp.status_code == 200:
            resp = resp.json()
            if resp['success']:
                self.service_url = service_url
                self.api_key = api_key
                self.session = sess
            else: 
                raise ConnectionError('connection unsuccessful: {}'.format(resp))
        else:
            raise RuntimeError('failed to connect to {} ({})'.format(service_url,resp.status_code))

    # SUBSTANCES

    def add_substance(self,name,source='',other_names=[],descriptors={},properties={},documents={}):
        """Add a Substance to the database.

        A Substance is defined by a name and a set of descriptors.
        Optionally, the substance source data may be attached as a string.
        Optionally, any number of aliases may be assigned to the Substance.

        Parameters
        ----------
        name : str
            A name for the Substance.
            If this name already exists in the database,
            the add_substance operation will fail.
        source : str
            A representation of the structure of the Substance,
            sufficient for extracting descriptors.
            For example, a molecule might be represented by a SMILES string,
            and a crystalline solid might be represented by a CIF file.
        other_names : list
            Any number of additional names to assign to the Substance.
            Substance names must be unique, so if any of these names
            are already assigned to substances in the database,
            this operation will fail.
        descriptors : dict
            Keys are descriptor names, and values are descriptor values.
            Descriptors are used to encode substances for modeling,
            so they are expected to be real-valued.
        properties : dict
            Keys are property names, and values are property values.
            This is intended for storing properties 
            that can be described by a single number,
            such that these properties can be used for rapid filtering.
            Properties with complicated structure 
            (e.g. multiple measurements at different conditions)
            should be stored in documents.
        documents : dict
            Keys are document names, and values are document full texts.
            This should be used to store any substance data
            that do not fit neatly as descriptors or properties.

        Returns
        -------
        response : dict
            Dict containing status report.
        """
        resp = self.session.post(
            self.service_url+'add_substance', 
            headers={'x-api-key':self.api_key},
            json={
                'name':name,
                'descriptors':descriptors,
                'properties':properties,
                'documents':documents,
                'source':source,
                'other_names':other_names
            }
        )
        if resp.status_code == 200:
            respdata = resp.json()
            return respdata
        else:
            return {'success':False,'status_code':resp.status_code}

    def update_substance(self,substance_name,source='',other_names=[],descriptors={},properties={},documents={}):
        """Update the attributes of an existing substance

        Parameters
        ----------
        substance_name : str
            A name that is already assigned to the Substance of interest. 
        source : str
            A string representing of the structure of the Substance,
            sufficient for extracting descriptors.
        other_names : list
            Any number of additional names to assign to the Substance.
        descriptors : dict
            Keys are descriptor names, and values are descriptor values.
        properties : dict
            Keys are property names, and values are property values.
        documents : dict
            Keys are document names, and values are document full texts.

        Returns
        -------
        response : dict
            Dict containing status report and results.
        """
        resp = self.session.post(
            self.service_url+'update_substance', 
            headers={'x-api-key':self.api_key},
            json={
                'substance_name':substance_name,
                'source':source,
                'other_names':other_names,
                'descriptors':descriptors,
                'properties':properties,
                'documents':documents
            }
        )
        if resp.status_code == 200:
            respdata = resp.json()
            return respdata
        else:
            return {'success':False,'status_code':resp.status_code}


    # DESCRIPTORS

    def check_substance_names(self,substance_names):
        """Check for existence of substances by name.

        Parameters
        ----------
        substance_names : list
            List of names (strings) to be checked.

        Returns
        -------
        response : dict
            Dict containing status report and results.
        """
        resp = self.session.post(
            self.service_url+'check_substance_names', 
            headers={'x-api-key':self.api_key},
            json={'substance_names':substance_names}
        )
        if resp.status_code == 200:
            respdata = resp.json()
            return respdata
        else:
            return {'success':False,'status_code':resp.status_code}

    def add_substance_names(self,substance_name,other_names):
        """Add aliases to a Substance in the database.

        Parameters
        ----------
        substance_name : str
            A name that is already assigned to the Substance of interest. 
        other_names : list
            Any number of additional names to assign to the Substance.
            Substance names must be unique, so if any of these names
            are already assigned to substances in the database,
            this operation will fail.

        Returns
        -------
        response : dict
            Dict containing status report and results.
        """
        resp = self.session.post(
            self.service_url+'add_substance_names', 
            headers={'x-api-key':self.api_key},
            json={
                'substance_name':substance_name,
                'other_names':other_names
            }
        )
        if resp.status_code == 200:
            respdata = resp.json()
            return respdata
        else:
            return {'success':False,'status_code':resp.status_code}


    def get_descriptors(self,substance_names,descriptor_names=[]):
        """Get substance descriptors by providing substance names.

        Descriptors are looked up and returned for all substance names
        that are found in Aionics' substances database.
        Substance names that are not found in the database 
        are dropped from the table of results.

        This function returns a process id that can be used
        to track the progress of the computation and, 
        when finished, fetch the results.

        Parameters
        ----------
        substance_names : list
            List of names (strings) of each substance to be looked up.
        descriptor_names : list 
            If provided, the returned descriptors will be filtered
            to include only these names. 

        Returns
        -------
        response : dict
            Dict containing status report and, if successful,
            a pandas DataFrame full of descriptor data. 
        """
        resp = self.session.post(
            self.service_url+'get_descriptors', 
            headers={'x-api-key':self.api_key},
            json={
                'substance_names':substance_names
            }
        )
        if resp.status_code == 200:
            respdata = resp.json()
            ddf = pd.DataFrame.from_dict(respdata['descriptors'],orient='index')
            if descriptor_names:
                descnms = [descnm for descnm in descriptor_names if descnm in ddf.columns]
                ddf = ddf[descnms].copy()
                for subsnm in respdata['descriptors'].keys():
                    respdata['descriptors'][subsnm] = ddf.loc[subsnm].to_dict()
            respdata['descriptor_table'] = ddf
            return respdata
        else:
            return {'success':False,'status_code':resp.status_code}

