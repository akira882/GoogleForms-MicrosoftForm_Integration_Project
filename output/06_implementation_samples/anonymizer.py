#!/usr/bin/env python3
"""
個人情報匿名化スクリプト（改正個人情報保護法準拠）

Claude APIに送信する前に個人情報を匿名化します。
"""

import hashlib
from typing import Dict, Any

class DataAnonymizer:
    """個人情報匿名化クラス"""
    
    @staticmethod
    def anonymize_email(email: str) -> str:
        """メールアドレスをSHA-256ハッシュ化（不可逆）"""
        return hashlib.sha256(email.encode('utf-8')).hexdigest()[:16]
    
    @staticmethod
    def anonymize_name(name: str) -> str:
        """氏名をMD5ハッシュ化して仮名化"""
        hash_value = hashlib.md5(name.encode('utf-8')).hexdigest()[:8]
        return f"Person_{hash_value}"
    
    @staticmethod
    def anonymize_phone(phone: str) -> str:
        """電話番号のマスキング（先頭3桁と末尾4桁のみ保持）"""
        digits = ''.join(filter(str.isdigit, phone))
        if len(digits) >= 7:
            return f"{digits[:3]}-****-{digits[-4:]}"
        return "***-****-****"
    
    def anonymize_pii(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """全個人情報を一括匿名化"""
        anonymized = data.copy()
        
        if 'email' in anonymized:
            anonymized['email_hash'] = self.anonymize_email(anonymized['email'])
            del anonymized['email']
        
        if 'name' in anonymized:
            anonymized['name_id'] = self.anonymize_name(anonymized['name'])
            del anonymized['name']
        
        if 'phone' in anonymized:
            anonymized['phone_masked'] = self.anonymize_phone(anonymized['phone'])
            del anonymized['phone']
        
        return anonymized
