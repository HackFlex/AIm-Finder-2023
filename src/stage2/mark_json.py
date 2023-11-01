from lxml import etree
import json
from os.path import splitext


class MarkJSON:
    def __init__(self, file_origin=None, file_result=None) -> None:
        self.file_origin = file_origin
        self.file_result = file_result
        self.transfer_list = []

    def set_file_origin(self, file_origin) -> None:
        self.file_origin = file_origin

    def set_file_result(self, file_result) -> None:
        self.file_result = file_result

    def create_mark(self) -> None:
        if self.file_origin is None and self.file_result is None:
            print("Empty filenames")
            return

        with open(file_result, "r") as f:
            marking = json.load(f)

        for mark in marking:
            entity = (mark["start"], mark["end"], mark["decorCode"])
            self._append_entity(self.transfer_list, mark["xPath"], entity)

        self._change_path_to_text(self.transfer_list, self.file_origin)

    def export(self, filename=None) -> str:
        if self.file_origin is None and self.file_result is None:
            print("Empty filenames")
            return ""

        if filename is None:
            prefix = splitext(self.file_origin)[0]
            suffix = "_train"
            ext = ".json"
            filename = prefix + suffix + ext

        with open(filename, "w") as f:
            json.dump(self.transfer_list, f, indent=4, ensure_ascii=False)

        return filename

    def _append_entity(
        self, source: list[dict], content_path: str, entity: tuple
    ) -> None:
        for item in source:
            if item["text"] == content_path:
                item["entity"].append(entity)
                return

        source.append({"text": content_path, "entity": [entity]})

    def _get_text_by_xpath(self, root: etree._Element, path: str) -> str:
        items = path.split("/")[2:]
        ns = "{" + root.nsmap[None] + "}"
        curr_elem = root

        for item in items:
            curr_elem = curr_elem.find(f"{ns}{item}")
            if curr_elem is None:
                return ""

        return curr_elem.text.strip()

    def _change_path_to_text(self, source: list[dict], filename: str) -> None:
        tree = etree.parse(filename)
        root = tree.getroot()

        for item in source:
            text = self._get_text_by_xpath(root, item["text"])
            item["text"] = text


if __name__ == "__main__":
    # file_origin = 'epicrisis.xml'
    # file_result = 'epicrisis_result.json'
    file_origin = "dataset/Эпикризы_пример_19_05_2023/Эпикриз_1932660249_v1.xml"
    file_result = "dataset/Эпикризы_пример_19_05_2023/Эпикриз_1932660249_v1_result.json"

    mark_json = MarkJSON(file_origin, file_result)
    mark_json.create_mark()
    mark_json.export()
