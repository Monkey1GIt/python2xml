# -*- coding:utf-8 -*-
from xml.etree.ElementTree import ElementTree, Element
import os


def add_newxml(title, content_html, link):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_name = dir_path + '/XML_Cfan.xml'
    # print(dir_path)
    tree = ElementTree()
    tree.parse(file_name)
    root = tree.getroot()
    # for child in root[0]:
    #     print(child.tag, child.attrib)
    item = Element('item')
    root[0].insert(6, item)
    # 追加新文章的 title description link
    item_title = Element('title')
    item_title.text = title
    item.append(item_title)
    item_description = Element('description')
    # item_description.text = '<![CDATA[' + content_html + ' ]]>'
    item_description.text = content_html
    item.append(item_description)
    item_link = Element('link')
    item_link.text = link
    item.append(item_link)
    # 让结果保存进文件就可以了
    tree.write(file_name, encoding='utf-8', xml_declaration=True)


if __name__ == '__main__':
    title = 'The title'
    link = 'http://www.link.html'
    content_html = '''
      <td> The content </td>
    '''
    add_newxml(title, content_html, link)
