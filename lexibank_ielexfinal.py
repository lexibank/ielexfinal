from collections import defaultdict
from pathlib import Path

import attr
import pylexibank
from clldutils.misc import slug


@attr.s
class CustomLanguage(pylexibank.Language):
    SubGroup = attr.ib(default=None)


class Dataset(pylexibank.Dataset):
    id = "ielexfinal"
    dir = Path(__file__).parent
    language_class = CustomLanguage

    def cmd_makecldf(self, args):
        languages = args.writer.add_languages(
            lookup_factory=lambda c: c['ID'].lower()
        )
        concepts = args.writer.add_concepts(
            id_factory=lambda c: c.id.split("-")[-1] + "_" + slug(c.english),
            lookup_factory=lambda c: c.english
        )
        
        for row in self.raw_dir.read_csv("ielex-130421-ag-cc.txt", delimiter="\t", dicts=True):
            concept = row['cc_alias'].split("-")[0]

            # NB the below includes forms marked 'exclude'
            loan = True if row['status'] else False

            for lex in args.writer.add_forms_from_value(
                Parameter_ID=concepts[concept],
                Language_ID=languages[row["language"].lower()],
                Value=row["lexeme"],
                Cognacy=row["cc_alias"],
                Source="dunn2021",
                Loan=loan):
                
                args.writer.add_cognate(
                    lexeme=lex,
                    Cognateset_ID=row["cc_alias"],
                    Source="dunn2021")
            
        args.writer.add_sources()
