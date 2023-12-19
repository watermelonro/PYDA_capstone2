import pandas as pd
import pickle

# data 폴더에 있는 승하차인구 수 데이터 불러오기
df = pd.read_excel('../data/승하차인구수.xlsx')


## 지하철역 이름만 남기기 ex)동대문 ##
# [지하철역]열에서 지하철역 뒤에 (역 서브명) 지우기
df['지하철역'] = df['지하철역'].str.split('(').str[0]

# 중복된 지하철역의 [승하차인구수]를 하나로 합친 df 생성, [호선명]도 삭제
passenger_df = df.groupby('지하철역')['승하차인구수'].sum().reset_index()

print(passenger_df)


#다른 파일에서 df를 부를 수 있게 저장
with open( "passenger", "wb" ) as file:
    pickle.dump( passenger_df, file)