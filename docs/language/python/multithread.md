# 多线程

## 问题描述

1. 使用两个线程。
2. 线程二阻塞等待线程一提出问题。
3. 线程一提出问题，阻塞等待线程二回答。
4. 线程二回答线程一的问题，然后阻塞等待线程一继续提问。
5. 线程一打印线程二的回答，然后提出新的问题，阻塞等待线程二回答。
6. 重复步骤 4 和步骤 5。

## 具体实现

```python
import threading
import time


def ask_question():
    while True:
        answer = question_answered.wait()  # P(a)
        question_answered.clear()
        print("Thread 1: What is your name?")
        print("Thread 1: Thank you, ", answer)
        question_asked.set()  # V(q)


def answer_question():
    while True:
        question = question_asked.wait()  # P(q)
        question_asked.clear()
        print("Thread 2: My name is XXX.")
        time.sleep(2)
        question_answered.set()  # V(a)


if __name__ == "__main__":
    question_asked = threading.Event()
    question_answered = threading.Event()
    t1 = threading.Thread(target=ask_question)
    t2 = threading.Thread(target=answer_question)
    question_answered.set()  # 让 question_asked 先运行，破除死锁
    t1.start()
    t2.start()
```
