import json
import pandas as pd
import matplotlib.pyplot as plt

decoder = json.JSONDecoder()

with open('results/Tweets-PUT-S3-sF1ta-3-2021-12-01-04-28-43-b75a2f92-9763-4937-8c61-85a2fff45108', 'r') as content_file:

    content = content_file.read()

    content_length = len(content)
    decode_index = 0

    result_dict = {}

    while decode_index < content_length:
        try:
            obj, decode_index = decoder.raw_decode(content, decode_index)
            print("File index:", decode_index)
            print(obj)
            result_dict[decode_index] = obj
        except json.JSONDecodeError as e:
            print("JSONDecodeError:", e)
            # Scan forward and keep trying to decode
            decode_index += 1

print(result_dict)

df = pd.DataFrame(result_dict)
df = df.T
dfplot = df.groupby("sentiment").count()
dfplot.plot.bar(rot=0)
plt.bar()
