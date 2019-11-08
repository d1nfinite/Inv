# Inv
Inv是一款擦除Linux入侵痕迹的工具

## 安装
```
git clone https://github.com/d1nfinite/Inv.git
```

## 使用
```
python3 Inv.py --accurate
python Inv.py --help
```

## 目录结构说明
```
├── Inv.py
└── lib
    ├── common
    │   ├── global_var.py
    │   ├── log.py
    │   ├── log.pyc
    │   └── pub.py
    └── plugins
        ├── apache_log_clean.py
        ├── clean.py
        ├── history_clean.py
        ├── known_hosts_clean.py
        ├── nginx_log_clean.py
        ├── ssh_clean.py
        └── uxtmp_clean.py
```
