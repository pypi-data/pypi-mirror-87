def get_data_from_tag_name(xml, tag, class_mapping=str, index=0):
    tags = get_xml_from_tag_name(xml=xml, tag=tag)
    if tags:
        data = [class_mapping(tag.firstChild.nodeValue) for tag in tags]
        return data[index] if index is not None else data


def get_xml_from_tag_name(xml, tag):
    return xml.getElementsByTagName(tag)
