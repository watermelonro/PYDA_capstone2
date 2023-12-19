import pandas as pd

# 엑셀 파일 경로 지정
excel_file_path = r'C:\Users\user\Desktop\학교 수업\2학년\2학기_기말\파이썬을 이용한 데이터사이언스\시간대별_승하차합_15년~23년10월.xlsx'

# 엑셀 파일 불러오기
df = pd.read_excel(excel_file_path, sheet_name='Sheet1')


# 'column_name' 열의 값에 따라 그룹화/ 2015년1월부터 2023년 10월까지의 승하차인구수를 각 호선별 역별을 그룹화
grouped_df = df.groupby(['호선명', '지하철역'])


# '승하차인구수' 열에 대한 평균 계산
average_values = grouped_df['승하차인구수'].mean().round().astype(int)


# 결과를 딕셔너리로 변환
result_dict = average_values.to_dict()


# 딕셔너리의 키를 행으로, 값은 열로 변환하여 데이터프레임 생성
result_df = pd.DataFrame(list(result_dict.keys()), columns=['호선명', '지하철역'])
result_df['승하차인구수'] = result_dict.values()


# 데이터프레임을 엑셀 파일로 저장
result_df.to_excel(r'C:\Users\user\Desktop\학교 수업\2학년\2학기_기말\파이썬을 이용한 데이터사이언스\승하차_인구수.xlsx', index=False)

