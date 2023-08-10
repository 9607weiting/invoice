
import logging
import os

standard_format = "%(asctime)s [%(name)s:%(lineno)d] [%(levelname)s]- %(message)s"


def create_logger(folder_name):

    log_name = 'log.log'

    # 相对路径: 创建一个log文件夹

    save_to = f'log\\{folder_name}'

    # 如果不存在定义的日志目录就创建一个
    try:
        if os.path.exists(save_to):

            print(f'>>> folder already existed: {save_to}')

        else:

            os.makedirs(save_to, exist_ok=True)


    except Exception as e:

        print(f">>> Something went wrong when created: {e}")

    logging.basicConfig(
                        filename=f'{save_to}\\{log_name}',
                        filemode='a',
                        format=standard_format,
                        level=logging.INFO
                        )

    logger = logging.getLogger(__name__)  # 生成一个log实例

    return logger
