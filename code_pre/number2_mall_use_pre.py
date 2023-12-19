import pandas as pd
import pickle

# data 폴더에 있는 사용 상가 수 데이터 불러오기
df = pd.read_excel('../data/사용상가수_합산 합친거.xlsx')


## 지하철역 이름만 남기기 ex)동대문 ##
# '00(1)역' 형태 처리
df['상가이름'] = df['상가이름'].str.split('(').str[0]
# 'OO역' 형태 처리
df['상가이름'] = df['상가이름'].str.split('역').str[0]

## 사용 상가 수가 맞는 df 만들기 ##
# 중복된 지하철역의 [사용 상가 수]를 하나로 합친 df 생성, [호선명]도 삭제
mall_use_df = df.groupby('상가이름')['사용 상가 수'].sum().reset_index()

# [상가이름]열을 [지하철역]열으로 이름 바꾸기
mall_use_df.rename(columns={'상가이름': '지하철역'}, inplace=True)

print(mall_use_df)

#다른 파일에서 df를 부를 수 있게 저장
with open( "mall_use", "wb" ) as file:
    pickle.dump( mall_use_df, file)