import datetime
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Аналіз покупок користувачів",
    page_icon="🛒",
)

st.title('Аналіз даних покупок в супермаркеті')

name = st.text_input('Як Вас звати?')
if name:
    st.write(f"Вітаємо, {name}!")

DATE_COLUMN = 'Date'
DATA_URL = ('https://docs.google.com/spreadsheets/d/e/2PACX-1vQf1s4z3C0iRAKOu6ClRTZbqN4ocTWoJX5KLynr7iB_ieK2bP5eZXmX7zyHBr9lmLud1ec4Ve71544L/pub?gid=335944704&single=true&output=csv')


@st.cache_data
def load_data():
    data = pd.read_csv(DATA_URL)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

data_load_state = st.text('Завантаження даних...')
data = load_data()
data_load_state.text("Дані завантажені!")

show_data = st.checkbox('Переглянути дані')

if show_data:
    display_rows = st.slider(
        'Оберіть, з якого по який рядочки даних ви хочете переглянути',
        min_value=0,
        max_value=len(data),
        value=(1000, 10000))
    # Відображення даних залежно від вибраного діапазону рядків
    st.write(data.iloc[display_rows[0]:display_rows[1]])

show_hist = st.sidebar.checkbox('Показати гістограми')
сolumns_for_hist = [
    'DISC',
    'Amount',
    'Net Bill Amount',
    'GST',
    'Gross Bill Amount',
    '% Profit Margin',
    '% Operating Cost',
    '% Product Cost',
    'Profit Margin',
    'Operating Cost',
    'Product Cost',
    'Age',
    'Gender',
    'City',
    'Country',
    'Payment Mode'
]
if show_hist:
    selected_columns = st.sidebar.multiselect(
        'Оберіть колонку для побудови гістограми',
        сolumns_for_hist
    )

    # Показ гістограм за вибраними колонками
    for column in selected_columns:
        fig = px.histogram(data, x=column)
        fig.update_traces(opacity=.6) # аби встановити прозорість
        st.subheader(f'Розподіл за {column}')
        st.plotly_chart(fig)

show_average_indicators = st.sidebar.checkbox('Показати середні показники в динаміці за датою')
сolumns_for_chart = [
    'DISC',
    'Amount',
    'Net Bill Amount',
    'GST',
    'Gross Bill Amount',
    '% Profit Margin',
    '% Operating Cost',
    '% Product Cost',
    'Profit Margin',
    'Operating Cost',
    'Product Cost'
]

if show_average_indicators:
    selected_columns = st.sidebar.multiselect(
        'Оберіть колонку для побудови графіку в динаміці',
        сolumns_for_chart
    )

    display_dates = st.slider(
        'Оберіть діапазон дат для перегляду',
        min_value=data.Date.min(),
        max_value=data.Date.max(),
        value=(
            datetime.datetime(2016, 1, 1, 0, 0),
            datetime.datetime(2016, 12, 31, 0, 0)
        )
    )
    # Фільтрація даних за вибраним діапазоном дат
    filtered_data = data[(data['Date'] >= display_dates[0]) & (data['Date'] <= display_dates[1])]

    # Групування по даті та обчислення середніх значень за обраною колонкою
    avg_data = filtered_data.groupby('Date')[selected_columns].mean().reset_index()

    # Побудова графіків середніх значень
    for column in selected_columns:
        st.subheader(f'Динаміка середніх значень {column}')
        st.line_chart(avg_data.set_index('Date')[column], y=[column])

st.button("Re-run")