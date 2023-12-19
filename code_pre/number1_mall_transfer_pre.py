import pandas as pd
import pickle

# data 폴더에 있는 상가 수, 환승역 수 데이터 불러오기
df = pd.read_excel('../data/상가수_환승역수.xlsx')


## 지하철역 이름만 남기기 ex)동대문 ##
# [지하철역]열에서 지하철역 뒤에 (역 서브명) 지우기
df['지하철역'] = df['지하철역'].str.split('(').str[0]

# [호선명] 열 지우기
df = df.drop('호선명', axis=1)

## 상가 수가 맞는 df 만들기 ##
# 중복된 지하철역의 [상가수]를 하나로 합친 df 생성
grouped_df = df.groupby('지하철역')['상가수'].sum().reset_index()

## 환승역 수가 맞는 df 만들기 ##
# 원래 df에서 지하철역이 중복된 값 삭제
no_duplicates_df = df.drop_duplicates(subset='지하철역')
# # no_duplicates_df에서 [상가수]열을 삭제해 [환승역수]열만 남기기
no_duplicates_df = no_duplicates_df.drop('상가수', axis=1)

## 상가 수, 환승역 수 모두 맞는 df 만들기 ##
# 환승역 수가 맞는 df와 상가 수가 맞는 df를 [지하철역]을 기준으로 합치기
mall_transfer_df = pd.merge(no_duplicates_df, grouped_df, on='지하철역', how='left')

## 의미없는 공실률을 막기 위해 상가 수가 어느 정도 있는 역만 남기기 ##
# 상가 수가 4개 이상인 역만 남겨 새로운 df 생성
mall_transfer_df= mall_transfer_df[mall_transfer_df['상가수'] >= 4]
# null값 확인 -> 상가 수가 4개 이상인 역 중 null값은 없음
# print(mall_transfer_df.isna().any(axis=1))

# 불러온 df 확인용
# print(grouped_df)
# print(no_duplicates_df)
# print(mall_transfer_df)

print(mall_transfer_df)

#다른 파일에서 df를 부를 수 있게 저장
with open( "mall_transfer", "wb" ) as file:
    pickle.dump( mall_transfer_df, file)