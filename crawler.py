from bs4.element import ResultSet
import requests
from bs4 import BeautifulSoup
from requests.models import Response

# URL link for crawling
# URL: str = "https://create.arduino.cc/projecthub/TheGadgetBoy/ds18b20-digital-temperature-sensor-and-arduino-9cc806?ref=platform&ref_id=424_popular___&offset=2"


def crawl_project(url: str) -> dict:

    TITLE_TAG = 'h1'
    COMPONENTS_TAG = 'tbody'
    COMPONENT_NUMBER_SEPERATOR = '×'
    LINK_TAG = 'input'
    LINK_TAG_CLASS_NAME = 'embed-code'

    # Final dictionary contains all info of a project
    project: dict = {'title': "", 'components': {}, 'link': ""}

    __soup__: BeautifulSoup = None

    def crawl(url: str) -> BeautifulSoup:
        page: Response = requests.get(url)
        soup: BeautifulSoup = BeautifulSoup(page.content, 'html.parser')
        return soup

    __soup__ = crawl(url)

    # Hepler function
    def get_all_tags(tag: str, soup: BeautifulSoup = __soup__) -> ResultSet:
        all_tags: ResultSet = soup.find_all(tag)
        return all_tags

    # Hepler function
    def get_tag(tag: str, soup: BeautifulSoup = __soup__) -> ResultSet:
        tag: ResultSet = soup.find(tag)
        return tag

    def get_tag_by_class(tag: str,
                         class_name: str,
                         soup: BeautifulSoup = __soup__) -> ResultSet:
        tag_with_class: ResultSet = soup.find(tag, {'class': class_name})
        return tag_with_class

    def set_project_title(title_tag_list: ResultSet) -> None:
        project['title'] = title_tag_list[0].get_text()

    def set_components(components_tag: ResultSet) -> None:
        for i in components_tag:
            text: str = i.get_text()
            index: int = text.find(COMPONENT_NUMBER_SEPERATOR)
            if index:
                component_number: str = text[index::]
                component_name: str = text[:index:]
                project['components'][component_name] = component_number

    def set_project_link(project_link_tag: ResultSet) -> None:
        project["link"] = project_link_tag.get('value')

    def run() -> dict:
        set_project_title(get_all_tags(TITLE_TAG))
        set_components(get_tag(COMPONENTS_TAG))
        set_project_link(get_tag_by_class(LINK_TAG, LINK_TAG_CLASS_NAME))
        return project

    return run()


# print(crawl_project(URL))
