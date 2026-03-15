#!/usr/bin/env python3
"""
西北农林科技大学课表导入飞书待办技能
支持校历作息时间（夏令时/冬令时自动切换）、课程表解析、飞书任务创建

Author: 薛麟麒
Version: 1.0.0
"""

import os
import sys
import json
import uuid
import argparse
import re
from datetime import datetime, timezone, timedelta
from pathlib import Path

try:
    import requests
    import xlrd
except ImportError:
    print("❌ 缺少依赖，请安装：pip install -r requirements.txt")
    sys.exit(1)


# ============================================================================
# 作息时间配置
# ============================================================================

class NWSUAFSchedule:
    """西北农林科技大学作息时间管理"""
    
    # 夏令时：5 月 1 日 - 9 月 30 日
    SUMMER_TIME = {
        '1-2': ('08:00', '09:40'),
        '3-4': ('10:10', '11:50'),
        '5-6': ('14:30', '16:10'),
        '7-8': ('16:30', '18:10'),
        '5-8': ('14:30', '18:10'),  # 实验课
        '1-8': ('08:00', '18:10'),   # 全天实验
        '9-10': ('19:00', '20:35'),
        '11-12': ('20:45', '22:20'),
    }
    
    # 冬令时：10 月 1 日 - 4 月 30 日
    WINTER_TIME = {
        '1-2': ('08:00', '09:40'),
        '3-4': ('10:10', '11:50'),
        '5-6': ('14:00', '15:40'),
        '7-8': ('16:00', '17:40'),
        '5-8': ('14:00', '17:40'),
        '1-8': ('08:00', '17:40'),
        '9-10': ('19:00', '20:35'),
        '11-12': ('20:45', '22:20'),
    }
    
    @classmethod
    def is_summer_time(cls, date: datetime) -> bool:
        """判断日期是否在夏令时期间"""
        month = date.month
        day = date.day
        
        # 5 月 1 日 - 9 月 30 日
        if 5 <= month <= 9:
            return True
        # 4 月 30 日及之前
        if month == 4 and day <= 30:
            return False
        # 10 月 1 日及之后
        if month == 10 and day >= 1:
            return False
        return False
    
    @classmethod
    def get_times(cls, date: datetime) -> dict:
        """获取指定日期的作息时间表"""
        if cls.is_summer_time(date):
            return cls.SUMMER_TIME
        return cls.WINTER_TIME
    
    @classmethod
    def parse_time_slot(cls, time_slot_str: str, date: datetime) -> tuple:
        """解析节次字符串，返回开始和结束时间"""
        times = cls.get_times(date)
        
        # 匹配"第 X-Y 节"格式
        match = re.search(r'第 (\d+)-(\d+) 节', time_slot_str)
        if match:
            key = f"{match.group(1)}-{match.group(2)}"
            return times.get(key, (None, None))
        return None, None


# ============================================================================
# 飞书 API 客户端
# ============================================================================

class FeishuTaskClient:
    """飞书任务 API 客户端"""
    
    def __init__(self, app_id: str, app_secret: str, user_open_id: str):
        self.app_id = app_id
        self.app_secret = app_secret
        self.user_open_id = user_open_id
        self.base_url = "https://open.feishu.cn/open-apis"
        self._tenant_token = None
    
    def get_tenant_access_token(self) -> str:
        """获取 tenant_access_token"""
        if self._tenant_token:
            return self._tenant_token
        
        url = f"{self.base_url}/auth/v3/tenant_access_token/internal"
        payload = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }
        resp = requests.post(url, json=payload, timeout=30)
        result = resp.json()
        
        if result.get("code") != 0:
            raise RuntimeError(f"获取 token 失败：{result}")
        
        self._tenant_token = result["tenant_access_token"]
        return self._tenant_token
    
    def _headers(self) -> dict:
        """获取请求头"""
        token = self.get_tenant_access_token()
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
    
    def create_tasklist(self, name: str) -> str:
        """创建任务分组，返回 GUID"""
        url = f"{self.base_url}/task/v2/tasklists?user_id_type=open_id"
        payload = {"name": name}
        resp = requests.post(url, headers=self._headers(), json=payload, timeout=30)
        result = resp.json()
        
        if result.get("code") != 0:
            raise RuntimeError(f"创建分组失败：{result}")
        
        return result["data"]["tasklist"]["guid"]
    
    def get_tasklists(self) -> list:
        """获取所有任务分组"""
        url = f"{self.base_url}/task/v2/tasklists?user_id_type=open_id"
        resp = requests.get(url, headers=self._headers(), timeout=30)
        result = resp.json()
        
        if result.get("code") != 0:
            raise RuntimeError(f"获取分组失败：{result}")
        
        return result.get("data", {}).get("items", [])
    
    def create_task(self, summary: str, description: str, 
                    start_time: datetime, end_time: datetime,
                    tasklist_guid: str = None) -> dict:
        """创建任务"""
        url = f"{self.base_url}/task/v2/tasks?user_id_type=open_id"
        
        # 北京时间戳
        cn_tz = timezone(timedelta(hours=8))
        start_cn = start_time.replace(tzinfo=cn_tz)
        end_cn = end_time.replace(tzinfo=cn_tz)
        
        payload = {
            "summary": summary,
            "description": description,
            "start": {
                "timestamp": str(int(start_cn.timestamp() * 1000)),
                "is_all_day": False
            },
            "due": {
                "timestamp": str(int(end_cn.timestamp() * 1000)),
                "is_all_day": False
            },
            "members": [{
                "id": self.user_open_id,
                "type": "user"
            }],
            "client_token": str(uuid.uuid4()),
        }
        
        if tasklist_guid:
            payload["tasklist_guid"] = tasklist_guid
        
        resp = requests.post(url, headers=self._headers(), json=payload, timeout=30)
        result = resp.json()
        
        if result.get("code") != 0:
            raise RuntimeError(f"创建任务失败：{result}")
        
        return result["data"]["task"]
    
    def delete_task(self, task_guid: str) -> bool:
        """删除任务"""
        url = f"{self.base_url}/task/v2/tasks/{task_guid}?user_id_type=open_id"
        resp = requests.delete(url, headers=self._headers(), timeout=30)
        result = resp.json()
        return result.get("code") == 0
    
    def get_tasks(self) -> list:
        """获取所有任务"""
        url = f"{self.base_url}/task/v2/tasks?user_id_type=open_id"
        resp = requests.get(url, headers=self._headers(), timeout=30)
        result = resp.json()
        
        if result.get("code") != 0:
            raise RuntimeError(f"获取任务失败：{result}")
        
        return result.get("data", {}).get("items", [])


# ============================================================================
# 课表解析
# ============================================================================

class CalendarParser:
    """课表 Excel 解析器"""
    
    @staticmethod
    def parse_excel(excel_path: str) -> list:
        """解析课表 Excel 文件"""
        workbook = xlrd.open_workbook(excel_path)
        sheet = workbook.sheet_by_index(0)
        
        events = []
        for row_idx in range(1, sheet.nrows):
            row = sheet.row_values(row_idx)
            if len(row) < 5:
                continue
            
            event = {
                'title': str(row[0]).strip() if row[0] else '',
                'start_time': str(row[1]).strip() if row[1] else '',
                'location': str(row[2]).strip() if row[2] else '',
                'description': str(row[3]).strip() if row[3] else '',
            }
            events.append(event)
        
        return events
    
    @staticmethod
    def filter_by_class(events: list, target_class: str) -> list:
        """过滤指定班级的课程"""
        filtered = []
        for event in events:
            desc = event.get('description', '')
            if '班级：' in desc:
                classes_str = desc.split('班级：')[1].split('\n')[0]
                classes = [c.strip() for c in classes_str.split(',')]
                if target_class in classes:
                    filtered.append(event)
        return filtered


# ============================================================================
# 主程序
# ============================================================================

def load_env():
    """加载环境变量"""
    env_file = Path(__file__).parent / '.env'
    if env_file.exists():
        with open(env_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ.setdefault(key.strip(), value.strip())


def main():
    parser = argparse.ArgumentParser(
        description='西北农林科技大学课表导入飞书待办',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python nwafu_task_feishu.py --excel 课表.xls --class "生技 2402"
  python nwafu_task_feishu.py --excel 课表.xls --class "生技 2402" --delete-all
        """
    )
    
    parser.add_argument('--excel', required=True, help='课表 Excel 文件路径')
    parser.add_argument('--class', dest='target_class', required=True, help='班级名称')
    parser.add_argument('--start-date', default='2026-03-02', help='开学日期')
    parser.add_argument('--action', choices=['create', 'delete', 'sync'], default='create',
                       help='操作类型')
    parser.add_argument('--delete-all', action='store_true', help='删除所有任务')
    parser.add_argument('--app-id', help='飞书 App ID')
    parser.add_argument('--app-secret', help='飞书 App Secret')
    parser.add_argument('--user-id', help='用户 Open ID')
    parser.add_argument('--debug', action='store_true', help='调试模式')
    
    args = parser.parse_args()
    
    # 加载环境变量
    load_env()
    
    # 获取配置
    app_id = args.app_id or os.getenv('FEISHU_APP_ID')
    app_secret = args.app_secret or os.getenv('FEISHU_APP_SECRET')
    user_id = args.user_id or os.getenv('FEISHU_USER_OPEN_ID')
    
    if not all([app_id, app_secret, user_id]):
        print("❌ 缺少飞书配置，请设置环境变量或命令行参数")
        print("   FEISHU_APP_ID, FEISHU_APP_SECRET, FEISHU_USER_OPEN_ID")
        sys.exit(1)
    
    # 初始化客户端
    client = FeishuTaskClient(app_id, app_secret, user_id)
    
    # 删除所有任务
    if args.delete_all:
        print("🗑️  删除所有任务...")
        tasks = client.get_tasks()
        deleted = 0
        for task in tasks:
            guid = task.get('guid')
            if guid:
                try:
                    if client.delete_task(guid):
                        deleted += 1
                except:
                    pass
        print(f"✅ 删除完成：{deleted} 个")
        return
    
    # 解析课表
    print(f"📚 解析课表：{args.excel}")
    events = CalendarParser.parse_excel(args.excel)
    print(f"   总事件数：{len(events)}")
    
    my_events = CalendarParser.filter_by_class(events, args.target_class)
    print(f"   {args.target_class} 班事件：{len(my_events)}")
    
    if not my_events:
        print("❌ 未找到课程事件")
        return
    
    # 创建分组
    print("\n📁 创建任务分组...")
    course_guid = client.create_tasklist("课程")
    lab_guid = client.create_tasklist("实验")
    print(f"   课程分组：{course_guid}")
    print(f"   实验分组：{lab_guid}")
    
    # 创建任务
    print(f"\n📝 创建任务（{args.target_class}）...\n")
    
    created = 0
    for event in my_events:
        try:
            date_str = event['start_time'].split(' ')[0]
            date = datetime.strptime(date_str, '%Y-%m-%d')
            desc = event.get('description', '')
            
            # 解析节次
            time_slot = desc.split('节次：')[1].split('\n')[0] if '节次：' in desc else ''
            start_time_str, end_time_str = NWSUAFSchedule.parse_time_slot(time_slot, date)
            
            if not start_time_str:
                if args.debug:
                    print(f"  ⚠️  跳过：{event['title']} (无法解析节次)")
                continue
            
            start = datetime.strptime(f"{date_str} {start_time_str}", '%Y-%m-%d %H:%M')
            end = datetime.strptime(f"{date_str} {end_time_str}", '%Y-%m-%d %H:%M')
            
            course = event['title'].split(' (')[0]
            location = event.get('location', '待定')
            week = desc.split('周次：')[1].split('\n')[0] if '周次：' in desc else ''
            
            summary = f"📚 {course}"
            description = f"""📅 日期：{start.strftime('%Y-%m-%d')}
⏰ 时间：{start.strftime('%H:%M')}-{end.strftime('%H:%M')}
📍 地点：{location}
📚 周次：{week}"""
            
            task = client.create_task(
                summary=summary,
                description=description,
                start_time=start,
                end_time=end,
                tasklist_guid=course_guid
            )
            
            created += 1
            if created % 20 == 0:
                print(f"  ✅ 已创建 {created} 个任务")
                
        except Exception as e:
            if args.debug:
                print(f"  ❌ {event.get('title', '未知')}: {e}")
    
    print(f"\n📊 创建完成：{created} 个任务")
    print(f"✅ 完成！")


if __name__ == '__main__':
    main()
