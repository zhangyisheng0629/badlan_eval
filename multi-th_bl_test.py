import csv
import requests
import pandas as pd
from tqdm import tqdm,trange
from threading import Thread
from multiprocessing import Process
from pathlib import Path

def bad_lan_recog(url, file_path,i):
    df = pd.read_csv(file_path)

    # print("Evaling ", file_path," ...")
    for idx in tqdm(df.index,position=0):
        line = df.iloc[idx].loc["msg"]
        question = line

        resp = requests.post(url=url, json={"content": f"""{question}""", "model": "yw"})
        # json文件，resp.json()["label"]——label，resp.json()["prob"]——prob
        resp_json = resp.json()
        df.loc[idx, "label"] = resp_json["data"]["label"]
        df.loc[idx, "prob"] = resp_json["data"]["prob"]


    save_path=Path(file_path).stem + "v2_mul-th_eval"+Path(file_path).suffix
    df.to_csv(save_path, sep=",",encoding="utf-8",index=False)
    print(f"Save at {save_path} ")


def main():
    TEXT_MATCH_URL = "http://10.248.33.108:9890/api/match"
    FILE_PATH = ["六品堂旗舰店_客服消息.csv",
                 "olayks旗舰店_客服消息.csv",
                 "美的官方自营旗舰店_客服消息.csv",
                 "zd振德旗舰店_客服消息.csv",
                 "美的自营_2023_08_24.csv"]


    for i,file_path in enumerate(FILE_PATH):
        thread_gen=f"thread_{i}=Thread(target=bad_lan_recog,args=(TEXT_MATCH_URL,file_path,i))"
        exec(thread_gen)
        exec(f"thread_{i}.start()")
        # accruacy = bad_lan_recog(TEXT_MATCH_URL, file_path)



if __name__ == '__main__':
    main()
