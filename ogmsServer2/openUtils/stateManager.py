"""
Author: DiChen
Date: 2024-09-06 17:21:20
LastEditors: DiChen
LastEditTime: 2024-09-06 20:05:03
"""

# 定义状态常量
STATE_INIT = 0b1  # 1: 初始化状态
STATE_RUNNING = 0b10  # 2: 运行中状态
STATE_COMPLETED = 0b100  # 4: 已完成状态
STATE_ERROR = 0b1000  # 8: 错误状态


class StateManager:
    def __init__(self):
        # 初始化状态，默认处于 INIT 状态
        self.current_state = STATE_INIT

    def set_state(self, state):
        """设置状态"""
        self.current_state |= state

    def clear_state(self, state):
        """清除状态"""
        self.current_state &= ~state

    def is_state_set(self, state):
        """检查状态是否已设置"""
        return self.current_state & state != 0

    def transition_to(self, state):
        """状态转换逻辑，确保状态转换符合预期"""
        if state == STATE_RUNNING and not self.is_state_set(STATE_INIT):
            print("Cannot run without initialization")
            return

        if state == STATE_COMPLETED and not self.is_state_set(STATE_RUNNING):
            print("Cannot complete without running")
            return

        if state == STATE_ERROR:
            print("Error occurred, transitioning to ERROR state")
            self.current_state = state
            return

        self.current_state = state
        print(f"Transitioned to state: {bin(self.current_state)}")

    def get_current_state(self):
        """获取当前状态"""
        return bin(self.current_state)
