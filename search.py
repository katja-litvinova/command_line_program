import selenium.webdriver as webdriver
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.common.by import By
from operator import itemgetter
from argparse import ArgumentParser, Namespace
from tabulate import tabulate

SearchResult = dict[str, str]
SearchResults = list[SearchResult]

YOUSICIAN_SEARCH = "https://yousician.com/songs"


def validate_cli_args(args: Namespace) -> bool:
    if not args or not args.search:
        return False
    return True


def validate_search_results(search_results: SearchResults) -> None:
    if not search_results:
        raise ValueError("Search result is empty.")
    return


def sort_search_results(search_results: SearchResults) -> SearchResults:
    return sorted(search_results, key=itemgetter("artist", "song"))


def get_search_results(search_argument: str) -> SearchResults:
    browser = webdriver.Chrome()
    try:
        browser.get(YOUSICIAN_SEARCH)
    except WebDriverException:
        raise ValueError("Couldn't load the page. No internet connection.")

    browser.implicitly_wait(10)

    try:
        accept_cookies_button = browser.find_element(
            By.CSS_SELECTOR, "#onetrust-accept-btn-handler"
        )
        browser.execute_script("arguments[0].click();", accept_cookies_button)

        search_field = browser.find_element(
            By.XPATH, "//input[contains(@class, 'SearchInput__Input-sc-1o849ds-2')]"
        )
        search_field.send_keys(search_argument)
        search_field.submit()

        raw_search_results = browser.find_elements(
            By.XPATH, "//a[contains(@class, 'TableRow-sc-13kvz5q-0')]"
        )
    except NoSuchElementException:
        raise ValueError("Can't navigate on the page. Check page elements naming.")

    search_results: SearchResults = []
    for song_artist in raw_search_results:
        song, artist = song_artist.text.split("\n")
        search_results.append({"artist": artist, "song": song})
    browser.quit()
    return search_results


def main() -> None:
    parser = ArgumentParser(
        description="A command line program to check the search results"
    )
    parser.add_argument(
        "--search",
        type=str,
        nargs=1,
        metavar="search_argument",
        help="Search for song or artist.\n"
        "If your search argument has more than one word then use double quotes",
    )
    args = parser.parse_args()
    if not validate_cli_args(args):
        print("Empty search argument.")
        return

    try:
        unsorted_search_results = get_search_results(args.search)
        validate_search_results(unsorted_search_results)
    except ValueError as e:
        print(str(e))
        return

    sorted_search_results = sort_search_results(unsorted_search_results)
    table_data = [list(el.values()) for el in sorted_search_results]
    print(tabulate(table_data, headers=["Artist", "Song"]))
    return


if __name__ == "__main__":
    main()
