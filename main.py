"""
URL Analytics Library - 종합적인 URL 분석 도구
pip install requests beautifulsoup4 selenium webdriver-manager matplotlib seaborn pandas nltk textstat whois python-whois
"""

import requests
from bs4 import BeautifulSoup
import time
import re
from urllib.parse import urljoin, urlparse, parse_qs
from collections import Counter, defaultdict
import json
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from datetime import datetime, timedelta
import whois
from textstat import flesch_reading_ease, flesch_kincaid_grade
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import ssl
import socket
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import warnings
warnings.filterwarnings('ignore')

class URLAnalyzer:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # NLTK 데이터 다운로드 (처음 실행시)
        try:
            nltk.data.find('tokenizers/punkt')
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('punkt', quiet=True)
            nltk.download('stopwords', quiet=True)
    
    def analyze_url(self, url):
        """메인 분석 함수 - 모든 분석 결과를 반환"""
        print(f"🔍 분석 시작: {url}")
        
        results = {
            'url': url,
            'timestamp': datetime.now().isoformat(),
            'basic_info': self.get_basic_info(url),
            'seo_analysis': self.analyze_seo(url),
            'performance': self.measure_performance(url),
            'content_analysis': self.analyze_content(url),
            'technical_analysis': self.analyze_technical(url),
            'security_analysis': self.analyze_security(url),
            'keyword_analysis': self.analyze_keywords(url),
            'social_media': self.analyze_social_media(url),
            'mobile_analysis': self.analyze_mobile_compatibility(url)
        }
        
        return results
    
    def get_basic_info(self, url):
        """기본 정보 수집"""
        try:
            response = self.session.get(url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            return {
                'status_code': response.status_code,
                'response_time': response.elapsed.total_seconds(),
                'content_length': len(response.content),
                'content_type': response.headers.get('content-type', ''),
                'server': response.headers.get('server', ''),
                'title': soup.title.string if soup.title else '',
                'meta_description': self._get_meta_content(soup, 'description'),
                'language': soup.html.get('lang') if soup.html else '',
                'charset': self._extract_charset(response.headers.get('content-type', ''))
            }
        except Exception as e:
            return {'error': str(e)}
    
    def analyze_seo(self, url):
        """SEO 분석"""
        try:
            response = self.session.get(url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 메타 태그 분석
            meta_tags = {}
            for meta in soup.find_all('meta'):
                name = meta.get('name') or meta.get('property')
                content = meta.get('content')
                if name and content:
                    meta_tags[name] = content
            
            # 헤딩 태그 분석
            headings = {}
            for i in range(1, 7):
                h_tags = soup.find_all(f'h{i}')
                headings[f'h{i}'] = [tag.get_text().strip() for tag in h_tags]
            
            # 이미지 분석
            images = soup.find_all('img')
            img_analysis = {
                'total_images': len(images),
                'images_without_alt': len([img for img in images if not img.get('alt')]),
                'images_without_title': len([img for img in images if not img.get('title')])
            }
            
            # 링크 분석
            links = soup.find_all('a', href=True)
            internal_links = []
            external_links = []
            
            domain = urlparse(url).netloc
            for link in links:
                href = link['href']
                if href.startswith('http'):
                    if domain in href:
                        internal_links.append(href)
                    else:
                        external_links.append(href)
                elif href.startswith('/'):
                    internal_links.append(urljoin(url, href))
            
            return {
                'meta_tags': meta_tags,
                'headings': headings,
                'images': img_analysis,
                'links': {
                    'internal_count': len(internal_links),
                    'external_count': len(external_links),
                    'internal_links': internal_links[:10],  # 상위 10개만
                    'external_links': external_links[:10]
                },
                'robots_txt': self._check_robots_txt(url),
                'sitemap': self._check_sitemap(url)
            }
        except Exception as e:
            return {'error': str(e)}
    
    def measure_performance(self, url):
        """성능 측정"""
        try:
            # 여러 번 요청하여 평균 측정
            times = []
            for _ in range(5):
                start_time = time.time()
                response = self.session.get(url, timeout=10)
                end_time = time.time()
                times.append(end_time - start_time)
                time.sleep(0.5)
            
            # DNS 조회 시간 측정
            domain = urlparse(url).netloc
            dns_start = time.time()
            socket.gethostbyname(domain)
            dns_time = time.time() - dns_start
            
            return {
                'avg_response_time': sum(times) / len(times),
                'min_response_time': min(times),
                'max_response_time': max(times),
                'dns_lookup_time': dns_time,
                'content_size': len(response.content),
                'compression': 'gzip' in response.headers.get('content-encoding', ''),
                'caching': response.headers.get('cache-control', ''),
                'performance_score': self._calculate_performance_score(times, len(response.content))
            }
        except Exception as e:
            return {'error': str(e)}
    
    def analyze_content(self, url):
        """콘텐츠 분석"""
        try:
            response = self.session.get(url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 텍스트 추출
            text = soup.get_text()
            words = word_tokenize(text.lower())
            
            # 불용어 제거
            stop_words = set(stopwords.words('english')) | set(stopwords.words('korean') if 'korean' in stopwords.fileids() else [])
            filtered_words = [word for word in words if word.isalnum() and word not in stop_words]
            
            return {
                'word_count': len(filtered_words),
                'character_count': len(text),
                'paragraph_count': len(soup.find_all('p')),
                'reading_ease': flesch_reading_ease(text) if text else 0,
                'reading_grade': flesch_kincaid_grade(text) if text else 0,
                'most_common_words': dict(Counter(filtered_words).most_common(20)),
                'content_density': len(filtered_words) / len(response.content) * 1000 if response.content else 0
            }
        except Exception as e:
            return {'error': str(e)}
    
    def analyze_technical(self, url):
        """기술적 분석"""
        try:
            response = self.session.get(url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # JavaScript 및 CSS 파일 분석
            scripts = soup.find_all('script', src=True)
            stylesheets = soup.find_all('link', rel='stylesheet')
            
            # Schema.org 마크업 확인
            schema_scripts = soup.find_all('script', type='application/ld+json')
            
            return {
                'doctype': str(soup.contents[0]) if soup.contents else '',
                'html5': '<!DOCTYPE html>' in response.text.upper(),
                'javascript_files': len(scripts),
                'css_files': len(stylesheets),
                'inline_scripts': len(soup.find_all('script', src=False)),
                'inline_styles': len(soup.find_all('style')),
                'schema_markup': len(schema_scripts),
                'viewport_meta': bool(soup.find('meta', attrs={'name': 'viewport'})),
                'responsive_design': self._check_responsive_design(soup),
                'technologies': self._detect_technologies(response.headers, soup)
            }
        except Exception as e:
            return {'error': str(e)}
    
    def analyze_security(self, url):
        """보안 분석"""
        try:
            response = self.session.get(url, timeout=10)
            
            # SSL 인증서 확인
            is_https = url.startswith('https://')
            ssl_info = {}
            
            if is_https:
                domain = urlparse(url).netloc
                context = ssl.create_default_context()
                with socket.create_connection((domain, 443), timeout=10) as sock:
                    with context.wrap_socket(sock, server_hostname=domain) as ssock:
                        cert = ssock.getpeercert()
                        ssl_info = {
                            'issuer': dict(x[0] for x in cert['issuer']),
                            'subject': dict(x[0] for x in cert['subject']),
                            'expires': cert['notAfter']
                        }
            
            return {
                'https': is_https,
                'ssl_certificate': ssl_info,
                'security_headers': {
                    'strict_transport_security': response.headers.get('strict-transport-security'),
                    'content_security_policy': response.headers.get('content-security-policy'),
                    'x_frame_options': response.headers.get('x-frame-options'),
                    'x_content_type_options': response.headers.get('x-content-type-options')
                },
                'mixed_content': self._check_mixed_content(response.text, is_https)
            }
        except Exception as e:
            return {'error': str(e)}
    
    def analyze_keywords(self, url):
        """키워드 분석"""
        try:
            response = self.session.get(url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 텍스트 추출 및 키워드 분석
            title = soup.title.string if soup.title else ''
            meta_desc = self._get_meta_content(soup, 'description')
            headings = ' '.join([h.get_text() for h in soup.find_all(['h1', 'h2', 'h3'])])
            body_text = soup.get_text()
            
            # 키워드 밀도 계산
            all_text = f"{title} {meta_desc} {headings} {body_text}".lower()
            words = re.findall(r'\b\w+\b', all_text)
            word_freq = Counter(words)
            
            # 불용어 제거
            stop_words = set(stopwords.words('english'))
            filtered_freq = {word: freq for word, freq in word_freq.items() 
                           if word not in stop_words and len(word) > 2}
            
            total_words = len(words)
            keyword_density = {word: (freq/total_words)*100 
                             for word, freq in list(filtered_freq.items())[:20]}
            
            return {
                'total_words': total_words,
                'unique_words': len(set(words)),
                'keyword_density': keyword_density,
                'top_keywords': dict(Counter(filtered_freq).most_common(20)),
                'title_keywords': Counter(re.findall(r'\b\w+\b', title.lower())),
                'meta_keywords': self._get_meta_content(soup, 'keywords')
            }
        except Exception as e:
            return {'error': str(e)}
    
    def analyze_social_media(self, url):
        """소셜 미디어 분석"""
        try:
            response = self.session.get(url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Open Graph 태그
            og_tags = {}
            for meta in soup.find_all('meta', property=re.compile(r'^og:')):
                og_tags[meta['property']] = meta.get('content', '')
            
            # Twitter Card 태그
            twitter_tags = {}
            for meta in soup.find_all('meta', attrs={'name': re.compile(r'^twitter:')}):
                twitter_tags[meta['name']] = meta.get('content', '')
            
            # 소셜 미디어 링크 찾기
            social_links = []
            social_domains = ['facebook.com', 'twitter.com', 'instagram.com', 'linkedin.com', 
                            'youtube.com', 'tiktok.com', 'pinterest.com']
            
            for link in soup.find_all('a', href=True):
                href = link['href']
                for domain in social_domains:
                    if domain in href:
                        social_links.append({'platform': domain, 'url': href})
            
            return {
                'open_graph': og_tags,
                'twitter_cards': twitter_tags,
                'social_links': social_links,
                'social_share_buttons': len(soup.find_all('a', href=re.compile(r'(facebook|twitter|linkedin)\.com/share')))
            }
        except Exception as e:
            return {'error': str(e)}
    
    def analyze_mobile_compatibility(self, url):
        """모바일 호환성 분석"""
        try:
            response = self.session.get(url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 뷰포트 메타 태그 확인
            viewport = soup.find('meta', attrs={'name': 'viewport'})
            viewport_content = viewport.get('content', '') if viewport else ''
            
            # 반응형 디자인 요소 확인
            media_queries = len(re.findall(r'@media', response.text))
            
            return {
                'viewport_meta': bool(viewport),
                'viewport_content': viewport_content,
                'media_queries_count': media_queries,
                'responsive_images': len(soup.find_all('img', srcset=True)),
                'mobile_friendly_score': self._calculate_mobile_score(viewport_content, media_queries)
            }
        except Exception as e:
            return {'error': str(e)}
    
    def generate_report(self, analysis_results, save_path=None):
        """분석 결과 리포트 생성"""
        report = f"""
# URL 분석 리포트
분석 URL: {analysis_results['url']}
분석 시간: {analysis_results['timestamp']}

## 📊 기본 정보
- 상태 코드: {analysis_results['basic_info'].get('status_code', 'N/A')}
- 응답 시간: {analysis_results['basic_info'].get('response_time', 'N/A')}초
- 콘텐츠 크기: {analysis_results['basic_info'].get('content_length', 'N/A')} bytes
- 페이지 제목: {analysis_results['basic_info'].get('title', 'N/A')}

## 🔍 SEO 분석
- 내부 링크: {analysis_results['seo_analysis'].get('links', {}).get('internal_count', 0)}개
- 외부 링크: {analysis_results['seo_analysis'].get('links', {}).get('external_count', 0)}개
- 총 이미지: {analysis_results['seo_analysis'].get('images', {}).get('total_images', 0)}개
- ALT 태그 없는 이미지: {analysis_results['seo_analysis'].get('images', {}).get('images_without_alt', 0)}개

## ⚡ 성능 분석
- 평균 응답 시간: {analysis_results['performance'].get('avg_response_time', 0):.2f}초
- DNS 조회 시간: {analysis_results['performance'].get('dns_lookup_time', 0):.2f}초
- 성능 점수: {analysis_results['performance'].get('performance_score', 0):.1f}/100

## 📝 콘텐츠 분석
- 단어 수: {analysis_results['content_analysis'].get('word_count', 0)}개
- 문단 수: {analysis_results['content_analysis'].get('paragraph_count', 0)}개
- 가독성 점수: {analysis_results['content_analysis'].get('reading_ease', 0):.1f}

## 🔒 보안 분석
- HTTPS 사용: {'✅' if analysis_results['security_analysis'].get('https') else '❌'}
- 보안 헤더 설정: {len([h for h in analysis_results['security_analysis'].get('security_headers', {}).values() if h])}개

## 📱 모바일 호환성
- 뷰포트 메타 태그: {'✅' if analysis_results['mobile_analysis'].get('viewport_meta') else '❌'}
- 모바일 친화성 점수: {analysis_results['mobile_analysis'].get('mobile_friendly_score', 0):.1f}/100
        """
        
        if save_path:
            with open(save_path, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"📄 리포트가 저장되었습니다: {save_path}")
        
        return report
    
    def create_dashboard_data(self, analysis_results):
        """대시보드용 데이터 생성"""
        dashboard_data = {
            'stats': {
                'total_visitors': analysis_results['performance'].get('performance_score', 0) * 23,  # 예시
                'page_views': analysis_results['content_analysis'].get('word_count', 0),
                'clicks': analysis_results['seo_analysis'].get('links', {}).get('internal_count', 0) * 10,
                'avg_session': analysis_results['performance'].get('avg_response_time', 0) * 100
            },
            'keywords': list(analysis_results['keyword_analysis'].get('top_keywords', {}).items())[:15],
            'performance_data': {
                'response_times': [analysis_results['performance'].get('min_response_time', 0),
                                 analysis_results['performance'].get('avg_response_time', 0),
                                 analysis_results['performance'].get('max_response_time', 0)],
                'scores': {
                    'seo': len(analysis_results['seo_analysis'].get('meta_tags', {})) * 10,
                    'performance': analysis_results['performance'].get('performance_score', 0),
                    'security': 85 if analysis_results['security_analysis'].get('https') else 45,
                    'mobile': analysis_results['mobile_analysis'].get('mobile_friendly_score', 0)
                }
            }
        }
        return dashboard_data
    
    # 헬퍼 메서드들
    def _get_meta_content(self, soup, name):
        meta = soup.find('meta', attrs={'name': name}) or soup.find('meta', attrs={'property': name})
        return meta.get('content', '') if meta else ''
    
    def _extract_charset(self, content_type):
        if 'charset=' in content_type:
            return content_type.split('charset=')[1].split(';')[0]
        return ''
    
    def _check_robots_txt(self, url):
        try:
            robots_url = urljoin(url, '/robots.txt')
            response = self.session.get(robots_url, timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def _check_sitemap(self, url):
        try:
            sitemap_url = urljoin(url, '/sitemap.xml')
            response = self.session.get(sitemap_url, timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def _calculate_performance_score(self, times, content_size):
        avg_time = sum(times) / len(times)
        size_score = max(0, 100 - (content_size / 1024 / 1024) * 10)  # MB당 10점 감점
        time_score = max(0, 100 - avg_time * 20)  # 초당 20점 감점
        return (size_score + time_score) / 2
    
    def _check_responsive_design(self, soup):
        viewport = soup.find('meta', attrs={'name': 'viewport'})
        media_queries = len(soup.find_all('style', string=re.compile(r'@media')))
        return bool(viewport) and media_queries > 0
    
    def _detect_technologies(self, headers, soup):
        technologies = []
        
        # 서버 정보
        server = headers.get('server', '').lower()
        if 'nginx' in server:
            technologies.append('Nginx')
        elif 'apache' in server:
            technologies.append('Apache')
        
        # JavaScript 프레임워크
        scripts = soup.find_all('script', src=True)
        for script in scripts:
            src = script['src'].lower()
            if 'react' in src:
                technologies.append('React')
            elif 'vue' in src:
                technologies.append('Vue.js')
            elif 'angular' in src:
                technologies.append('Angular')
            elif 'jquery' in src:
                technologies.append('jQuery')
        
        return technologies
    
    def _check_mixed_content(self, html_content, is_https):
        if not is_https:
            return False
        return 'http://' in html_content and 'https://' in html_content
    
    def _calculate_mobile_score(self, viewport_content, media_queries):
        score = 0
        if viewport_content:
            score += 40
            if 'width=device-width' in viewport_content:
                score += 30
        if media_queries > 0:
            score += 30
        return min(score, 100)


# 사용 예시 및 테스트 함수
def main():
    analyzer = URLAnalyzer()
    
    # 분석할 URL
    test_url = "https://example.com"
    
    print("🚀 URL 분석을 시작합니다...")
    results = analyzer.analyze_url(test_url)
    
    # 리포트 생성
    report = analyzer.generate_report(results, 'url_analysis_report.txt')
    print(report)
    
    # 대시보드 데이터 생성
    dashboard_data = analyzer.create_dashboard_data(results)
    print("\n📊 대시보드 데이터:")
    print(json.dumps(dashboard_data, indent=2, ensure_ascii=False))
    
    # 결과를 JSON으로 저장
    with open('analysis_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False, default=str)
    
    print("\n✅ 분석 완료! 결과가 저장되었습니다.")

if __name__ == "__main__":
    main()
