# third_platform_spider

三方爬虫平台 代码

#使用说明

## 安装依赖包

pip install -r requirements.txt 

## 配置 chrome_driver

settings 文件中的 driver_path 
例如：driver_path = r'F:\zhangcrworkspace\23年1月\spider_3rd\spider_3rd\chromedriver'

## 配置 chrome 执行路径

chrome执行路径 默认为空 无异常 不配置即可 
chrome_path = ''

## 配置 数据库连接
settings 文件中的 db_env 切换生产测试数据

## 任务执行

每周一 执行 清除任务状态

python main.py init_task

采集指定平台 python main.py 平台名

示例：

python main.py conforama 

python main.py mano 

python main.py cd

## 调度

欧洲站点对应国内凌晨1点为热卖时刻

每周一 凌晨0点 conforama 1点 mano 2点 cd 执行采集  
每周二 凌晨0点 conforama 1点 mano 2点 cd 执行采集  
第一次采集触发反爬 任务状态不会更新 第二次 仅采集未完成的任务


