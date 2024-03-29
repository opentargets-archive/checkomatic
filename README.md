# Check-O-Matic
Note: Check-O-Matic is not compatible with GraphQL-API at the moment.

## Install

```
pip install opentargets-checkomatic
opentargets_checkomatic eval -f platform-api.yml
```

The `YAML` file can be like this
```yaml
checkomatic:
  client:
    host: https://open-targets-eu-dev.appspot.com
    port: 443
    size: 100 # max size to fetch when query and it is applicable
  rules:
    targets:
      ENSG00000198947:
        - o.approved_symbol == 'DMD'
        - o.approved_name == 'dystrophin'
        - o.tractability.smallmolecule.top_category == 'Unknown'
        - o.tractability.antibody.top_category == 'Predicted Tractable - High confidence'
    diseases:
      Orphanet_908:
        - o.label == 'Fragile X syndrome'
        - ('eye disease' in o.therapeutic_labels)
      Orphanet_273:
        - o.label == 'Steinert myotonic dystrophy'
      Orphanet_93256:
        - o.label == 'Fragile X-associated tremor/ataxia syndrome'
    associations:
      # these (targets and diseases) use dataframes (t) instead addict.Dict object (o)
      # those are easier to manipulate and filter by
      targets:
        PRDX1:
        DMD:
          - ('Orphanet_98896' in to_vlist(jp.parse('data[*].disease.id').find(d)))
        CD86:
          - ('EFO_0003885' in to_vlist(jp.parse('data[*].disease.id').find(d)))
        ITGAL:
          - ('EFO_0003767' in to_vlist(jp.parse('data[*].disease.id').find(d)))
      diseases:
        Orphanet_93256:
        EFO_0003767:
          # NOD2, IL10RA, IL23R, ITGAL in IBD
          - not set(['NOD2', 'IL10RA', 'ITGAL']) - to_vset(jp.parse('data[*].target.gene_info.symbol').find(d))
        EFO_0000384:
          # TNF, PTGS2, PTGS1 in crohns disease
          - not set(['TNF', 'PTGS2', 'PTGS1']) - to_vset(jp.parse('data[*].target.gene_info.symbol').find(d))
        EFO_0000249:
          # APP, SORL1, ABCA7, ADAM10 in alzheimers disease
          - not set(['APP', 'SORL1', 'ABCA7', 'ADAM10']) - to_vset(jp.parse('data[*].target.gene_info.symbol').find(d))
        Orphanet_399:
          # huntington disease
          - not set(['HTT']) - to_vset(jp.parse('data[*].target.gene_info.symbol').find(d))
    evidences:
      ENSG00000102081-Orphanet_908:
        # http://purl.obolibrary.org/obo/SO_0001583
        - ('missense_variant' in to_vlist(jp.parse('data[*].evidence.evidence_codes_info[*][*].label').find(d)))
    searches:
      diseases:
        "crohn disease":
          - len(o.data) > 0
        Orphanet_908:
          - o.data[0].data.name == 'Fragile X syndrome'
          - o.data[0].data.association_counts.total > 400
          - o.data[0].data.association_counts.direct > 400
      targets:
        "mt-nd":
          - len(o.data) > 0
    stats:
      - o.data_version == "18.12"
      - o.targets.total > 28000 and o.targets.total < 50000
      - o.diseases.total > 10000 and o.diseases.total < 20000
      - len(o.associations.datatypes.keys()) == 7
      - ('sysbio' in o.associations.datatypes.affected_pathway.datasources)
      - |-
        dts = o.associations.datatypes.keys()
        dss = []
        for dt in dts:
          dss += o.associations.datatypes[dt].datasources.keys()
        output = len(dss) == 19
```

Each item can be either
- single-line python boolean expression
- multi-line python code setting the output variable to a boolean expression
the data remains in memory across the full list to check for the specific object

## Things already injected
- o as addict.Dict object with either the object itself or multiple results inside the o.data field
- d as python dict object with either the object itself or multiple results inside the d['data'] field
- jp module as an abbreviation standing for jsonpath-rw
- to_vlist(iterable) function to transform jp find() to a list of values
- to_vset(iterable) function to transform jp find() to a set of values

## Rules
- targets - an Ensembl ID
- diseases - a disease ID (EFO, Orphanet, ...) 
- associations - you have 2 subsections, targets and diseases. Whether it is a target or a disease it returns all associations to the object
- evidences - it returns up to size evidences for that association tuple (t,d)
- searches - you have 2 subsections, targets and diseases. Whether it is a target or a disease it returns up to size search results filtered by either target or disease 
- stats - currently returns an object with the aggregation v3/platform/public/utils/stats endpoint returns
- metrics - currently returns an object with the aggregation v3/platform/public/utils/metrics endpoint returns

# Copyright

Copyright 2014-2018 Biogen, Celgene Corporation, EMBL - European Bioinformatics Institute, GlaxoSmithKline, Takeda Pharmaceutical Company and Wellcome Sanger Institute

This software was developed as part of the Open Targets project. For more information please see: http://www.opentargets.org

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

