import os
import csv
from bs4 import BeautifulSoup

class AmazonPagesHandler:
    def __init__(self, path, save_to):
        """
        Class to handle the parsing of prime video listing from Amazon web pages.
        
        Args:
            path (str): Path to the directory containing the html files.
            save_to (str): Path to the csv file where the metadata will be saved.
        """
        self.path = path
        self.files = [os.path.join(path, p) for p in os.listdir(path)]
        self.parsed = []
        self.save_to = save_to
    
    def save_metadata(self):
        with open(self.save_to, "w", newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(self.parsed)
    
    def parse_files(self):
        counter = 0
        for index, file in enumerate(self.files):
            print(f"Parsing {index + 1}/{len(self.files)}...")
            with open(file, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f.read(), features='html.parser')
                
                for movie in soup.find_all("div", {"class": "s-list-col-right"}):
                    movie_title = movie.find("h2").find("a")
                    title = movie_title.text.strip()
                    link = movie_title["href"]

                    print(title, counter)
                    counter += 1

                    tags = []
                    spans = movie.find("div", {"class": "a-size-base"}).find_all('span')
                    for span in spans:
                        if span.text != "" and span.text !=" | ":
                            tags.append(span.text)

                    tags = "|".join(tags).strip()

                    self.parsed.append([title, link, tags])
        
        self.save_metadata()
        