
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import warnings

warnings.filterwarnings("ignore")

sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)

print("Loading data...\n")

df1 = pd.read_csv('bank-full.csv', sep=';')
df2 = pd.read_csv('bank-additional-full.csv', sep=';')
df = pd.concat([df1, df2], ignore_index=True)

df['duration_min'] = df['duration'] / 60.0
df['y_binary'] = df['y'].map({'yes': 1, 'no': 0})

print(f"Total Contacts     : {len(df):,}")
print(f"Total Conversions  : {df['y_binary'].sum():,}")
print(f"Overall CR         : {df['y_binary'].mean()*100:.2f}%\n")

os.makedirs("charts", exist_ok=True)

try:
    import plotly.express as px
    plotly_available = True
    print("Plotly is available - Interactive HTML charts will be generated")
except ImportError:
    plotly_available = False
    print("Plotly not available - Only static PNG charts will be generated")

fig, ax = plt.subplots()
counts = [len(df) - df['y_binary'].sum(), df['y_binary'].sum()]
ax.bar(['No', 'Yes'], counts, color=['lightgray', 'steelblue'])
ax.set_title('Overall Conversion: Yes vs No')
ax.set_ylabel('Number of Contacts')
for i, v in enumerate(counts):
    ax.text(i, v + 800, f"{v:,}", ha='center')
plt.savefig("charts/01_Overall_Conversion.png", bbox_inches='tight', dpi=200)
plt.close()
print("Saved: 01_Overall_Conversion.png")

if plotly_available:
    fig1 = px.pie(names=['No', 'Yes'], values=counts, title='Overall Conversion Rate')
    fig1.write_html("charts/01_Overall_Conversion_Interactive.html")

channel = df.groupby('contact')['y_binary'].agg(['count', 'sum']).reset_index()
channel['conv_rate'] = (channel['sum'] / channel['count'] * 100).round(2)

fig, ax = plt.subplots()
sns.barplot(data=channel, x='contact', y='conv_rate', hue='contact', palette='Blues', legend=False, ax=ax)
ax.set_title('Conversion Rate by Contact Channel')
ax.set_ylabel('Conversion Rate (%)')
for i, row in channel.iterrows():
    ax.text(i, row['conv_rate'] + 0.5, f"{row['conv_rate']}%", ha='center')
plt.savefig("charts/02_Channel_Funnel.png", bbox_inches='tight', dpi=200)
plt.close()
print("Saved: 02_Channel_Funnel.png")

if plotly_available:
    fig2 = px.bar(channel, x='contact', y='conv_rate', text='conv_rate',
                  title='Interactive: Conversion by Contact Channel',
                  color='conv_rate', color_continuous_scale='Blues')
    fig2.update_traces(hovertemplate='<b>%{x}</b><br>Rate: %{y:.2f}%<br>Contacts: %{customdata[0]:,}<br>Conversions: %{customdata[1]:,}<extra></extra>',
                       customdata=channel[['count','sum']])
    fig2.write_html("charts/02_Channel_Funnel_Interactive.html")

bins = [0, 1, 3, 5, 10, np.inf]
labels = ['<1min', '1-3min', '3-5min', '5-10min', '>10min']
df['duration_bin'] = pd.cut(df['duration_min'], bins=bins, labels=labels, right=False)

dur = df.groupby('duration_bin', observed=True)['y_binary'].agg(['count', 'sum']).reset_index()
dur['conv_rate'] = (dur['sum'] / dur['count'] * 100).round(2)

fig, ax = plt.subplots()
sns.barplot(data=dur, x='duration_bin', y='conv_rate', hue='duration_bin', palette='Greens', legend=False, ax=ax)
ax.set_title('Zero-Lag: Conversion by Call Duration')
ax.set_ylabel('Conversion Rate (%)')
for i, row in dur.iterrows():
    ax.text(i, row['conv_rate'] + 1, f"{row['conv_rate']}%", ha='center')
plt.savefig("charts/03_Duration_Funnel.png", bbox_inches='tight', dpi=200)
plt.close()
print("Saved: 03_Duration_Funnel.png")

if plotly_available:
    fig3 = px.bar(dur, x='duration_bin', y='conv_rate', text='conv_rate',
                  title='Interactive: Conversion by Call Duration',
                  color='conv_rate', color_continuous_scale='Tealgrn')
    fig3.update_traces(hovertemplate='<b>%{x}</b><br>Rate: %{y:.2f}%<br>Calls: %{customdata[0]:,}<br>Conversions: %{customdata[1]:,}<extra></extra>',
                       customdata=dur[['count','sum']])
    fig3.write_html("charts/03_Duration_Funnel_Interactive.html")

month_order = ['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']
monthly = df.groupby('month')['y_binary'].agg(['count','sum']).reset_index()
monthly['conv_rate'] = (monthly['sum']/monthly['count']*100).round(1)
monthly['month'] = pd.Categorical(monthly['month'], categories=month_order, ordered=True)
monthly = monthly.sort_values('month')

fig, ax = plt.subplots()
sns.barplot(data=monthly, x='month', y='conv_rate', hue='month', palette='viridis', legend=False, ax=ax)
ax.set_title('Monthly Conversion Rates')
ax.set_ylabel('Conversion Rate (%)')
for i, row in monthly.iterrows():
    ax.text(i, row['conv_rate'] + 0.5, f"{row['conv_rate']}%", ha='center')
plt.savefig("charts/04_Monthly_Seasonality.png", bbox_inches='tight', dpi=200)
plt.close()
print("Saved: 04_Monthly_Seasonality.png")

if plotly_available:
    fig4 = px.bar(monthly, x='month', y='conv_rate', text='conv_rate',
                  title='Interactive: Monthly Conversion Rates',
                  color='conv_rate', color_continuous_scale='Viridis')
    fig4.update_traces(hovertemplate='<b>%{x}</b><br>Rate: %{y:.1f}%<br>Contacts: %{customdata[0]:,}<br>Conversions: %{customdata[1]:,}<extra></extra>',
                       customdata=monthly[['count','sum']])
    fig4.write_html("charts/04_Monthly_Seasonality_Interactive.html")

df['age_group'] = pd.cut(df['age'], bins=[0,25,35,45,55,65,100],
                         labels=['<25','25-34','35-44','45-54','55-64','65+'])

age = df.groupby('age_group', observed=True)['y_binary'].agg(['count','sum']).reset_index()
age['conv_rate'] = (age['sum']/age['count']*100).round(1)

fig, ax = plt.subplots()
sns.barplot(data=age, x='age_group', y='conv_rate', hue='age_group', palette='plasma', legend=False, ax=ax)
ax.set_title('Conversion Rate by Age Group')
ax.set_ylabel('Conversion Rate (%)')
for i, row in age.iterrows():
    ax.text(i, row['conv_rate'] + 0.5, f"{row['conv_rate']}%", ha='center')
plt.savefig("charts/05_Age_Group.png", bbox_inches='tight', dpi=200)
plt.close()
print("Saved: 05_Age_Group.png")

if plotly_available:
    fig5 = px.bar(age, x='age_group', y='conv_rate', text='conv_rate',
                  title='Interactive: Conversion by Age Group',
                  color='conv_rate', color_continuous_scale='Plasma')
    fig5.update_traces(hovertemplate='<b>%{x}</b><br>Rate: %{y:.1f}%<br>Contacts: %{customdata[0]:,}<br>Conversions: %{customdata[1]:,}<extra></extra>',
                       customdata=age[['count','sum']])
    fig5.write_html("charts/05_Age_Group_Interactive.html")


job = df.groupby('job')['y_binary'].agg(['count','sum']).reset_index()
job['conv_rate'] = (job['sum']/job['count']*100).round(2)
job = job.sort_values('conv_rate', ascending=False).head(10)

fig, ax = plt.subplots()
sns.barplot(data=job, x='conv_rate', y='job', hue='job', palette='mako', legend=False, ax=ax)
ax.set_title('Top 10 Jobs by Conversion Rate')
ax.set_xlabel('Conversion Rate (%)')
plt.savefig("charts/06_Top_Jobs.png", bbox_inches='tight', dpi=200)
plt.close()
print("Saved: 06_Top_Jobs.png")

edu = df.groupby('education')['y_binary'].agg(['count','sum']).reset_index()
edu['conv_rate'] = (edu['sum']/edu['count']*100).round(2)

fig, ax = plt.subplots()
sns.barplot(data=edu, x='education', y='conv_rate', hue='education', palette='Blues', legend=False, ax=ax)
ax.set_title('Conversion by Education')
plt.xticks(rotation=30)
plt.savefig("charts/07_Education.png", bbox_inches='tight', dpi=200)
plt.close()
print("Saved: 07_Education.png")

pout = df.groupby('poutcome')['y_binary'].agg(['count','sum']).reset_index()
pout['conv_rate'] = (pout['sum']/pout['count']*100).round(2)

fig, ax = plt.subplots()
sns.barplot(data=pout, x='poutcome', y='conv_rate', hue='poutcome', palette='RdYlGn', legend=False, ax=ax)
ax.set_title('Conversion by Previous Outcome')
plt.savefig("charts/08_Previous_Outcome.png", bbox_inches='tight', dpi=200)
plt.close()
print("Saved: 08_Previous_Outcome.png")

df['housing_loan'] = df['housing'] + " + " + df['loan']
hl = df.groupby('housing_loan')['y_binary'].agg(['count','sum']).reset_index()
hl['conv_rate'] = (hl['sum']/hl['count']*100).round(2)

fig, ax = plt.subplots()
sns.barplot(data=hl, x='housing_loan', y='conv_rate', hue='housing_loan', palette='viridis', legend=False, ax=ax)
ax.set_title('Conversion by Housing & Loan')
plt.xticks(rotation=30)
plt.savefig("charts/09_Housing_Loan.png", bbox_inches='tight', dpi=200)
plt.close()
print("Saved: 09_Housing_Loan.png")

camp = df.groupby('campaign')['y_binary'].mean().reset_index()
camp = camp[camp['campaign'] <= 10]

fig, ax = plt.subplots()
sns.lineplot(data=camp, x='campaign', y='y_binary', marker='o', color='darkblue', ax=ax)
ax.set_title('Conversion Rate vs Number of Calls')
plt.savefig("charts/10_Campaign_Effect.png", bbox_inches='tight', dpi=200)
plt.close()
print("Saved: 10_Campaign_Effect.png")

fig, ax = plt.subplots()
sns.boxplot(data=df, x='y', y='balance', showfliers=False, palette='Set2', ax=ax)
ax.set_title('Balance Distribution: Yes vs No')
plt.savefig("charts/11_Balance_Boxplot.png", bbox_inches='tight', dpi=200)
plt.close()
print("Saved: 11_Balance_Boxplot.png")

df['segment'] = df['job'] + " | " + df['education']
seg = df.groupby('segment')['y_binary'].agg(['count','sum']).reset_index()
seg['conv_rate'] = (seg['sum']/seg['count']*100).round(2)
seg = seg[seg['count'] >= 200].nlargest(10, 'conv_rate')

fig, ax = plt.subplots(figsize=(10, 8))
sns.barplot(data=seg, x='conv_rate', y='segment', hue='segment', palette='crest', legend=False, ax=ax)
ax.set_title('Top 10 Best Segments')
ax.set_xlabel('Conversion Rate (%)')
plt.savefig("charts/12_Top_Segments.png", bbox_inches='tight', dpi=200)
plt.close()
print("Saved: 12_Top_Segments.png")

print("\nAll charts generated successfully!")
print("Static PNG files are in the 'charts' folder.")
if plotly_available:
    print("Interactive HTML files (with hover tooltips) are also saved with _Interactive suffix.")
else:
    print("To get interactive hover charts, run: pip install plotly")