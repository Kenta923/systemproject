#最終変更日7月13日
#IDデータを作成するプログラム
#SubjectIDに「'科目ID'」, SThourに「開始時刻(時)」,　STminに「開始時刻(分)」, fileIDmに「履修者データ」を渡す
#15回分のIDデータが作成される
import ReadCsv
import os
import random
from datetime import datetime
import csv
from operator import itemgetter, attrgetter

def generate(SubjectID, SThour, STmin, fileIDm):
    SubjectInformation = []
    ReadCsv.readCsv('TestSubject.csv', SubjectInformation)
    #ReadCsv.readCsv(f'{SubjectID}-Schedule.csv', SubjectInformation)
    print(SubjectInformation)

    H = SThour
    m0 = STmin

    #講義回ごとの正規分布の平均(mus)と標準偏差(sigmas)
    mus = [3, 5, 5, 7, 9, 10, 10, 10, 10, 10, 12, 10, 11, 8, 7]
    sigmas = [5, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10]

    DataIDm = []
    ReadCsv.readCsv(fileIDm, DataIDm)
    print(DataIDm)

    #データを出力するディレクトリがなければ作成 
    os.makedirs(SubjectID, exist_ok=True)

    #CSVファイルのヘッダ
    header = ['年月日'] + ['時刻'] + ['IDm']

    for i in range(len(SubjectInformation[0])):
        Y = int(SubjectInformation[0][i])
        print(Y)
        M = int(SubjectInformation[1][i])
        print(M)
        D = int(SubjectInformation[2][i])
        print(D)
        mu = mus[i]
        sigma = sigmas[i]
        N = len(DataIDm)
        RD = generate_random_datetimes(Y, M, D, H, m0, mu, sigma, N)
    
        #DataRDがランダムな時間を格納するリスト
        DataRD = []
        for j in range(len(RD)):
            YMD = '{:%Y-%m-%d}'.format(RD[j])
            HTS = '{:%X}'.format(RD[j])
            DataRD.append([YMD, HTS])
    
        #時間の順にソートする
        DataRD.sort(key=itemgetter(1))

        #シャッフル
        numbers = [j for j in range(len(DataIDm))]
        random.shuffle(numbers)

        #リストにIDmを付加する
        for j in range(len(RD)):
            k = numbers[j]
            DataRD[j].append(DataIDm[k][0])
    
        #ファイルに出力
        #FileOut = f'{SubjectID}/{SubjectID}-{str(Y)}{str(M).zfill(2)}{str(D).zfill(2)}.csv'
        FileOut = f'{SubjectID}/{SubjectID}-AttendanceList{i+1}.csv'
        with open(FileOut, 'w', encoding = "utf_8", newline = '') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(header)
            writer.writerows(DataRD)

# ランダムな時間と秒を発生させる関数
# 年，月，日，開始時間は固定，乱数の分布として正規分布を設定
def generate_random_datetimes(Y, M, D, H, m0, mu, sigma, N):
    MinMax = 59
    rand_datetimes = []
    for i in range(N):
        ValMin = int(random.normalvariate(mu, sigma))
        m = m0+ValMin
        Hp = H
        Mp = m
        # 分が59を超えたら時間を+1，分を-60
        if Mp > MinMax:
            Hp += 1
            Mp -= MinMax+1
        # 分が負の値となったら時間を-1，分を+60
        elif Mp < 0:
            Hp -= 1
            Mp += MinMax+1
        # 一旦datetime型のnowに今の時刻を入れる
        now = datetime.now()
        # 設定したランダム日時に入れ替える
        # 秒は一様乱数で1から59までの値を入れる
        rand_datetime = now.replace(year=Y, month=M, day=D, hour=Hp, minute=Mp,
                                    second=random.randint(1,59))
        rand_datetimes.append(rand_datetime)
    return rand_datetimes

if __name__ == '__main__':
    SubjectID = 'F1'
    generate(SubjectID, 8, 50, os.path.abspath(f'risyu_{SubjectID}.csv'))
