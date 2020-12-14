import json


class Result():
    def __init__(self, raw_output):
        # メンバ変数
        self.raw_output = ''
        self.key = ''
        self.query = ''
        self.selected = []

        # メンバ変数への初期値格納
        self.raw_output = raw_output
        raw_output_array = raw_output[:-1].split('\n')  # 最後の一文字は改行コード
        self.query = raw_output_array[0]
        self.key = raw_output_array[1]
        self.selected = raw_output_array[2:]

    def to_json(self, print_query, print_key):
        json_obj = {}
        if print_query:
            json_obj.update({'query': self.query})
        if print_key:
            json_obj.update({'key': self.key})
        json_obj.update({'output': self.selected})
        return json.dumps(json_obj)
