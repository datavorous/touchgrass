from src.backend.api import API
from src.engine.dumbo import DumboEngine  # Using DumboEngine as default
from src.uci import UCIHandler

def main():
    api = API()
    engine = DumboEngine(api)
    handler = UCIHandler(engine, api)
    handler.run()

if __name__ == "__main__":
    main()
