#!/usr/bin/env python3
"""
統一スキーマ変換スクリプト

Google FormsとMicrosoft Formsのデータを統一スキーマv1.1に変換します。
"""

import json
import uuid
from datetime import datetime
from typing import Dict, Any

class SchemaDataNormalizer:
    """統一スキーマ変換クラス"""
    
    @staticmethod
    def normalize_google_forms(data: Dict[str, Any]) -> Dict[str, Any]:
        """Google Formsデータを統一スキーマに変換"""
        return {
            'response_id': data.get('response_id', str(uuid.uuid4())),
            'form_source': 'google_forms',
            'form_id': data.get('form_id', ''),
            'form_title': data.get('form_title', ''),
            'submitted_at': data.get('submitted_at', datetime.utcnow().isoformat()),
            'respondent_email': data.get('respondent_email', ''),
            'responses': data.get('responses', []),
            'metadata': {
                'company': data.get('metadata', {}).get('company', 'GMO TECH'),
                'department': data.get('metadata', {}).get('department', ''),
                'integration_timestamp': datetime.utcnow().isoformat(),
                'data_version': 'v1.1'
            }
        }
    
    @staticmethod
    def normalize_ms_forms(data: Dict[str, Any]) -> Dict[str, Any]:
        """Microsoft Formsデータを統一スキーマに変換"""
        return {
            'response_id': str(uuid.uuid4()),
            'form_source': 'ms_forms',
            'form_id': data.get('id', ''),
            'form_title': data.get('title', ''),
            'submitted_at': data.get('submitDate', datetime.utcnow().isoformat()),
            'respondent_email': data.get('responder', ''),
            'responses': [
                {
                    'question_id': q.get('questionId', ''),
                    'question_text': q.get('questionText', ''),
                    'answer': q.get('answer', ''),
                    'question_type': 'text'  # MS Formsは型判定が困難
                }
                for q in data.get('questions', [])
            ],
            'metadata': {
                'company': 'GMO TECH',
                'department': '',
                'integration_timestamp': datetime.utcnow().isoformat(),
                'data_version': 'v1.1'
            }
        }

if __name__ == "__main__":
    # 使用例
    normalizer = SchemaDataNormalizer()
    sample_data = {
        "response_id": "google-123",
        "form_id": "form-abc",
        "form_title": "採用アンケート",
        "submitted_at": "2026-02-12T10:30:00Z",
        "respondent_email": "test@gmo-tech.test",
        "responses": [
            {
                "question_id": "q1",
                "question_text": "志望動機",
                "answer": "AI活用に惹かれました",
                "question_type": "text"
            }
        ],
        "metadata": {"company": "Client"}
    }
    print(json.dumps(normalizer.normalize_google_forms(sample_data), indent=2, ensure_ascii=False))
