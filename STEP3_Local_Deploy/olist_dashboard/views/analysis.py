"""Olist 데이터 분석 페이지."""
import streamlit as st

from utils.data import (
    chart_category, chart_delivery, chart_monthly, chart_region, chart_time,
    filter_data, insights, kpis, load_data,
)


def show_chart(figure, description, alt, height=320):
    figure.update_layout(title=None, margin=dict(l=8, r=8, t=12, b=8))
    st.plotly_chart(figure, height=height, alt=alt, config={"displayModeBar": False})
    st.caption(description)


st.markdown("Olist / **데이터 분석**")
st.title("데이터 분석", icon=":material/analytics:")
st.markdown("주문과 매출의 흐름, 인기 상품군, 배송과 별점의 관계를 살펴보세요.")

orders, items = load_data()
months = sorted(orders["월"].unique())
state = st.sidebar.selectbox("고객 지역", ["전체"] + sorted(orders["customer_state"].unique()))
period = st.sidebar.select_slider("기간", options=months, value=(months[0], months[-1]))
filtered_orders, filtered_items = filter_data(orders, items, state, period)
st.badge(f"배송 완료 주문 · {period[0]} ~ {period[1]} · {state}", color="violet")

if filtered_orders.empty:
    st.warning("선택한 지역과 기간에 주문이 없습니다. 사이드바에서 조건을 바꿔 보세요.")
    st.stop()

metric_icons = ("receipt_long", "payments", "shopping_cart", "local_shipping", "schedule", "star")
for column, (label, value), icon in zip(
    st.columns(3) + st.columns(3), kpis(filtered_orders).items(), metric_icons
):
    column.metric(label, value, icon=f":material/{icon}:", border=True)

with st.container(border=True):
    st.subheader("월별 실적", icon=":material/bar_chart:")
    metric = st.radio("지표", ["매출", "주문 수", "객단가"], horizontal=True)
    figure, description = chart_monthly(filtered_orders, metric)
    values = figure.data[0].y
    peak = max(values)
    figure.update_traces(marker_color=["#22826A" if value == peak else "#365479" for value in values])
    show_chart(figure, description, f"월별 {metric} 추이. 녹색 막대는 최고값입니다.", height=360)

left, right = st.columns(2)
with left.container(border=True, height="stretch"):
    st.subheader("요일·시간별 주문", icon=":material/calendar_month:")
    figure, description = chart_time(filtered_orders)
    figure.update_traces(x=sorted(filtered_orders["주문시각"].dt.hour.unique()))
    show_chart(figure, description, "요일과 시간대별 주문량을 보여 주는 열지도")

with right.container(border=True, height="stretch"):
    st.subheader("상품군별 매출 상위 10개", icon=":material/category:")
    if filtered_items["product_category_name_english"].notna().any():
        figure, description = chart_category(filtered_items)
        show_chart(figure, description, "매출 상위 상품군의 가로 막대그래프")
    else:
        st.info("선택한 조건에 상품군 정보가 없습니다.")

left, right = st.columns(2)
with left.container(border=True, height="stretch"):
    st.subheader("배송과 별점", icon=":material/local_shipping:")
    figure, _ = chart_delivery(filtered_orders)
    figure.update_traces(marker_color=[
        "#7554A3" if status == "지연 도착" else "#365479" for status in figure.data[0].x
    ])
    figure.update_yaxes(range=[0, 5.5], tickvals=list(range(6)))
    late_share = filtered_orders["지연"].mean()
    show_chart(figure, f"선택한 조건의 배송 지연율은 **{late_share:.1%}**입니다.",
               "제때 도착한 주문과 지연된 주문의 평균 별점 비교")

with right.container(border=True, height="stretch"):
    st.subheader("브라질 주별 비교", icon=":material/public:")
    figure, description = chart_region(filtered_orders)
    show_chart(figure, description, "주별 배송 기간과 평균 별점. 원의 크기는 주문 수를 나타냅니다.")

with st.expander("핵심 인사이트", icon=":material/lightbulb:"):
    for sentence in insights(filtered_orders):
        st.markdown(f"- {sentence}")

with st.expander("주문 데이터 및 CSV", icon=":material/table_chart:"):
    st.dataframe(filtered_orders.head(100), alt="선택한 조건의 배송 완료 주문 100건 미리보기")
    st.download_button("CSV 내려받기", filtered_orders.to_csv(index=False).encode("utf-8-sig"), "olist_orders.csv")

