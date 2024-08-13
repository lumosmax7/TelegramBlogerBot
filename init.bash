#!/bin/bash

# init requirement
install_python3() {
    if command -v python3 &> /dev/null; then
        echo "Python 3 已经安装."
    else
        echo "安装 Python 3..."
        if [ -f /etc/debian_version ]; then
            sudo apt update
            sudo apt install -y python3 python3-pip
        elif [ -f /etc/redhat-release ]; then
            sudo yum install -y python3 python3-pip
        elif [ -f /etc/fedora-release ]; then
            sudo dnf install -y python3 python3-pip
        elif [ -f /etc/arch-release ]; then
            sudo pacman -Syu python --noconfirm
        else
            echo "无法识别的Linux发行版，请手动安装Python"
            exit 1
        fi
    fi
}

install_python3_pip(){
    if command -v pip3 &> /dev/null; then
        echo "pip 已经安装."
    else
        echo "安装 pip..."
        if [ -f /etc/debian_version ]; then
            sudo apt update
            sudo apt install -y python3-pip
        elif [ -f /etc/redhat-release ]; then
            sudo yum install -y python3-pip
        elif [ -f /etc/fedora-release ]; then
            sudo dnf install -y python3-pip
        elif [ -f /etc/arch-release ]; then
            sudo pacman -Syu python-pip --noconfirm
        else
            echo "无法识别的Linux发行版，请手动安装pip"
            exit 1
        fi
    fi
}

# 检查并安装 systemctl
install_systemctl() {
    if command -v systemctl &> /dev/null; then
        echo "systemctl 已经安装."
    else
        echo "安装 systemctl..."
        if [ -f /etc/debian_version ]; then
            sudo apt update
            sudo apt install -y systemd
        elif [ -f /etc/redhat-release ]; then
            sudo yum install -y systemd
        elif [ -f /etc/fedora-release ]; then
            sudo dnf install -y systemd
        elif [ -f /etc/arch-release ]; then
            sudo pacman -Syu systemd --noconfirm
        else
            echo "无法识别的Linux发行版，请手动安装systemctl"
            exit 1
        fi
    fi
}

load_requirement(){
    /usr/bin/pip3 install -r requirement.txt
      if [ $? -ne 0 ]; then
          echo "安装失败，退出."
          exit 1
      else echo "requirement 已安装."
      fi
}

# 检查并安装 Node.js 和 npm
install_nodejs() {
    if command -v node &> /dev/null && command -v npm &> /dev/null; then
        echo "Node.js 和 npm 已经安装." #TODO:利用该方法安装nodejs版本可能过低
    else
        echo "安装 Node.js 和 npm..."
        if [ -f /etc/debian_version ]; then
            sudo apt update
            sudo apt install -y nodejs npm
        elif [ -f /etc/redhat-release ]; then
            sudo yum install -y nodejs npm
        elif [ -f /etc/fedora-release ]; then
            sudo dnf install -y nodejs npm
        elif [ -f /etc/arch-release ]; then
            sudo pacman -Syu nodejs npm --noconfirm
        else
            echo "无法识别的Linux发行版，请手动安装Node.js 和 npm."
            exit 1
        fi
    fi
}

# 安装 Hexo
install_hexo() {
    echo "安装 Hexo..."
    npm install -g hexo-cli --unsafe-perm=true --user root
    if command -v hexo &> /dev/null; then
        echo "Hexo 安装成功."
    else
        echo "Hexo 安装失败，请检查 npm 设置."
        exit 1
    fi
}


# 创建一个新的 systemd 服务
create_service() {
    SERVICE_NAME=$1
    PYTHON_SCRIPT=$2
    SERVICE_FILE=/etc/systemd/system/${SERVICE_NAME}.service

    if [ ! -f "$PYTHON_SCRIPT" ]; then
        echo "Python 脚本文件 ${PYTHON_SCRIPT} 不存在."
        exit 1
    fi

    echo "创建 systemd 服务..."

    sudo bash -c "cat > ${SERVICE_FILE}" <<EOL
[Unit]
Description=${SERVICE_NAME}
After=network.target

[Service]
ExecStart=/usr/bin/python3 ${PYTHON_SCRIPT}
Restart=always
User=root
Group=root

[Install]
WantedBy=multi-user.target
EOL

    echo "重新加载 systemd 守护进程..."
    sudo systemctl daemon-reload

    echo "启动并启用服务..."
    sudo systemctl start ${SERVICE_NAME}
    sudo systemctl enable ${SERVICE_NAME}

    echo "服务 ${SERVICE_NAME} 已经成功创建并启动."
}

install_git() {
    if command -v git &> /dev/null; then
        echo "Git 已经安装."
    else
        echo "安装 Git..."
        if [ -f /etc/debian_version ]; then
            sudo apt update
            sudo apt install -y git
        elif [ -f /etc/redhat-release ]; then
            sudo yum install -y git
        elif [ -f /etc/fedora-release ]; then
            sudo dnf install -y git
        elif [ -f /etc/arch-release ]; then
            sudo pacman -Syu git --noconfirm
        else
            echo "无法识别的 Linux 发行版，请手动安装 Git."
            exit 1
        fi
    fi
}

init_depend(){
      install_python3
      install_systemctl
      load_requirement
      install_nodejs
      install_hexo
      install_git
}



# 主函数
init_fun() {
      SERVICE_NAME=TgBlogBot
      PYTHON_SCRIPT=$(pwd)/main.py
      CONFIG_FILE=$(pwd)/config.py
      HEXO_CONFIG_FILE="_config.yml"


      echo "请输入Tg Bot TOKEN:"
      read TOKEN

      echo "请输入BLOG_PATH:"
      read BLOG_PATH

      echo "请输入Github_Page_URL:"
      read GP_URL

      echo "更新配置文件..."

      sed -i "s|^TOKEN =.*|TOKEN = '${TOKEN}'|" ${CONFIG_FILE}
      sed -i "s|^BLOG_PATH =.*|BLOG_PATH = '${BLOG_PATH}'|" ${CONFIG_FILE}
      sed -i "s|^GP_URL =.*|GP_URL = '${GP_URL}'|" ${CONFIG_FILE}

      echo "config.py 文件已更新."
      echo "正在安装依赖，请稍后"
      init_depend
      echo "-------------------"

      echo "请确认是否配置hexo中的_config.yml（Y/N）"
      read choice
      if [ "$choice" = "N" ] || [ "$choice" = "n" ]; then
         echo "初始化TgBlogBot中止"
         exit 1
      fi
      echo "正在创建服务，请稍后"
      create_service ${SERVICE_NAME} ${PYTHON_SCRIPT}

      mkdir source/_drafts

}

main() {
     echo "欢迎使用 TgBlogBot ！"
     echo "-------------------"
     echo "请选择要进行的操作："
     echo "1. 初始化 TgBlogBot"
     echo "2. 查看运行状态"
     echo "3. 退出"
     read choice
     case $choice in
       1) init_fun ;;
       2) systemctl status TgBlogBot ;;
       3) exit 0 ;;
       *) echo "无效的选择，请重新运行脚本并输入有效的选项。" ;;
     esac


}

main "$@"
