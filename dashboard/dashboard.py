import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')

def create_sum_product_df(df):
    sum_product_df = df.groupby(by="product_category_name_english").order_item_id.sum().sort_values(ascending=False).reset_index()
    return sum_product_df



all_df = pd.read_csv("all_data.csv")

datetime_columns = ["order_purchase_timestamp"]
all_df.sort_values(by="order_purchase_timestamp", inplace=True)
all_df.reset_index(inplace=True)
 
for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

min_date = all_df["order_purchase_timestamp"].min()
max_date = all_df["order_purchase_timestamp"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://i.pinimg.com/originals/45/8b/0a/458b0a1ea92c0b7e39d0d427c5262dfb.jpg")
    
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    
main_df = all_df[(all_df["order_purchase_timestamp"] >= str(start_date)) & 
                (all_df["order_purchase_timestamp"] <= str(end_date))]

sum_product_df = create_sum_product_df(main_df)
beauty_categories = ['perfumery', 'health_beauty', 'cosmetics']
beauty_overall_data = main_df[main_df['product_category_name_english'].isin(beauty_categories)]
beauty_overall_sales_trend = beauty_overall_data.resample('ME', on='order_purchase_timestamp').size()

st.header('Dicoding Submission Dashboard :sparkles:')
st.subheader('Most and Least Purchased Product in Range '+str(start_date)+' - '+str(end_date))
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(40, 15))
 
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
 
sns.barplot(x="order_item_id", y="product_category_name_english", data=sum_product_df.head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Number of Purchased", fontsize=50)
ax[0].set_title("Most Purchased Product", loc="center", fontsize=70)
ax[0].tick_params(axis ='y', labelsize=40)
ax[0].tick_params(axis='x', labelsize=50)

 
sns.barplot(x="order_item_id", y="product_category_name_english", data=sum_product_df.sort_values(by="order_item_id", ascending=True).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Number of Purchased", fontsize=50)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Least Purchased Product", loc="center", fontsize=70)
ax[1].tick_params(axis='y', labelsize=40)
ax[1].tick_params(axis='x', labelsize=50)

st.pyplot(fig)

st.subheader('Overall Sales Trend of Beauty Products')
plt.figure(figsize=(10, 6))
plt.plot(beauty_overall_sales_trend.index, beauty_overall_sales_trend.values, marker='o', color='teal')
plt.xlabel('Date', fontsize=12)
plt.ylabel('Number of Sales', fontsize=12)
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()

st.pyplot(plt)