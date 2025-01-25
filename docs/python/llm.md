# LLM

```python
import copy
import json
import os

from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())
client = OpenAI()


def traverse_directory(path):
    for dirpath, dirnames, filenames in os.walk(path):
        for file in filenames:
            print(os.path.join(dirpath, file))


def code2prompt(filename):
    """Translate source code into prompt.

    Returns:
        string: Prompt that can be used by GPT.
    """
    """

    """
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()

    # 任务描述
    instruction = """
    你的任务是解释代码。我们只会提供 C/C++ 语言、Python 语言、Java 语言让你分析。
    并且在这个项目中，有可能多种语言是混用的。
    """

    # 输出格式定义各种约束
    output_format = """
    以 JSON 格式输出。

    1. 在 json 中 main 函数始终作为一级目录；
    2. 如果有多个 main 函数，应该有多个一级目录；
    3. 被 main 函数调用的其他函数是二级目录，以此类推，直到在当前目录下找不到更深层的调用关系。

    只输出包含用户提及的字段，不要猜测任何用户未直接提及的字段。
    DO NOT OUTPUT NULL-VALUED FILED! 确保输出能被 json.loads 加载。
    """

    # 例子可以让输出更稳定
    # 多轮对话的上下文就是调用链中的上下级关系，在 JSON 格式中，上文在 prev 字段中保存，下文在 next 字段中保存
    examples = """
    只有 1 个 main 函数的项目：
    客服：有什么可以帮助你吗？
    用户：在这个项目中包含了几个 main 函数？
    客服：一个。
    用户：请分析 main 文件中的代码。
    客服：这是 main 函数的功能描述。
    用户：在函数 main 中调用了哪些函数？
    客服：函数 main 调用了 func1 和 func2。
    用户：请分析 func1 和 func2 的功能。
    客服：这是函数 func1 的功能描述，这是函数 func2 的功能描述。
    用户：请根据你之前的回答，汇总一下，生成 JSON 格式的输出。
    客服：
    [
        {
            "main": {
                "desc": "这是函数 main 的功能描述",
                "prev": null,
                "next": {
                    "func1": {
                        "desc": "这是函数 func1 的功能描述",
                        "prev": "main",
                        "next": {
                            "func2": {
                                "desc": "这是函数 func2 的功能描述",
                                "prev": "func1",
                                "next": null
                            },
                        },
                    },
                    "func3": {
                        "desc": "这是函数 func3 的功能描述",
                        "prev": "main",
                        "next": null
                    },
                }
            }
        }
    ]

    含有 2 个 main 函数的项目：
    客服：有什么可以帮助你吗？
    用户：在这个项目中包含了几个 main 函数？
    客服：两个。
    用户：请分析 main1 文件中的代码。
    客服：这是函数 main1 的功能描述。
    用户：请分析 main2 文件中的代码。
    客服：这是函数 main2 的功能描述。
    用户：请根据你之前的回答，汇总一下，生成 JSON 格式的输出。
    客服：
    [
        {
            "main1": {
                "desc": "这是函数 main1 的功能描述",
                "prev": null,
                "next": null
            }
        },
        {
            "main2": {
                "desc": "这是函数 main2 的功能描述",
                "prev": null,
                "next": null
            }
        }
    ]
    """

    # 需要解析的文本
    input_text = f"""
    {content}
    """

    prompt = f"""
    {instruction}\n\n{output_format}\n\n例如：\n{examples}\n\n用户输入：\n{input_text}
    """

    return prompt


class NLU:
    """自然语言理解（Nature Language Understanding, NLU），调用 GPT 获得反馈。"""

    def __init__(self, filename):
        self.prompt_template = code2prompt(filename)

    def _get_completion(self, prompt, model="gpt-3.5-turbo"):
        messages = [{"role": "user", "content": prompt}]
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0,  # 模型输出的随机性，0 表示随机性最小
        )
        semantics = json.loads(response.choices[0].message.content)
        return {k: v for k, v in semantics.items() if v}

    def parse(self, user_input):
        prompt = self.prompt_template.replace("__INPUT__", user_input)
        return self._get_completion(prompt)


class DST:
    """对话状态跟踪（Dialogue State Tracking），实现多轮对话。"""

    def __init__(self):
        pass

    def update(self, state, nlu_semantics):
        if "name" in nlu_semantics:
            state.clear()
        if "sort" in nlu_semantics:
            slot = nlu_semantics["sort"]["value"]
            if slot in state and state[slot]["operator"] == "==":
                del state[slot]
        for k, v in nlu_semantics.items():
            state[k] = v
        return state


class MockedDB:
    """假数据库，为模型提供持久化能力。"""

    def __init__(self):
        self.data = [
            {
                "main": {
                    "desc": "这是函数 main 的功能描述。",
                    "prev": "null",
                    "next": {
                        "func1": {
                            "desc": "这是函数 func1 的功能描述。",
                            "prev": "main",
                            "next": "null",
                        },
                    },
                },
            }
        ]

    def retrieve(self, **kwargs):
        records = []
        for r in self.data:
            select = True
            if r["requirement"]:
                if "status" not in kwargs or kwargs["status"] != r["requirement"]:
                    continue
            for k, v in kwargs.items():
                if k == "sort":
                    continue
                if k == "data" and v["value"] == "无上限":
                    if r[k] != 1000:
                        select = False
                        break
                if "operator" in v:
                    if not eval(str(r[k]) + v["operator"] + str(v["value"])):
                        select = False
                        break
                elif str(r[k]) != str(v):
                    select = False
                    break
            if select:
                records.append(r)
        if len(records) <= 1:
            return records
        key = "price"
        reverse = False
        if "sort" in kwargs:
            key = kwargs["sort"]["value"]
            reverse = kwargs["sort"]["ordering"] == "descend"
        return sorted(records, key=lambda x: x[key], reverse=reverse)


class DialogManager:
    def __init__(self, prompt_templates):
        self.state = {}
        self.session = [
            {
                "role": "system",
                "content": "你的任务是解释代码。我们只会提供 C/C++ 语言、Python 语言、Java 语言让你分析。",
            }
        ]
        self.nlu = NLU()
        self.dst = DST()
        self.db = MockedDB()
        self.prompt_templates = prompt_templates

    def _wrap(self, user_input, records):
        if records:
            prompt = self.prompt_templates["recommand"].replace("__INPUT__", user_input)
            r = records[0]
            for k, v in r.items():
                prompt = prompt.replace(f"__{k.upper()}__", str(v))
        else:
            prompt = self.prompt_templates["not_found"].replace("__INPUT__", user_input)
            for k, v in self.state.items():
                if "operator" in v:
                    prompt = prompt.replace(
                        f"__{k.upper()}__", v["operator"] + str(v["value"])
                    )
                else:
                    prompt = prompt.replace(f"__{k.upper()}__", str(v))
        return prompt

    def _call_chatgpt(self, prompt, model="gpt-3.5-turbo"):
        session = copy.deepcopy(self.session)
        session.append({"role": "user", "content": prompt})
        response = client.chat.completions.create(
            model=model,
            messages=session,
            temperature=0,
        )
        return response.choices[0].message.content

    def run(self, user_input):
        # 调用NLU获得语义解析
        semantics = self.nlu.parse(user_input)
        print("===semantics===")
        print(semantics)

        # 调用DST更新多轮状态
        self.state = self.dst.update(self.state, semantics)
        print("===state===")
        print(self.state)

        # 根据状态检索DB，获得满足条件的候选
        records = self.db.retrieve(**self.state)

        # 拼装prompt调用chatgpt
        prompt_for_chatgpt = self._wrap(user_input, records)
        print("===gpt-prompt===")
        print(prompt_for_chatgpt)

        # 调用chatgpt获得回复
        response = self._call_chatgpt(prompt_for_chatgpt)

        # 将当前用户输入和系统回复维护入chatgpt的session
        self.session.append({"role": "user", "content": user_input})
        self.session.append({"role": "assistant", "content": response})
        return response


if __name__ == "__main__":
    curr_dir = os.getcwd()
    traverse_directory(curr_dir)
    code2prompt(curr_dir + "/analyzer/main.py")
```
