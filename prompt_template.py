import json
import os
from typing import Dict, List
from datetime import datetime

class PromptTemplateManager:
    def __init__(self):
        self.templates_dir = "templates"
        self.ensure_template_directory()
        self._templates: Dict[str, Dict] = {}
        self.load_templates()

    def ensure_template_directory(self):
        """テンプレートディレクトリが存在しない場合は作成"""
        if not os.path.exists(self.templates_dir):
            os.makedirs(self.templates_dir)

    def load_templates(self):
        """保存されているテンプレートを読み込む"""
        template_file = os.path.join(self.templates_dir, "templates.json")
        if os.path.exists(template_file):
            try:
                with open(template_file, "r", encoding="utf-8") as f:
                    self._templates = json.load(f)
            except Exception as e:
                print(f"テンプレート読み込みエラー: {str(e)}")
                self._templates = {}

    def save_templates(self):
        """テンプレートをファイルに保存"""
        template_file = os.path.join(self.templates_dir, "templates.json")
        try:
            with open(template_file, "w", encoding="utf-8") as f:
                json.dump(self._templates, f, ensure_ascii=False, indent=2)
        except Exception as e:
            raise Exception(f"テンプレート保存エラー: {str(e)}")

    def add_template(self, name: str, content: str, description: str = "") -> bool:
        """新しいテンプレートを追加"""
        if not name or not content:
            return False

        template_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self._templates[template_id] = {
            "name": name,
            "content": content,
            "description": description,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.save_templates()
        return True

    def get_template(self, template_id: str) -> Dict:
        """指定されたIDのテンプレートを取得"""
        return self._templates.get(template_id, {})

    def list_templates(self) -> List[Dict]:
        """全てのテンプレートをリスト形式で取得"""
        return [
            {"id": k, **v}
            for k, v in self._templates.items()
        ]

    def delete_template(self, template_id: str) -> bool:
        """テンプレートを削除"""
        if template_id in self._templates:
            del self._templates[template_id]
            self.save_templates()
            return True
        return False

    def update_template(
        self,
        template_id: str,
        name: str | None = None,
        content: str | None = None,
        description: str | None = None
    ) -> bool:
        """テンプレートを更新"""
        if template_id not in self._templates:
            return False

        template = self._templates[template_id]
        if name is not None:
            template["name"] = name
        if content is not None:
            template["content"] = content
        if description is not None:
            template["description"] = description

        self.save_templates()
        return True