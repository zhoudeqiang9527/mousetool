import tkinter as tk
from tkinter import ttk, messagebox
import pyautogui
import time

class MouseKeyboardTool:
    def __init__(self, root):
        self.root = root
        self.root.title("键鼠操作工具")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        
        # 设置pyautogui安全模式
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.1
        
        self.setup_ui()
    
    def setup_ui(self):
        # 主框架
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 坐标X
        ttk.Label(main_frame, text="坐标X:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.x_var = tk.StringVar(value="100")
        self.x_entry = ttk.Entry(main_frame, textvariable=self.x_var, width=15)
        self.x_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        
        # 坐标Y
        ttk.Label(main_frame, text="坐标Y:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.y_var = tk.StringVar(value="100")
        self.y_entry = ttk.Entry(main_frame, textvariable=self.y_var, width=15)
        self.y_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        
        # 点击数
        ttk.Label(main_frame, text="点击数:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.click_count_var = tk.StringVar(value="1")
        self.click_count_entry = ttk.Entry(main_frame, textvariable=self.click_count_var, width=15)
        self.click_count_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        
        # 执行按钮
        self.execute_btn = ttk.Button(main_frame, text="执行鼠标点击", command=self.execute_mouse_clicks)
        self.execute_btn.grid(row=3, column=0, columnspan=2, pady=20, sticky=(tk.W, tk.E))
        
        # 状态标签
        self.status_label = ttk.Label(main_frame, text="就绪", foreground="green")
        self.status_label.grid(row=4, column=0, columnspan=2, pady=10)
        
        # 进度条
        self.progress = ttk.Progressbar(main_frame, mode='determinate')
        self.progress.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # 配置列权重
        main_frame.columnconfigure(1, weight=1)
    
    def validate_inputs(self):
        """验证输入参数"""
        try:
            x = int(self.x_var.get())
            y = int(self.y_var.get())
            click_count = int(self.click_count_var.get())
            
            if x < 0 or y < 0:
                raise ValueError("坐标不能为负数")
            if click_count <= 0:
                raise ValueError("点击数必须大于0")
                
            # 检查坐标是否在屏幕范围内
            screen_width, screen_height = pyautogui.size()
            if x >= screen_width or y >= screen_height:
                raise ValueError(f"坐标超出屏幕范围 ({screen_width}x{screen_height})")
                
            return x, y, click_count
        except ValueError as e:
            messagebox.showerror("输入错误", str(e))
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
        self.status_label.config(text="执行中...", foreground="orange")
        
        # 设置进度条
        self.progress['maximum'] = click_count
        self.progress['value'] = 0
        
        try:
            current_x, current_y = x, y
            screen_height = pyautogui.size()[1]
            
            for i in range(click_count):
                # 更新进度
                self.progress['value'] = i + 1
                self.root.update()
                
                # 移动到指定坐标
                pyautogui.moveTo(current_x, current_y)
                time.sleep(0.1)
                
                # 执行点击
                pyautogui.click()
                time.sleep(0.1)
                
                # 向下移动5像素
                current_y += 5
                
                # 检查是否到达屏幕底部
                if current_y >= screen_height - 50:  # 留50像素边距
                    # 执行滚轮操作
                    pyautogui.scroll(-3)  # 向下滚动
                    time.sleep(0.2)
                    # 重置Y坐标到起始位置
                    current_y = y
                
                # 再次移动到新坐标
                pyautogui.moveTo(current_x, current_y)
                time.sleep(0.1)
                
                # 再次点击
                pyautogui.click()
                time.sleep(0.1)
                
                # 再次向下移动5像素
                current_y += 5
                
                # 检查是否需要滚轮操作
                if current_y >= screen_height - 50:
                    pyautogui.scroll(-3)
                    time.sleep(0.2)
                    current_y = y
            
            self.status_label.config(text="执行完成", foreground="green")
            messagebox.showinfo("完成", f"已完成 {click_count} 次点击操作")
            
        except pyautogui.FailSafeException:
            self.status_label.config(text="操作被中断", foreground="red")
            messagebox.showwarning("中断", "操作被安全机制中断（鼠标移动到屏幕左上角）")
        except Exception as e:
            self.status_label.config(text="执行出错", foreground="red")
            messagebox.showerror("错误", f"执行过程中出现错误：{str(e)}")
        finally:
            # 重新启用按钮
            self.execute_btn.config(state='normal')
            self.progress['value'] = 0

def main():
    root = tk.Tk()
    app = MouseKeyboardTool(root)
    root.mainloop()

if __name__ == "__main__":
    main()
