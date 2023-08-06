from html.parser import HTMLParser
from json import loads
from os.path import basename
from zipfile import ZipFile

FILE_NAME = "memoinfo.jlqm"

DATA_KEY = "Memo"

INPUT_HTML_KEY = "Desc"

INPUT_TIME_CREATED_KEY = "CreatedTime"

INPUT_TIME_MODIFIED_KEY = "ModifiedTime"

OUTPUT_FILENAME_KEY = "filename"

OUTPUT_HTML_KEY = "html"

OUTPUT_TEXT_KEY = "text"

OUTPUT_TIME_CREATED_KEY = "created"

OUTPUT_TIME_MODIFIED_KEY = "modified"


class MemoHTMLParser(HTMLParser):
    def parse(self, data):
        self.lines = []
        self.feed(data)
        return "\n".join(self.lines)

    def handle_data(self, data):
        self.lines.append(data)


__html_parser_instance__ = MemoHTMLParser()


def extract_data_from_lqm_file(lqm_file_path):
    with ZipFile(lqm_file_path, "r") as zip_file:
        with zip_file.open(FILE_NAME) as json:
            data = {OUTPUT_FILENAME_KEY: basename(lqm_file_path)}
            data.update(parse_memo_data(loads(json.read())[DATA_KEY]))

            return data


def parse_memo_data(memo):
    html = memo[INPUT_HTML_KEY]

    return {
        OUTPUT_TIME_CREATED_KEY: memo[INPUT_TIME_CREATED_KEY],
        OUTPUT_TIME_MODIFIED_KEY: memo[INPUT_TIME_MODIFIED_KEY],
        OUTPUT_HTML_KEY: html,
        OUTPUT_TEXT_KEY: __html_parser_instance__.parse(html),
    }
