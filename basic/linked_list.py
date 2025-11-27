# 链表是一种常见的数据结构，由一系列节点组成，每个节点包含数据和指向下一个节点的引用。
# 与数组不同，链表在内存中不需要连续的空间，插入和删除操作更高效。

# 1. 定义链表节点类
class ListNode:
    """链表节点类，包含数据和指向下一个节点的引用"""
    def __init__(self, data):
        self.data = data  # 节点存储的数据
        self.next = None  # 指向下一个节点的引用，初始为None

# 2. 创建链表节点
node1 = ListNode(10)
node2 = ListNode(20)
node3 = ListNode(30)

# 3. 连接节点形成链表
node1.next = node2  # node1指向node2
node2.next = node3  # node2指向node3

# 4. 遍历链表并打印所有节点数据
def print_linked_list(head):
    """遍历链表并打印所有节点数据"""
    current = head
    while current is not None:
        print(current.data, end=" -> ")
        current = current.next
    print("None")  # 表示链表结束

print("=== 链表遍历示例 ===")
print_linked_list(node1)

# 5. 在链表头部插入新节点
def insert_at_head(head, data):
    """在链表头部插入新节点"""
    new_node = ListNode(data)
    new_node.next = head
    return new_node

print("\n=== 在头部插入新节点(5) ===")
node1 = insert_at_head(node1, 5)
print_linked_list(node1)

# 6. 在链表尾部添加新节点
def append_to_tail(head, data):
    """在链表尾部添加新节点"""
    new_node = ListNode(data)
    if head is None:
        return new_node
    
    current = head
    while current.next is not None:
        current = current.next
    current.next = new_node
    return head

print("\n=== 在尾部添加新节点(40) ===")
node1 = append_to_tail(node1, 40)
print_linked_list(node1)

# 7. 删除指定值的节点
def delete_node(head, data):
    """删除第一个值为data的节点"""
    if head is None:
        return None
    
    # 如果要删除的是头节点
    if head.data == data:
        return head.next
    
    current = head
    while current.next is not None and current.next.data != data:
        current = current.next
    
    # 如果找到了要删除的节点
    if current.next is not None:
        current.next = current.next.next
    
    return head

print("\n=== 删除值为20的节点 ===")
node1 = delete_node(node1, 20)
print_linked_list(node1)

# 8. 获取链表长度
def get_length(head):
    """计算链表长度"""
    length = 0
    current = head
    while current is not None:
        length += 1
        current = current.next
    return length

print(f"\n=== 链表长度 ===")
print(f"当前链表长度: {get_length(node1)}")

# 9. 查找特定值的节点
def find_node(head, data):
    """查找值为data的节点，返回节点位置(从0开始)"""
    position = 0
    current = head
    while current is not None:
        if current.data == data:
            return position
        current = current.next
        position += 1
    return -1  # 未找到返回-1

print(f"\n=== 查找节点 ===")
search_value = 30
position = find_node(node1, search_value)
if position != -1:
    print(f"值 {search_value} 在链表中的位置: {position}")
else:
    print(f"值 {search_value} 不在链表中")

# 10. 反转链表
def reverse_linked_list(head):
    """反转链表"""
    prev = None
    current = head
    while current is not None:
        next_node = current.next  # 保存下一个节点
        current.next = prev       # 反转指针
        prev = current            # prev向前移动
        current = next_node       # current向前移动
    return prev

print(f"\n=== 反转链表 ===")
node1 = reverse_linked_list(node1)
print_linked_list(node1)

# 11. 实际应用场景：学生成绩管理
print(f"\n=== 实际应用：学生成绩管理系统 ===")

class Student:
    """学生类，包含姓名和成绩"""
    def __init__(self, name, score):
        self.name = name
        self.score = score
    
    def __str__(self):
        return f"{self.name}: {self.score}分"

# 创建学生链表
student1 = ListNode(Student("张三", 85))
student2 = ListNode(Student("李四", 92))
student3 = ListNode(Student("王五", 78))

student1.next = student2
student2.next = student3

# 打印所有学生信息
def print_students(head):
    """打印学生链表"""
    current = head
    while current is not None:
        print(current.data)
        current = current.next

print("学生成绩列表:")
print_students(student1)

# 计算平均成绩
def calculate_average_score(head):
    """计算学生平均成绩"""
    total = 0
    count = 0
    current = head
    while current is not None:
        total += current.data.score
        count += 1
        current = current.next
    return total / count if count > 0 else 0

average = calculate_average_score(student1)
print(f"\n平均成绩: {average:.2f}分")

# 12. 链表与列表的对比
print(f"\n=== 链表与Python列表的对比 ===")
print("链表优点:")
print("- 插入和删除操作效率高(不需要移动其他元素)")
print("- 内存使用灵活，不需要连续空间")
print("- 大小可以动态扩展")
print("\n链表缺点:")
print("- 随机访问效率低(需要从头遍历)")
print("- 每个节点需要额外空间存储指针")
print("- 缓存局部性差")

print("\nPython列表优点:")
print("- 随机访问速度快(通过索引)")
print("- 内存连续，缓存友好")
print("\nPython列表缺点:")
print("- 插入和删除可能需要移动大量元素")
print("- 预分配内存可能导致空间浪费")