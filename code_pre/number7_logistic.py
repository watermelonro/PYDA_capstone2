import pandas as pd
import pickle

# 다른 py파일에서 필요한 df 가져오기
with open( "interrelation", "rb" ) as file:
    passenger_mall_interrelation_df = pickle.load(file)

with open( "rent_fee", "rb" ) as file:
    rent_fee_df = pickle.load(file)


# 로지스틱 회귀 분석을 위한 [1제곱미터당 평균 월임대료], [환승역수], [공실0/1], [승하차인구수] 데이터가 있는 df 가져와서 필요한 것만 남기기
logistic_df = pd.merge(rent_fee_df, passenger_mall_interrelation_df, on='지하철역', how='left')
logistic_df = logistic_df.drop(['상가수','사용 상가 수','공실률'], axis=1)

# 공실0/1 에서 0과 1인 행만 남기기
logistic_df = logistic_df[(logistic_df['공실0/1'] == 0) | (logistic_df['공실0/1'] == 1)]

## NaN값 채우기
# 공실0/1 에서 0이고 NaN이 아닌 행들을 선택
row_not_0 = logistic_df[(logistic_df['공실0/1'] == 0) & (~logistic_df['1제곱미터당 평균 월임대료'].isnull())]
# 위에서 선택한 행들의 [1제곱미터당 평균 월임대료] 열의 평균 계산
row_not_0_average = row_not_0['1제곱미터당 평균 월임대료'].mean()
# [공실0/1]이 0이고 [1제곱미터당 평균 월임대료] 가 NaN인 행에 위의 평균 추가
logistic_df['1제곱미터당 평균 월임대료'] = logistic_df['1제곱미터당 평균 월임대료'].fillna(row_not_0_average)

print(logistic_df)

# # 로지스틱 df을 엑셀파일로 저장
# logistic_df.to_excel('../data_pre/로지스틱_테이블.xlsx',index=False)