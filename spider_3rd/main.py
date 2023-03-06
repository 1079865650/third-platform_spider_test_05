from scrapy.cmdline import execute
import os
import sys
from reset_task import reset_task_status
from scrapy import spiderloader
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings

def run_spider(plat):
    settings = get_project_settings()
    runner = CrawlerRunner(settings)
    # 查看现有爬虫
    spider_loader = spiderloader.SpiderLoader.from_settings(settings)
    run_list = []
    # 按指定类型排序  列表最先
    def rule(hang):
        if 'category' in hang:
            return 0
        if 'asin' in hang:
            return 1
        if 'reviews' in hang:
            return 2
    # 筛选站点爬虫
    for spider in spider_loader.list():
        if plat in spider:
            run_list.append(spider)
    # 将 spider 逐个添加到 CrawlerProcess 实例及 crawlers 列表中
    run_list = sorted(run_list, key=lambda x:rule(x))
    # 打印执行列表
    print('spider task list:',run_list)
    crawlers = []

    for spider in run_list:
        print(f'Running spider {spider}')
        spider_cls = spider_loader.load(spider)
        runner.crawl(spider_cls, settings)

    d = runner.join()
    d.addBoth(lambda _: reactor.stop())

    reactor.run()
    # 获取爬虫的统计信息
    stats_dict = {}
    for crawler in crawlers:
        stats_dict[crawler.spider.name] = crawler.stats.get_stats()

    return stats_dict

if __name__ == '__main__':
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    print('get plat:',sys.argv[1])
    plat = sys.argv[1]
    if plat == 'init_task':
        reset_task_status()

    if plat in ['conforama','mano','cd']:
        spider_stats = run_spider(plat)
        print(spider_stats)



