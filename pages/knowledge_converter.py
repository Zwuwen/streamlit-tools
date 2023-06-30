from typing import Dict, Any

import pandas as pd
import streamlit as st
from xml.dom import minidom


def create_property_info_node(root, row):
    def create_node(name,value):
        n = root.createElement(name)
        n.appendChild(root.createTextNode(str(value).replace('\n','').replace('\r\n','').replace('、',',').replace('  ',' ')))
        return n

    property_info = root.createElement('propertyInfo')
    node_names = ['device', 'property', 'operator', 'value','AIModel']
    for node_name in node_names:
        # node = root.createElement(node_name)
        if node_name in row.index:
            node = create_node(node_name,row.loc[node_name])
            property_info.appendChild(node)

    return property_info

def create_event_type_eng_node(root, row):
    def create_classify_info_node():
        classify_info = root.createElement('classifyInfo')

        class_eng = root.createElement('en')
        class_eng.appendChild(root.createTextNode(row.loc['eventClassEng'].replace('、',',')))
        class_chi = root.createElement('cn')
        class_chi.appendChild(root.createTextNode(row.loc['eventClassChi'].replace('、',',')))

        classify_info.appendChild(class_eng)
        classify_info.appendChild(class_chi)
        return classify_info

    event_type_eng = root.createElement(row.loc['eventTypeEng'])
    name = root.createElement('name')
    name.appendChild(root.createTextNode(row.loc['eventTypeChi']))
    event_type_eng.appendChild(name)

    event_type_eng.appendChild(create_classify_info_node())

    return event_type_eng

def create_knowledge_type_node(root, knowledge_type_v, df):
    knowledge_type = root.createElement(knowledge_type_v)
    event_type_dict = dict()
    for index, row in df.iterrows():
        event_type_eng_v = row.loc['eventTypeEng']
        if event_type_eng_v not in event_type_dict:
            event_type_dict[event_type_eng_v] = create_event_type_eng_node(root, row)

        event_type_eng = event_type_dict[event_type_eng_v]
        event_type_eng.appendChild(create_property_info_node(root, row))

    for _, event_type_eng in event_type_dict.items():
        knowledge_type.appendChild(event_type_eng)
    return knowledge_type

def create_knowledge_node(root, dfs):
    knowledge = root.createElement('knowledge')
    for k, df in dfs.items():
        try:
            knowledge_type_v = df['knowledgeType'].values[0]
        except KeyError:
            knowledge_type_v = 'Universal'
        knowledge_type = create_knowledge_type_node(root, knowledge_type_v, df)
        knowledge.appendChild(knowledge_type)
    return knowledge

def create_xml(dfs: Dict[Any,pd.DataFrame]):
    root = minidom.Document()
    root.appendChild(create_knowledge_node(root, dfs))
    xml_str = root.toprettyxml(indent="\t", encoding="utf-8")
    return xml_str

def main():
    st.title("Knowledge converter")
    uploaded_file = st.file_uploader(" ", type="xlsx")
    if uploaded_file is not None:
        dfs = pd.read_excel(uploaded_file, sheet_name=None)
        if 'knowledgeType' in list(dfs.values())[0].columns:
            xml_str = create_xml(dfs)
            filename = 'AI_knowledge.xml'
            st.download_button(filename, data=xml_str, file_name=filename, mime="text/xml")
        else:
            for k, df in dfs.items():
                xml_str = create_xml(dict({k:df}))
                filename = f"{k}_knowledge.xml"
                st.download_button(filename, data=xml_str, file_name=filename, mime="text/xml")




if __name__ == "__main__":
    main()