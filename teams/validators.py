from datetime import datetime

class ValidateTitlesError(Exception):
    default_message = "titles cannot be negative"

    def __init__(self, message=None):
        self.message = message or self.default_message

def is_not_validate_titles(titles):
    if titles < 0:
        raise ValidateTitlesError('titles cannot be negative')

    return titles

def is_not_validate_titles_quantity(titles, date):
    date_format = "%Y-%m-%d"
    parsed_date = datetime.strptime(date, date_format)
    year = parsed_date.year
    title = 1

    for i in range (year, 2022, 4):
        title += 1
        
    if titles > title:
        raise ValidateTitlesError("impossible to have more titles than disputed cups")

    return titles


class ValidateFirstCupError(Exception):
    default_message = "there was no world cup this year"

    def __init__(self, message=None):
        self.message = message or self.default_message


def is_not_validate_first_cup(date):
    years_copa = [1930, 1934, 1938, 1950, 1954, 1958, 1962, 1966, 1970, 1974, 1978, 1982, 1986, 1990, 1994, 1998, 2002, 2006, 2010, 2014, 2018, 2022]
    date_format = "%Y-%m-%d"
    parsed_date = datetime.strptime(date, date_format)
    year = parsed_date.year

    if year < 1930 or not year in years_copa:
        raise ValidateFirstCupError

    return year


