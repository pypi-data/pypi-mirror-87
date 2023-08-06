import time
import re

import requests

from ows_language_model.config import config


if __name__ == "__main__":
    success = 0
    failures = 0
    ti = time.time()
    for i in range(0, 1000000):
        url = f"http://gutenberg.org/files/{i}/{i}-0.txt"
        response = requests.get(url)
        if response.status_code == 200:
            response.encoding = 'utf-8'
            text = response.text
            success += 1
            print(f"{i} : {success} successes, {failures} failures. {(time.time()-ti):.3} seconds since the last success.")
            with open(config.DATA_FOLDER / f'doc_{i}', 'w') as f:
                f.write(text)
            ti = time.time()
            if (i % 10) == 0:
                time.sleep(5)
        else:
            failures +=1
        