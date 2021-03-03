from pathlib import Path
import pandas as pd

if __name__ == '__main__':
    filepath = Path('../data/data_去除無用資訊.csv').resolve()
    df = pd.read_csv(str(filepath), header=None, low_memory=False)
    series = df.loc[:,10]
    #b = series.sort_values(ascending=True)
    obj = list()
    num = list()
    for i in range(len(series)):
        if not series[i] in obj:
            obj.append(series[i])
            num.append(1)
        else:
            location = obj.index(series[i])
            num[location] += 1
    
    for i in range(len(obj)):
        print(f'1\t{obj[i]}\t{num[i]}')

    print(f'len = {len(obj)}')