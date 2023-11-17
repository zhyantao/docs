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
import queue
import threading
import time

exitFlag = 0

threadList = ["Thread-Q", "Thread-A"]
threads = []

questionQueueLock = threading.Lock()
questionQueue = queue.Queue(10)
answerQueue = queue.Queue(10)
questionList = [
    "What is your name?",
    "Where are you from?",
    "How's the weather today?",
    "What day is it today?",
    "Do you like fruits?",
]
answerList = ["Sam", "China", "Sunny", "Friday", "Yes"]
for answer in answerList:
    answerQueue.put(answer)


class myThread(threading.Thread):
    def __init__(self, threadId, name, q):
        threading.Thread.__init__(self)
        self.threadId = threadId
        self.name = name
        self.q = q

    def run(self):
        print("Starting " + self.name)
        process_data(self.name, self.q)
        print("Exiting " + self.name)


def process_data(threadName, q):
    global answerList
    while not exitFlag:
        questionQueueLock.acquire()
        if threadName == "Thread-Q" and not questionQueue.empty():
            question = q.get()
            questionQueueLock.release()
            question_answered.wait()  # P(a)
            question_answered.clear()
            print("Thread-Q: " + question)
            question_asked.set()  # V(q)
        elif threadName == "Thread-A" and not answerQueue.empty():
            questionQueueLock.release()
            question_asked.wait()  # P(q)
            question_asked.clear()
            print("Thread-A: " + answerQueue.get())
            question_answered.set()  # V(a)
        else:
            questionQueueLock.release()


if __name__ == "__main__":
    # 创建同步事件
    question_asked = threading.Event()
    question_answered = threading.Event()
    question_answered.set()  # 让 question_asked 先运行，破除死锁

    # 创建新线程
    threadId = 1
    for tName in threadList:
        thread = myThread(threadId, tName, questionQueue)
        thread.start()
        threads.append(thread)
        threadId += 1

    # 填充队列
    questionQueueLock.acquire()
    for question in questionList:
        questionQueue.put(question)
    questionQueueLock.release()

    # 等待队列清空
    while not questionQueue.empty() or not answerQueue.empty():
        pass

    # 通知线程是时候退出
    exitFlag = 1

    # 等待所有线程完成
    for t in threads:
        t.join()
    print("Exiting Main Thread")
```
