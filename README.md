# Olist 이커머스 AI  분석 모델

브라질 온라인 마켓플레이스 Olist의 주문 데이터를 분석하는 Streamlit 대시보드입니다. 매출과 주문 흐름을 살펴보고, 리뷰·상품·판매자 데이터를 활용한 AI 모델을 체험할 수 있습니다.

## 주요 기능

| 화면 | 할 수 있는 일 |
| --- | --- |
| 홈 | 월별 주문, 월별 매출, 별점 분포, AI 모델 구성을 한눈에 확인 |
| 데&#8288;이&#8288;터&nbsp;분&#8288;석 | 지역과 기간을 선택해 월별 실적, 요일·시간별 주문, 상품군별 매출, 배송과 별점, 브라질 주별 지표 비교. 주문 데이터 CSV 다운로드 |
| 리&#8288;뷰&nbsp;감&#8288;성&nbsp;분&#8288;석 | 리뷰 문장을 입력해 긍정·부정 감성 판정 |
| 상&#8288;품&nbsp;추&#8288;천 | 선택한 상품과 비슷한 상품 찾기 |
| 판&#8288;매&#8288;자&nbsp;유&#8288;형 | 판매 지표를 입력해 판매자 유형 확인 |
| 판&#8288;매&#8288;자&nbsp;이&#8288;탈&nbsp;위&#8288;험 | 판매자별 이탈 위험과 관리 우선순위 확인 |
| 분&#8288;석&nbsp;Q&#8288;&&#8288;A | Olist 분석 자료를 검색하고 근거 ID와 함께 답변 확인 |

## 로컬에서 실행

Python 3.12 환경을 기준으로 합니다.

```bash
git clone https://github.com/sinyoungk0711-droid/Olist_Data_Analysis.git
cd Olist_Data_Analysis/STEP3_Local_Deploy/olist_dashboard
python -m pip install -r requirements.txt
python -m pip install "streamlit==1.67.0"
python -m streamlit run app.py
```

브라우저에서 [http://localhost:8501](http://localhost:8501)에 접속합니다. Streamlit 버전은 현재 홈 화면의 차트와 아이콘 기능을 기준으로 지정했습니다.

**분석 Q&A**를 사용하려면 OpenAI API 키가 필요합니다. 대시보드 사이드바에 입력하거나, 환경 변수 `OPENAI_API_KEY` 또는 로컬 `.streamlit/secrets.toml`에 설정할 수 있습니다. API 키는 저장소에 올리지 마세요.

## 앱 구성

앱 코드는 [STEP3_Local_Deploy/olist_dashboard](STEP3_Local_Deploy/olist_dashboard)에 있습니다.

- `app.py`는 앱의 시작 파일이며 페이지 메뉴를 등록합니다.
- `views/`는 홈, 데이터 분석, AI 모델, 분석 Q&A 화면을 담고 있습니다.
- `utils/`는 데이터 처리, 모델 실행, 분석 자료 검색에 사용하는 코드를 담고 있습니다.

## 데이터 출처

브라질 이커머스 주문 데이터는 [Olist Brazilian E-Commerce Public Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)을 사용합니다.
