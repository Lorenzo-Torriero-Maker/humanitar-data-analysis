# -*- coding: utf-8 -*-


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

#Data Cleaning#
df = pd.read_csv("Fin.csv")
df = df[df['statusname'] == 'Paid']
pattern1 = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}$'
pattern2 = r'^\d{4}-\d{2}-\d{2}'
df = df[df['realbegin'].str.match(pattern1, na=False)]
df = df[df['birthdate'].str.match(pattern2, na=False)]
df['realbegin'] = pd.to_datetime(df['realbegin'])
df['birthdate'] = pd.to_datetime(df['birthdate'],errors = 'coerce')
start_date = pd.Timestamp('1900-01-01')
end_date = pd.Timestamp('2024-01-01')
df = df[(df['birthdate'] >= start_date) & (df['birthdate'] <= end_date)]
df["Age"] = (df['realbegin'] - df['birthdate']).dt.days // 365
df = df.drop_duplicates()

#Age x N_Exams#

num_exams = df['Age'].value_counts().sort_index()

plt.figure(figsize=(12, 8))
plt.hist(df['Age'], bins=range(df['Age'].min(), df['Age'].max() + 2), color='#4a90e2', edgecolor='black', align='left')
plt.xlabel('Idade (Anos)', fontsize=14)
plt.ylabel('Número de Plantões', fontsize=14)
plt.title('Número de Plantões por Idade', fontsize=16, fontweight='bold')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

plt.tight_layout()
plt.show()

'''This code generates a histogram showing the distribution of the number of shifts by age. Each bar represents the number of shifts performed 
by people in a specific age group, making it possible to see how shift frequency varies across ages. The x-axis shows age, while the y-axis shows the number of 
shifts for each age.'''

#Frequency x Age#
exams = df.groupby(['Age', 'Id']).size()
total_exams = exams.groupby('Age').mean()/12

plt.figure(figsize=(12, 7))
plt.plot(total_exams.index, total_exams.values, color='teal', linewidth=2, marker='o', markersize=5)
plt.grid(visible=True, which='both', linestyle='--', linewidth=0.5, alpha=0.7)
plt.xlabel('Idade (Anos)', fontsize=14)
plt.ylabel('Frequência', fontsize=14)
plt.title('Frequência de Plantões por Idade', fontsize=16, fontweight='bold')
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

plt.show()

'''This code generates a line chart showing the average monthly shift frequency by age. The average is calculated by dividing the total number of shifts for each age 
by the number of months. The x-axis represents age, while the y-axis shows the average monthly frequency of shifts.'''

#Histograms#
one_year_ago1 = datetime.now() - timedelta(days = 365)
df2 = df[df['realbegin'] >= one_year_ago1]
really_active_doctors = df2.groupby(['Id']).size()/48
really_active_doctors = really_active_doctors[really_active_doctors > 3]
df2 = df2[df2['Id'].isin(really_active_doctors.index)]
today = pd.Timestamp(datetime.now())
df2['Real_Age'] = ((pd.Timestamp.now() - df2['birthdate']).dt.days // 365.25).astype(int)
df2 = df2[["Id","Real_Age"]].drop_duplicates()

plt.figure(figsize=(12, 8))
plt.hist(df2['Real_Age'], bins=range(df2['Real_Age'].min(), df2['Real_Age'].max() + 2), color='#ff7f50', edgecolor='black', align='left')
plt.xlabel('Idade (Anos)', fontsize=14)
plt.ylabel('Número de Médicos', fontsize=14)
plt.title('Número de Médicos Muito Ativos por Idade ', fontsize=16, fontweight='bold')
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

plt.tight_layout()
plt.show()

plt.figure(figsize=(12, 8))
plt.hist(df2['Real_Age'], bins=range(df2['Real_Age'].min(), df2['Real_Age'].max() + 2), color='#ff7f50', edgecolor='black', align='left',cumulative = True)
plt.xlabel('Idade (Anos)', fontsize=14)
plt.ylabel('Número de Médicos', fontsize=14)
plt.title('Número de Médicos Muito Ativos por Idade ', fontsize=16, fontweight='bold')
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

plt.tight_layout()
plt.show()


'''This code generates a histogram showing the number of highly active physicians by age. A physician is considered “highly active” when they perform more than three 
shifts per week on average over the previous year. The initial filter selects physicians with activity in the last 365 days, and the minimum 
threshold of three shifts per week, or 48 shifts per year, is applied to identify these professionals. The x-axis represents age, while the y-axis shows 
the number of highly active physicians in each age group.'''

df3 = df.copy()
df3 = df[df['realbegin'] >= one_year_ago1]
active_doctors = df3.groupby(['Id']).size()/12
active_doctors = active_doctors[active_doctors > 3]
active_doctors = active_doctors.index.difference(really_active_doctors.index)
df3 = df3[df3['Id'].isin(active_doctors)]
df3['Real_Age'] = ((pd.Timestamp.now() - df3['birthdate']).dt.days // 365.25).astype(int)
df3 = df3[["Id","Real_Age"]].drop_duplicates()


plt.figure(figsize=(12, 8))
plt.hist(df3['Real_Age'], bins=range(df3['Real_Age'].min(), df3['Real_Age'].max() + 2), color='#e74c3c', edgecolor='black', align='left', alpha=0.8)
plt.xlabel('Idade (Anos)', fontsize=14)
plt.ylabel('Número de Médicos', fontsize=14)
plt.title('Número de Médicos Ativos por Idade', fontsize=16, fontweight='bold')
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

plt.tight_layout()
plt.show()

plt.figure(figsize=(12, 8))
plt.hist(df3['Real_Age'], bins=range(df3['Real_Age'].min(), df3['Real_Age'].max() + 2), color='#e74c3c', edgecolor='black', align='left', alpha=0.8,cumulative = True)
plt.xlabel('Idade (Anos)', fontsize=14)
plt.ylabel('Número de Médicos', fontsize=14)
plt.title('Número de Médicos Ativos por Idade', fontsize=16, fontweight='bold')
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

plt.tight_layout()
plt.show()


'''This code generates a histogram showing the number of active physicians by age. A physician is classified as “active” if they completed more than 
three shifts per month, on average, during the previous year. Physicians already classified as “highly active” — those who performed more 
than three shifts per week — are excluded from this group. The x-axis represents age, while the y-axis shows the number of active physicians in each age group.'''

one_year_ago1 = datetime.now() - timedelta(days = 182)
df4 = df[df['realbegin'] >= one_year_ago1]
non_active_doctors = df4.groupby(['Id']).size()/12
non_active_doctors = non_active_doctors[non_active_doctors < 3]
df4 = df4[df4['Id'].isin(non_active_doctors.index)]
df4['Real_Age'] = ((pd.Timestamp.now() - df4['birthdate']).dt.days // 365.25).astype(int)
df4 = df4[["Id","Real_Age"]].drop_duplicates()


plt.figure(figsize=(12, 8))
plt.hist(df4['Real_Age'], bins=range(df4['Real_Age'].min(), df4['Real_Age'].max() + 2), color='#2ecc71', edgecolor='black', align='left', alpha=0.8)
plt.xlabel('Idade (Anos)', fontsize=14)
plt.ylabel('Número de Médicos', fontsize=14)
plt.title('Número de Médicos Inativos por Idade', fontsize=16, fontweight='bold')
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

plt.tight_layout()
plt.show()

plt.figure(figsize=(12, 8))
plt.hist(df4['Real_Age'], bins=range(df4['Real_Age'].min(), df4['Real_Age'].max() + 2), color='#2ecc71', edgecolor='black', align='left', alpha=0.8,cumulative = True)
plt.xlabel('Idade (Anos)', fontsize=14)
plt.ylabel('Número de Médicos', fontsize=14)
plt.title('Número de Médicos Inativos por Idade', fontsize=16, fontweight='bold')
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

plt.tight_layout()
plt.show()

'''This code generates a histogram showing the number of inactive physicians by age. A physician is considered “inactive” when 
they have completed fewer than three shifts per month on average during the previous six months, meaning fewer than 18 shifts 
during the period. The x-axis represents age, while the y-axis shows the number of inactive physicians in each age group.'''

#Frequency x N_Doctors#
one_year_ago = datetime.now() - timedelta(days = 365)
active_doctors = df[df['realbegin'] >= one_year_ago]
active_doctors = active_doctors.groupby(['Id']).size()/12

plt.figure(figsize=(12, 8))
plt.hist(active_doctors, bins=30, color='#e67e22', edgecolor='black', alpha=0.8)
plt.yscale('log')
plt.xlabel('Frequência Mensal de Plantões', fontsize=14)
plt.ylabel('Número de Médicos', fontsize=14)
plt.title('Frequência de Plantões por Número de Médicos', fontsize=16, fontweight='bold')
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

plt.tight_layout()
plt.show()


plt.figure(figsize=(12, 8))
plt.hist(active_doctors, bins=30, color='#e67e22', edgecolor='black', alpha=0.8,cumulative = True)
plt.yscale('log')
plt.xlabel('Frequência Mensal de Plantões', fontsize=14)
plt.ylabel('Número de Médicos', fontsize=14)
plt.title('Frequência de Plantões por Número de Médicos', fontsize=16, fontweight='bold')
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

plt.tight_layout()
plt.show()
'''his code generates a histogram showing the distribution of average monthly shift frequency among physicians active during the previous year. In this analysis, an 
active physician is anyone who completed at least one shift per month on average during the last year. The x-axis shows monthly shift frequency, 
while the y-axis indicates the number of physicians within each frequency range.'''
