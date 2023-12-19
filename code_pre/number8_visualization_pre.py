import pandas as pd
import pickle

# 다른 py파일에서 필요한 df 가져오기
with open( "passenger", "rb" ) as file:
    passenger_df = pickle.load(file)

with open( "rent_fee", "rb" ) as file:
    rent_fee_df = pickle.load(file)

# 다른 폴더에 있는 면적 상가업종 데이터 불러오기
category_df = pd.read_excel('../data/상가업종.xlsx')
linear_df = pd.read_excel('../data_pre/선형회귀_테이블.xlsx')

# 필요한 열들만 가져오기
category_df = category_df[['역명', '업종']]

# null값이 있는 행 삭제
category_df = category_df.dropna()

# [역명]열을 [지하철역]열으로 이름 바꾸기
category_df.rename(columns={'역명': '지하철역'}, inplace=True)

## 시각화할 데이터 프레임 만들기
# 업종 데이터와 승하차수 데이터 합치기
category_df = pd.merge(category_df, passenger_df, on='지하철역', how='left')
# 위의 데이터와 공실0/1과 1제곱미터당 평균 월임대료가 있는 데이터 합치기
category_df = pd.merge(category_df, linear_df, on='지하철역', how='left')

# null값이 있는 행은 공실0/1로 나누어지지 않은 역이니 삭제
category_df = category_df.dropna()

# 시각화에 필요 없는 열 삭제
category_df = category_df.drop(['공실률'], axis=1)

# [업종]열에 있는 '[상가]' 표시와 괄호 없애기
category_df['업종'] = category_df['업종'].str.split(']').str[1]
category_df['업종'] = category_df['업종'].str.split('(').str[0]


print(category_df)

# # 시각화 df을 엑셀파일로 저장
# category_df.to_excel('../data_pre/시각화_테이블.xlsx',index=False)

