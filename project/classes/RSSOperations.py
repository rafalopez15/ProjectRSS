import requests, os
import xml.etree.ElementTree as ET
from datetime import datetime

class RSSOperations:

    def __init__(self):
        pass

    
    def get_xml(self, url):
        """
        Writes an XML file pulled from a company file to the local directory.

        Parameters
        ----------
        url : str
            Takes in a url as a string that should contain the RSS Feed URL.
        """
        response = requests.get(url)
        with open('rss-feed.xml', 'wb') as file:
            file.write(response.content)

    
    def find_date(self):
        """
        Finds a tag which contains the date of the last updated item.
        Parameters
        ----------
        root : Element
            A root to the elements of the tree.
        
        Returns
        -------
        str
            A date in string format.
        """
        # Search XML tree for first 'pubDate' tag which corresponds to the latest publish date
        tree = ET.parse('rss-feed.xml')
        root = tree.getroot()
        try:
            # The iterable object is the list of matches found
            date = datetime.strptime(next(root.iter('pubDate')).text[:25], "%a, %d %b %Y %H:%M:%S")
            return date.strftime("%Y-%m-%d %H:%M:%S")
        except StopIteration:
            return '' # Return empty string if no element matches were found

        
    def remove_file(self):
        os.remove('rss-feed.xml')