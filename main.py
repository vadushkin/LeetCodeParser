import os
import pathlib
from pathlib import Path
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

absolute_path = r""


def change_work_directory(path: Path) -> Path:
    current_directory = Path(path)
    os.chdir(current_directory)
    return current_directory


def get_html_for_all_problems(all_problems_url: str) -> webdriver.Chrome.page_source:
    browser = webdriver.Chrome()
    browser.get(all_problems_url)
    time.sleep(5)
    html = browser.page_source
    browser.quit()
    return html


def get_html_for_task(url_: str, language: str) -> webdriver.Chrome.page_source:
    browser = webdriver.Chrome()
    browser.get(url_)

    time.sleep(7)

    browser.find_element("id", "headlessui-listbox-button-:ri:").click()

    elements = browser.find_elements("class name", "whitespace-nowrap")

    for element in elements:
        if element.text == language:
            element.click()
            break

    time.sleep(3)

    html = browser.page_source
    browser.quit()

    return html


def get_data_about_task(html: str):
    soup = BeautifulSoup(html, "lxml")
    tasks_row = soup.find("div", role="rowgroup")
    task_line = tasks_row.find("div", role="row").find_all("div", class_="mx-2 py-[11px]")
    data = task_line[1].find("a")
    task_link = "https://leetcode.com" + data.get("href")
    task_name = data.text
    task_difficulty = task_line[4].find("span").text

    return {
        "task_link": task_link,
        "task_name": task_name,
        "task_difficulty": task_difficulty
    }


def get_example_code_for_task(html: BeautifulSoup, one_example: str) -> str:
    """Return the sample code for task"""

    code = ""

    example_codes = html.find("div", class_="view-lines monaco-mouse-cursor-text").find_all("div", class_="view-line")

    name_of_function = ""

    for index, example_code in enumerate(example_codes):
        if index == 1:
            name_of_function += example_code.text.split()[1][:-6]

        code += example_code.text.replace('\xa0', ' ') + "\n"

    code += " " * 8 + "pass" + "\n\n"

    code += f"""
def main():
    s = Solution()
    print(s.{name_of_function}({one_example}))


if __name__ == '__main__':
    main()

\"\"\"Tests:
1. 

2. 
\"\"\"
"""

    return code


def get_description_for_task(html: BeautifulSoup) -> tuple[str, str]:
    """Return the description code for task"""

    description = html.find("div", class_="_1l1MA")

    complicated_text = "\"\"\"\n"

    for p in description.find_all("p")[:-5]:
        text = p.text.split()

        for j in range(10, len(text), 10):
            complicated_text += ' '.join(text[j - 10:j]) + "\n"

    examples = description.find_all("pre")

    complicated_text += "\n"

    one_example = ""

    for index, example in enumerate(examples, 1):
        if index == 1:
            text = example.text.split("\n")[0].split()[1:]

            for i in range(3, len(text) + 1, 3):
                e = text[i - 3: i][2]

                one_example += e

        complicated_text += f"* Example {index}:" + "\n" + example.text + "\n"

    complicated_text += "Constraints:\n\n"

    constraints = description.find_all("li")

    for index, constraint in enumerate(constraints):
        complicated_text += "* " + constraint.find("code").text + "\n"

    complicated_text += "\"\"\""

    return complicated_text, one_example


def get_description_and_example_code(task_url: str) -> tuple[str, str]:
    """Return a description and an example code"""

    soup = BeautifulSoup(get_html_for_task(task_url, "Python3"), "lxml")

    description, one_example = get_description_for_task(soup)
    example_code = get_example_code_for_task(soup, one_example)

    return description, example_code


def create_folder_and_files(absolute_path_: str, data: dict):
    task_link, task_name, task_difficulty = data.get("task_link"), data.get("task_name"), data.get("task_difficulty")
    task_description, example_code = get_description_and_example_code(task_link)

    if not task_link or not task_name or not task_link:
        return

    current_directory = Path(absolute_path_)
    os.chdir(current_directory)

    for difficult in current_directory.iterdir():
        if task_difficulty == difficult.name:
            break
    else:
        pathlib.Path(f"{task_difficulty}/").mkdir(parents=True, exist_ok=True)

    current_directory = change_work_directory(current_directory / task_difficulty)

    pathlib.Path(f"{task_name}/").mkdir(parents=True, exist_ok=True)

    _ = change_work_directory(current_directory / task_name)

    with open("name_task.py", "w", encoding="utf-8") as file, open("v1.py", "w", encoding="utf-8") as file2:
        file.write(task_description)
        file2.write(example_code)


if __name__ == "__main__":
    try:
        url = "https://leetcode.com/problemset/all/"
        create_folder_and_files(absolute_path, get_data_about_task(get_html_for_all_problems(url)))
    except NoSuchElementException as _ex:
        print(f"Error: {_ex}.")
        print(f"Please retry again!")
