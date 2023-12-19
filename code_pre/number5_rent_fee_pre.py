import pandas as pd
import pickle

# data 폴더에 있는 면적 월임대료 데이터 불러오기
df = pd.read_excel('../data/면적_월임대료_상가번호 중복 제거(최종).xlsx')


# 월임대료 '원' 지우기
df['월임대료'] = df['월임대료'].str.split('원').str[0]
# 면적 '(㎡)' 지우기
df['면적'] = df['면적'].str.split('(').str[0]

## 지하철역 이름만 남기기 ex)동대문 ##
# '00(1)역' 형태 처리
df['상가이름'] = df['상가이름'].str.split('(').str[0]
# 'OO역' 형태 처리
df['상가이름'] = df['상가이름'].str.split('역').str[0]

# 호선명 열 지우기
df = df.drop('호선명', axis=1)

# '월임대료' 열의 데이터 타입을 숫자로 변환
df['월임대료'] = pd.to_numeric(df['월임대료'].str.replace(',', ''), errors='coerce')


## 다른 py파일에서 필요한 df 가져와서 필요한 부분만 남기기 ## -----------------------
# 우리가 분석할 상가 수가 4개 이상인 지하철역만 가져오고 싶어 mall_trandter_df를 가져옴
with open( "interrelation", "rb" ) as file:
    passenger_mall_interrelation_df = pickle.load(file)

# 가져온 df에서 [지하철역]열만 남기기
station_df = passenger_mall_interrelation_df.drop(['환승역수','상가수','사용 상가 수','공실률','공실0/1','승하차인구수'], axis=1)
## -------------------------------------------------------------------------


# 가져온 df에 면적과 월임대료를 left조인
rent_fee_df = pd.merge(station_df, df, left_on='지하철역', right_on='상가이름', how='left')


## average_rent_df 코드 ## -------------------------------------------------
# [지하철역]을 기준으로 그룹화하고 null값을 빼고 [월임대료]의 평균을 구하기
average_rent_df = rent_fee_df.groupby('지하철역')['월임대료'].mean().reset_index()
# [월임대료]열을 [평균월임대료]열으로 이름 바꾸기
average_rent_df.rename(columns={'월임대료': '평균월임대료'}, inplace=True)
## ------------------------------------------------------------------------

# [지하철역], [면적], [월임대료] 가 있는 df에 [평균월임대료] 합치기
rent_fee_df = pd.merge(rent_fee_df, average_rent_df, on='지하철역', how='left')

# [월임대료] 열의 null 값을 [평균월임대료]로 채우기
rent_fee_df['월임대료'] = rent_fee_df['월임대료'].fillna(rent_fee_df['평균월임대료'])

# [1제곱미터당 평균 월임대료] 열 만들기
rent_fee_df['면적'] = pd.to_numeric(df['면적'], errors='coerce')
rent_fee_df['1제곱미터당 평균 월임대료'] = rent_fee_df['월임대료'] / rent_fee_df['면적']

# 이제 필요없는 열 삭제
rent_fee_df = rent_fee_df.drop(['상가이름', '평균월임대료', '월임대료', '면적'], axis=1)

# 지하철역마다 1제곱미터당 평균 월임대료 구하기
rent_fee_df = rent_fee_df.groupby('지하철역')['1제곱미터당 평균 월임대료'].mean().reset_index()

print(rent_fee_df)

#다른 파일에서 df를 부를 수 있게 저장
with open( "rent_fee", "wb" ) as file:
    pickle.dump( rent_fee_df, file)