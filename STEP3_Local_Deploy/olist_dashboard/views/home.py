"""Olist 대시보드 홈."""
import plotly.graph_objects as go
import streamlit as st

from utils.data import chart_monthly, kpis, load_data

st.markdown("Olist / **홈**")
st.title("Olist 이커머스 대시보드")
st.markdown("브라질 마켓플레이스의 주문 흐름을 살펴보고, 리뷰·상품·판매자 데이터를 활용한 AI 모델을 체험하세요.")

orders, _ = load_data()
st.badge(f"{orders['월'].min()} ~ {orders['월'].max()} 데이터", color="violet", icon=":material/calendar_month:")
summary = kpis(orders)
monthly_orders = orders.groupby("월").size()
ratings = orders["review_score"].value_counts().reindex(range(1, 6), fill_value=0)
model_areas = {"리뷰": 1, "상품": 1, "판매자": 2}

sales, note = chart_monthly(orders, "매출")
revenue = sales.data[0].y
peak = max(revenue)
sales.update_traces(marker_color=["#22826A" if value == peak else "#365479" for value in revenue])

cards = (
    ("분석한 주문", summary["주문 수"], "receipt_long", "blue", "월별 주문 수",
     go.Figure(go.Scatter(x=monthly_orders.index, y=monthly_orders.values, mode="lines")),
     "월별 주문 건수의 변화"),
    ("총매출", summary["매출"], "payments", "green", "월별 매출 (R$)",
     sales, "월별 매출 추이. 녹색 막대는 매출이 가장 높은 달입니다."),
    ("평균 별점", summary["평균 리뷰"], "star", "blue", "별점별 리뷰 수",
     go.Figure(go.Scatter(x=ratings.index, y=ratings.values, mode="markers", marker=dict(size=11)))
     .update_xaxes(tickmode="linear", dtick=1, ticksuffix="점").update_yaxes(rangemode="tozero"),
     "1점부터 5점까지 별점별 리뷰 건수"),
    ("AI 모델", f"{sum(model_areas.values())}개", "smart_toy", "violet", "기능별 모델 구성",
     go.Figure(go.Pie(labels=list(model_areas), values=list(model_areas.values()),
                     hole=0.58, sort=False, textinfo="label+value",
                     textposition="inside", hovertemplate="%{label} %{value}개<extra></extra>")),
     "리뷰 모델 1개, 상품 모델 1개, 판매자 모델 2개"),
)
for row in (cards[:2], cards[2:]):
    for column, (label, value, icon, color, subtitle, chart, alt) in zip(st.columns(2), row):
        with column.container(border=True, gap="small"):
            st.metric(f":{color}-background[{label}]", value, icon=f":material/{icon}:")
            st.markdown(f"**{subtitle}**")
            chart.update_layout(title=None, margin=dict(l=8, r=8, t=8, b=8), showlegend=False)
            st.plotly_chart(chart, height=220, alt=alt, config={"displayModeBar": False})

st.caption(note)
if st.button("데이터 분석 보기", type="primary", icon=":material/arrow_forward:", key="open_analysis"):
    st.switch_page("views/analysis.py")



st.header("AI 도구", anchor="ai-tools")
tools = (
    ("sentiment", "리뷰 감성 분석", ":material/chat:", "리뷰가 긍정적인지 부정적인지 확인합니다."),
    ("recommend", "상품 추천", ":material/shopping_bag:", "선택한 상품과 비슷한 상품 5개를 찾습니다."),
    ("segment", "판매자 유형", ":material/storefront:", "지표 5개로 판매자 유형을 확인합니다."),
    ("churn", "판매자 이탈 위험", ":material/monitoring:", "이탈 확률이 높은 판매자부터 확인합니다."),
)
for row in (tools[:2], tools[2:]):
    for column, (path, label, icon, description) in zip(st.columns(2), row):
        with column.container(border=True, height="stretch", gap="small"):
            st.page_link(f"views/{path}.py", label=f"**{label}**", icon=icon, width="stretch")
            st.markdown(description)

st.header("데이터에 질문하기", anchor="analysis-qa")
with st.container(border=True, gap="small"):
    st.page_link("views/qa.py", label="**분석 Q&A**", icon=":material/forum:", width="stretch")
    st.markdown("주문과 판매자에 대해 질문하면 분석 결과에서 근거를 찾습니다.")
    st.caption("OpenAI API 키 필요")

with st.expander("데이터 및 모델 파일"):
    st.markdown("""
- **데이터 분석** · orders, items
- **리뷰 감성 분석** · `part7_1_sentiment_ml.pkl`
- **상품 추천** · `part6_recommend.pkl`
- **판매자 유형** · `part8_seller_segment.pkl`
- **판매자 이탈 위험** · `part9_seller_churn.pkl`, `seller_table.csv`
- **분석 Q&A** · `olist_facts.csv`, `olist_model_guide.md`
""")
    st.caption("모델 파일 합계 약 340KB · 리뷰 감성 분석은 STEP1 머신러닝 모델(07_1) 사용")


