import pandas as pd
import re

# 크롤링을 통해 얻은 면적_월임대료 데이터 불러오기
df = pd.read_excel(r'C:\Users\user\Desktop\학교 수업\2학년\2학기_기말\파이썬을 이용한 데이터사이언스\면적_월임대료_상가번호 중복 제거(최종).xlsx', sheet_name='Sheet1')


# 각 역에 현재 활성화된 상가의 수를 알기 위해
# 마지막에 나온 '역'을 기준으로 앞 문자열만 남기고 뒷 문자열을 역으로 대체/ ~~역 ~~호 라서 ~~역끼리 그룹화하기 위해선 역 뒤의 ~~호를 지워줘야함
df['상가이름'] = df['상가이름'].apply(lambda x: re.sub('(.*)역.*', r'\1역', x))


# '상가이름'을 기준으로 그룹화하고 각 그룹의 개수 세기
grouped_count = df.groupby(['호선명', '상가이름']).size()
# for group_name, size in grouped_count.items():
#     print(f"Group: {group_name}, Size: {size}")
# print(grouped_count)


# 결과를 딕셔너리로 변환
result_dict = grouped_count.to_dict()


# 딕셔너리의 키를 행으로, 값은 열로 변환하여 데이터프레임 생성
result_df = pd.DataFrame(list(result_dict.keys()), columns=['호선명', '상가이름'])
result_df['사용 상가 수'] = result_dict.values()

# 데이터프레임을 엑셀 파일로 저장
result_df.to_excel(r'C:\Users\user\Desktop\학교 수업\2학년\2학기_기말\파이썬을 이용한 데이터사이언스\사용상가수_돌려서 나온거.xlsx', index=False)
