A python library for extracting inflections and synonyms

    from sauce.nltkrdf.wordnet import WordnetEnricher
    
    data = """[{"@id":"https://api.sauce-project.tech/assets/1234","@type":["https://vocabularies.sauce-project.tech/core/Asset"],"https://vocabularies.sauce-project.tech/core/depicts":[{"@id":"https://api.sauce-project.tech/depictions/1234"}]},{"@id":"https://api.sauce-project.tech/depictions/1234","@type":["https://vocabularies.sauce-project.tech/core/Depiction"],"https://vocabularies.sauce-project.tech/core/label":[{"@value":"running"}]},{"@id":"https://vocabularies.sauce-project.tech/core/Asset"},{"@id":"https://vocabularies.sauce-project.tech/core/Depiction"}]"""
    
    enricher = WordnetEnricher(data)
    enriched_asset = enricher.enrich()