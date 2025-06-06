"""
Flask HTML URL Analyzer - 깔끔한 HTML 인터페이스
기존 main.py의 URLAnalyzer를 Flask로 서빙
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import json
from datetime import datetime
import threading
import time

# main.py에서 URLAnalyzer import
from main import URLAnalyzer

app = Flask(__name__)
CORS(app)

# 전역 analyzer 인스턴스
analyzer = URLAnalyzer()

@app.route('/')
def index():
    """메인 페이지"""
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze_url():
    """URL 분석 API"""
    try:
        data = request.get_json()
        url = data.get('url', '').strip()
        analysis_type = data.get('analysis_type', '전체 분석')
        
        if not url or not url.startswith(('http://', 'https://')):
            return jsonify({
                'success': False,
                'error': '올바른 URL을 입력해주세요 (http:// 또는 https://로 시작)'
            })
        
        # 분석 실행
        if analysis_type == '빠른 분석':
            # 기본 정보와 성능만 분석
            basic_info = analyzer.get_basic_info(url)
            performance = analyzer.measure_performance(url)
            
            results = {
                'url': url,
                'basic_info': basic_info,
                'performance': performance,
                'timestamp': datetime.now().isoformat()
            }
        else:
            # 전체 분석
            results = analyzer.analyze_url(url)
        
        # 대시보드용 데이터 생성
        dashboard_data = analyzer.create_dashboard_data(results)
        
        return jsonify({
            'success': True,
            'results': results,
            'dashboard_data': dashboard_data,
            'summary': generate_summary_data(results)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'분석 중 오류 발생: {str(e)}'
        })

@app.route('/api/quick-test/<path:test_url>')
def quick_test(test_url):
    """빠른 테스트 API"""
    try:
        if not test_url.startswith(('http://', 'https://')):
            test_url = 'https://' + test_url
            
        basic_info = analyzer.get_basic_info(test_url)
        
        return jsonify({
            'success': True,
            'url': test_url,
            'status_code': basic_info.get('status_code'),
            'response_time': basic_info.get('response_time'),
            'title': basic_info.get('title', '')
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

def generate_summary_data(results):
    """요약 데이터 생성"""
    basic = results.get('basic_info', {})
    performance = results.get('performance', {})
    seo = results.get('seo_analysis', {})
    content = results.get('content_analysis', {})
    security = results.get('security_analysis', {})
    mobile = results.get('mobile_analysis', {})
    
    return {
        'url': results.get('url', ''),
        'status_code': basic.get('status_code', 'N/A'),
        'title': basic.get('title', 'N/A'),
        'response_time': round(basic.get('response_time', 0), 2),
        'content_size': basic.get('content_length', 0),
        'server': basic.get('server', 'N/A'),
        'performance_score': round(performance.get('performance_score', 0), 1),
        'avg_response_time': round(performance.get('avg_response_time', 0), 2),
        'internal_links': seo.get('links', {}).get('internal_count', 0),
        'external_links': seo.get('links', {}).get('external_count', 0),
        'total_images': seo.get('images', {}).get('total_images', 0),
        'images_without_alt': seo.get('images', {}).get('images_without_alt', 0),
        'word_count': content.get('word_count', 0),
        'paragraph_count': content.get('paragraph_count', 0),
        'reading_ease': round(content.get('reading_ease', 0), 1),
        'https_enabled': security.get('https', False),
        'security_headers': len([h for h in security.get('security_headers', {}).values() if h]),
        'mobile_friendly': mobile.get('mobile_friendly_score', 0) if mobile else 0,
        'viewport_meta': mobile.get('viewport_meta', False) if mobile else False
    }

if __name__ == '__main__':
    print("🚀 Flask URL Analyzer 시작...")
    print("📱 http://localhost:5000 에서 확인하세요!")
    app.run(debug=True, host='0.0.0.0', port=5000)