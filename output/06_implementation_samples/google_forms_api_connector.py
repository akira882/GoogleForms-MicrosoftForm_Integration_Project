#!/usr/bin/env python3
"""
Google Forms APIデータ取得スクリプト

このスクリプトはGoogle Forms APIを使用してフォームの回答を取得します。
Make.comのHTTPモジュールから呼び出すことを想定しています。

Requirements:
    pip install google-api-python-client google-auth google-auth-oauthlib

Usage:
    python google_forms_api_connector.py --form-id 1A2B3C4D5E6F --credentials /path/to/credentials.json
"""

import argparse
import json
from typing import List, Dict, Any
from googleapiclient.discovery import build
from google.oauth2 import service_account

class GoogleFormsConnector:
    """Google Forms API接続クラス"""
    
    # Google Forms API のスコープ
    SCOPES = [
        'https://www.googleapis.com/auth/forms.responses.readonly',
        'https://www.googleapis.com/auth/forms.body.readonly'
    ]
    
    def __init__(self, credentials_path: str):
        """
        初期化
        
        Args:
            credentials_path: サービスアカウントJSONファイルのパス
        """
        self.credentials = service_account.Credentials.from_service_account_file(
            credentials_path, 
            scopes=self.SCOPES
        )
        self.service = build('forms', 'v1', credentials=self.credentials)
    
    def get_form_metadata(self, form_id: str) -> Dict[str, Any]:
        """
        フォームのメタデータを取得
        
        Args:
            form_id: Google FormsのフォームID
            
        Returns:
            フォームのメタデータ
        """
        form = self.service.forms().get(formId=form_id).execute()
        
        return {
            'form_id': form_id,
            'form_title': form.get('info', {}).get('title', ''),
            'description': form.get('info', {}).get('description', ''),
            'questions': [
                {
                    'question_id': item.get('questionItem', {}).get('question', {}).get('questionId', ''),
                    'question_text': item.get('title', ''),
                    'question_type': self._get_question_type(item)
                }
                for item in form.get('items', [])
                if 'questionItem' in item
            ]
        }
    
    def get_responses(self, form_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        """
        フォームの回答を取得
        
        Args:
            form_id: Google FormsのフォームID
            limit: 取得する回答数の上限
            
        Returns:
            回答データのリスト
        """
        responses = self.service.forms().responses().list(formId=form_id).execute()
        
        form_metadata = self.get_form_metadata(form_id)
        
        result = []
        for response in responses.get('responses', [])[:limit]:
            result.append(self._format_response(response, form_metadata))
        
        return result
    
    def _get_question_type(self, item: Dict[str, Any]) -> str:
        """質問タイプを判定"""
        question_item = item.get('questionItem', {}).get('question', {})
        
        if 'textQuestion' in question_item:
            return 'text'
        elif 'choiceQuestion' in question_item:
            choice_type = question_item['choiceQuestion'].get('type', '')
            if choice_type == 'CHECKBOX':
                return 'checkbox'
            else:
                return 'multiple_choice'
        elif 'dateQuestion' in question_item:
            return 'date'
        elif 'fileUploadQuestion' in question_item:
            return 'file_upload'
        else:
            return 'unknown'
    
    def _format_response(self, response: Dict[str, Any], form_metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        統一スキーマv1.1に変換
        
        Args:
            response: Google Forms APIの生データ
            form_metadata: フォームのメタデータ
            
        Returns:
            統一スキーマ形式の回答データ
        """
        response_id = response.get('responseId', '')
        submitted_at = response.get('lastSubmittedTime', '')
        respondent_email = response.get('respondentEmail', '')
        
        # 質問と回答のマッピング
        answers = response.get('answers', {})
        responses_list = []
        
        for question in form_metadata['questions']:
            question_id = question['question_id']
            if question_id in answers:
                answer_data = answers[question_id]
                
                # 回答を抽出
                answer_value = self._extract_answer_value(answer_data)
                
                responses_list.append({
                    'question_id': question_id,
                    'question_text': question['question_text'],
                    'answer': answer_value,
                    'question_type': question['question_type']
                })
        
        # 統一スキーマv1.1形式
        return {
            'response_id': response_id,
            'form_source': 'google_forms',
            'form_id': form_metadata['form_id'],
            'form_title': form_metadata['form_title'],
            'submitted_at': submitted_at,
            'respondent_email': respondent_email,
            'responses': responses_list,
            'metadata': {
                'company': 'GMO Tech',  # Make.comで動的に設定
                'department': '',
                'integration_timestamp': '',  # Make.comで設定
                'data_version': 'v1.1'
            }
        }
    
    def _extract_answer_value(self, answer_data: Dict[str, Any]) -> Any:
        """回答値を抽出"""
        if 'textAnswers' in answer_data:
            answers = answer_data['textAnswers'].get('answers', [])
            if len(answers) == 1:
                return answers[0].get('value', '')
            else:
                return [a.get('value', '') for a in answers]
        
        elif 'fileUploadAnswers' in answer_data:
            files = answer_data['fileUploadAnswers'].get('answers', [])
            return [f.get('fileId', '') for f in files]
        
        else:
            return ''


def main():
    """メイン処理"""
    parser = argparse.ArgumentParser(description='Google Forms API接続スクリプト')
    parser.add_argument('--form-id', required=True, help='Google FormsのフォームID')
    parser.add_argument('--credentials', required=True, help='サービスアカウントJSONファイルのパス')
    parser.add_argument('--limit', type=int, default=100, help='取得する回答数の上限')
    
    args = parser.parse_args()
    
    connector = GoogleFormsConnector(args.credentials)
    
    print(f"フォームID: {args.form_id} から回答を取得中...")
    responses = connector.get_responses(args.form_id, limit=args.limit)
    
    print(json.dumps(responses, ensure_ascii=False, indent=2))
    print(f"\n取得件数: {len(responses)}件")


if __name__ == '__main__':
    main()
