
# 软件包及镜像源管理

本文提到的各种类型的源（比如 `pip`，`npm`，`apt`，`yum`），都可以通过国内一些公司或高校的镜像站中找到。比如常用的镜像站有：

- 阿里巴巴官方镜像站：<https://developer.aliyun.com/mirror/>
- 腾讯软件源：<https://mirrors.cloud.tencent.com/>
- 网易开源镜像站：<http://uni.mirrors.163.com/>
- 清华大学开源软件镜像站：<https://mirrors.tuna.tsinghua.edu.cn/>
- 中科大镜像站：<http://mirrors.ustc.edu.cn/>
- 浙江大学开源镜像站：<http://mirrors.zju.edu.cn/>

## pip 源

镜像站中的 PyPI 即为 `pip` 源。`pip` 是 Python 包管理工具，该工具提供了对 Python 包的查找、下载、安装、卸载的功能。

（1）**永久使用国内镜像源**：Windows 用户修改文件 `C:\Users\%USERNAME%\pip\pip.ini`（如果没有则新建），
Linux 用户修改文件 `~/.config/pip/pip.conf`（如果没有则新建），然后在相关文件中添加如下内容。
注意，`trusted-host` 非必须，使用时提示不受信任可添加 `--trusted-host=mirrors.aliyun.com`。

```bash
[global]
index-url=http://mirrors.aliyun.com/pypi/simple/
[install]
trusted-host=mirrors.aliyun.com
```

（2）**临时使用国内镜像源**，只需要在命令后面加上 `-i` 参数：

```bash
pip install pythonModuleName -i https://mirror.baidu.com/pypi/simple
```

```{admonition} 其他公司或高校提供的镜像源
:class: dropdown

- 官方源：<https://pypi.python.org/pypi>
- 豆瓣源：<https://pypi.doubanio.com/simple/>
- 阿里云源：<http://mirrors.aliyun.com/pypi/simple/>
- 中科大源：<https://mirrors.ustc.edu.cn/pypi/web/simple/>
- 百度源：<https://mirror.baidu.com/pypi/simple>
- 清华源：<https://pypi.tuna.tsinghua.edu.cn/simple/>
- 更多：<https://blog.csdn.net/u011433858/article/details/80398947>
```

（3）**离线安装第三方库**。从 <https://pypi.org/> 搜索相应的版本并下载。
使用如下命令进行安装。

```bash
pip install /path/to/file.whl
```

（4）**如果使用的是 conda 管理各个版本的 Python**，可以修改文件
`C:\Users\%USERNAME%\.condarc`（如果没有则新建），添加如下内容：

```bash
channels:
  - defaults
show_channel_urls: true
default_channels:
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/r
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/msys2
custom_channels:
  conda-forge: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  msys2: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  bioconda: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  menpo: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  pytorch: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  simpleitk: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
```

## apt/yum 源

不同的 Linux 系统提供了不同的软件包管理器，其中典型的两种是：

- 高级打包工具（英语：Advanced Packaging Tools，缩写为 APT）
- YUM（全称为 Yellow dog Updater, Modified）

软件包管理器可以自动地下载、配置、安装、卸载自家的软件包，比如 `.deb` 和 `.rpm`。
软件包管理器会自动地处理软件包之间的依赖关系，给用户提供了极大方便。

更新镜像源后，不要忘记更新缓存：

```bash
sudo apt-get clean all
sudo apt-get update
```

从镜像源中**获取不到**的软件安装包，可以从 <https://pkgs.org/> 查一下，然后用离线的方式安装。
Ubuntu 用 `dpkg` 命令安装，CentOS 用 `rpm` 命令安装。

当然，你也可以选择使用下载**源代码的方式安装**：

```bash
./configure --prefix=/path/to/install/
make
sudo make install
```

如果使用 `apt` 命令安装了软件，卸载软件的方式如下：

- 仅卸载应用程序：`sudo apt-get remove <packagename>`
- 卸载应用程序及其依赖：`sudo apt-get -y autoremove <packagename>`
- 删除用户数据：`sudo apt-get -y purge <packagename>`
- 卸载应用程序及其依赖并删除用户数据：`sudo apt-get -y autoremove --purge <packagename>`

## npm 源

`npm` 是 JavaScript 世界的包管理工具，并且是 Node.js 平台的默认包管理工具。
通过 `npm` 可以安装、共享、分发代码，管理项目依赖关系。默认源是 <https://www.npmjs.com/>。

（1）**临时改变镜像源**

```bash
# 方法一：通过 config 命令
npm config set registry http://registry.cnpmjs.org
npm info express

# 方法二：通过 npm 命令
npm --registry http://registry.cnpmjs.org info express
```

（2）**永久修改镜像源**

1. 打开配置文件：`~/.npmrc`
2. 写入配置：`registry=https://registry.npm.taobao.org`

## Maven 源

如果使用 IDEA 默认的国外镜像源比较慢（会导致下载 Maven Wrapper 失败），可尝试使用国内镜像源：

- 阿里云：<https://developer.aliyun.com/mirror/>
- 腾讯云：<https://mirrors.cloud.tencent.com/>
- 网易 163：<http://uni.mirrors.163.com/>

IDEA 默认的 Maven 配置文件在 `C:\Users\%USERNAME%\.m2` 目录下，如果你能够在找到 `settings.xml`
文件的话，那直接修改配置文件就可以了。
如果找不到这个文件的话，自己新建一个 `settings.xml`，然后在文件中写入下面的内容（以阿里镜像源为例）：

````{admonition} settings.xml
:class: dropdown

```{code-block} xml
<?xml version="1.0" encoding="UTF-8"?>

<!--
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License.
-->

<!--
 | This is the configuration file for Maven. It can be specified at two levels:
 |
 |  1. User Level. This settings.xml file provides configuration for a single user,
 |                 and is normally provided in ${user.home}/.m2/settings.xml.
 |
 |                 NOTE: This location can be overridden with the CLI option:
 |
 |                 -s /path/to/user/settings.xml
 |
 |  2. Global Level. This settings.xml file provides configuration for all Maven
 |                 users on a machine (assuming they're all using the same Maven
 |                 installation). It's normally provided in
 |                 ${maven.conf}/settings.xml.
 |
 |                 NOTE: This location can be overridden with the CLI option:
 |
 |                 -gs /path/to/global/settings.xml
 |
 | The sections in this sample file are intended to give you a running start at
 | getting the most out of your Maven installation. Where appropriate, the default
 | values (values used when the setting is not specified) are provided.
 |
 |-->
<settings xmlns="http://maven.apache.org/SETTINGS/1.2.0"
          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xsi:schemaLocation="http://maven.apache.org/SETTINGS/1.2.0 https://maven.apache.org/xsd/settings-1.2.0.xsd">
  <!-- localRepository
   | The path to the local repository maven will use to store artifacts.
   |
   | Default: ${user.home}/.m2/repository
  <localRepository>/path/to/local/repo</localRepository>
  -->

  <!-- interactiveMode
   | This will determine whether maven prompts you when it needs input. If set to false,
   | maven will use a sensible default value, perhaps based on some other setting, for
   | the parameter in question.
   |
   | Default: true
  <interactiveMode>true</interactiveMode>
  -->

  <!-- offline
   | Determines whether maven should attempt to connect to the network when executing a build.
   | This will have an effect on artifact downloads, artifact deployment, and others.
   |
   | Default: false
  <offline>false</offline>
  -->

  <!-- pluginGroups
   | This is a list of additional group identifiers that will be searched when resolving plugins by their prefix, i.e.
   | when invoking a command line like "mvn prefix:goal". Maven will automatically add the group identifiers
   | "org.apache.maven.plugins" and "org.codehaus.mojo" if these are not already contained in the list.
   |-->
  <pluginGroups>
    <!-- pluginGroup
     | Specifies a further group identifier to use for plugin lookup.
    <pluginGroup>com.your.plugins</pluginGroup>
    -->
  </pluginGroups>

  <!-- proxies
   | This is a list of proxies which can be used on this machine to connect to the network.
   | Unless otherwise specified (by system property or command-line switch), the first proxy
   | specification in this list marked as active will be used.
   |-->
  <proxies>
    <!-- proxy
     | Specification for one proxy, to be used in connecting to the network.
     |
    <proxy>
      <id>optional</id>
      <active>true</active>
      <protocol>http</protocol>
      <username>proxyuser</username>
      <password>proxypass</password>
      <host>proxy.host.net</host>
      <port>80</port>
      <nonProxyHosts>local.net|some.host.com</nonProxyHosts>
    </proxy>
    -->
  </proxies>

  <!-- servers
   | This is a list of authentication profiles, keyed by the server-id used within the system.
   | Authentication profiles can be used whenever maven must make a connection to a remote server.
   |-->
  <servers>
    <!-- server
     | Specifies the authentication information to use when connecting to a particular server, identified by
     | a unique name within the system (referred to by the 'id' attribute below).
     |
     | NOTE: You should either specify username/password OR privateKey/passphrase, since these pairings are
     |       used together.
     |
    <server>
      <id>deploymentRepo</id>
      <username>repouser</username>
      <password>repopwd</password>
    </server>
    -->

    <!-- Another sample, using keys to authenticate.
    <server>
      <id>siteServer</id>
      <privateKey>/path/to/private/key</privateKey>
      <passphrase>optional; leave empty if not used.</passphrase>
    </server>
    -->
  </servers>

  <!-- mirrors
   | This is a list of mirrors to be used in downloading artifacts from remote repositories.
   |
   | It works like this: a POM may declare a repository to use in resolving certain artifacts.
   | However, this repository may have problems with heavy traffic at times, so people have mirrored
   | it to several places.
   |
   | That repository definition will have a unique id, so we can create a mirror reference for that
   | repository, to be used as an alternate download site. The mirror site will be the preferred
   | server for that repository.
   |-->
  <mirrors>
    <!-- mirror
     | Specifies a repository mirror site to use instead of a given repository. The repository that
     | this mirror serves has an ID that matches the mirrorOf element of this mirror. IDs are used
     | for inheritance and direct lookup purposes, and must be unique across the set of mirrors.
     |
    <mirror>
      <id>mirrorId</id>
      <mirrorOf>repositoryId</mirrorOf>
      <name>Human Readable Name for this Mirror.</name>
      <url>http://my.repository.com/repo/path</url>
    </mirror>
     -->
    <mirror>
      <id>aliyunmaven</id>
      <mirrorOf>*</mirrorOf>
      <name>阿里云公共仓库</name>
      <url>https://maven.aliyun.com/repository/public</url>
    </mirror>
    <mirror>
      <id>maven-default-http-blocker</id>
      <mirrorOf>external:http:*</mirrorOf>
      <name>Pseudo repository to mirror external repositories initially using HTTP.</name>
      <url>http://0.0.0.0/</url>
      <blocked>true</blocked>
    </mirror>
  </mirrors>

  <!-- profiles
   | This is a list of profiles which can be activated in a variety of ways, and which can modify
   | the build process. Profiles provided in the settings.xml are intended to provide local machine-
   | specific paths and repository locations which allow the build to work in the local environment.
   |
   | For example, if you have an integration testing plugin - like cactus - that needs to know where
   | your Tomcat instance is installed, you can provide a variable here such that the variable is
   | dereferenced during the build process to configure the cactus plugin.
   |
   | As noted above, profiles can be activated in a variety of ways. One way - the activeProfiles
   | section of this document (settings.xml) - will be discussed later. Another way essentially
   | relies on the detection of a system property, either matching a particular value for the property,
   | or merely testing its existence. Profiles can also be activated by JDK version prefix, where a
   | value of '1.4' might activate a profile when the build is executed on a JDK version of '1.4.2_07'.
   | Finally, the list of active profiles can be specified directly from the command line.
   |
   | NOTE: For profiles defined in the settings.xml, you are restricted to specifying only artifact
   |       repositories, plugin repositories, and free-form properties to be used as configuration
   |       variables for plugins in the POM.
   |
   |-->
  <profiles>
    <!-- profile
     | Specifies a set of introductions to the build process, to be activated using one or more of the
     | mechanisms described above. For inheritance purposes, and to activate profiles via <activatedProfiles/>
     | or the command line, profiles have to have an ID that is unique.
     |
     | An encouraged best practice for profile identification is to use a consistent naming convention
     | for profiles, such as 'env-dev', 'env-test', 'env-production', 'user-jdcasey', 'user-brett', etc.
     | This will make it more intuitive to understand what the set of introduced profiles is attempting
     | to accomplish, particularly when you only have a list of profile id's for debug.
     |
     | This profile example uses the JDK version to trigger activation, and provides a JDK-specific repo.
    <profile>
      <id>jdk-1.4</id>

      <activation>
        <jdk>1.4</jdk>
      </activation>

      <repositories>
        <repository>
          <id>jdk14</id>
          <name>Repository for JDK 1.4 builds</name>
          <url>http://www.myhost.com/maven/jdk14</url>
          <layout>default</layout>
          <snapshotPolicy>always</snapshotPolicy>
        </repository>
      </repositories>
    </profile>
    -->
    <profile>
      <id>jdk-1.8</id>

      <activation>
        <jdk>1.8</jdk>
      </activation>

      <repositories>
        <repository>
          <id>spring</id>
          <url>https://maven.aliyun.com/repository/spring</url>
          <releases>
            <enabled>true</enabled>
          </releases>
          <snapshots>
            <enabled>true</enabled>
          </snapshots>
        </repository>
      </repositories>
    </profile>
    <!--
     | Here is another profile, activated by the system property 'target-env' with a value of 'dev',
     | which provides a specific path to the Tomcat instance. To use this, your plugin configuration
     | might hypothetically look like:
     |
     | ...
     | <plugin>
     |   <groupId>org.myco.myplugins</groupId>
     |   <artifactId>myplugin</artifactId>
     |
     |   <configuration>
     |     <tomcatLocation>${tomcatPath}</tomcatLocation>
     |   </configuration>
     | </plugin>
     | ...
     |
     | NOTE: If you just wanted to inject this configuration whenever someone set 'target-env' to
     |       anything, you could just leave off the <value/> inside the activation-property.
     |
    <profile>
      <id>env-dev</id>

      <activation>
        <property>
          <name>target-env</name>
          <value>dev</value>
        </property>
      </activation>

      <properties>
        <tomcatPath>/path/to/tomcat/instance</tomcatPath>
      </properties>
    </profile>
    -->
  </profiles>

  <!-- activeProfiles
   | List of profiles that are active for all builds.
   |
  <activeProfiles>
    <activeProfile>alwaysActiveProfile</activeProfile>
    <activeProfile>anotherAlwaysActiveProfile</activeProfile>
  </activeProfiles>
  -->
</settings>
```
````

当然，你也可以自己从 Maven
[官方仓库](https://maven.apache.org/download.html) 下载 `apache-maven-3.8.5-bin.zip`。
然后，1）配置环境变量 `MAVEN_HOME` 或 `M2_HOME` [^cite_ref-1]，
2）修改 `apache-maven-3.8.5/conf/settings.xml`。

修改完成后，在 IDEA 中记得勾选 `文件` > `设置` > `构建、执行、部署` > `构建工具` > `Maven` > `使用 Maven 包装器` > `重写`。

## Linux 本地源

```{hint}
以下内容未经验证！
```

1. 安装好 Linux 操作系统；
2. 将安装镜像 `.iso` 文件上传至虚拟机任意目录；
3. 使用如下命令完成后续操作：

    ```bash
    sudo mkdir /dev/local_mirror
    mount -o loop /home/CentOS-6.10-x86_64-bin-DVD1.iso /dev/local_mirror/
    sudo mkdir /mnt/local_mirror
    sudo cp -r /dev/local_mirror/* /mnt/local_mirror
    cd /etc/yum.repos.d/
    rename .repo .repo.bak *.repo
    cp CentOS-Base.repo.bak CentOS_local.repo
    cp CentOS-Media.repo.bak CentOS-local.repo
    vim CentOS-local.repo
    ```

4. 写入如下内容：

    ```bash
    [LocalMirror]
    name=LocalMirror
    baseurl=file:///mnt/local_mirror
    enabled=1
    gpgcheck=0
    ```

5. 更新 yum 源

    ```bash
    yum clean all
    yum repolist
    sudo umount /dev/local_mirror
    sudo rm /dev/local_mirror/ -rf
    ```

---

[^cite_ref-1]: Maven 安装与配置 <https://www.cnblogs.com/seve/p/10903679.html>
