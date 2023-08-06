# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['politylink',
 'politylink.elasticsearch',
 'politylink.graphql',
 'politylink.helpers']

package_data = \
{'': ['*']}

install_requires = \
['elasticsearch>=7.9.1,<8.0.0',
 'kanjize>=0.1.0,<0.2.0',
 'pandas>=1.0.5,<2.0.0',
 'sgqlc>=11.0,<12.0']

setup_kwargs = {
    'name': 'politylink',
    'version': '0.1.41',
    'description': '',
    'long_description': '## インストール\n```\npip install politylink\n```\n\n## 使い方\n\n### GraphQLClient\n\nPolityLinkの[GraphQLエンドポイント](https://graphql.politylink.jp/)にアクセスするためのGraphQLClientが用意されています。\n```\nfrom politylink.graphql.client import GraphQLClient\nclient = GraphQLClient()\n```\n\n`exec`メソッドを使えば任意のGraphQLクエリを実行することができます。\n```\nquery = """\nquery {\n  Bill(filter: {submittedDate: {year: 2020, month: 1, day: 20}}) {\n    name\n  }\n}\n"""\nclient.exec(query)\n```\n2020年1月20日に提出された3つの法律案の名前が得られるはずです。\n```\n{\'data\': {\'Bill\': [{\'name\': \'特定複合観光施設区域の整備の推進に関する法律及び特定複合観光施設区域整備法を廃止する法律案\'},\n   {\'name\': \'地方交付税法及び特別会計に関する法律の一部を改正する法律案\'},\n   {\'name\': \'平成三十年度歳入歳出の決算上の剰余金の処理の特例に関する法律案\'}]}}\n```\n\nGraphQLClientは[sgglc](https://github.com/profusion/sgqlc)のラッパークラスであり、クエリをコードで組み立てることも可能です。例えば上のクエリを組み立てると以下のようになります。\n```\nfrom politylink.graphql.schema import Query, _BillFilter, _Neo4jDateTimeInput\nfrom sgqlc.operation import Operation\n\nop = Operation(Query)\nbill_filter = _BillFilter(None)\nbill_filter.submitted_date = _Neo4jDateTimeInput(year=2020, month=1, day=20)\nbills = op.bill(filter=bill_filter)\nbills.name()\nclient.exec(op)\n```\n',
    'author': 'Mitsuki Usui',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://politylink.jp',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
