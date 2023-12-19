import pandas as pd


file_path = r'C:\Users\user\Desktop\학교 수업\2학년\2학기_기말\파이썬을 이용한 데이터사이언스\면적_월임대료.xlsx'
df_width_price = pd.read_excel(file_path, sheet_name='Sheet1')


# 상가이름의 값이 같은 두 행 중에서, 월임대료의 값이 '원'이거나 값이 없으면 해당 행을 제거
df_del_won_or_null = df_width_price[~((df_width_price.duplicated(subset='상가이름', keep=False)) & ((df_width_price['월임대료'] == '원') | (df_width_price['월임대료'] == '')))]

# 상가이름의 값이 같은 두 행 중에서, 월임대료의 값이 같으면 첫 번째 나오는 행을 남기고 나머지 중복된 행을 제거
df_del_dup_price = df_del_won_or_null[~(df_del_won_or_null.duplicated(subset=['상가이름', '월임대료'], keep='first'))]

# 상가이름의 값이 같은 두 행 중에서, 면적의 값이 같으면 첫 번째 나오는 행을 남기고 나머지 중복된 행을 제거
df_del_dup_width = df_del_dup_price[~(df_del_dup_price.duplicated(subset=['상가이름', '면적'], keep='first'))]

# 데이터프레임을 엑셀 파일로 저장
df_del_dup_width.to_excel(r'C:\Users\user\Desktop\학교 수업\2학년\2학기_기말\파이썬을 이용한 데이터사이언스\면적_월임대료_상가번호 중복 제거(최종).xlsx', index=False)

