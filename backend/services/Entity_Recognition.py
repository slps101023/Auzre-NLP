import spacy
import spacy_entity_linker

def extract_entities(text):
    nlp = spacy.load("en_core_web_sm")

    nlp.add_pipe("entityLinker", last=True)

    doc = nlp(text)
    entities_info = []
    
    for entity in doc._.linkedEntities:
        span_text = str(entity.get_span())
        wikidata_id = entity.get_id()
        entities_info.append({
            "name": span_text,
            "url": f"https://www.wikidata.org/wiki/Special:GoToLinkedPage/enwiki/Q{wikidata_id}",
        })
    
    return entities_info

if __name__ == "__main__":
    sample_text = (
        "Yesterday, NASA announced that Dr. Mark Davis, who holds a PhD in astrophysics, "
        "found water on Mars. He previously studied at the Massachusetts Institute of Technology."
    )
    result_wiki = extract_entities(sample_text)
    docs_wiki = [doc_wiki for doc_wiki in result_wiki]
    print(docs_wiki)
    entity_to_url = []
    # for doc_wiki in result_wiki:
    #     for entity in doc_wiki.entities:
    #         if entity.data_source == "Wikipedia":
    #             entity_to_url.append({"name": entity.name, "url": entity.url})
