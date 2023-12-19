import pandas as pd
import pickle

# 다른 py파일에서 필요한 df 가져오기
with open( "mall_transfer", "rb" ) as file:
    mall_transfer_df = pickle.load(file)

with open( "mall_use", "rb" ) as file:
    mall_use_df = pickle.load(file)

with open( "passenger", "rb" ) as file:
    passenger_df = pickle.load(file)


# 불러온 df들 중 상가 수,환승역 수 df와 사용 상가 수 df를 [지하철역]을 기준으로 합치기
passenger_mall_interrelation_df = pd.merge(mall_transfer_df, mall_use_df, on='지하철역', how='left')

# 역의 공실률을 구하기
passenger_mall_interrelation_df['공실률'] = (passenger_mall_interrelation_df['상가수'] - passenger_mall_interrelation_df['사용 상가 수']) / passenger_mall_interrelation_df['상가수'] * 100

# [사용 상가 수]가 [상가수]보다 많은 역의 공실률을 0으로 바꾸기
# 동대문에 동대문역사공원역이 포함된 거 처리하는 코드 / 동대문역은 공실률이 0%이므로 상관없음
passenger_mall_interrelation_df['공실률'][passenger_mall_interrelation_df['공실률'] < 0]=0

# [공실률]을 기준으로 공실률이 높은 역에는 0, 공실률이 낮은 역에는 1, 그 사이 역들에는 2를 할당
passenger_mall_interrelation_df['공실0/1'] = pd.cut(passenger_mall_interrelation_df['공실률'],
                                               bins=[-float("inf"),
                                                     passenger_mall_interrelation_df['공실률'].quantile(0.1),
                                                     passenger_mall_interrelation_df['공실률'].quantile(0.9),
                                                     float("inf")],
                                               labels=[1,2,0],
                                               right=True)

# 위에서 계속 만든 df에 [승하차인구수] 열을 추가
passenger_mall_interrelation_df = pd.merge(passenger_mall_interrelation_df, passenger_df, on='지하철역', how='left')

# 공실0/1 에서 0과 1인 행만 남기기
passenger_mall_interrelation_df = passenger_mall_interrelation_df[(passenger_mall_interrelation_df['공실0/1'] == 0) | (passenger_mall_interrelation_df['공실0/1'] == 1)]

# 불러온 df 확인용
# print(mall_transfer_df)
# print(mall_use_df)
# print(passenger_df)

print(passenger_mall_interrelation_df)


# 다른 파일에서 df를 부를 수 있게 저장
with open( "interrelation", "wb" ) as file:
    pickle.dump( passenger_mall_interrelation_df, file)

# # 상관관계 df을 엑셀파일로 저장
# passenger_mall_interrelation_df.to_excel('../data_pre/상관관계_테이블.xlsx',index=False)