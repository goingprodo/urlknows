# 🔍 URL Analytics Dashboard

정확한 데이터로 더 나은 인사이트를 제공하는 종합적인 URL 분석 도구

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)
![Chart.js](https://img.shields.io/badge/Chart.js-3.9+-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📊 주요 기능

### 🌐 **종합 URL 분석**
- **기본 정보**: 상태코드, 응답시간, 콘텐츠 크기, 서버 정보
- **SEO 분석**: 메타태그, 헤딩구조, 이미지 ALT, 내부/외부 링크
- **성능 측정**: 평균 응답시간, DNS 조회시간, 압축여부, 캐싱
- **콘텐츠 분석**: 단어수, 가독성 점수, 주요 키워드 추출
- **보안 분석**: HTTPS, SSL 인증서, 보안 헤더, Mixed Content
- **모바일 호환성**: 뷰포트 메타태그, 반응형 디자인, 미디어 쿼리

### 📈 **시각적 대시보드**
- **실시간 차트**: 성능, SEO, 키워드, 품질 점수 차트
- **반응형 디자인**: 모바일/태블릿 완벽 지원
- **인터랙티브 UI**: 부드러운 애니메이션과 글라스모피즘 효과
- **원클릭 테스트**: 유명 사이트 빠른 분석

## 🚀 빠른 시작

### 1️⃣ **자동 설치 (권장)**

```bash
# 가상환경 생성 및 패키지 설치
make_venv.bat

# 앱 실행
run_gpu.bat
```

### 2️⃣ **수동 설치**

```bash
# 저장소 클론
git clone <repository-url>
cd urlknows

# Python 가상환경 생성
python -m venv venv

# 가상환경 활성화 (Windows)
venv\Scripts\activate

# 패키지 설치
pip install -r requirements.txt

# 앱 실행
python app.py
```

### 3️⃣ **브라우저 접속**

```
http://localhost:5000
```

## 📁 프로젝트 구조

```
urlknows/
├── 📄 main.py              # URLAnalyzer 핵심 라이브러리
├── 🌐 app.py               # Flask 웹 서버
├── 📋 requirements.txt     # 필요한 패키지 목록
├── ⚙️ make_venv.bat       # 자동 설치 스크립트
├── 🚀 run_gpu.bat         # 실행 스크립트
├── 📂 templates/
│   └── 🎨 index.html      # 메인 웹 인터페이스
├── 📂 venv/               # Python 가상환경
└── 📂 __pycache__/        # Python 캐시 파일
```

## 🛠️ 기술 스택

### **백엔드**
- **Python 3.10+**: 핵심 분석 엔진
- **Flask**: 웹 서버 프레임워크
- **BeautifulSoup4**: HTML 파싱
- **Requests**: HTTP 요청 처리
- **NLTK**: 자연어 처리
- **TextStat**: 가독성 분석

### **프론트엔드**
- **HTML5/CSS3**: 모던 웹 표준
- **JavaScript ES6+**: 인터랙티브 기능
- **Chart.js 3.9**: 데이터 시각화
- **Axios**: HTTP 클라이언트
- **Font Awesome**: 아이콘

### **분석 라이브러리**
- **SSL/Socket**: 보안 분석
- **Whois**: 도메인 정보
- **Pandas**: 데이터 처리
- **Matplotlib/Seaborn**: 통계 시각화

## 📦 의존성 패키지

```txt
requests
beautifulsoup4
selenium
webdriver-manager
matplotlib
seaborn
pandas
nltk
textstat
whois
python-whois
gradio
plotly
flask
flask-cors
```

## 🎯 사용법

### **1. 기본 URL 분석**
1. 웹 인터페이스에서 URL 입력
2. 분석 타입 선택 (전체 분석 / 빠른 분석)
3. "🚀 분석 시작" 클릭
4. 실시간 결과 확인

### **2. 예시 URL 테스트**
- Google, GitHub, Wikipedia, Stack Overflow 원클릭 테스트

### **3. 분석 결과 해석**
- **성능 점수**: 0-100점 (높을수록 좋음)
- **SEO 요소**: 링크, 이미지, 메타태그 분석
- **보안 등급**: HTTPS, 보안 헤더 검사
- **모바일 친화성**: 반응형 디자인 평가

## 🔧 개발자 가이드

### **URLAnalyzer 클래스 사용**

```python
from main import URLAnalyzer

# 분석기 초기화
analyzer = URLAnalyzer()

# URL 분석 실행
results = analyzer.analyze_url("https://example.com")

# 리포트 생성
report = analyzer.generate_report(results, 'report.txt')

# 대시보드 데이터 생성
dashboard_data = analyzer.create_dashboard_data(results)
```

### **주요 메서드**
- `analyze_url(url)`: 전체 분석 실행
- `get_basic_info(url)`: 기본 정보만 수집
- `analyze_seo(url)`: SEO 요소 분석
- `measure_performance(url)`: 성능 측정
- `analyze_security(url)`: 보안 검사

### **API 엔드포인트**
- `POST /api/analyze`: URL 분석 실행
- `GET /api/quick-test/<url>`: 빠른 테스트

## 🎨 UI 특징

### **디자인**
- **글라스모피즘**: 반투명 블러 효과
- **그라데이션**: 다채로운 색상 조합
- **애니메이션**: 부드러운 전환 효과
- **다크 테마**: 눈에 편한 어두운 배경

### **반응형**
- **데스크톱**: 1400px 최대 너비
- **태블릿**: 768px 이하 최적화
- **모바일**: 480px 이하 세로 배치

## 🐛 문제 해결

### **일반적인 오류**

1. **패키지 설치 오류**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

2. **NLTK 데이터 오류**
   ```python
   import nltk
   nltk.download('punkt')
   nltk.download('stopwords')
   ```

3. **포트 충돌**
   ```python
   # app.py에서 포트 변경
   app.run(debug=True, host='0.0.0.0', port=5001)
   ```

### **성능 최적화**
- 분석 시간이 오래 걸리는 경우 "빠른 분석" 모드 사용
- 큰 웹사이트는 타임아웃 증가 필요

## 📈 향후 계획

- [ ] **PDF 리포트 생성**
- [ ] **도메인 비교 분석**
- [ ] **분석 히스토리 저장**
- [ ] **API 키 인증**
- [ ] **실시간 모니터링**
- [ ] **Lighthouse 점수 통합**

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.

## 🙏 감사의 말

- [Chart.js](https://www.chartjs.org/) - 데이터 시각화
- [Flask](https://flask.palletsprojects.com/) - 웹 프레임워크
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) - HTML 파싱
- [Font Awesome](https://fontawesome.com/) - 아이콘

---

## 📄 License

- **Non-Commercial**: AGPL-3.0
- **Commercial**: [Contact us](mailto:license@yourcompany.com)

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)

---

**Made with ❤️ by URLKnows Team**

📧 문의사항이 있으시면 언제든 연락해주세요!
