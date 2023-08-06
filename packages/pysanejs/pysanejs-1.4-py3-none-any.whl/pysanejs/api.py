#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
from urllib.parse import urljoin
from typing import Union, Dict, List, Optional


class SaneJS():

    def __init__(self, root_url: str='https://sanejs.circl.lu/'):
        self.root_url = root_url
        self.session = requests.session()

    @property
    def is_up(self) -> bool:
        try:
            r = self.session.head(self.root_url)
            return r.status_code == 200
        except Exception:
            return False

    def sha512(self, sha512: Union[str, list]) -> Dict[str, List[str]]:
        '''Search for a hash (sha512)
        Reponse:
            {
              "response": [
                "libraryname|version|filename",
                ...
              ]
            }
        '''
        r = self.session.post(self.root_url, json={'sha512': sha512})
        return r.json()

    def library(self, library: Union[str, list], version: Optional[str]=None) -> Dict[str, Dict[str, Dict[str, Dict[str, str]]]]:
        ''' Search for a library by name.
        Response:
            {
              "response": {
                "libraryname": {
                  "version": {
                    "filename": "sha512",
                    ...
                  }
                  ...
                },
                ...
              }
            }
        '''
        to_query = {'library': library}
        if version:
            to_query['version'] = version
        r = self.session.post(urljoin(self.root_url, 'library'), json=to_query)
        return r.json()
