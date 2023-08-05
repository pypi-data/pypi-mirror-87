import requests
import progressbar
from pathlib import Path
import argparse
from argparse import HelpFormatter
import textwrap

formated_string = f'''Traindex CLI is intalled correctly.

[1] Go to file directory you want to upload.
[2] Make sure presigned.json is there.
[3] Type `triandexcli`.
[4] Wait till the dataset is uploaded.'''


class RawFormatter(HelpFormatter):
    def _fill_text(self, text, width, indent):
        return "\n".join([textwrap.fill(line, width) for line in textwrap.indent(textwrap.dedent(text), indent).splitlines()])



parser = argparse.ArgumentParser(description=formated_string, formatter_class=RawFormatter)
args = parser.parse_args()



def main():
    data = eval(open('presigned.json').read())
    upload_by = data['upload_by']
    max_size = data['max_size']
    urls = data['urls']
    file_size = data['file_size']
    bar = progressbar.ProgressBar(maxval=file_size, \
        widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    target_file = Path(data['file_name'])
    upload_id = data['upload_id']
    bucket_name = data['bucket_name']
    key = data['key']
    json_object = dict()
    parts = []
    file_size_counter = 0
    with target_file.open('rb') as fin:
        bar.start()
        for num, url in enumerate(urls):
            part = num + 1
            file_data = fin.read(max_size)
            file_size_counter += len(file_data)
            res = requests.put(url, data=file_data)
            
            if res.status_code != 200:
                print (res.status_code)
                print ("Error while uploading your data.")
                return None
            bar.update(file_size_counter)
            etag = res.headers['ETag']
            parts.append((etag, part))
        bar.finish()
        json_object['parts'] = [
            {"ETag": eval(x), 'PartNumber': int(y)} for x, y in parts]
        json_object['upload_id'] = upload_id
        json_object['key'] = key
        json_object['bucket_name'] = bucket_name
    requests.post('https://9xej02xwza.execute-api.us-west-2.amazonaws.com/prod/cli-combine', json={'parts': json_object})
    print ("Dataset is uploaded successfully")

if __name__ == "__main__":
    main()    
