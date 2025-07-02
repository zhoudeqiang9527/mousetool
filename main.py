import tkinter as tk
from tkinter import ttk, messagebox
import pyautogui
import time
import json
import os

class MouseKeyboardTool:
    def __init__(self, root):
        self.root = root
        
        # 加载配置文件
        self.config = self.load_config()
        
        # 设置窗口属性
        self.root.title(self.config['ui']['window_title'])
        self.root.geometry(f"{self.config['ui']['window_width']}x{self.config['ui']['window_height']}")
        self.root.resizable(self.config['ui']['window_resizable'], self.config['ui']['window_resizable'])
        
        # 设置pyautogui安全模式
        pyautogui.FAILSAFE = self.config['pyautogui']['failsafe']
        pyautogui.PAUSE = self.config['pyautogui']['pause']
        
        self.setup_ui()
        
        # 启动鼠标位置跟踪
        self.start_mouse_tracking()
    
    def load_config(self):
        """加载配置文件"""
        config_path = os.path.join(os.path.dirname(__file__), 'config.json')
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            # 如果配置文件不存在，返回默认配置
            return self.get_default_config()
        except json.JSONDecodeError:
            # 如果配置文件格式错误，返回默认配置
            return self.get_default_config()
    
    def get_default_config(self):
        """获取默认配置"""
        return {
            'ui': {'window_title': '键鼠操作工具', 'window_width': 550, 'window_height': 300, 'window_resizable': False, 'padding': '20'},
            'mouse': {'default_x': 100, 'default_y': 100, 'default_click_count': 1, 'move_step': 5, 'scroll_threshold_y': 930,  'click_delay': 0.1, 'scroll_delay': 0.2},
            'pyautogui': {'failsafe': True, 'pause': 0.1},
            'tracking': {'update_interval_ms': 100},
            'ui_text': {'coordinate_x_label': '坐标X:', 'coordinate_y_label': '坐标Y:', 'click_count_label': '点击数:', 'execute_button_text': '执行鼠标点击', 'current_x_prefix': '当前X: ', 'current_y_prefix': '当前Y: ', 'status_ready': '就绪', 'status_executing': '执行中...', 'status_completed': '执行完成', 'status_interrupted': '操作被中断', 'status_error': '执行出错', 'current_position_default': '--'},
            'messages': {'input_error_title': '输入错误', 'completion_title': '完成', 'completion_message': '已完成 {count} 次点击操作', 'interrupt_title': '中断', 'interrupt_message': '操作被安全机制中断（鼠标移动到屏幕左上角）', 'error_title': '错误', 'error_message': '执行过程中出现错误：{error}', 'negative_coordinates_error': '坐标不能为负数', 'invalid_click_count_error': '点击数必须大于0', 'coordinates_out_of_bounds_error': '坐标超出屏幕范围 ({width}x{height})'}
        }
    
    def setup_ui(self):
        # 主框架
        main_frame = ttk.Frame(self.root, padding=self.config['ui']['padding'])
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 坐标X
        ttk.Label(main_frame, text=self.config['ui_text']['coordinate_x_label']).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.x_var = tk.StringVar(value=str(self.config['mouse']['default_x']))
        self.x_entry = ttk.Entry(main_frame, textvariable=self.x_var, width=15)
        self.x_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        
        # 当前X坐标显示
        self.current_x_label = ttk.Label(main_frame, text=f"{self.config['ui_text']['current_x_prefix']}{self.config['ui_text']['current_position_default']}", foreground="blue")
        self.current_x_label.grid(row=0, column=2, sticky=tk.W, padx=(10, 0), pady=5)
        
        # 坐标Y
        ttk.Label(main_frame, text=self.config['ui_text']['coordinate_y_label']).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.y_var = tk.StringVar(value=str(self.config['mouse']['default_y']))
        self.y_entry = ttk.Entry(main_frame, textvariable=self.y_var, width=15)
        self.y_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        
        # 当前Y坐标显示
        self.current_y_label = ttk.Label(main_frame, text=f"{self.config['ui_text']['current_y_prefix']}{self.config['ui_text']['current_position_default']}", foreground="blue")
        self.current_y_label.grid(row=1, column=2, sticky=tk.W, padx=(10, 0), pady=5)
        
        # 点击数
        ttk.Label(main_frame, text=self.config['ui_text']['click_count_label']).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.click_count_var = tk.StringVar(value=str(self.config['mouse']['default_click_count']))
        self.click_count_entry = ttk.Entry(main_frame, textvariable=self.click_count_var, width=15)
        self.click_count_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        
        # 执行按钮
        self.execute_btn = ttk.Button(main_frame, text=self.config['ui_text']['execute_button_text'], command=self.execute_mouse_clicks)
        self.execute_btn.grid(row=3, column=0, columnspan=2, pady=20, sticky=(tk.W, tk.E))
        
        # 状态标签
        self.status_label = ttk.Label(main_frame, text=self.config['ui_text']['status_ready'], foreground="green")
        self.status_label.grid(row=4, column=0, columnspan=2, pady=10)
        
        # 进度条
        self.progress = ttk.Progressbar(main_frame, mode='determinate')
        self.progress.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # 配置列权重
        main_frame.columnconfigure(1, weight=1)
        main_frame.columnconfigure(2, weight=0)
    
    def validate_inputs(self):
        """验证输入参数"""
        try:
            x = int(self.x_var.get())
            y = int(self.y_var.get())
            click_count = int(self.click_count_var.get())
            
            if x < 0 or y < 0:
                raise ValueError(self.config['messages']['negative_coordinates_error'])
            if click_count <= 0:
                raise ValueError(self.config['messages']['invalid_click_count_error'])
                
            # 检查坐标是否在屏幕范围内
            screen_width, screen_height = pyautogui.size()
            if x >= screen_width or y >= screen_height:
                raise ValueError(self.config['messages']['coordinates_out_of_bounds_error'].format(width=screen_width, height=screen_height))
                
            return x, y, click_count
        except ValueError as e:
            messagebox.showerror(self.config['messages']['input_error_title'], str(e))
            return None
    
    def execute_mouse_clicks(self):
        """执行鼠标点击操作"""
        # 验证输入
        result = self.validate_inputs()
        if result is None:
            return
            
        x, y, click_count = result
        
        # 禁用按钮
        self.execute_btn.config(state='disabled')
        self.status_label.config(text=self.config['ui_text']['status_executing'], foreground="orange")
        
        # 设置进度条
        self.progress['maximum'] = click_count
        self.progress['value'] = 0
        
        try:
            current_x, current_y = x, y
            
            for i in range(click_count):
                # 更新进度
                self.progress['value'] = i + 1
                self.root.update()
                
                # 移动到指定坐标
                pyautogui.moveTo(current_x, current_y)
                time.sleep(self.config['mouse']['click_delay'])
                
                # 执行点击
                pyautogui.click()
                time.sleep(self.config['mouse']['click_delay'])
                
                # 向下移动指定像素
                current_y += self.config['mouse']['move_step']
                
                # 检查Y值是否大于阈值
                if current_y > self.config['mouse']['scroll_threshold_y']:
                    # 先点击当前位置确保焦点正确
                    pyautogui.click(current_x, current_y)
                    time.sleep(self.config['mouse']['click_delay'])
                    # 计算滚轮量
                    # 向上滚动的距离 = 距离阈值 - 当前距离，是step的整数倍
                    scroll_amount = current_y * 2 - y - self.config['mouse']['scroll_threshold_y'] + (self.config['mouse']['move_step'] * 3)                    
                    scroll_amount = scroll_amount * -1
                    print(f"scroll_amount00001: {scroll_amount}   y: {y}")                    
                    
                    # 向上滚动
                    # 执行滚轮操作
                    # 执行滚轮操作
                    pyautogui.scroll(scroll_amount)
                    time.sleep(self.config['mouse']['scroll_delay'])
                    # 重置Y坐标到起始位置
                    current_y = y
                
                # 再次移动到新坐标
                pyautogui.moveTo(current_x, current_y)
                time.sleep(self.config['mouse']['click_delay'])
                
                # 再次点击
                pyautogui.click()
                time.sleep(self.config['mouse']['click_delay'])
                
                # 再次向下移动指定像素
                current_y += self.config['mouse']['move_step']
                
                # 检查是否需要滚轮操作
                if current_y > self.config['mouse']['scroll_threshold_y']:
                    # 先点击当前位置确保焦点正确
                    pyautogui.click(current_x, current_y)
                    time.sleep(self.config['mouse']['click_delay'])
                     # 计算滚轮量
                    # 向上滚动的距离 = 距离阈值 - 当前距离
                    scroll_amount = current_y * 2 - y - self.config['mouse']['scroll_threshold_y'] + (self.config['mouse']['move_step'] * 3)
                    
                    scroll_amount = scroll_amount * -1
                    print(f"scroll_amount00002: {scroll_amount}   y: {y}   current_y: {current_y}")
                    pyautogui.scroll(scroll_amount)
                    time.sleep(self.config['mouse']['scroll_delay'])
                    current_y = y
            
            self.status_label.config(text=self.config['ui_text']['status_completed'], foreground="green")
            messagebox.showinfo(self.config['messages']['completion_title'], self.config['messages']['completion_message'].format(count=click_count))
            
        except pyautogui.FailSafeException:
            self.status_label.config(text=self.config['ui_text']['status_interrupted'], foreground="red")
            messagebox.showwarning(self.config['messages']['interrupt_title'], self.config['messages']['interrupt_message'])
        except Exception as e:
            self.status_label.config(text=self.config['ui_text']['status_error'], foreground="red")
            messagebox.showerror(self.config['messages']['error_title'], self.config['messages']['error_message'].format(error=str(e)))
        finally:
            # 重新启用按钮
            self.execute_btn.config(state='normal')
            self.progress['value'] = 0
    
    def start_mouse_tracking(self):
        """启动鼠标位置实时跟踪"""
        self.update_mouse_position()
    
    def update_mouse_position(self):
        """更新鼠标位置显示"""
        try:
            x, y = pyautogui.position()
            self.current_x_label.config(text=f"当前X: {x}")
            self.current_y_label.config(text=f"当前Y: {y}")
        except Exception:
            # 如果获取鼠标位置失败，显示默认值
            self.current_x_label.config(text="当前X: --")
            self.current_y_label.config(text="当前Y: --")
        
        # 根据配置的间隔更新
        self.root.after(self.config['tracking']['update_interval_ms'], self.update_mouse_position)

def main():
    root = tk.Tk()
    app = MouseKeyboardTool(root)
    root.mainloop()

if __name__ == "__main__":
    main()
