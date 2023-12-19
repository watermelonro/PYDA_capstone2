import pandas as pd
import pickle

# 다른 py파일에서 필요한 df 가져오기
with open( "interrelation", "rb" ) as file:
    passenger_mall_interrelation_df = pickle.load(file)

with open( "rent_fee", "rb" ) as file:
    rent_fee_df = pickle.load(file)


# [공실률], [공실0/1], [1제곱미터당 평균 월임대료] 데이터가 있는 상관관계 df를 가져와서 선형회귀를 위한 df를 만들기
rent_fee_linear_df = pd.merge(rent_fee_df, passenger_mall_interrelation_df, on='지하철역', how='left')
rent_fee_linear_df = rent_fee_linear_df.drop(['환승역수','상가수','사용 상가 수','승하차인구수'], axis=1)

# 공실0/1 에서 0과 1인 행만 남기기
rent_fee_linear_df = rent_fee_linear_df[(rent_fee_linear_df['공실0/1'] == 0) | (rent_fee_linear_df['공실0/1'] == 1)]

## NaN값 채우기
# 공실0/1 에서 0이고 NaN이 아닌 행들을 선택
row_0 = rent_fee_linear_df[(rent_fee_linear_df['공실0/1'] == 0) & (~rent_fee_linear_df['1제곱미터당 평균 월임대료'].isnull())]
# 위에서 선택한 행들의 [1제곱미터당 평균 월임대료] 열의 평균 계산
row_0_average = row_0['1제곱미터당 평균 월임대료'].mean()
# [공실0/1]이 0이고 [1제곱미터당 평균 월임대료] 가 NaN인 행에 위의 평균 추가
rent_fee_linear_df['1제곱미터당 평균 월임대료'] = rent_fee_linear_df['1제곱미터당 평균 월임대료'].fillna(row_0_average)

print(rent_fee_linear_df)

# # 선형회귀 df을 엑셀파일로 저장
# rent_fee_linear_df.to_excel('../data_pre/선형회귀_테이블.xlsx',index=False)