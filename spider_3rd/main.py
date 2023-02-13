from scrapy.cmdline import execute
import os
import sys
from reset_task import reset_task_status

if __name__ == '__main__':
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    print(sys.argv[1])
    plat = sys.argv[1]
    if plat == 'init_task':
        reset_task_status();

    if plat in ['conforama','mano','cd']:
        execute(['scrapy','crawl','spider_'+plat+'_category'])
        execute(['scrapy','crawl','spider_'+plat+'_asin'])


