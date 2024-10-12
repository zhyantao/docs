# Windows Path

## Java

| 变量名      | 变量值                                  |
| ----------- | --------------------------------------- |
| `JAVA_HOME` | `D:\Program Files\Java\jdk-1.8`         |
| `JDK_HOME`  | `%JAVA_HOME%`                           |
| `JRE_HOME`  | `%JAVA_HOME%\jre`                       |
| `CLASSPATH` | `.;%JAVA_HOME%\lib;%JAVA_HOME%\jre\lib` |
| `PATH`      | `%JAVA_HOME%\bin`                       |

```{note}
配置好 Java 环境变量才能让 VS Code 识别到 Java 环境。
```

## Python

| 变量名       | 变量值                                            |
| ------------ | ------------------------------------------------- |
| `PYTHONHOME` | `D:\Program Files\Python38`                       |
| `PYTHONPATH` | `%PYTHONHOME%\Lib;%PYTHONHOME%\Lib\site-packages` |
| `PATH`       | `%PYTHONHOME%\Scripts;%PYTHONHOME%`               |

## Maven

| 变量名       | 变量值                              |
| ------------ | ----------------------------------- |
| `MAVEN_HOME` | `D:\ProgramData\apache-maven-3.9.9` |
| `M2_HOME`    | `%MAVEN_HOME%`                      |
| `PATH`       | `%MAVEN_HOME%\bin`                  |
