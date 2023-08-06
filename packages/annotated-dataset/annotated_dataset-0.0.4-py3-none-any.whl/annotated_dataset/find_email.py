from typing import List
import re
from annotated_dataset.annotation import Annotation


REGEX_EMAIL = re.compile(r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)")


def find_email(text: str, email_label='email') -> List[Annotation]:
    results = []
    for match in re.finditer(REGEX_EMAIL, text):
        results.append(
            Annotation(label=email_label,
                       start=match.span(0)[0],
                       stop=match.span(0)[1]
                       ))
    return results
