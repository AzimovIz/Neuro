from gliba import *
import asyncio
import spacy
from spacy.lang.ru import Russian

nlp = spacy.load('ru_core_news_sm')

async def main():
    print('ok')


if __name__ == '__main__':
    asyncio.run(main())
