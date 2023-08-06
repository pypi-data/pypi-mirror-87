from dataclasses import dataclass
from typing import List

@dataclass
class RecipeLink:
    title: str
    url: str
    website: str

@dataclass
class SearchResult:
    results : List[RecipeLink]
    website : str
    keyword : str

    def __init__(self, keyword, website, results):
        self.keyword = keyword
        self.website = website
        self.results = results
    
    def merge(self, result : SearchResult) -> SearchResult:
        return SearchResult(self.keyword, self.website, self.results + result.results)
    
    @property
    def length(self):
        return len(self.results)