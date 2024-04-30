# doenv
from os.path import join, dirname
from dotenv import load_dotenv
load_dotenv(join(dirname(__file__), '.env'))

# Internal
import outils

if __name__ == "__main__":
    name_file = './input.csv'
    datas = outils.read_file(name_file)
    outils.worker(datas)