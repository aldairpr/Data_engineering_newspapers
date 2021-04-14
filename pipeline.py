import logging
import subprocess
import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
news_sites_uids = ['eluniversal', 'xataka']


def main():
    logger.info('Starting ETL process')
    _extract()
    _transform()
    _load()
    logger.info('ETL process finished')


def _extract():
    logger.info('Starting extract process')
    now = datetime.datetime.now().strftime('%Y_%m_%d')
    for news_site_uid in news_sites_uids:
        subprocess.run(['python', 'extract_main.py', news_site_uid], cwd='./extract')
        subprocess.call('cp extract/{news_site_uid}_{datetime}_articles.csv transform/{news_site_uid}.csv'.format(news_site_uid=news_site_uid,datetime=now), shell=True)


def _transform():
    logger.info('Starting transform process')
    for news_site_uid in news_sites_uids:
        dirty_data_filename = '{}.csv'.format(news_site_uid)
        clean_data_filename = 'clean_{}'.format(dirty_data_filename)
        subprocess.run(['python', 'transform_main.py', dirty_data_filename], cwd='./transform')
        subprocess.call('mv transform/{} load'.format(clean_data_filename), shell=True)
    subprocess.call('rm transform/*.csv', shell=True)


def _load():
    logger.info('Starting load process')
    for news_site_uid in news_sites_uids:
        clean_data_filename = 'clean_{}.csv'.format(news_site_uid)
        subprocess.run(['python', 'load_main.py', clean_data_filename], cwd='./load')
    subprocess.call('rm load/*.csv', shell=True)


if __name__ == '__main__':
    main()
