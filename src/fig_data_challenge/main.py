from pipeline import ExcelFilePipeline
from utils import setup_logger

if __name__ == '__main__':
    pipeline_cls = ExcelFilePipeline(file_path='data/restaurant_data.xlsx')
    pipeline_cls.upload_to_db()