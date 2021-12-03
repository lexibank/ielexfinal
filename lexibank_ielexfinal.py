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
        data = self.raw_dir.read_csv("ielex.csv", delimiter=",", dicts=True)
        concept_lookup = {}
        glosses = {
                "FEAR (TO BE AFRAID)": "FEAR (BE AFRAID)",
                }
        for concept in self.concepts:
            idx = concept["ID"] + "_" + slug(concept["ENGLISH"])
            args.writer.add_concept(
                ID=idx,
                Name=concept["ENGLISH"],
                Concepticon_ID=concept["CONCEPTICON_ID"],
                Concepticon_Gloss=glosses.get(concept["CONCEPTICON_GLOSS"],
                    concept["CONCEPTICON_GLOSS"]),
            )
            concept_lookup[concept["CONCEPTICON_GLOSS"]] = idx
        languages = args.writer.add_languages(lookup_factory="Name")
        args.writer.add_sources()

        for row in data:
            lex = args.writer.add_form(
                    Parameter_ID=concept_lookup[row["CONCEPT"]],
                    Language_ID=languages[row["LANGUAGE"]],
                    Value="---",
                    Form="---",
                    Cognacy=row["COGNATE"],
                    Source="dunn2021"
                    )
            args.writer.add_cognate(
                    lexeme=lex,
                    Cognateset_ID=row["COGNATE"],
                    Source="dunn2021"
                    )

