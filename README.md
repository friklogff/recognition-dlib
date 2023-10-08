这是一组关于在Linux系统上安装Python 3.9以及更改pip源的步骤。以下是每个步骤的解释：

**1) 安装编译 Python 需要的依赖包**
首先，您需要更新系统软件包列表，并安装编译Python所需的依赖包。这些包包括构建工具和Python的各种库，用于支持Python的不同功能和模块。

```bash
sudo apt-get update
sudo apt install -y build-essential zlib1g-dev \
libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libsqlite3-dev \
libreadline-dev libffi-dev curl libbz2-dev
```

**2) 下载最新版本的Python 3.9源码并解压**
使用wget下载Python 3.9的源代码压缩文件，并使用tar命令解压缩它。

```bash
wget https://www.python.org/ftp/python/3.9.10/Python-3.9.10.tgz
tar xvf Python-3.9.10.tgz
```

**3) 运行配置命令**
进入解压后的Python源代码目录并运行configure命令，以准备编译Python。--enable-optimizations标志用于启用编译时的优化。

```bash
cd Python-3.9.10
./configure --enable-optimizations
```

**4) 编译安装Python 3.9**
使用make命令编译Python。这可能需要一段时间，大约半个小时左右，具体时间取决于您的系统性能。

```bash
make -j4  # 使用-j标志以并行编译，数字4表示同时使用4个CPU核心
sudo make altinstall  # 使用altinstall以防止覆盖系统默认的Python版本
```

**5) 检查Python版本**
安装完成后，您可以使用以下命令来验证Python版本：

```bash
python3.9 --version
```

**6) 更新pip**
使用新安装的Python 3.9的pip来更新pip本身：

```bash
/usr/local/bin/python3.9 -m pip install --upgrade pip
```

**7) 更换pip源的方法**
在中国大陆等地区，访问Python官方源可能会较慢，因此更换pip源以提高下载速度是一个好主意。

**永久更换pip源的方法：**
a. 创建~/.pip目录并在其中创建pip.conf配置文件，并将源设置为清华源。

```bash
mkdir -p ~/.pip
cat <<EOF > ~/.pip/pip.conf
[global]
timeout = 6000
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
trusted-host = pypi.tuna.tsinghua.edu.cn
EOF
```

b. 现在，使用pip3安装Python库时，将从清华源下载，速度会更快。

**临时更换pip源的方法：**
如果您只想为特定包更改pip源，可以使用以下命令，将`<packagename>`替换为您要安装的包名。

```bash
pip3 install <packagename> -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn
```

这将在临时情况下使用清华源来安装特定包。